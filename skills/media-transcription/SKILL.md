---
name: media-transcription
description: Transcribe a local video or audio file, or a YouTube video, into timestamped text — the YouTube automatic captions when the recording is on YouTube, a local whisper-cpp transcription, condensed text versions of both, and the rules for combining the two sources. Also shrinks a large video file while keeping the audio unchanged. Use whenever a recording needs a transcript, on its own or from a skill that processes recordings, such as trinodb-contributor-call-processing or trinodb-community-broadcast.
---

# Media transcription

Use this skill to turn a recording into timestamped transcripts. It covers the
mechanics only: getting the audio, transcribing it, and condensing the result
into text that is easy to read and analyze. What to do with the transcripts,
for example chapters, minutes, or a video description, is up to the user or the
calling skill.

## Inputs and files

Ask for, or take from the calling skill:

* {{source}}, the path to a local video or audio file, or a YouTube URL. Any
  format that `ffmpeg` reads works, such as MP4, MOV, MKV, M4A, MP3, or WAV.
* {{name}}, the base name for the output files. Default to the file name of a
  local source without its extension.
* {{outdir}}, the folder for the output files. Default to a folder named
  {{name}} in the current working directory, and create it if needed.

If {{source}} is a local file, ask whether the recording is also on YouTube. If
it is, remember the URL as {{url}} and use both sources.

The skill writes the following files into {{outdir}}. A calling skill can
change the names to fit its own scheme:

| File | Content |
| --- | --- |
| `{{name}}-transcript-whisper.vtt` | Raw whisper-cpp transcript |
| `{{name}}-transcript-whisper.txt` | Condensed whisper-cpp transcript |
| `{{name}}-transcript-youtube.vtt` | Raw YouTube captions |
| `{{name}}-transcript-youtube.txt` | Condensed YouTube captions |

Keep downloaded and intermediate files such as the audio in a scratch folder
{{outdir}}/.scratch inside the working directory, not in a system temporary
directory. Refer to it with absolute paths and never `cd` into it. Claude Code
can adopt the folder as its working directory and leave a `.claude` folder
behind. Delete the scratch folder when done.

## Tools

The skill needs `ffmpeg` and `whisper-cpp` from Homebrew, `yt-dlp` for YouTube
sources, and the whisper large-v3-turbo model of about 1.6 GB. Check what is
installed with `which ffmpeg whisper-cli yt-dlp`, and confirm with the user
before installing anything that is missing:

```
brew install ffmpeg whisper-cpp yt-dlp
mkdir -p ~/.cache/whisper-cpp
curl -L -o ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin \
  https://huggingface.co/ggerganov/whisper.cpp/resolve/main/ggml-large-v3-turbo.bin
```

The model lives outside the working directory. Ask the user before reading it.
In a sandboxed agent session, the `whisper-cli` command may also need an
exception from the sandbox to read the model and use the GPU.

## YouTube captions

When the recording is on YouTube, start with the automatic captions. They
download in seconds and mark each change of speaker. Download them with
`yt-dlp`, which also prints the video title and duration:

```
yt-dlp --skip-download --write-auto-subs --sub-langs "en-orig" \
  --sub-format vtt --print "%(title)s | %(duration_string)s" --no-simulate \
  -o "{{outdir}}/.scratch/captions" "{{url}}"
```

Request the `en-orig` track. The `en` track is the same speech recognition
output, but downloading it often fails with `HTTP Error 429: Too Many
Requests`. The captions are usually missing for a few hours after an upload or
a live stream. If `yt-dlp` reports that there are no subtitles, they are not
ready yet. Continue with whisper-cpp alone and tell the user to add the captions
in a second pass later.

Move the captions to `{{outdir}}/{{name}}-transcript-youtube.vtt`. They repeat
each line across consecutive cues and contain inline timing tags. Condense them
to one timestamped line per unique text:

```
awk '/-->/{t=substr($1,1,8); next}
  NF && !/^(WEBVTT|Kind:|Language:)/ {
    gsub(/<[^>]*>/, ""); gsub(/&gt;/, ">")
    if (!($0 in seen)) { seen[$0] = 1; print t " " $0 }
  }' "{{outdir}}/{{name}}-transcript-youtube.vtt" \
  > "{{outdir}}/{{name}}-transcript-youtube.txt"
```

## Local whisper-cpp transcript

