# Cover Prompt Publication

Treat the cover production prompt and the article-visible prompt as separate artifacts.

## Options

```json
{
  "opening_hero": {
    "enabled": false,
    "ratio": "4:3",
    "placement": "before_intro",
    "marker": "opening-hero"
  },
  "cover_prompt": {
    "enabled": false,
    "placement": "before_endcap",
    "title": "封面 Prompt",
    "marker": "cover-prompt"
  }
}
```

Keep both options disabled unless the current request or resolved user configuration enables them. Enabling one does not enable the other.

## Production and reader prompts

Preserve the production prompt as an internal artifact with the full composition, crop, source, editing, and output requirements. Derive the reader prompt from the final method actually used.

Remove from the reader prompt:

- local and temporary file paths;
- internal conversation context and working notes;
- tool names, retry history, and intermediate failures;
- claims that a supplied artwork or deterministic Logo composition came from text generation alone;
- private brand facts or unpublished source material.

Retain in the reader prompt:

- intended asset type and aspect ratio;
- subject, composition, visual hierarchy, palette, and rendering language;
- Logo placement and the requirement to use the official `publication.logo` asset without redrawing it or substituting a studio/product mark;
- meaningful negative constraints;
- required public-domain or licensed input artwork when reproduction depends on it.

## Article block

Render only a heading and one directly copyable prompt block. Use `data-lovstudio-block="cover-prompt"` as the unique marker. Place the block after the article conclusion and before the stable brand endcap by default. Do not add a process diary, model commentary, or reuse instructions around it.

## Opening hero

When enabled, create a reading-oriented image rather than reusing the sharing cover without review. Default to `4:3`, place the official publisher Logo from `publication.logo` near the lower center, preserve a single visual focal point, and insert the block before the introduction with `data-lovstudio-block="opening-hero"`. Keep it outside introduction cards, blockquotes, borders, and colored content containers.

## Validation

- Confirm each enabled block appears exactly once.
- Confirm the opening hero is the first article body block and uses the expected CDN asset after reload.
- Confirm the reader prompt matches the final cover method and contains no private path.
- Confirm title, digest, sharing cover, TOC, article body, and endcap remain unchanged unless separately authorized.
