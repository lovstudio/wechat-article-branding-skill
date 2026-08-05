# Changelog

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
