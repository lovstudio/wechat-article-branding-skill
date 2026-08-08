# Changelog

## 0.7.0

- Align the canonical Skill name, kit name, entrypoint, README commands, and embedded-module compatibility labels to `sgc-wechat-article-branding-skill`.
- Treat the published name alignment as the release baseline for channel packaging.

## 0.6.1

- Add the skill-owned `prompts/cover-hero-editorial-painterly.md` production template for artistic-base covers.
- Require `cover-direction` to read the shared template before creating an article-specific cover Prompt instance.
- Keep the reader-visible Prompt option separate from the internal production Prompt while making both traceable inside the branding skill.

## 0.6.0

- Persist the previous cover-creation skill's art direction for branded covers: editorial hero composition, painterly rendering, explicit palette, no generated text, and a center-safe zone for the publisher Logo.
- Add a visual quality gate that rejects generic warm still-life substitutions when the configured cover direction calls for an authored artistic base.

## 0.5.0

- Add a dedicated cover-composition module that restores the established WeChat cover treatment: artistic background, bottom dimming, and the official publisher Logo centered directly on the canvas.
- Derive the square sharing crop from the centered-logo wide composition and keep the composition separate from the optional opening hero.

## 0.4.0

- Separate the publisher/account identity from the studio and product brands through a required `publication` profile.
- Require covers and opening heroes to use the official publisher Logo, with no silent fallback to a studio or product Logo.
- Render only the primary URL for each product in stable endcaps and reject duplicated product links in brand-level link lists.

## 0.3.0

- Add independent `opening_hero` and `cover_prompt` publication options.
- Separate private production prompts from sanitized reader-copyable cover prompts.
- Define default placement, unique markers, and reload acceptance for opening hero and cover prompt blocks.

## 0.2.0

- Add title polishing as a separate content-intelligence step, including publisher voice and interview/reprint handling.
- Keep approved brand endcaps stable and independent from article-specific metaphors or conclusions.
- Extend the quality gate to verify title identity, reprint context, and reusable brand copy.

## 0.1.0

- Add the article-access, content-intelligence, cover-direction, brand-application, and quality-gate modules.
- Add full, content, cover, brand, and audit pipelines.
- Add portable brand-profile configuration and deterministic profile validation.
