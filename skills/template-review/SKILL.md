---
name: template-review
description: Review notification templates for copy quality, correctness, channel fit, and deliverability. Produces a severity-grouped report and then asks before applying fixes.
---

# Template review

This skill guides an agent through a thorough review of a notification template — email, push, SMS, in-app, or chat — and returns a structured report grouped by severity. The agent does not edit the template until the user confirms which findings to apply.

This skill is self-contained in a single `SKILL.md` on purpose so it can be pasted into Knock as one text blob. The `House style` section below is the primary place to customize this skill for your team.

## 1. When to use

Use this skill whenever a user asks to:

- Review, proofread, edit, critique, or QA a notification template.
- Check a Knock workflow step's message template (email, SMS, push, chat, in-app feed, in-app guide).
- Validate subject lines, preheaders, CTAs, or body copy before a send.
- Sanity-check variables, conditionals, and links inside a template.

If the user only wants generic copywriting advice without a specific template in hand, prefer the `notification-best-practices` skill instead.

## 2. Review workflow

Follow these steps in order. Do not skip the confirmation step at the end.

1. Identify the channel(s) and the template type (transactional, lifecycle, promotional, or system).
2. Load the `House style` block below and apply its overrides wherever they conflict with the defaults in this file.
3. Run the `Universal copy-editing checklist` against every channel the template targets.
4. Run the `Channel checks` section for each channel.
5. If the template is an email, also run the `Email deep-dive`.
6. Run the `Variables, conditionals, and logic` and `Link verification` sections. Flag anything that cannot be validated without sample data or a live network check, and ask for what you need.
7. Produce the report in the exact format defined in `Output format`.
8. **Do not apply any fixes yet.** End the turn by asking the user which items they want applied: all blockers, blockers plus recommended, everything, or a custom subset.
9. Only after the user confirms, apply the chosen fixes. Preserve template syntax (Liquid, Handlebars, MJML, Markdown) exactly as authored.

## 3. House style (customize this section)

Edit this section to match your team's style guide. Write in plain English — the agent will respect whatever you put here. Delete anything that doesn't apply, add anything that does. If this section looks untouched from the defaults below, note that in the report summary so the user knows the review used defaults.

### Voice and tone

- Friendly-professional. Warm but not casual.
- No exclamation marks in subject lines.
- Avoid hype and marketing superlatives ("amazing", "revolutionary", "game-changing").

### Grammar and punctuation

- Use the Oxford comma.
- Use contractions ("you're", "we'll") — they sound more human.
- Prefer em-dashes over parentheses for asides.
- Use curly quotes, not straight.
- No double spaces after periods.

### Casing

- Sentence case for subject lines, buttons, and headings ("Your order has shipped", not "Your Order Has Shipped").
- Preserve product term casing exactly — see the glossary below.

### Emoji

- Use sparingly. Never more than one per message.
- None in SMS.
- Never in subject lines.

### Links and CTAs

- One primary CTA per message.
- Anchor text must describe the destination. Never "click here", "this link", or bare URLs.
- All links must use `https://`.
- Preferred button verbs: View, Open, Confirm, Reply, Track.

### Formats

- Dates: `Mon, Jan 23, 2026`
- Times: `2:30 PM EST` (always include timezone for transactional)
- Currency: `$1,234.56 USD`
- Default locale: `en-US`

### Glossary (canonical casing)

| Correct       | Also flag                         |
|---------------|-----------------------------------|
| Knock         | knock, KNOCK                      |
| in-app feed   | In-App Feed, inapp feed, in app feed |
| workflow      | Workflow, work flow               |
| guide         | Guide (when used generically)     |

### Forbidden phrases

Flag any occurrence of these:

- click here
- please find attached
- as per
- kindly
- hit us up

## 4. Universal copy-editing checklist

Apply to every channel:

