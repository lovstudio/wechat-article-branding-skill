# Brand Profile

The profile contains approved public facts and presentation rules. It is data, not an implementation mode.

## Minimal schema

```json
{
  "publication": {
    "name": "PUBLISHER_NAME",
    "logo": "PORTABLE_PUBLISHER_LOGO_PATH",
    "logo_policy": "publisher_only"
  },
  "brand": {
    "name": "BRAND_NAME",
    "site": "https://example.com",
    "language": "zh-CN",
    "tone": ["professional", "restrained"],
    "public_facts": ["APPROVED_PUBLIC_FACT"],
    "forbidden_context": ["INTERNAL_CONTEXT_PATTERN"]
  },
  "visual": {
    "primary_color": "#00B38A",
    "cover_style": "editorial",
    "cover_ratios": ["2.35:1", "1:1"]
  },
  "products": [
    {
      "name": "PRODUCT_NAME",
      "promise": "USER_VISIBLE_RESULT",
      "url": "https://example.com/product"
    }
  ],
  "blocks": {
    "endcap": {
      "enabled": true,
      "mode": "stable",
      "product_link_policy": "primary_only",
      "title": "APPROVED_ENDCAP_TITLE",
      "paragraphs": ["APPROVED_ENDCAP_PARAGRAPH"],
      "links": [
        {"label": "BRAND_NAME", "url": "https://example.com"}
      ]
    },
    "opening_hero": {
      "enabled": false,
      "ratio": "4:3",
      "logo_position": "lower_center"
    },
    "cover_prompt": {
      "enabled": false,
      "title": "封面 Prompt",
      "placement": "before_endcap"
    },
    "product_intro": true,
    "copyable_assets": "optional"
  }
}
```

## Rules

- `publication` is the visible publisher/account identity. Covers and opening heroes must use `publication.logo`, never an organization, studio, or product logo inferred from `brand` or `products`.
- `publication.logo_policy` must be `publisher_only`. If its official asset is missing, ask one focused question instead of silently falling back to another logo.
- Use the supplied official publisher asset directly or create deterministic color variants from it. Do not redraw the mark with a generative model.
- Treat only `public_facts`, product promises, names, URLs, and approved design fields as publishable.
- Treat `forbidden_context` as a final-output exclusion list, never as copy.
- Keep product promises outcome-led; do not invent metrics, customers, awards, integrations, or capabilities.
- When `blocks.endcap` is an object, treat its title, paragraphs, and links as approved fixed copy. `mode` must be `stable`; article-specific adaptation is limited to placement and visual hierarchy.
- `products[].url` is the one primary public link for that product. With `product_link_policy: primary_only`, render at most that one link; do not append repositories, download pages, documentation, or other secondary links unless the current request explicitly asks for them.
- `blocks.endcap.links` contains non-product links such as the studio home page. Product URLs are resolved from `products[].url` and must not be duplicated in this list.
- Treat `blocks.opening_hero` and `blocks.cover_prompt` as independent opt-in publication components. Do not infer one from the other.
- Publish only a sanitized reader prompt; keep production prompts, local paths, model notes, and intermediate instructions out of the article.
- Resolve relative asset paths against the profile location.
- Profiles may reference private local assets, but committed examples must use placeholders.
