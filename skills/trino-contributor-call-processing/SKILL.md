---
name: trino-contributor-call-processing
description: Instructions for processing the video recording from a Trino contributor call recording available on YouTube to create time stamped list of topics and expanded summary for wiki. Use when you uploaded the recording and need to make it consumable for the community.
---

# Trino contributor call processing

Use this skill to process the video recording from a [Trino contributor
call](https://www.youtube.com/playlist?list=PLFnr63che7wYkKTBWGulzVbzLSV_wrSBq)
recording available on YouTube to create time stamped list of topics for the
video description and expanded summary for [the contributor meetings wiki
page](https://github.com/trinodb/trino/wiki/Contributor-meetings).

## Processing steps

Ask the user to provide the URL to the video recording on YouTube and remember
it as {{url}}.

Ask the user for the date of the meeting in the format YYYY-MM-DD and remember it as {{date}}. This will be used to locate the section in the wiki for the meeting and to create a new section if it does not exist.

Ask the user for the path to the local file with the rough meeting notes
markdown file and remember it as {{draftnotes}}. If there is no file, proceed without it.

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

### YouTube description

Create a text file named `youtube-description.txt` with a list of the topics and
their start time formatted in minutes and seconds:

```
- mm:ss topic one
- mm:ss topic two
```

Add the following section to the file after the list

```
More details available in the meeting minutes at 
https://github.com/trinodb/trino/wiki/Contributor-meetings

Call organized and hosted by Manfred Moser. Sponsor him at 
https://github.com/sponsors/mosabua to support this and other open source initiatives.
```

### Minutes

Use the same information as stored in the YouTube description you just created.

Create a second file named `minutes.md` using markdown formatting for the
content with a 80 character hard wrap for paragraphs. Use the following
structure and insert data from analyzing the minutes and the video:

```
# <video title>

[📹 Video recording on YouTube with timestamps]({{url}})

**Attendees**


**Topics**

```

### Attendees list

For the section of attendees, use their GitHub username and link to their
profile in markdown format. List one attendee per line, followed by a comma. 

Consult the list of [Trino contributors](https://github.com/orgs/trinodb/people)
for a list of potential attendees. Also look at common attendees from prior
events from the
[wiki](https://github.com/trinodb/trino/wiki/Contributor-meetings).

Typically the first entrance is Manfred Moser aka mosabua with

```
[mosabua](https://github.com/mosabua) (Host and organizer),
```

Other commons examples might be

```
[dprophet](https://github.com/dprophet),
[wendigo](https://github.com/wendigo), 
[pettyjamesm](https://github.com/pettyjamesm),
[dain](https://github.com/dain),
[martint](https://github.com/martint),
[electrum](https://github.com/electrum),
[sajjoseph](https://github.com/sajjoseph), 
[raunaqmorarka](https://github.com/raunaqmorarka)
```

If you can't determine the GitHub details, just use the name from the video as
you can determine it.

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
the info you already have and any further details received.etails received.