- **Typos and misspellings**, including doubled words ("the the") and homophones (their/there/they're, your/you're, its/it's, affect/effect, then/than).
- **Grammar**: subject-verb agreement, pronoun agreement, consistent tense, no dangling or misplaced modifiers, parallel structure in lists.
- **Punctuation**: comma usage matches the Oxford comma rule in house style, consistent quote style (straight vs. curly), proper ellipses, correct em-dash / en-dash usage, no double spaces.
- **Capitalization**: sentence case vs. title case per house style; product names, features, and proper nouns match the casing in the house style glossary.
- **Voice**: prefer active voice. Flag passive constructions unless they're intentional (e.g., when the actor is unknown or irrelevant).
- **Specificity and context**: every notification should answer "what happened, why does it matter to me, and what can I do next?" Vague subjects like "Update available" are always a finding.
- **Consistent terminology**: names of features and objects match the product UI and each other throughout the template.
- **Reading level**: plain language unless the audience is technical. Avoid jargon, acronyms without expansion, and marketing fluff.
- **Forbidden phrases**: flag any match against the forbidden phrases list in house style.
- **Internationalization risks**: concatenated strings that assume English word order, hard-coded dates or currencies, missing pluralization branches, gendered assumptions.
- **Inclusive language**: avoid gendered defaults ("he/she"), ableist metaphors, and culturally narrow idioms.

## 5. Channel checks

For each channel the template targets, verify:

### Email
- Subject line and preheader present, distinct, and complementary.
- Content is scannable in the first 2–3 seconds.
- Single primary CTA unless the template type explicitly warrants more.

### Push
- Under ~120 characters total (title + body) to survive lock-screen truncation.
- Primary payload survives the first ~40 characters (title).
- Deep link points to the most relevant in-app destination, not just the home screen.
- Tone is terse and specific; no marketing fluff.

### SMS
- Under 160 characters when possible; if longer, segments cleanly.
- No links unless shortened and branded; no HTML; no emoji unless house style explicitly allows it in SMS.
- Includes sender identity (users can't see a "from" name).
- Includes opt-out instructions for non-transactional messages ("Reply STOP to unsubscribe").

### In-app
- Fits the target surface (feed item, toast, banner, modal) without truncation.
- Actionable from within the product; CTA opens the relevant view, doesn't just dismiss.
- Tone matches the product UI, not an email voice.

### Chat (Slack / Teams / etc.)
- Renders in the platform's native formatting (mrkdwn for Slack, adaptive cards for Teams).
- Primary info survives collapsed/preview view.
- Threaded vs. top-level posting is appropriate for the event.
- Mentions (@user, @channel) are used deliberately, not by default.

## 6. Email deep-dive

Email has the most surface area, so apply this additional checklist whenever the template is email.

### Headers
- **From name** and **from address** set, recognizable, and consistent with prior sends.
- **Reply-to** is a monitored address — never `noreply@` for any email where the user might reasonably respond (billing issues, support, onboarding).
- **Subject line** ≤ ~50 characters to avoid truncation on mobile; front-loads the key info.
- **Preheader** present, distinct from the subject, and not accidentally leaking layout text ("View in browser", "Unsubscribe", or raw Liquid).

### Structure
- One clear primary CTA above the fold.
- Scannable hierarchy: headline, supporting context, CTA, secondary info.
- Works when the recipient reads only the first screen.

### Links
- Every `href` is present, non-empty, and uses `https://`.
- No `#`, `example.com`, `localhost`, or unresolved `{{ }}` placeholders shipped to production.
- Anchor text is descriptive — no "click here", "this link", or bare URLs.
- Tracked/redirect links resolve to the intended destination.
- Unsubscribe link present for marketing and lifecycle mail.

### Images
- Every `<img>` has `alt` text that conveys meaning (or `alt=""` if purely decorative).
- Dimensions set via `width` / `height` so layout doesn't jump.
- Template is readable with images off — no image-only CTAs, no critical info locked inside an image.

### Dark mode
- No hard-coded `#000` or `#fff` in places that invert poorly.
- Logos and icons have transparent backgrounds or dark-mode variants.
- Links remain legible against inverted backgrounds.

### Accessibility
- Logical heading order (`h1` → `h2` → `h3`, no skipping).
- Text contrast meets WCAG AA (4.5:1 for body, 3:1 for large text).
- Descriptive link text (screen readers announce links out of context).
- `lang` attribute set on the root element; matches the locale being sent.
- Table-based layouts include `role="presentation"` where appropriate.

### Deliverability hygiene
- No ALL CAPS subject lines, no runs of `!!!` or `$$$`.
- Reasonable text-to-image ratio; not a single image wrapped in one link.
- Visible unsubscribe link and a physical mailing address for marketing/commercial mail (CAN-SPAM).
- `List-Unsubscribe` header expected for bulk sends (verify with the sending infra, not in the template itself — flag as a reminder).

### Localization
- Every user-facing string is either a variable or a localization key, not hard-coded English.
- Dates, times, numbers, and currency use locale-aware formatters.
- Layout tolerates ~30% text expansion (German, French) without breaking.
- RTL-safe if any target locale requires it (Arabic, Hebrew).

### HTML / MJML hygiene
- Balanced tags, valid nesting, no stray closing tags.
- Template syntax (`{{ }}`, `{% %}`) is correctly closed; no raw syntax visible in the rendered output.
- MJML components used idiomatically; no raw `<table>` hacks when an `<mj-section>` would do.
- No inline JavaScript (most clients strip it anyway, and it's a spam signal).

## 7. Variables, conditionals, and logic

- Every `{{ variable }}` has an expected type (string, number, date, object) and a documented fallback for when it's null or missing.
- Conditionals (`{% if %}`, `{% case %}`) cover the realistic branches: empty, singular, plural, zero, error state.
- No PII is exposed in subject lines or push/preview surfaces where it could appear on a lock screen.
- Loops (`{% for %}`) handle empty collections gracefully.
- If validation requires sample data you don't have, list the specific variables and ask for representative values before finalizing the report.

## 8. Link verification

- List every URL found in the template, including ones built from variables.
- Classify each as:
  - `ok (static check only)` — well-formed, uses `https://`, descriptive anchor text.
  - `placeholder` — obvious stand-in (`example.com`, `#`, `localhost`, `TODO`).
  - `template variable` — built from `{{ }}`; correctness depends on runtime data.
  - `suspicious` — HTTP instead of HTTPS, shortener of unknown provenance, or mismatched anchor text vs. destination.
- Note explicitly that a static review cannot prove a link is reachable. Offer to run a live check if the environment permits.

## 9. Output format (required)

Return the review in exactly this shape. Keep the headings verbatim so downstream tooling can parse them.

```markdown
# Template review: <template name or channel>

## Summary
<2–3 sentence overall read. Note if house style defaults were used.>

## Blockers
- [ ] <issue> — <where (line, selector, or section)> — <suggested fix>

## Recommended
- [ ] <issue> — <where> — <suggested fix>

## Nits
- [ ] <issue> — <where> — <suggested fix>

## Links found
- <url> — <ok | placeholder | template variable | suspicious>

## Variables found
- <name> — <type guess> — <has fallback? yes/no>

## Next step
Which items would you like me to apply?
- all blockers
- blockers + recommended
- everything
- pick specific items (reply with the item numbers or a short list)
```

If a section has no findings, keep the heading and write `None.` underneath it. Never silently omit a section.

### Severity definitions

- **Blocker** — the send is broken or harmful if you ship it as-is. Examples: broken link, unresolved template variable visible in the rendered output, missing unsubscribe on marketing mail, legal risk, factual error, wrong recipient data in subject, CTA leads to the wrong destination.
- **Recommended** — hurts clarity, deliverability, accessibility, or brand consistency, but the send still functions. Examples: vague subject line, missing alt text, passive voice where active would be stronger, inconsistent product term casing.
- **Nit** — stylistic or preference-level. Safe to ignore. Examples: em-dash vs. en-dash choice, slight rewording for rhythm, optional emoji.

## 10. After the report

Stop. Do not edit the template until the user replies with what they want applied.

When you do apply fixes:

- Preserve template syntax (`{{ }}`, `{% %}`, MJML tags, Markdown) exactly as authored.
- Preserve the original file's indentation, quote style, and line endings.
- Make the minimum change that resolves the finding — don't rewrite untouched copy.
- If a fix would alter meaning or tone in a debatable way, surface the proposed change in the chat before writing it.
- After applying, briefly summarize what changed and which findings are now resolved.

## 11. Quick reference

Top findings to look for on any template:

1. Unresolved `{{ variable }}` or `{% if %}` syntax visible in rendered output.
2. Broken, placeholder, or non-HTTPS links.
3. Subject line that's vague, over ~50 characters, or uses ALL CAPS.
4. Preheader missing, duplicated from subject, or leaking layout text.
5. More than one primary CTA competing for attention.
6. Images without alt text, or critical info locked in an image.
7. Forbidden phrases from house style, especially "click here".
8. Inconsistent casing of product terms.
9. Missing unsubscribe or physical address on marketing mail.
10. Hard-coded dates, currencies, or English strings that block localization.
