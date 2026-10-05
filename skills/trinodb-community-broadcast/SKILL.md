---
name: trinodb-community-broadcast
description: Run the mechanics of a Trino Community Broadcast episode — the local episode folder, the announcement pull request on trino.io that lists the upcoming episode with its live stream links, the guest invite with the StreamYard link, the Trino events calendar entry, and the episode page pull request that is opened before the show as the working show notes and merged after the recording with the chapter list and the reset of the upcoming episode placeholder. Child skill of the trinodb family. Use when preparing, announcing, or publishing a Trino Community Broadcast episode.
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
- `trinodb-contributor-call-processing` for the transcription of a recording
  with `yt-dlp` and whisper-cpp, which the chapter list of an episode reuses.

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
10. Add the chapter list and the final details to the episode page, and merge
    the pull request.
11. Close the tracking issue.

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

Create the chapter list from the YouTube recording with the transcription steps
in `trinodb-contributor-call-processing`, and keep the transcripts in the
episode folder. Use the same list for the chapters in the YouTube video
description.

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
