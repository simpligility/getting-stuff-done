---
name: trinodb-contributor-call-processing
description: Process the recording of a Trino contributor call from YouTube into a timestamped topic list for the video description and an expanded summary for the contributor meetings wiki. Use after the recording is uploaded, when it needs to be made consumable for the community.
---

# Trino contributor call processing

Use this skill to process the video recording from a [Trino contributor
call](https://www.youtube.com/playlist?list=PLFnr63che7wYkKTBWGulzVbzLSV_wrSBq)
recording available on YouTube to create time stamped list of topics for the
video description and expanded summary for [the contributor meetings wiki
page](https://github.com/trinodb/trino/wiki/Contributor-meetings).

It builds on the shared context in the `trinodb` skill, which covers the
organization and points at the development roles page that lists the
maintainers by name.

## Processing steps

Ask the user to provide the URL to the video recording on YouTube and remember
it as {{url}}.

Ask the user for the date of the meeting in the format YYYY-MM-DD and remember
it as {{date}}. This will be used to locate the section in the wiki for the
meeting and to create a new section if it does not exist. Also remember the
date without dashes in the format YYYYMMDD as {{compactdate}} for the names of
the output files.

Ask the user for the path to the local file with the rough meeting notes
markdown file and remember it as {{draftnotes}}. If there is no file, proceed
without it.

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

Both output files are working documents that stay local. Expect several passes
over them to refine the wording and to verify each timestamp against the
recording. Once they are final, copy and paste the content into the YouTube
video description and the wiki page in the browser. Do not clone the wiki or
push either file from the command line.

### Transcription

Analyzing the video requires a timestamped transcript. Keep all downloaded and
generated files in a scratch directory, not next to the output files.

First, try the YouTube captions with `yt-dlp`. This also prints the video title
and duration:

```
yt-dlp --skip-download --write-auto-subs --write-subs --sub-langs "en.*" \
  --sub-format vtt --print "%(title)s | %(duration_string)s" --no-simulate \
  -o transcript "{{url}}"
```

Automatic captions are usually missing for a few hours after the upload. If
`yt-dlp` reports that there are no subtitles, transcribe the audio locally with
whisper-cpp instead. It requires `ffmpeg` and `whisper-cpp` from Homebrew and
the large-v3-turbo model of about 1.6 GB. Confirm with the user before
installing anything that is missing:

```
brew install ffmpeg whisper-cpp
mkdir -p ~/.cache/whisper-cpp
curl -L -o ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
```

Download the audio, convert it to 16 kHz mono, and transcribe it. Pass the
expected attendee names and project terms with `--prompt` to improve the
spelling of names:

```
yt-dlp -f bestaudio -x --audio-format wav -o "audio.%(ext)s" "{{url}}"
ffmpeg -i audio.wav -ar 16000 -ac 1 audio16.wav
whisper-cli -m ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin -f audio16.wav \
  -l en -ovtt -of transcript \
  --prompt "Trino contributor call. Manfred Moser, Dain Sundstrom, ..."
```

On Apple silicon, whisper-cpp transcribes a one-hour call in about two minutes.
The timestamps are accurate enough for the topic list. Expect garbled product
names, people's names, and occasional wrong words, so verify facts against the
draft notes, the linked pull requests, and the wiki. The transcript has no
speaker labels, so infer speakers from context and flag any attribution that
is uncertain.

Condense the VTT file to one timestamped line per cue before reading it:

```
awk '/-->/{t=substr($1,1,8); next} NF && !/WEBVTT/{print t" "$0}' \
  transcript.vtt > transcript.txt
```

Keep the raw full transcript next to the output files as
`tcc-{{compactdate}}-transcript.vtt`, so it stays available for later
refinement and for comparing transcription sources. The YouTube captions
download as `transcript.en.vtt` or similar, the whisper-cpp output as
`transcript.vtt`. Delete the remaining scratch files such as the audio.

### YouTube description

Create a text file named `tcc-{{compactdate}}-youtube-description.txt` with a
list of the topics and their start time formatted in minutes and seconds:

```
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

Create a second file named `tcc-{{compactdate}}-minutes.md` using markdown
formatting for the content with a 80 character hard wrap for paragraphs. Use the following
structure and insert data from analyzing the minutes and the video:

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
full names in the following tables and use the matching GitHub account.

Trino maintainers are frequent attendees:

| Name | GitHub |
| --- | --- |
| Chen Jian | [chenjian2664](https://github.com/chenjian2664) |
| Dain Sundstrom | [dain](https://github.com/dain) |
| Yuya Ebihara | [ebyhr](https://github.com/ebyhr) |
| David Phillips | [electrum](https://github.com/electrum) |
| Piotr Findeisen | [findepi](https://github.com/findepi) |
| Ashhar Hasan | [hashhar](https://github.com/hashhar) |
| Kasia Findeisen | [kasiafi](https://github.com/kasiafi) |
| Grzegorz Kokosiński | [kokosing](https://github.com/kokosing) |
| Łukasz Osipiuk | [losipiuk](https://github.com/losipiuk) |
| Martin Traverso | [martint](https://github.com/martint) |
| James Petty | [pettyjamesm](https://github.com/pettyjamesm) |
| Praveen Krishna | [Praveen2112](https://github.com/Praveen2112) |
| Raunaq Morarka | [raunaqmorarka](https://github.com/raunaqmorarka) |
| Karol Sobczak | [sopel39](https://github.com/sopel39) |
| Mateusz Gajewski | [wendigo](https://github.com/wendigo) |

The maintainers of the subprojects aws-proxy, charts, grafana-trino, trino.io,
trino-gateway, trino-go-client, trino-js-client, and trino-odbc attend as well:

| Name | GitHub |
| --- | --- |
| Jaeho Yoo | [Chaho12](https://github.com/Chaho12) |
| Cole Bowden | [colebow](https://github.com/colebow) |
| Erik Anderson | [dprophet](https://github.com/dprophet) |
| Jan Waś | [nineinchnick](https://github.com/nineinchnick) |
| Star Poon | [oneonestar](https://github.com/oneonestar) |
| Jordan Zimmerman | [Randgalt](https://github.com/Randgalt) |
| Filipe Regadas | [regadas](https://github.com/regadas) |
| Riley McDowell | [rileymcdowell](https://github.com/rileymcdowell) |
| Pablo Arteaga | [vagaerg](https://github.com/vagaerg) |
| Vishal Jadhav | [vishalya](https://github.com/vishalya) |

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

These tables are references for matching names heard in the video to GitHub
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
so it can be recorded on the tracking ticket.

### Tracking ticket

Each call has a tracking ticket in Manfred's [contributions
tracker](https://github.com/simpligility/contributions). Find the open issue
titled `Trino contributor call {{date}}` with the `Trino community` label using
the `gh` command line tool.

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
