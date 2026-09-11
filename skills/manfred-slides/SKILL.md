---
name: manfred-slides
description: Manfred Moser's personal conventions for presentation slide decks — structure, narrative flow, density, and slide content. Layers on top of the general `slides-prep` workflow skill and extends `manfred-writing`, and activates both. A component of the `manfred` skill family. Activate only when the `manfred` skill is already active and its index directs you here, or when Manfred explicitly invokes it; do not auto-activate on generic slide or presentation work by description match alone.
---

# Manfred Moser — presentation slide decks

> **Base-context check.** This skill encodes Manfred's personal conventions and
> assumes the `manfred` base skill established the working context. If `manfred`
> was not activated earlier in this session, pause and ask before applying these
> conventions: "The `manfred` base skill isn't active this session — load it
> first for full context, or proceed anyway?" Once `manfred` is active (or the
> user confirms), continue without asking again.

This skill holds Manfred's personal slide **preferences** — structure,
narrative, density, and slide content. The **mechanics and workflow** — the
markdown outline format, generating and editing the deck, the `gws` tooling,
autofit, backgrounds, and keeping the outline and deck in sync — live in the
general `slides-prep` skill. This skill only layers Manfred's taste on top.

Activate the companions together. When this skill is active, also invoke
`slides-prep` for the workflow and `manfred-writing` for voice and the markdown
house style, including the 80-character hard wrap. The dependency is one-way:
`slides-prep` is a general skill and never depends on this one, so activating it
does not pull `manfred-slides` in — this skill has to bring it along.

Use this skill as extra guidance whenever the deck is Manfred's.

## Working style

- Manfred never edits PowerPoint or Keynote files directly. Work stays in a
  markdown outline or in Google Slides.
- Focus effort on content, structure, and flow rather than on tool-specific
  formatting or theming.

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
- Cap a bullet list at seven items, optionally followed by one related line — a
  conclusion, takeaway, or short quote that ties the list together. Past seven,
  split across slides. Even near seven, consider whether a tighter split reads
  better.
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
- Use images and memes sparingly and only when they add real value to the point
  being made.
- In a markdown outline, capture each diagram, chart, or image in a `## Visual`
  section (see `slides-prep`) describing what it shows, since visuals do not
  survive a text export.
