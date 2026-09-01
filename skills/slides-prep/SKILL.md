---
name: slides-prep
description: Prepare a conference talk end to end, from proposal through a slide-ready markdown outline to a finalized deck. Covers the CFP/abstract, an idea dump, a per-slide outline in a fixed markdown format, a speaker-notes trim pass, generating a PowerPoint — today via Claude Cowork — that gets imported into Google Slides, and reviewing the deck through to finished. Enter at any point and move in either direction — draft from scratch, review an existing deck, generate a single new slide to paste in, or reconstruct the markdown outline from an existing Google Slides or PowerPoint deck. Use when planning a talk, writing a proposal, turning talk ideas into an outline, adding or reworking slides, or reviewing the resulting deck. General and tool-agnostic; the manfred-slides and manfred-writing skills are optional helpers that layer in when available.
---

# slides-prep — from talk proposal to a finished deck

This skill covers the whole path from a talk proposal to a finalized deck:
writing the proposal, capturing raw ideas, shaping them into a per-slide outline
in markdown, generating a deck from that outline, and reviewing every step
through to the finished deck. It stays in charge through finalization — the
review of the generated deck is part of this skill, not a handoff to another.

The phases are not a one-way pipeline. **Enter at whatever point matches what you
already have** — a rough idea, a finished outline, or an existing deck you only
want reviewed — and move in either direction between the markdown outline and
the deck. Each operation stands on its own, so pick the one you need
rather than always starting at the top.

It is a general skill. It does not assume a particular speaker, employer, or
event. Keep any person- or company-specific content in the event files, not in
this skill.

## Scope — the operations this skill covers

Any of these, in any order and as standalone entry points:

- Talk proposals and CFP submissions: title, abstract, speaker bio, takeaways.
- An idea dump that captures everything before it is structured.
- A per-slide outline in the markdown format from the outline format section.
- A speaker-notes trim pass.
- Generating a deck from the outline — the whole deck, or a single new slide to
  paste into a deck that already exists.
- Reconstructing the markdown outline from an existing deck, in Google Slides or
  as a `.pptx`.
- Reviewing an existing deck and finalizing it against the conventions here.

Moving between the markdown and the deck is **deliberate, not automatic**. There
is no reliable one-click sync in either direction: generating a deck from the
outline and reconstructing the outline from a deck are both real operations, but
each is a discrete step you run when you need it. Treat whichever artifact you
are actively working in as the source of truth for that session, and reconcile
the other on purpose rather than assuming they stay in lockstep.

Once a deck exists and is what the talk is presented from, the deck is the
authoritative artifact. The outline is a pre-deck authoring scaffold: keep it
when it was used to build the deck or individual slides, and drop it when the
deck was built directly in the deck tool with no outline behind it, rather than
leaving a stale stub. Syncing an outline to a live deck is one-way —
reconstruct it from the deck (see below); markdown edits cannot be pushed back
into Google Slides while preserving the design.

## Composing with other skills

This skill is designed to compose with, but never depend on, a personal skill
set. When those skills are available, use them; when they are not, this skill
stands on its own.

- **manfred-writing**, when present: the voice, audience, and markdown house
  style — including the 80-character hard wrap — apply to all prose written
  here, in proposals and in slide content alike. Invoke it for any writing.
- **manfred-slides**, when present: an optional, Manfred-specific helper — his
  personal deck structure, one-idea-per-slide, and narrative preferences. It is
  a guideline that layers on top of this skill's process, not a skill to hand
  off to. This skill still drives the work through finalization; use
  manfred-slides as extra guidance when the deck is Manfred's.

If neither is available, follow the slide conventions inlined in this skill and
write in clear, plain prose.

## Workspace layout

Work lives in a slides workspace repository, one directory per event. The
directory name is a slug of `event-location-year-month`, lowercase, hyphenated,
with the month as two digits — for example `devopscon-sandiego-2026-06` or
`kubecon-na-saltlakecity-2026-11`. Including the month keeps directories
sortable and avoids collisions when there are several events in a year.

Each event directory holds:

| File | Purpose |
|---|---|
| `index.md` | The brief: event and CFP details, speaker bio, abstract, and the raw idea dump. The starting point and the source of truth for intent. |
| `outline.md` | The per-slide outline in the outline format. The working document for the whole prep phase. |
| `speaker-notes-trim.md` | Optional scratch file for a one-off speaker-notes trim pass. Temporary — delete it once the trimmed notes are back in the outline or the deck; not a deliverable worth keeping. |
| `STATUS.md` | Where the talk stands — proposed, accepted, outlined, generated, delivered — plus links once it exists (deck, recording, event log). |
| templates | Optional. Reusable master `.pptx` templates (a dark and a light master, say) when the generator needs one. If present, the only decks kept in git. |

