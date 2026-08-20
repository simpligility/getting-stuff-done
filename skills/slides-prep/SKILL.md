---
name: slides-prep
description: Prepare a conference talk end to end, from proposal through a slide-ready markdown outline to a finalized deck. Covers the CFP/abstract, an idea dump, a per-slide outline in a fixed markdown format, a speaker-notes trim pass, generating a PowerPoint (today via Claude Cowork) that gets imported into Google Slides, and reviewing the deck through to finished. Use when planning a talk, writing a proposal, turning talk ideas into an outline, or reviewing the resulting deck. General and tool-agnostic; the manfred-slides and manfred-writing skills are optional helpers that layer in when available.
---

# slides-prep — from talk proposal to a slide-ready outline

This skill covers the whole path from a talk proposal to a finalized deck:
writing the proposal, capturing raw ideas, shaping them into a per-slide outline
in markdown, generating a first deck from that outline, and reviewing every step
through to the finished deck. It stays in charge through finalization — the
review of the generated deck is part of this skill, not a handoff to another.

It is a general skill. It does not assume a particular speaker, employer, or
event. Keep any person- or company-specific content in the event files, not in
this skill.

## Scope — where this skill starts and stops

In scope:

- Talk proposals and CFP submissions: title, abstract, speaker bio, takeaways.
- An idea dump that captures everything before it is structured.
- A per-slide outline in the markdown format below.
- A speaker-notes trim pass.
- Generating a first deck from the outline and importing it into slide software.
- Reviewing the generated deck and finalizing it against the conventions here.

The one thing to understand about the boundary is mechanical, not a scope
limit: **the round trip does not work yet.** Once the markdown outline becomes a
deck and that deck is imported into Google Slides, later edits happen in the
deck, and there is no reliable way to sync them back into the markdown. So get
the markdown as good as it can be first, generate once, and treat the generated
deck as the source of truth from that moment on. The review continues in the
deck itself — still driven by this skill — through to a finished deck.

## Composing with other skills

This skill is designed to compose with, but never depend on, a personal skill
set. When those skills are available, use them; when they are not, this skill
stands on its own.

- **manfred-writing** (if present): the voice, audience, and markdown house
  style — including the 80-character hard wrap — apply to all prose written
  here, in proposals and in slide content alike. Invoke it for any writing.
- **manfred-slides** (if present): an optional, Manfred-specific helper — his
  personal deck structure, one-idea-per-slide, and narrative preferences. It is
  a guideline that layers on top of this skill's process, not a skill to hand
  off to. This skill still drives the work through finalization; use
  manfred-slides as extra guidance when the deck is Manfred's.

If neither is available, follow the slide conventions inlined below and write in
clear, plain prose.

## Workspace layout

Work lives in a slides workspace repository, one directory per event. The
directory name is a slug of `event-location-year`, lowercase, hyphenated — for
example `devopscon-sandiego-2026` or `kubecon-na-saltlakecity-2026`.

Each event directory holds:

| File | Purpose |
|---|---|
| `index.md` | The brief: event and CFP details, speaker bio, abstract, and the raw idea dump. The starting point and the source of truth for intent. |
| `outline.md` | The per-slide outline in the format below. The working document for the whole prep phase. |
| `speaker-notes-trim.md` | Optional. A trim pass that moves anything already visible on a slide out of its speaker notes. Create it only when notes need cleanup. |
| `STATUS.md` | Where the talk stands — proposed, accepted, outlined, generated, delivered — plus links once it exists (deck, recording, event log). |
| templates | Reusable master `.pptx` templates (for example a dark and a light master). The only decks kept in git. |

Generated and working `.pptx` files are throwaway — they exist only to carry the
outline into slide software (see the generation step), so keep them out of
version control. The markdown outline is the source of truth; the reusable
templates are the only decks worth committing. Keep one canonical copy of the
templates and reference it rather than duplicating per event.

## Workflow

The phases are ordered but iterative. Move forward, but expect to loop back —
especially between the outline and content phases.

1. **Proposal / CFP.** Draft the title, abstract, bio, and audience takeaways.
   Capture the submitted text verbatim in `index.md` once submitted, so later
   work stays honest to what the event and attendees were promised.

2. **Event setup.** Once accepted, record the concrete constraints in `index.md`
   and `STATUS.md`: dates, location, talk length, session type, audience level,
   and any format rules from the organizers. Length and audience drive slide
   count and depth more than anything else.

