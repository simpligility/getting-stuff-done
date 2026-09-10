---
name: manfred-slides
description: Manfred Moser's conventions for presentation slide decks — structure, narrative flow, and slide content. Extends the `manfred-writing` skill and is a component of the `manfred` skill family. Activate only when the `manfred` skill is already active and its index directs you here, or when Manfred explicitly invokes it; do not auto-activate on generic slide or presentation work by description match alone.
---

# Manfred Moser — presentation slide decks

> **Base-context check.** This skill encodes Manfred's personal conventions and
> assumes the `manfred` base skill established the working context. If `manfred`
> was not activated earlier in this session, pause and ask before applying these
> conventions: "The `manfred` base skill isn't active this session — load it
> first for full context, or proceed anyway?" Once `manfred` is active (or the
> user confirms), continue without asking again.

This skill extends `manfred-writing`. All of its voice, tone, audience, and
markdown house-style rules apply to slide content as well — this skill only adds
the structure, narrative, and slide-specific guidance on top. When working on a
deck, treat `manfred-writing` as active too and invoke it if it is not.

The general `slides-prep` skill drives the whole talk process — proposal, idea
dump, the slide-ready markdown outline, generating the deck, and reviewing it
through to finished. This skill is an optional, Manfred-specific guideline that
layers his personal deck preferences on top of that process; `slides-prep` does
not hand off to it. Use this skill as extra guidance whenever the deck is
Manfred's.

## Tooling and workflow

Slides are tool-agnostic in principle, but the default workflow now pairs a
markdown outline with a Google Slides deck, kept in sync through the `gws`
Google Workspace CLI. Focus effort on content, structure, and flow rather than
on tool-specific formatting or theming. When the source is markdown, follow the
`manfred-writing` markdown house style, including the 80-character hard wrap.

### Primary — markdown outline plus Google Slides via gws

- Author and iterate the per-slide flow in a markdown outline, following the
  `slides-prep` format and the markdown house style.
- Drive the Google Slides deck with the `gws` CLI from
  https://github.com/googleworkspace/cli. It reads and writes Docs and Slides
  through the Workspace REST APIs, so it can ingest source docs, build a deck
  from the outline, and edit an existing deck in place.
- One-time requirements and setup:
  - Install the `gws` CLI and the Google Cloud CLI that `gws auth setup`
    depends on.
  - Run `gws auth setup` as the account that owns the target files. Reuse an
    existing GCP project you can already access to sidestep org-policy limits on
    creating projects, and enable the Docs, Slides, and Drive APIs on it.
  - Grant the Docs, Slides, and Drive scopes at the OAuth consent screen.
- Read a doc with `gws docs documents get`. Read a deck with
  `gws slides presentations get`, and apply changes with
  `gws slides presentations batchUpdate`, validating first with `--dry-run`.
- Content lives in placeholders addressed by object ID. Slide titles, body
  text, and speaker notes through each slide's `speakerNotesObjectId` are all
  editable this way.

### Fallback — when gws is unavailable or not wanted

- Pure markdown rendered with reveal.js, where the markdown is the final
  product.
- Ideate in markdown, generate a PowerPoint from it — today through Claude
  Cowork — then import into Google Slides and refine there.
- Manfred never edits PowerPoint or Keynote files directly. Work stays in
  markdown or Google Slides.

### Keeping the outline and deck in sync

The markdown outline and the Google Slides deck are both living artifacts and
stay in sync going forward. Manfred edits either one and says which file he
changed. Design, layout, images, and other visual work live in Slides, so every
deck change must be surgical.

- Target only the specific slides, placeholders, or notes that changed with a
  minimal `batchUpdate`. Never delete the deck and rebuild it from the outline
  — that destroys the visual work.
- When Manfred changes the outline, apply only the matching slide edits. When he
  changes the deck, pull just those changes back into the outline.
- On the deck-to-outline direction, write the markdown immediately and show the
  diff inline rather than waiting for approval, since git is the safety net.
  Commit the markdown at checkpoints, not once per sync.
- A full rebuild is only for the first build of a deck from an outline, or when
  Manfred explicitly asks to start over.
- Design does not round-trip through markdown. Keep the outline on content,
  structure, and speaker notes, and describe visuals in a `## Visual` section
  rather than mirroring the styling. For the deck-to-outline direction, see the
  export-and-selectively-apply loop in `slides-prep`, which still applies when
  reconciling deck edits back into the outline.

When the deck was built directly in Slides and no outline was ever authored, the
outline is redundant. Drop it rather than leave a stale stub that lies about the
deck.

## Structure

- Open with a title slide: talk title, Manfred's name, role, and the event or
  date when relevant.
- Add a short roadmap or agenda only when the talk is long enough to need one;
  skip it for short talks.
- Group slides into clear sections with section-divider slides so the audience
  always knows where they are.
- Close with the key takeaways and a clear call to action or next steps.
- End the deck with a Questions and Answers slide, followed by a Thank you slide
  carrying Manfred's contact details and relevant links so the audience can
  follow up.

## One idea per slide

- Each slide makes a single point. If a slide needs two ideas, split it.
- Write the headline as the takeaway, not a label. "Sigstore signs without
  managing keys" beats "Sigstore".
- Keep text minimal. No paragraphs on slides — short phrases and a few bullets
  at most. The spoken narrative carries the detail.
- Prefer a strong visual, diagram, or single example over a wall of text.

Slides support the talk; they are not a document to be read without the
presenter. The audience should not be able to get the point from the slides
alone — the presenter delivers the substance, and the slides reinforce it.

## Lists and density

- Use itemized lists only when a list is genuinely the right shape for the
  content. Use numbered lists only when the order matters.
- Keep any list well under seven items. Even near that count, consider breaking
  it across several slides instead.
- More slides with tighter focus beat one dense slide that lingers on screen and
  never changes. A slide that stays up for a long time is usually a sign it is
  doing too much.

## Narrative and flow

- A deck is a story, not a document. Establish the problem, build tension, then
  resolve it with the solution and the evidence.
- Make each slide follow naturally from the one before it. The audience should
  feel a through-line, not a list.
- Signpost transitions between sections so the structure is audible, not just
  visible.
- Match depth to the audience and the time slot, the same way `manfred-writing`
  matches content to its readers.

## Code and demos

- Show only the code that matters. Trim imports, boilerplate, and anything not
  central to the point, and highlight the key lines.
- Keep snippets large enough to read from the back of the room.
- Prefer a live or recorded demo over static terminal screenshots when it adds
  real value, and always have a fallback in case the demo fails.

## Speaker notes

- Manfred rarely uses speaker notes and talks off the cuff. When notes exist,
  they are short glanceable reminders only — keywords, a cue, a number to hit.
- Never write full sentences or scripted prose in speaker notes. They are
  prompts, not a transcript.
- Put any factual claim that needs a citation on the slide itself or on a
  references slide rather than burying the source in notes.

## Visuals

- Use diagrams to explain architecture and flows rather than describing them in
  bullets.
- Keep one consistent visual style across the deck.
- Ensure every visual is legible at presentation size and has enough contrast.
- Use images and memes sparingly and only when they add real value to the point being made.
- In a markdown outline, capture each diagram, chart, or image in a `## Visual`
  section (see `slides-prep`) describing what it shows, since visuals do not
  survive a text export.