Generated and working `.pptx` files are throwaway — they exist only to carry the
outline into slide software as described in the generation step, so keep them
out of version control. The markdown outline is the source of truth.

Templates are **optional**. Some generators need a master `.pptx` to carry the
visual style; others do not — a Claude Cowork setup, for example, can hold the
brand style as a skill of its own, so no template file is required. When
templates are used, they are the only decks worth committing: keep one canonical
copy and reference it rather than duplicating per event. When the generator
already knows the brand style, skip templates entirely.

## Workflow

The following phases are the natural order for a talk built from scratch, but
they are also independent entry points. Start wherever your material already is,
run only the phases you need, and loop back freely — especially between the
outline and content phases. The two cross-cutting operations — generating a
single slide and reconstructing the outline from an existing deck — live in
"Moving between the markdown and the deck".

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

4. **Outline.** Turn the dump into `outline.md` using the outline format — one
   `# Slide N` heading per slide, a title that states the takeaway, a short
   `## On slide` list, and glanceable `## Speaker notes`. Build the narrative
   arc: set up the problem, build tension, resolve it, and end with a call to
   action, a Q&A slide, and a thank-you/contact slide.

5. **Content iteration.** Refine `outline.md` until it is good enough to
   generate from. Keep one idea per slide, keep on-slide text minimal, split
   dense slides, and make each slide follow from the one before it. This is
   where most of the time goes.

6. **Speaker-notes trim.** Trim each slide's notes down to what is not already
   on the slide — delivery cues, pacing, extra facts, callbacks — so notes stay
   prompts, not a script. Apply the trim directly in the outline (and later in
   the deck). A `speaker-notes-trim.md` scratch file is fine if you want a place
   to work, but treat it as temporary and delete it once the notes are updated.

7. **Generate.** Generate a `.pptx` from the outline, then import it into Google
   Slides. See "Moving between the markdown and the deck" for how. Update
   `STATUS.md` to `generated`.

8. **Review and finalize.** Review the deck and finish it in the deck tool:
   visual design, layout, theming, and per-slide polish, checked against the
   one-idea-per-slide and narrative conventions here — and manfred-slides when
   the deck is Manfred's. This is a valid entry point on its own — arrive with
   an existing deck and do only this. Review happens in the deck; if you want
   the outline to reflect changes made there, reconstruct it as described in
   "Moving between the markdown and the deck". Update `STATUS.md` to `delivered`
   once the talk is given.

## Outline format

`outline.md` uses a fixed, simple structure so it reads well as a document and
generates cleanly into slides.

- A short header at the top. Do not repeat the event, speaker, dates, or talk
  length here — those live in `index.md`. Keep only what is specific to the
  deck: a pointer to `index.md`, a rough slide count, and any deck-wide
  conventions such as theme usage, color scheme, or reference decks.
- One `# Slide N - Title` heading per slide. Write the title as the **takeaway**,
  not a label: "Sigstore signs without managing keys", not "Sigstore". This
  heading is the outline's navigation label and may differ from the literal
  title shown on the slide.
- An optional theme or layout hint as an HTML comment directly under the
  heading, for example `<!-- theme: dark -->`. Comments carry hints for the deck
  build without appearing as slide content.
- `## On slide` — what the audience actually sees. Keep it short: a few bullets
  or a single strong line. No paragraphs. When the slide shows a title or
  header, repeat that literal text as the first line here, so the outline
  mirrors the rendered slide and a re-export diffs cleanly against it; slides
  with no title simply omit it.
- `## Visual` — optional. Describe any diagram, chart, screenshot, or image on
  the slide in plain language: what it depicts and the point it makes, like
  alt-text. Use it whenever a slide's meaning is carried by a visual, since
  visuals do not survive a text export. For an image-only slide, `## On slide`
  may hold just the title (or nothing) and `## Visual` carries the slide.
- `## Speaker notes` — glanceable reminders only: delivery cues, a number to
  hit, a story to tell, a callback. Never a full script.
- Use a `---` divider between major sections to keep the arc readable in the
  markdown.
- Dates anywhere in the event files (`index.md`, `STATUS.md`) use ISO 8601
  (`YYYY-MM-DD`); use `start/end` for a range, for example
  `2026-06-01/2026-06-05`.

Skeleton:

```markdown
# Talk outline — <takeaway-style talk title>

See `index.md` for event details, speaker bio, and the abstract.

Conventions: <deck-wide notes — theme usage, ~<n> slides, reference decks>

---

# Slide 1 - <takeaway title>
<!-- theme: dark -->

## On slide

- <literal slide title, if the slide shows one>
- <short line or two>

## Visual

- <what a diagram, chart, or image shows — omit the section when there is none>

## Speaker notes

- <delivery cue, not a script>
```