3. **Idea dump.** In `index.md`, dump every idea, section, example, and
   supporting fact with no structure. Volume first, judgment later. This is
   thinking on paper, not an outline.

4. **Outline.** Turn the dump into `outline.md` using the format below — one
   `# Slide N` heading per slide, a title that states the takeaway, a short
   `## On slide` list, and glanceable `## Speaker notes`. Build the narrative
   arc: set up the problem, build tension, resolve it, and end with a call to
   action, a Q&A slide, and a thank-you/contact slide.

5. **Content iteration.** Refine `outline.md` until it is good enough to
   generate from. Keep one idea per slide, keep on-slide text minimal, split
   dense slides, and make each slide follow from the one before it. This is
   where most of the time goes.

6. **Speaker-notes trim.** Optionally produce `speaker-notes-trim.md`: for each
   slide, strip anything from the notes that is already on the slide, leaving
   only delivery cues, pacing, extra facts, and callbacks. Notes are prompts,
   not a script.

7. **Generate.** Generate a first `.pptx` from the outline, then import it into
   Google Slides. See the next section for how. Update `STATUS.md` to
   `generated`.

8. **Review and finalize.** Review the generated deck and finish it in the deck
   tool: visual design, layout, theming, and per-slide polish, checked against
   the one-idea-per-slide and narrative conventions here (and manfred-slides
   when the deck is Manfred's). Because the round trip does not work yet, this
   review happens in the deck, not the markdown. Update `STATUS.md` to
   `delivered` once the talk is given.

## Outline format

`outline.md` uses a fixed, simple structure so it reads well as a document and
generates cleanly into slides.

- A short header at the top: speaker, event, target length, rough slide count,
  and any deck-wide conventions (for example a theme or color scheme).
- One `# Slide N - Title` heading per slide. Write the title as the **takeaway**,
  not a label: "Sigstore signs without managing keys", not "Sigstore".
- An optional theme or layout hint as an HTML comment directly under the
  heading, for example `<!-- theme: dark -->`. Comments carry hints for the deck
  build without appearing as slide content.
- `## On slide` — what the audience actually sees. Keep it short: a few bullets
  or a single strong line. No paragraphs.
- `## Speaker notes` — glanceable reminders only: delivery cues, a number to
  hit, a story to tell, a callback. Never a full script.
- Use a `---` divider between major sections to keep the arc readable in the
  markdown.

Skeleton:

```markdown
# Talk outline — <takeaway-style talk title>

Speaker: <name, role>
Event: <event, location, dates>
Target length: ~<n> min, ~<n> slides

Conventions: <deck-wide notes, e.g. theme usage, reference decks>

---

# Slide 1 - <takeaway title>
<!-- theme: dark -->

## On slide

- <short line or two>

## Speaker notes

- <delivery cue, not a script>
```

## Generating the deck

The markdown outline is the source of truth up to this point. Turning it into an
actual deck is a separate, one-way step.

- **Today: Claude Cowork.** Generate the `.pptx` from `outline.md` in Claude
  Cowork, using its slide skills and the reusable template deck(s). Claude Code
  in a terminal cannot produce or drive the deck directly, so this step moves to
  Cowork. Then import the generated `.pptx` into Google Slides.
- **Future: other generators.** This should become a choice, not a single path —
  for example a markdown-to-`pptx` CLI, or a reveal.js render when the markdown
  itself is the final product. Add them here as they are proven out.
- **Round trip.** A full round trip between the outline and the live deck is the
  goal but is not reliably possible yet. Until it is, generate once from a
  finished outline and then edit only in the deck.

## STATUS.md

Keep a short `STATUS.md` per event so the state is obvious at a glance. Track the
current stage and, once the talk exists and is delivered, the links.

- **Stage:** one of proposed, accepted, outlined, generated, delivered.
- **Event facts:** final title, date, location, session type, length.
- **Links:** slide deck, recording/video, and the event page. Fill these in as
  they become available; leave a clear placeholder until then.

## Finalizing

This skill stays in charge through to a finished deck — there is no handoff.
After generation and import, keep reviewing and polishing in the deck tool
against the conventions above, layering in manfred-slides as optional guidance
when the deck is Manfred's. Update `STATUS.md` as the stage advances —
`generated` after import, `delivered` after the talk.
