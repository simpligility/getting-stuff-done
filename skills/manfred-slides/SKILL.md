---
name: manfred-slides
description: Manfred Moser's conventions for presentation slide decks — structure, narrative flow, and slide content. Extends the `manfred-writing` skill and is a component of the `manfred` skill family. Activate only when the `manfred` skill is already active (its index directs you here) or when Manfred explicitly invokes it; do not auto-activate on generic slide or presentation work by description match alone.
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

Slides are tool-agnostic in principle, and Manfred's workflow shifts from deck to
deck:

- Sometimes the deck is pure Markdown rendered with reveal.js, and that Markdown
  is the final product.
- Sometimes he ideates the outline and content in Markdown, generates a
  PowerPoint from it, then continues refining in Google Slides.
- He never edits PowerPoint or Keynote files directly — work stays in Markdown
  or Google Slides.

Because of this, focus effort on content, structure, and flow rather than on
tool-specific formatting or theming. When the source is Markdown, follow the
`manfred-writing` markdown house style, including the 80-character hard wrap.

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
