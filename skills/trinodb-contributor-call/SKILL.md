---
name: trinodb-contributor-call
description: Prepare a Trino contributor call and process its recording — the local call folder with the draft notes, the tracking issue, the agenda topics from the contributor meetings wiki and recent releases, and after the call the processing of the YouTube recording into a timestamped topic list for the video description and expanded minutes for the wiki. Child skill of the trinodb family. Use when preparing an upcoming Trino contributor call, or after the recording is uploaded and needs to be made consumable for the community.
---

# Trino contributor call

Use this skill to prepare a [Trino contributor
call](https://www.youtube.com/playlist?list=PLFnr63che7wYkKTBWGulzVbzLSV_wrSBq)
and to process its recording on YouTube into a timestamped list of topics for
the video description and expanded minutes for [the contributor meetings wiki
page](https://github.com/trinodb/trino/wiki/Contributor-meetings).

It builds on the shared context in the `trinodb` skill. Load that skill first.

## Call lifecycle

Each call moves through the same steps:

1. Create the local call folder and the draft notes.
2. File or find the tracking issue.
3. Collect the agenda topics in the draft notes.
4. Check the calendar entry and post the reminder.
5. Host the call. Manfred records the attendees and further topics in the
   draft notes and saves the screenshot.
6. Process the recording into the YouTube description and the minutes.
7. Paste the description into the video and the minutes into the wiki.
8. Announce the recording and the minutes.
9. Comment on the tracking issue and close it.

Steps one to four are the [preparation](#preparation) and happen in the days
before the call. Steps six to nine follow the upload of the recording and
are described in [Processing the recording](#processing-the-recording).

## Local call folder

Ask the user for the date of the call in the format YYYY-MM-DD and remember it
as {{date}}. It locates the section for the call in the wiki. Also remember the
date without dashes in the format YYYYMMDD as {{compactdate}} for the names of
the folder and the files. When the current working directory is already named
`tcc-YYYYMMDD`, take the date from the name and confirm it with the user.

Keep all files for the call in a folder named `tcc-{{compactdate}}` in the
current working directory, and create it if it does not exist. When the current
working directory is that folder already, use it as is. The folder holds the
draft notes, both transcripts, the output files from each transcript, and the
merged final output files:

| File | Content |
| --- | --- |
| `tcc-{{compactdate}}.md` | Draft notes |
| `tcc-{{compactdate}}.png` | Screenshot for the run of show, the video edit, and the YouTube thumbnail |
| `tcc-{{compactdate}}-transcript-whisper.vtt` | Raw whisper-cpp transcript |
| `tcc-{{compactdate}}-transcript-whisper.txt` | Condensed whisper-cpp transcript |
| `tcc-{{compactdate}}-transcript-youtube.vtt` | Raw YouTube captions |
| `tcc-{{compactdate}}-transcript-youtube.txt` | Condensed YouTube captions |
| `tcc-{{compactdate}}-whisper-minutes.md` | Minutes from the whisper-cpp transcript |
| `tcc-{{compactdate}}-whisper-youtube-description.txt` | Description from the whisper-cpp transcript |
| `tcc-{{compactdate}}-youtube-minutes.md` | Minutes from the YouTube captions |
| `tcc-{{compactdate}}-youtube-youtube-description.txt` | Description from the YouTube captions |
| `tcc-{{compactdate}}-final-minutes.md` | Merged final minutes |
| `tcc-{{compactdate}}-final-youtube-description.txt` | Merged final description |

The screenshot belongs to the user and is not part of the processing. Leave it
in place.

## Preparation

### Draft notes

Create the draft notes file `tcc-{{compactdate}}.md` in the call folder, unless
it exists already. Use the same markdown formatting as the wiki page the notes
are later published on, as described in [Minutes](#minutes), with a hard wrap
at 80 characters. Before the call there is no recording, so leave out the video
link and the timestamps:

```
# Trino contributor call {{date}}

**Attendees**

* Manfred Moser ([mosabua](https://github.com/mosabua), host and organizer)

**Topics**

**{{topic title}}**

{{short note with markdown links to pull requests, issues, and release notes}}

```

Manfred types into the file during the call. Attendees go under **Attendees**
as described in [Attendees list](#attendees-list). Topics raised in the call go
under **Topics** with a title, the name of the person, a short note, and the
links to any pull requests and issues. Lines typed in a hurry during the call
are fine, and the processing tidies them up.

### Tracking issue

File or find the tracking issue for the call as described in [Tracking
issue](#tracking-issue).

### Agenda topics

Collect the topics for the call under **Topics** in the draft notes, each with
a short note and the relevant links. Only results count as topics. Do not carry
over follow-ups from the previous call. An open pull request without news is
left out unless someone brings it up again in the call, and a merged pull
request shows up as part of a release anyway. Check these sources:

* The [wiki page](https://github.com/trinodb/trino/wiki/Contributor-meetings),
  where contributors suggest topics ahead of the call. Read it without cloning
  from
  `https://raw.githubusercontent.com/wiki/trinodb/trino/Contributor-meetings.md`
  and look for a section for {{date}}.
* The releases since the previous call. Calls open with the new releases, so
  list each one with its version, date, and a link to the release notes. Check
  the GitHub releases of at least these repositories in the `trinodb`
  organization: `trino`, `trino-gateway`, `charts`, `trino-python-client`,
  `trino-go-client`, `trino-js-client`, `trino-query-ui`, and `grafana-trino`.
  Also check `trino-csharp-client`, `trino-odbc`, and `aws-proxy`. The
  `aws-proxy` repository tags versions without always publishing a release, so
  compare its tags as well. Do not mention that the next version of a project
  is in the works, since that is always implied.
* The tags of
  [trinodb/trino-packages](https://github.com/trinodb/trino-packages), which
  publishes no GitHub releases. A new tag named after a Trino version
  means the packages were updated to that version, so check the tags and the
  commits since the previous call instead of the releases.
* The changes to the website since the previous call, from the commits in the
  [trinodb/trino.io](https://github.com/trinodb/trino.io) repository. Do not
  add these to the draft notes. List them for the user, who decides whether
  any is worth a topic. Typically only new user testimonials and new tools on
  the ecosystem pages are.
* Any further topics from the user, such as requests received on Trino Slack.

Summarize the collected topics for the user and ask what to add, drop, or
reorder.

When the wiki has no section for {{date}} yet, offer the content of the draft
notes for the user to paste into the wiki in the browser as the section for the
call. Do not clone the wiki or push to it from the command line.

### Calendar entry and reminder

Calls are virtual and typically take place on the fourth Wednesday of the
month. Each call is listed on the Trino events Google Calendar, which the
[community page](https://trino.io/community.html#events) embeds. Ask the user
to confirm that the entry for {{date}} exists with the title `Trino contributor
call`, the start time, and a link to the wiki page.

Draft a short reminder for the user to post on [Trino
Slack](https://trino.io/slack) and LinkedIn before the call. It names the date
and time, invites anyone to join, lists the main agenda topics, and links to
the wiki page for topic suggestions. Manfred adds the connection details and
posts it himself. The calendar and the wiki are public, so keep the connection
details out of both unless the user asks to include them.

### Screenshot

Remind the user to save the screenshot of the call as `tcc-{{compactdate}}.png`
in the call folder.

## Processing the recording

Use the {{date}}, the {{compactdate}}, and the folder from [Local call
folder](#local-call-folder).

Ask the user to provide the URL to the video recording on YouTube and remember
it as {{url}}.

Ask the user for the path to the local file with the rough meeting notes
markdown file and remember it as {{draftnotes}}. Suggest
`tcc-{{compactdate}}/tcc-{{compactdate}}.md` as the default, and move a file
from another location into the folder after confirming with the user. If there
is no file, proceed without it.

Ingest the meeting notes markdown file.

Take note of the attendees and any topics that were discussed.

Ingest the [wiki
page](https://github.com/trinodb/trino/wiki/Contributor-meetings) and locate the
section for the meeting date and take note of the attendees and topic
information there. If the section does not exist, create a new section for the
meeting date.

Analyze the video to create a list of attendees, a time-stamped list of
sections that discuss different topics, and a short description for each topic.
Use the content from the {{draftnotes}} as suggestions and further details for
the topics. Also take note of the title of the video as {{title}}.

Run the analysis twice, once for each of the two transcripts described in the
following section, write the output files for each transcript, and merge the
results into the final output files. Each source catches details and
corrects errors that the other misses, so the merged result is clearly better
than either one alone.

The final output files are working documents that stay local. Expect several
passes over them to refine the wording and to verify each timestamp against the
recording. Once they are final, copy and paste the content into the YouTube
video description and the wiki page in the browser. Do not clone the wiki or
push either file from the command line.

### Transcription

Analyzing the video requires timestamped transcripts from two sources, the
YouTube automatic captions and a local whisper-cpp transcription. Create both
with the `media-transcription` skill, using {{url}} as the source,
`tcc-{{compactdate}}` as the output folder, and `tcc-{{compactdate}}` as the
base name. Start the whisper-cpp prompt with `Trino contributor call.` and add
the expected attendee names from the draft notes, the wiki, the maintainers in
the `trinodb` skill, and the table in [Attendees list](#attendees-list), and
the project terms from the draft notes.

The transcription steps come from the `media-transcription` skill. If it is not
installed, ask the user to install it from the [getting-stuff-done
repository](https://github.com/simpligility/getting-stuff-done) before
continuing.

Automatic captions are usually missing for a few hours after the upload. If
only one transcript is available, create the output files for that transcript,
copy them to the final output files, and tell the user to run the second pass
once the other transcript is available. The second pass writes the output files
for the other transcript and merges them into the existing final output files
as described in [Compare and merge](#compare-and-merge), so it keeps any manual
edits.

#### Compare and merge

Analyze each transcript on its own first and write its output files. Do not
edit these per-transcript files afterwards, so they stay a record of what each
source produced. Then compare the two results topic by topic and merge them into
the final output files. When no final output files exist yet, start from a copy
of the whisper-cpp output files:

* Timestamps: use the whisper-cpp timestamps. Where whisper-cpp squashed cues
  together, check the YouTube timestamps instead.
* Speakers: use the `>>` markers in the YouTube captions to decide who said
  what. Flag any attribution that is still uncertain.
* Names, terms, and numbers: prefer the whisper-cpp spelling. Where the two
  transcripts disagree on a fact such as a version or a pull request number,
  verify it against the linked pull requests, the releases on GitHub, the draft
  notes, and the wiki.
* Content: add details and topics that only one transcript picked up, for
  example a short side remark that the other transcript garbled.

When the final output files already exist from an earlier pass, merge into them
rather than replacing them, since they may contain the user's manual edits.
Summarize what the comparison found and changed, and ask the user to decide on
uncertain speakers, ambiguous attendees, and whether to include minor details
before finalizing.

### YouTube description

Create a text file named `tcc-{{compactdate}}-final-youtube-description.txt`,
or the per-transcript variant from the table of files. Start with the video
title in the form `Trino contributor call {{date}}`, then a blank line, then the
list of the topics and their start time formatted in minutes and seconds:

```
Trino contributor call {{date}}

- mm:ss topic one
- mm:ss topic two
```

Add the following section to the file after the list

```
More details available in the meeting minutes at 
https://github.com/trinodb/trino/wiki/Contributor-meetings

Call organized and hosted by Manfred Moser. Sponsor him at 
https://github.com/sponsors/mosabua to support this and other open source 
initiatives.
```

### Minutes

Use the same information as stored in the YouTube description you just created.

Create a second file named `tcc-{{compactdate}}-final-minutes.md`, or the
per-transcript variant from the table of files, using markdown
formatting for the content with a 80 character hard wrap for paragraphs. Use
the following structure and insert data from analyzing the minutes and the
video:

```
# <video title>

[📹 Video recording on YouTube with timestamps]({{url}})

**Attendees**


**Topics**

```

### Attendees list

For the section of attendees, use an unordered list with one attendee per item.
Use the full name of each person followed by their GitHub username linked to
their profile in markdown format.

Consult the [Trino roles page](https://trino.io/development/roles) for the
current maintainers and subproject maintainers, and the list of [Trino
contributors](https://github.com/orgs/trinodb/people) for anyone else. Also look
at common attendees from prior events from the
[wiki](https://github.com/trinodb/trino/wiki/Contributor-meetings).

Typically the first entry is Manfred Moser aka mosabua, with the role added
inside the same brackets. Further entries follow the same pattern without a
role:

```
* Manfred Moser ([mosabua](https://github.com/mosabua), host and organizer)
* Dain Sundstrom ([dain](https://github.com/dain))
```

Attendees introduce themselves and are announced by their full name, and the
transcript often garbles those names, so match what you hear against the
full names of the maintainers and in the following table, and use the matching
GitHub account.

Trino maintainers and the maintainers of the subprojects are frequent
attendees. Their names and GitHub accounts are in the maintainers section of
the `trinodb` skill.

Other contributors who attended recent calls:

| Name | GitHub |
| --- | --- |
| Ben Breakstone | [bbreak](https://github.com/bbreak) |
| Kent Murra | [kmurra](https://github.com/kmurra) |
| Peter Kosztolanyi | [koszti](https://github.com/koszti) |
| Nitesh Yadav | [niteshy](https://github.com/niteshy) |
| Omer Raifler | [OmerRaifler](https://github.com/OmerRaifler) |
| Oussama Ben Nasr | [oucemabennasr](https://github.com/oucemabennasr) |
| Roey Ogen | [RoeyoOgen](https://github.com/RoeyoOgen) |
| Sajumon Joseph | [sajjoseph](https://github.com/sajjoseph) |
| Tony Baeg | [tbaeg](https://github.com/tbaeg) |
| Darin Chandler | none known |

These lists are references for matching names heard in the video to GitHub
accounts. Only list people who actually attended the call.

If you can't determine the GitHub details, just use the full name on its own,
without brackets.

### Topics list

For the topics list, you need the following details for each topics

* {{timestamp in mm:ss format}}
* {{timestamp in seconds}}
* {{topic title}}
* {{description of the topic}}

For the description create a summary of the discussion of the topic and add
links and other information from the {{draftnotes}} and the wiki topic
information. If any other links to pull requests or issue numbers are
mentioned, see if you can locate them with the Trino repository at
https://github.com/trinodb/trino and insert relevant links.

Format each section in the following manner:

```
[{{timestamp in mm:ss format}}]({{url}}?t={{timestamp in seconds}}) **{{topic title}}**

{{description of the topic}}

```

Ask for a review of the files and assist with any further refinement, based on
the info you already have and any further details received.

### Announcement

Once the video description and the wiki page are updated, Manfred announces the
recording and the meeting notes on LinkedIn and in the `#announcements` channel
on [Trino Slack](https://trino.io/slack), which he has official access to post
in. Ask him for the URL of the LinkedIn post and remember it as {{linkedinurl}}
so it can be recorded on the tracking issue.

## Tracking issue

Each call has a tracking issue in Manfred's [contributions
tracker](https://github.com/simpligility/contributions). Follow the
`manfred-contributions` skill for the title form, the labels, the body, the
assignment, and the manual step that adds the issue to the project board. Skip
this section when working for anyone else.

As part of the preparation, look for the open issue titled `Trino contributor
call {{date}}` with the `trinodb-community` label:

```
gh issue list --repo simpligility/contributions \
  --label trinodb-community --state open \
  --search "Trino contributor call {{date}} in:title"
```

When none matches, draft one with that title and label, and confirm it with the
user before creating it.

After the minutes are published to the wiki and the description is added to the
video, add a comment to the issue that states what was done and links to the
published wiki section, for example:

```
hosted and posted meeting notes at
https://github.com/trinodb/trino/wiki/Contributor-meetings#trino-contributor-call-{{date}}
```

Add a second comment once the announcements are out, for example:

```
announced the recording and meeting notes on LinkedIn at {{linkedinurl}} and in
the announcements channel on Trino Slack
```

Confirm with the user before commenting, then close the issue. Comments can
still be added after the issue is closed, so a late announcement does not need
the issue reopened.
