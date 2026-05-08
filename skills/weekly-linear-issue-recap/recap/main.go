package main

import (
	"bufio"
	"encoding/json"
	"flag"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"
)

// JSON shapes from go-linear CLI output

type viewer struct {
	ID          string `json:"id"`
	Name        string `json:"name"`
	DisplayName string `json:"displayName"`
	Email       string `json:"email"`
}

type issueState struct {
	Name string `json:"name"`
}

type issueNode struct {
	ID          string     `json:"id"`
	Identifier  string     `json:"identifier"`
	Title       string     `json:"title"`
	Description string     `json:"description"`
	URL         string     `json:"url"`
	State       issueState `json:"state"`
	UpdatedAt   time.Time  `json:"updatedAt"`
	ArchivedAt  *time.Time `json:"archivedAt"`
}

type pageInfo struct {
	HasNextPage bool   `json:"hasNextPage"`
	EndCursor   string `json:"endCursor"`
}

type issueListResponse struct {
	Nodes    []issueNode `json:"nodes"`
	PageInfo pageInfo    `json:"pageInfo"`
}

type commentUser struct {
	Name string `json:"name"`
}

type commentNode struct {
	Body      string      `json:"body"`
	User      commentUser `json:"user"`
	CreatedAt time.Time   `json:"createdAt"`
}

type commentListResponse struct {
	Nodes    []commentNode `json:"nodes"`
	PageInfo pageInfo      `json:"pageInfo"`
}

type issueWithComments struct {
	Issue    issueNode
	Comments []commentNode
}

func main() {
	dryRun := flag.Bool("dry-run", false, "write the markdown file but skip creating the Linear issue")
	flag.Parse()

	if os.Getenv("LINEAR_API_KEY") == "" {
		fatal("LINEAR_API_KEY environment variable not set")
	}
	project := os.Getenv("RECAP_LINEAR_PROJECT")
	if project == "" {
		fatal("RECAP_LINEAR_PROJECT environment variable not set")
	}

	// Identify current user and ask for confirmation
	viewerData := runLinear("user", "get", "me")
	var v viewer
	mustUnmarshal(viewerData, &v, "viewer response")
	fmt.Printf("Current user: %s (%s)\n", v.Name, v.Email)
	if !confirm("Is this you? Proceed?") {
		fmt.Println("Aborted.")
		return
	}

	// Warn if not Friday
	now := time.Now()
	if now.Weekday() != time.Friday {
		fmt.Printf("Today is %s, not Friday.\n", now.Weekday())
		if !confirm("Proceed with weekly recap anyway?") {
			fmt.Println("Aborted.")
			return
		}
	}

	// Fetch all issues for the project assigned to current user
	fmt.Printf("\nFetching issues for project %q assigned to %s...\n", project, v.Name)
	issues := fetchIssues(project)
	fmt.Printf("Found %d issues.\n", len(issues))

	// For each issue, fetch comments from the past 7 days
	sevenDaysAgo := now.AddDate(0, 0, -7)
	var active []issueWithComments
	for i, issue := range issues {
		fmt.Printf("  [%d/%d] Fetching comments for %s...\n", i+1, len(issues), issue.Identifier)
		comments := fetchRecentComments(issue.ID)
		// Include issues updated this week or with recent comments; skip archived
		isArchived := issue.ArchivedAt != nil && issue.ArchivedAt.Before(sevenDaysAgo)
		hasRecentActivity := issue.UpdatedAt.After(sevenDaysAgo) || len(comments) > 0
		if !isArchived && hasRecentActivity {
			active = append(active, issueWithComments{issue, comments})
		}
	}
	fmt.Printf("%d issues with activity this week.\n\n", len(active))

	// Determine output path and write the file
	dateStr := now.Format("2006-01-02")
	outPath := filepath.Join(resolveOutputDir(), "update-"+dateStr+".md")
	content := buildMarkdown(v.Name, dateStr, active)
	if err := os.WriteFile(outPath, []byte(content), 0644); err != nil {
		fatal("writing output file: %v", err)
	}
	fmt.Printf("Wrote recap to: %s\n\n", outPath)

	if *dryRun {
		fmt.Println("Dry run: skipping Linear issue creation.")
		return
	}

	fmt.Println("The Details section contains raw issue data. Please:")
	fmt.Println("  1. Ask Claude to summarize the Details section")
	fmt.Println("  2. Fill in 'Summary for this week' and 'Plans for next week'")
	fmt.Println("  3. Press Enter here to create the Linear issue from the file")

	reader := bufio.NewReader(os.Stdin)
	reader.ReadString('\n')

	// Read the (possibly edited) file and create the Linear issue
	updated, err := os.ReadFile(outPath)
	if err != nil {
		fatal("reading output file: %v", err)
	}
	title := v.Name + " weekly update as of " + dateStr
	runLinear("issue", "create",
		"--project", project,
		"--assignee", v.Email,
		"--title", title,
		"--description", string(updated),
	)
	fmt.Println("Linear issue created.")
}