Extract the audio as 16 kHz mono WAV, which is what whisper-cpp expects. For a
local video or audio file, `ffmpeg` does this in one step, and `-vn` skips the
video stream:

```
ffmpeg -i "{{source}}" -vn -ar 16000 -ac 1 "{{outdir}}/.scratch/audio16.wav"
```

For a YouTube source, download the audio first:

```
yt-dlp -f bestaudio -x --audio-format wav \
  -o "{{outdir}}/.scratch/audio.%(ext)s" "{{url}}"
ffmpeg -i "{{outdir}}/.scratch/audio.wav" -ar 16000 -ac 1 \
  "{{outdir}}/.scratch/audio16.wav"
```

Right after a live stream, YouTube still serves the video as an archive in
thousands of small fragments, so the audio download of a 90 minute stream takes
several minutes.

Transcribe the audio into a VTT file:

```
whisper-cli -m ~/.cache/whisper-cpp/ggml-large-v3-turbo.bin \
  -f "{{outdir}}/.scratch/audio16.wav" -l en -ovtt \
  -of "{{outdir}}/{{name}}-transcript-whisper" \
  --prompt "Board meeting of the Example Society. Jane Doe, John Roe, ..."
```

On Apple silicon, whisper-cpp transcribes an hour of audio in about two
minutes.

The `--prompt` makes the biggest difference to the quality. Without it,
whisper-cpp guesses at names, places, and jargon. Ask the user for an agenda,
meeting notes, or a list of attendees before the first run, and pass the type
of recording, the full names of the speakers, and project and place names.
Keep the prompt to a few lines, since whisper-cpp only uses about the last 220
tokens of it. If a transcript comes back with garbled names, rerunning it with
a better prompt costs only a few minutes.

Condense the VTT file to one timestamped line per cue for reading and
analysis:

```
awk '/-->/{t=substr($1,1,8); next} NF && !/WEBVTT/{print t" "$0}' \
  "{{outdir}}/{{name}}-transcript-whisper.vtt" \
  > "{{outdir}}/{{name}}-transcript-whisper.txt"
```

## Strengths of each source

The two sources fail in different ways, so each catches errors the other makes:

* whisper-cpp is the better source for names, terms, numbers, and timestamps.
  It has no speaker labels, and during crosstalk it sometimes squashes several
  cues into a few seconds.
* The YouTube captions mark each change of speaker with `>>`, which makes them
  the better source for attributing statements to people. They garble names,
  terms, and numbers more than whisper-cpp does, and their timestamps at the
  start of a recording can run several seconds late.

When both are available, analyze each transcript on its own first, then compare
and merge the results:

* Timestamps: use the whisper-cpp timestamps. Where whisper-cpp squashed cues
  together, check the YouTube timestamps instead.
* Speakers: use the `>>` markers in the YouTube captions to decide who said
  what. Flag any attribution that is still uncertain.
* Names, terms, and numbers: prefer the whisper-cpp spelling. Where the two
  disagree on a fact, verify it against an independent source, such as the
  notes or the project the recording is about.
* Content: add details that only one transcript picked up.

With only a local file, there is no second source and no speaker labels. Say
so when a task depends on knowing who said what.

## Shrink a video

A screen or camera recording of a meeting is often far larger than it needs to
be. When the user wants a smaller copy, keep the audio stream unchanged and
re-encode only the video at a lower resolution and frame rate:

```
ffmpeg -i "{{source}}" -vf "scale=-2:720,fps=15" \
  -c:v libx265 -preset fast -crf 30 -x265-params log-level=error \
  -tag:v hvc1 -c:a copy -movflags +faststart \
  "{{outdir}}/{{name}}-small.mp4"
```

* `-c:a copy` keeps the audio bit for bit, so its quality does not change.
* The `hvc1` tag lets QuickTime and other Apple players open the HEVC file.
* A 79 minute 1080p meeting recording of 1.6 GB shrinks to about 150 MB in
  about three minutes. Lower the `-crf` value, for example to 26, if the video
  looks too soft.
* The hardware encoder `hevc_videotoolbox` is faster, but fails with error
  `-12908` inside a sandbox. The software encoder `libx265` works everywhere.

Use the small copy as the source for the transcription, since it has the same
audio. Never delete the original. Leave that to the user.

## Clean up

Delete the scratch folder with the audio once the transcripts are written. Keep
the raw VTT files and the condensed text files in {{outdir}}, so they stay
available for later passes.
