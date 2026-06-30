# weekly-asana-task-recap — status log

## 2026-06-30

Created as the Asana counterpart to `weekly-linear-issue-recap`. Same workflow,
different backend: it reads from and writes to Asana through the official Asana
MCP server rather than the `go-linear` CLI.

### Design decisions

- **SKILL.md only, no Go program.** The Linear recap has a Go helper that shells
  out to the `go-linear` CLI. Asana has no equivalent CLI — the official
  integration path is the hosted MCP server, and MCP tools can only be invoked
  by the MCP client (Claude) itself, not by an external subprocess. So the whole
  workflow is driven by Claude calling Asana MCP tools directly, with no
  mechanical helper to build or maintain.
- **Official OAuth MCP server**, not a PAT-based community server. Endpoint
  `https://mcp.asana.com/v2/mcp` (Streamable HTTP). Auth is OAuth 2.0 only —
  Asana does not support Personal Access Tokens for the MCP server. Setup
  requires creating an Asana MCP app (client ID/secret + redirect URI) and
  running `claude mcp add --transport http ... --callback-port 8080`.

### Tool / terminology mapping from the Linear skill

| Linear (go-linear)        | Asana (MCP)                                   |
|---------------------------|-----------------------------------------------|
| `user get me`             | `get_me`                                       |
| issue                     | task                                           |
| comment                   | story (returned inline by `get_task`)          |
| `issue list` by assignee  | `get_tasks` (project + assignee filter)        |
| `issue create`            | `create_tasks` (with `create_task_preview` first) |
| `RECAP_LINEAR_PROJECT`    | `RECAP_ASANA_PROJECT`                          |
| `RECAP_LINEAR_TEAM`       | `RECAP_ASANA_TEAM` (optional, disambiguation)  |
| issue URL                 | task `permalink_url`                           |

### Known gaps / things to verify with real data

- Exact `get_tasks` filter parameters for "completed within the last week" and
  the precise assignee field name come from the live `tools/list` schema against
  `https://mcp.asana.com/v2/mcp`; treat that as the source of truth since the
  tool set evolves.
- Whether `get_task` returns enough story/comment history (and author identity,
  to filter out bots/agents) for the weekly window, or whether pagination is
  needed.
- Asana task notes are plain text and do not render markdown richly. If rich
  formatting matters, switch to the `html_notes` field with limited HTML.
- A reported Claude Code re-auth bug can ignore the configured callback port and
  use a random localhost port, breaking the strict OAuth redirect-URI match
  (anthropics/claude-code#55067). Verify current status if re-auth fails.

### Sources

- https://developers.asana.com/docs/mcp-server
- https://developers.asana.com/docs/using-asanas-mcp-server
- https://developers.asana.com/docs/connecting-mcp-clients-to-asanas-v2-server
- https://developers.asana.com/docs/mcp-tools-reference