## Moving between the markdown and the deck

The markdown outline and the deck are two representations of the same talk.
Moving between them is deliberate — each direction is a discrete operation you
run when you need it, not an automatic sync.

### Generate the whole deck

- **Today: Claude Cowork.** Generate the `.pptx` from `outline.md` in Claude
  Cowork, using its slide and brand-style skills — and a reusable template deck
  only if that setup needs one. Claude Code in a terminal cannot produce or
  drive the deck directly, so this step moves to Cowork. Then import the
  generated `.pptx` into Google Slides.
- **Future: other generators.** This should become a choice, not a single path —
  for example a markdown-to-`pptx` CLI, or a reveal.js render when the markdown
  itself is the final product. Add them here as they are proven out.

### Generate or update a single slide

When the deck already exists and you only want to add or redo one slide, do not
regenerate the whole thing. Add or edit that slide in `outline.md`, generate
just that one slide — the same tool, scoped to the single `# Slide N` block —
and paste it into the deck at the right position. This keeps the manual work
already done in the deck intact, and it is the normal way to grow a deck
incrementally.

### Reconstruct the outline from an existing deck

You can also go the other way: build `outline.md` from a deck that already
exists in Google Slides or as a `.pptx`. Extract each slide's visible content
into an `## On slide` block and its notes into `## Speaker notes`, following the
outline format. Use this to

- start from a deck you already have and bring it under the markdown workflow,
- recover the outline after a stretch of manual editing in the deck, or
- get a base outline you can then extend with new slides.

Reconstruction is manual or tool-assisted and will not be perfectly lossless —
treat it as a draft that needs a cleanup pass, then reconcile by eye. A Google
Slides text export is not only lossy but **unstable between runs** — the same
deck exported twice can chunk differently. What breaks:

- Slide numbers are internal object ids, not deck order — never trust them.
- Body order is mostly reliable, but the **tail (closing slides) and section
  dividers can scramble, merge into a neighbor, split out on their own, or
  relocate** — a note-only or divider slide is especially prone to this.
- Diagrams flatten into unordered label soup that must be re-summarized by hand.
- On-slide text is not delimited from speaker notes; splitting them is a
  judgment call, and a note can surface as on-slide text (or vice versa) on one
  run and differently on the next.

Because of this, always verify a fresh export against the deck's known structure
and slide count rather than trusting any single export. Renumber into
presentation order and rebuild the diagram slides by eye.

To pull the text out of Google Slides, use the plain-text export endpoint
`https://docs.google.com/presentation/d/<id>/export/txt`. It needs the deck
link-shareable (anyone with the link can view) and returns a cross-host redirect
you follow to fetch the content — the raw material for both a cold
reconstruction and a sync diff.

### Sync an existing outline after deck edits

When both an outline and a deck exist and the deck has moved ahead — manual edits
in the deck tool — do **not** regenerate the outline from scratch. That throws
away hand-curated content the export cannot reproduce: `## Visual` summaries, the
correct on-slide/notes split, and the renumbered presentation order. Treat the
outline as the base of truth and the export as a *proposal*, then:

1. Export the current deck and diff it against the outline.
2. Classify each difference: a real edit made in the deck, an export artifact
   (mislabeling, chunking shift, dropped/merged/moved slide), or unsure.
3. Apply only the confirmed real edits. Never delete or overwrite outline
   content just because an export omitted or moved it — that is almost always
   export noise, not a deletion.
4. On anything unsure, ask rather than guess; the deck owner knows what they
   changed.

This diff-and-selectively-apply loop is the safe way to keep an outline current
with a deck that is being actively edited, and it protects curated content from
the export's instability. A `## Visual` block or a hand-rebuilt diagram slide is
a signal that the content is curated: refresh it only against a real deck change,
never from raw export text.

## STATUS.md

Keep a short `STATUS.md` per event so the state is obvious at a glance. Track the
current stage and, once the talk exists and is delivered, the links. Do not
repeat the talk title, dates, location, session type, or other event facts here
— those live in `index.md`. State once that details live in `index.md` and link
to it rather than duplicating, so the two files cannot drift apart.

- **Stage:** one of proposed, accepted, outlined, generated, delivered.
- **Links:** slide deck, recording/video, and the event page. Fill these in as
  they become available; leave a clear placeholder until then.
- **Open items:** anything still undecided or outstanding.

## Finalizing

This skill stays in charge through to a finished deck — there is no handoff.
After generation and import, keep reviewing and polishing in the deck tool
against these conventions, layering in manfred-slides as optional guidance
when the deck is Manfred's. Update `STATUS.md` as the stage advances —
`generated` after import, `delivered` after the talk.