func fetchIssues(project string) []issueNode {
	var all []issueNode
	cursor := ""
	for {
		args := []string{"issue", "list", "--project", project, "--assignee", "me", "--limit", "250"}
		if cursor != "" {
			args = append(args, "--after", cursor)
		}
		data := runLinear(args...)
		var resp issueListResponse
		mustUnmarshal(data, &resp, "issue list")
		all = append(all, resp.Nodes...)
		if !resp.PageInfo.HasNextPage {
			break
		}
		cursor = resp.PageInfo.EndCursor
	}
	return all
}

func fetchRecentComments(issueID string) []commentNode {
	data := runLinear("comment", "list", "--issue", issueID, "--created-after", "7d", "--limit", "250")
	var resp commentListResponse
	if err := json.Unmarshal(data, &resp); err != nil {
		return nil
	}
	var human []commentNode
	for _, c := range resp.Nodes {
		if !strings.Contains(strings.ToLower(c.User.Name), "agent") {
			human = append(human, c)
		}
	}
	return human
}

func buildMarkdown(name, date string, issues []issueWithComments) string {
	var b strings.Builder
	fmt.Fprintf(&b, "# %s weekly update as of %s\n\n", name, date)
	b.WriteString("## Plans for next week\n\n* \n* \n* \n\n")
	b.WriteString("## Summary for this week\n\n* \n* \n* \n\n")
	b.WriteString("## Details for this week\n\n")
	for _, iw := range issues {
		fmt.Fprintf(&b, "### [%s](%s)\n\n", iw.Issue.Title, iw.Issue.URL)
		if iw.Issue.Description != "" {
			b.WriteString("**Description:**\n\n")
			b.WriteString(iw.Issue.Description)
			b.WriteString("\n\n")
		}
		if len(iw.Comments) > 0 {
			for _, c := range iw.Comments {
				fmt.Fprintf(&b, "*%s on %s:*\n\n%s\n\n---\n\n",
					c.User.Name, c.CreatedAt.Format("2006-01-02"), c.Body)
			}
		}
	}
	return b.String()
}

func resolveOutputDir() string {
	cwd, err := os.Getwd()
	if err != nil {
		fatal("getting working directory: %v", err)
	}
	if filepath.Base(cwd) == "weekly-updates" {
		return cwd
	}
	sub := filepath.Join(cwd, "weekly-updates")
	if info, err := os.Stat(sub); err == nil && info.IsDir() {
		return sub
	}
	return cwd
}

// runLinear executes a go-linear subcommand and returns its stdout.
// The LINEAR_API_KEY environment variable is passed through automatically.
func runLinear(args ...string) []byte {
	cmd := exec.Command("go-linear", args...)
	out, err := cmd.Output()
	if err != nil {
		if exitErr, ok := err.(*exec.ExitError); ok {
			fatal("go-linear %s: %s", strings.Join(args, " "), exitErr.Stderr)
		}
		fatal("go-linear %s: %v", strings.Join(args, " "), err)
	}
	return out
}

func mustUnmarshal(data []byte, v any, context string) {
	if err := json.Unmarshal(data, v); err != nil {
		fatal("parsing %s: %v", context, err)
	}
}

func confirm(prompt string) bool {
	fmt.Printf("%s [y/N] ", prompt)
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	ans := strings.TrimSpace(strings.ToLower(scanner.Text()))
	return ans == "y" || ans == "yes"
}

func fatal(format string, args ...any) {
	fmt.Fprintf(os.Stderr, "error: "+format+"\n", args...)
	os.Exit(1)
}
