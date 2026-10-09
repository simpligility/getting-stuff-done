---
name: trinodb-community-broadcast
description: Run the mechanics of a Trino Community Broadcast episode — the local episode folder, the announcement pull request on trino.io that lists the upcoming episode with its live stream links, the guest invite with the StreamYard link, the Trino events calendar entry, and the episode page pull request that is opened before the show as the working show notes and merged after the recording with the chapter list, the reset of the upcoming episode placeholder, and the processing of the YouTube recording with whisper-cpp and the automatic captions into the chapter list and a ready to paste video description. Child skill of the trinodb family. Use when preparing, announcing, or publishing a Trino Community Broadcast episode.
---

# Trino Community Broadcast

Use this skill for the mechanics of an episode of the [Trino Community
Broadcast](https://trino.io/broadcast/), the live stream show of the Trino
project, usually shortened to TCB. It builds on these skills:

- `trinodb` for the organization and the fork-and-upstream contribution
  workflow that every pull request in this skill follows.
- `trinodb-website` for the local build of the
  [trinodb/trino.io](https://github.com/trinodb/trino.io) repository, the
  writing style for site content, and the linking traps.

The skill covers the mechanics only. Choosing topics and guests, briefing
guests, and running the live show are up to the hosts.

## Episode lifecycle

Each episode moves through the same steps. The two pull requests on trino.io
are the main deliverables:

1. File or find the tracking issue for the episode idea.
2. Agree on the guest, the topic, and the air date.
3. Create the local episode folder.
4. Open the announcement pull request and ask the guest to review the text.
5. Schedule the live stream, add the stream links, and merge the announcement.
6. Send the guests an invite with the StreamYard guest link.
7. Add the episode to the Trino events calendar.
8. Branch off the updated `master` with the merged announcement and open the
   episode page pull request. It stays open as the working show notes until
   after the show.
9. Air the episode live.
10. Process the recording into the chapter list and the YouTube description.
11. Add the chapter list and the final details to the episode page, and merge
    the pull request.
12. Follow up on YouTube, LinkedIn, and Trino Slack.
13. Close the tracking issue.

Ask the user for the episode number and remember it as {{number}}. Episodes are
numbered consecutively, and the current number is the one in the placeholder
under **Upcoming episodes** in `broadcast/index.md`.

## Tracking issue

Each episode has a tracking issue in Manfred's [contributions
tracker](https://github.com/simpligility/contributions). Follow the
`manfred-contributions` skill for the title form, the labels, the body, the
assignment, and the manual step that adds the issue to the project board. Skip
this section when working for anyone else.

Episode ideas are often filed long before a date exists, so look for an open
issue with the `trinodb-community-broadcast` label first:

```
gh issue list --repo simpligility/contributions \
  --label trinodb-community-broadcast --state open
```

When none matches, draft one titled `Record a TCB episode about <topic>`, with
the labels `trinodb-community` and `trinodb-community-broadcast`, and confirm
it with the user before creating it. Keep the issue current as the episode
moves along:

- Set the status to `In progress` once the guest and date are agreed.
- Add the announcement and episode page pull requests to the body as full URLs,
  along with the guest and the YouTube stream link.
- End the body with the next step, such as sending the guest invite or adding
  the chapter list after the show.
- Close the issue once the episode page pull request is merged. Closing moves
  the board item to `Done`.

## Local episode folder

Keep the working files for an episode in a folder named `tcb{{number}}` in the
current working directory, for example `tcb79`. It holds images for the title
slide, the thumbnail, and promotion, the draft show notes, and the transcripts.

The reusable show assets live in a sibling folder named
`trino-community-broadcast`: the intro and outro videos, the segment bumpers
for guest intro, release updates, demo, sponsor thanks, and upcoming events,
the background music, and the `Title Slide.pptx` template. Do not modify these
for a single episode. Copy what needs episode-specific changes, such as the
title slide, into the episode folder.

Images often come with a white background that needs to be transparent for the
title slide. JPEG has no alpha channel, so write the result as PNG. For flat
illustrations with dark outlines, a flood fill from the edges removes the
background and keeps white areas inside the figures:

```
magick input.jpeg -bordercolor white -border 1 -alpha set -fuzz 12% \
  -fill none -draw "color 0,0 floodfill" -shave 1x1 output.png
```

Verify the result by flattening it onto a loud color such as magenta and
looking at it. For rendered 3D images with soft shadows and white surfaces
without outlines, the flood fill either leaves the floor shadow or eats into
the figures. Lower the fuzz value to protect the figures, or use a
background-removal model instead.

## Announcement pull request

The announcement replaces the placeholder entry under **Upcoming episodes** in
`broadcast/index.md` with the details of the episode. Title the pull request
and commit `Announce TCB {{number}} about <topic>`. Reference pull requests are
[TCB 79](https://github.com/trinodb/trino.io/pull/855) and
[TCB 78](https://github.com/trinodb/trino.io/pull/824).

The placeholder between episodes looks like this:

```html
<dl>
<dt>February 2026: Trino Community Broadcast 79 - to be determined</dt>
<dd></dd>
</dl>
```

Replace it with the air date, the episode title, and a short paragraph in the
`<dd>` element:

```html
<dl>
<dt>7 Oct 2026: Trino Community Broadcast 79 - Going for 1.0.0</dt>
<dd><a href="https://github.com/nineinchnick">Jan Waś</a>
joins us to talk more about the amazing work on
<a href="https://github.com/trinodb/trino-go-client">the trino-go-client</a>
that led to the recent 1.0.0 release. We learn about the rich feature set,
collaborators, how we got here, performance, and next steps.
Live stream events on
<a href="https://www.youtube.com/watch?v=VIDEO_ID"><i class="fab fa-youtube" style="color: red;"></i> YouTube</a>, and
<a href="https://www.linkedin.com/events/EVENT_ID/"><i class="fab fa-linkedin" style="color: blue;"></i> LinkedIn</a>
</dd>
</dl>
```

Content of the entry:

- The paragraph introduces the guest with a link to their GitHub or LinkedIn
  profile, names the hosts when they differ from the usual, and lists what the
  episode covers. It becomes the `introduction` of the episode page later, so
  write it to stand on its own.
- The live stream links use the Font Awesome icons as shown. Add a Twitch link
  to `https://www.twitch.tv/simpligility` when the episode also streams there.
- Double-check the year in the date. The TCB 78 announcement went out in
  December with the past year and needed a [follow-up
  fix](https://github.com/trinodb/trino.io/pull/826).

Open the pull request before the stream links exist, and mention the guest in
the description to ask them to review the text, for example `Text okay though
@nineinchnick ?`. Then schedule the live stream in StreamYard, which creates
the YouTube and LinkedIn events, add their URLs to the entry, and merge once the
guest confirms.

## Guest invite

Once the stream is set up in StreamYard, send each guest a calendar invite for
the episode. The invite needs these details:

- The title `Trino Community Broadcast {{number}} - <episode title>`.
- The start time, plus time before the stream to check audio, video, and
  screen sharing.
- The StreamYard guest link to join the studio. Guests join the studio, not the
  public YouTube or LinkedIn stream.
- The YouTube and LinkedIn stream links, so guests can share them.
- A link to the episode page pull request, once it is open, so guests can
  review and add to the show notes.

Ask the user for the StreamYard guest link, the guest email addresses, and how
much earlier to start than the stream. The guest link is not public, so never
add it to trino.io, the pull requests, or the calendar entry.

## Calendar entry

After the announcement is merged, add the episode to the Trino events Google
Calendar, which the [community page](https://trino.io/community.html#events)
embeds. The entry needs these details:

- The title `Trino Community Broadcast {{number}} - <episode title>`.
- The start time and the duration of the stream.
- A description with the announcement paragraph, the YouTube and LinkedIn
  stream links, and a link to the [broadcast
  page](https://trino.io/broadcast/).

Use only public links in the calendar entry. The calendar is public, so it
must never carry the StreamYard guest link.

## Episode page pull request

Once the announcement is merged, update the local `master` from upstream, create
a new branch from it, and open the episode page pull request. Title the pull
request and commit `Add TCB {{number}}`. The reference is the [TCB 78 pull
request](https://github.com/trinodb/trino.io/pull/825), which was opened a month
before the show and merged a few days after it.

The pull request is the working document for the show. Fill in what is known
before the show — the hosts, the guest, the introduction, the release updates
and news, the topic outline, and the upcoming events — so it serves as the run
of show. Mention the guest in the description and add the details they send.
After the show, add the chapter list and adjust the content to what was
actually discussed, then squash and merge.

The pull request changes these files:

| File | Change |
|---|---|
| `_episodes/{{number}}.md` | New episode page |
| `assets/episode/tcb{{number}}_<name>.png` | Images shown on the episode page, if any |
| `broadcast/index.md` | Placeholder for the next episode replaces the announcement |

### Front matter

```yaml
---
layout: episode
title: "78: A view with a view with a view"
date: 2026-01-16
tags: trino view agent ai application architecture
youtube_id: "ovtTaYKIrQ8"
wistia_id:
sections:
  - time: 00:00
    title: "Introduction with Manfred and Cole"
  - time: 1:47
    title: Release updates for Trino 478 and 479
  - time: 17:01
    title: Introducing Rob Dickinson
introduction: |
  Long-time Trino user and expert Rob Dickinson joins Manfred and Cole to chat
  about ...
---
```

- `title` is the episode number, a colon, and the title from the announcement.
  Quote it.
- `date` is the air date.
- `tags` is a space-separated list of lowercase keywords.
- `youtube_id` is the ID from the YouTube stream URL in the announcement.
  Quote it, since IDs can start with a dash or look like a number.
- `wistia_id` stays empty. Wistia hosted older episodes only.
- `sections` is the chapter list, filled in after the show. Use `mm:ss`
  before the one hour mark and `h:mm:ss` after it. Quote a title that contains
  a colon.
- `introduction` reuses the announcement paragraph without the HTML and the
  stream links.

Create the chapter list as described in [Processing the
recording](#processing-the-recording), and use the same list for the chapters
in the YouTube video description.

### Body

The body follows a fixed sequence of `##` sections:

1. **Host** lists the hosts with a link to their LinkedIn profile, their title,
   and their employer. Copy the entries from the previous episode and confirm
   the current titles and employers with the user.
2. **Guest** lists the guests in the same form.
3. **Releases and news** has a `###` heading for every Trino release since the
   previous episode, linked as
   `{{site.baseurl}}/docs/current/release/release-<version>.html`, with a
   short list of highlights from the release notes. Close the releases
   with `As always, numerous performance improvements, bug fixes, and other
   features were added as well.` Then add `### Other releases and news` for
   subproject releases, contributor call minutes, and other project news.
4. **Introducing <guest first name>** is a short paragraph about the guest's
   background.
5. One or more topic sections, titled after the episode or the topics,
   summarize the discussion with links and embedded images.
6. **Resources** lists the links to the projects and material discussed.
7. **Rounding out** lists upcoming events with dates in the form `28 Jan 2026 -
   [Event](link)`, and ends with a call for guests and topics for the next
   episode.

Embed images with an HTML tag and the site base URL:

```html
<img src="{{site.baseurl}}/assets/episode/tcb78_virtual_view_topology.png"/>
```

### Reset the placeholder

In the same pull request, replace the announcement entry in
`broadcast/index.md` with a placeholder for the next episode, so the change
goes live together with the episode page. Use the expected month and year when
known:

```html
<dl>
<dt>February 2026: Trino Community Broadcast 79 - to be determined</dt>
<dd></dd>
</dl>
```

Build the site locally as described in `trinodb-website` and check the episode
page and the broadcast index before opening the pull request.

## Processing the recording

StreamYard streams the episode to YouTube and LinkedIn and leaves no local
recording, so process the YouTube video. The YouTube URL is the stream link
from the announcement, and the `youtube_id` in the episode front matter.
Remember it as {{url}}.

### Files

Keep the processing files in the episode folder `tcb{{number}}`:

| File | Content |
| --- | --- |
| `tcb{{number}}-transcript-whisper.vtt` | Raw whisper-cpp transcript |
| `tcb{{number}}-transcript-whisper.txt` | Condensed whisper-cpp transcript |
| `tcb{{number}}-transcript-youtube.vtt` | Raw YouTube captions |
| `tcb{{number}}-transcript-youtube.txt` | Condensed YouTube captions |
| `tcb{{number}}-whisper-youtube-description.txt` | Description from the whisper-cpp transcript |
| `tcb{{number}}-youtube-youtube-description.txt` | Description from the YouTube captions |
| `tcb{{number}}-final-youtube-description.txt` | Merged final description |

### Transcription

Use two timestamped transcripts, a local whisper-cpp transcription and the
YouTube automatic captions. Each catches details and corrects errors that the
other misses. Create both with the `media-transcription` skill, using {{url}}
as the source, the episode folder `tcb{{number}}` as the output folder, and
`tcb{{number}}` as the base name. Pass the episode title, the host and guest
names, and project terms in the whisper-cpp prompt, for example `Trino
Community Broadcast 79, Going for 1.0.0. Manfred Moser, ...`.

Right after the show, the audio download for whisper-cpp takes several minutes,
and the automatic captions are usually missing for a few hours.

Start with whichever transcript is available, write its description file, and
copy it to the final description. Tell the user to run the second pass once the
other transcript is available.

### Chapters

Read the whole transcript and create a chapter for each topic change. Typical
chapters, in order, are the introduction, the release updates, the subproject
and community news, the guest introduction, the discussion topics, each demo,
what's next for the guests, and rounding out with upcoming events. Keep
chapters at least a minute apart, and merge shorter ones.

Verify the facts heard in the recording before using them in titles or the
episode page. Check versions against the GitHub releases of the project, find
the pull requests and issues for features that are mentioned, and match
garbled names against the contributors on those pull requests with `gh`.

### YouTube description

Write the description file in the following format. YouTube turns the
timestamp lines into chapters, which requires the first one to be `0:00`.
YouTube also keeps every line break, so write the introduction paragraph on a
single line instead of hard wrapping it:

```
<guests> join Manfred Moser to talk about <topic>. We learn about <what the episode covers>.

0:00 Introduction with Manfred
1:02 Release updates for Trino 480, 481, 482, and 483
...

More details at https://trino.io/episodes/{{number}}

Episode hosted and organized by Manfred Moser. Sponsor his Trino-related and other open source work at
https://github.com/sponsors/mosabua
```

Base the introduction on the one from the episode page, but name Manfred
instead of "us", since the description stands on its own. The episode link
only works once the episode page pull request is merged.

### Compare and merge

For the second pass, write the description file for the second transcript
without looking at the final one, and do not edit the per-transcript files
afterwards. Then merge it into the final description, which may contain the
user's manual edits:

- Timestamps: use the whisper-cpp timestamps, unless whisper-cpp squashed cues
  together during crosstalk.
- Speakers: use the `>>` markers in the YouTube captions.
- Names, terms, and numbers: prefer whisper-cpp, and verify disagreements
  against GitHub.
- Content: add topics that only one transcript picked up.

Summarize what the comparison changed, and ask the user about uncertain
details.

### Episode page and video

Copy the chapters from the final description into the `sections` list of the
episode page, using `00:00` for the first entry. Update the guest
introduction, the topic sections, and the resources to what was actually
discussed, with links to the pull requests and releases found while verifying.

Once the user confirms the final description, they paste it into YouTube as
described in [After the show](#after-the-show). Do not change the video from
the command line.

## After the show

StreamYard already sets the thumbnail on the YouTube video, and the video is
added to the Trino Community Broadcast playlist, so neither needs a follow-up.
The remaining steps are manual in the browser. Remind the user of them once the
episode page is merged, since the steps link to it.

On YouTube:

- Paste the final description into the video description in YouTube Studio.
- Pin a comment with a link to the episode page.

On LinkedIn:

- Edit the text of the live video post to link to the YouTube recording and
  the episode page. LinkedIn has no clickable chapters, so add two or three
  highlights instead of the full chapter list.
- Post once in the event with the links to the recording and the episode page,
  which reaches the registered attendees who missed the stream.
- Publish a separate follow-up post a day or two later that tags the guests.
  Put the links in the first comment rather than the post, since LinkedIn tends
  to show posts with external links to fewer people. A short native clip of a
  highlight from the episode works better than a link.
- Reply to the comments left during the stream.

On Trino Slack:

- Announce the recording and the show notes in the `#announcements` channel on
  [Trino Slack](https://trino.io/slack), with links to the episode page and the
  YouTube recording. Manfred has official access to post there.

Ask the user for the URL of the LinkedIn post and add it to the tracking issue
with the episode page link before closing the issue.

StreamYard keeps the recording in its library with a download option. Download
it only when a local copy is needed, for example as a cleaner audio source for
the transcription or for cutting highlight clips.
