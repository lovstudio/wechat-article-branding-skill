# User Configuration

Resolve persistent brand and editorial preferences without creating a private implementation branch.

## Resolution order

1. Explicit values in the current request.
2. Skill-specific environment variables.
3. Shared profile JSON.
4. Safe inferred defaults such as the current language.
5. One focused question for a required user-facing value that remains unknown.

Default profile location:

```bash
${LOVSTUDIO_SKILLS_PROFILE:-$HOME/.lovstudio/skills/profile.json}
```

## First run

1. Prefill fields from the request and current project.
2. Load a brand-profile file referenced by the shared profile.
3. Validate it with `scripts/validate_brand_profile.py`.
4. Ask only for a missing field that changes public output.
5. Show values before persisting them with the user's knowledge.

Do not persist article bodies, cookies, edit tokens, private URLs, inferred claims, or temporary browser state.

## Shared profile example

```json
{
  "user": {
    "language": "zh-CN",
    "timezone": "Asia/Shanghai"
  },
  "brand": {
    "profile": "$HOME/.lovstudio/skills/brand.json"
  },
  "wechat_article_branding": {
    "brand_profile": "$HOME/.lovstudio/skills/wechat-article-branding-brand.json",
    "default_pipeline": "full",
    "polish_enabled": false,
    "cover_ratios": ["2.35:1", "1:1"],
    "cover_composition": {
      "base": "artistic",
      "art_direction": {
        "source_skill": "baoyu-cover-image",
        "style": "editorial",
        "type": "hero",
        "palette": "elegant",
        "rendering": "painterly",
        "text": "none",
        "mood": "balanced",
        "center_safe_zone": true
      },
      "logo": {
        "enabled": true,
        "position": "center",
        "max_width_ratio": 0.24,
        "panel": false
      },
      "background_dimming": {
        "enabled": true,
        "strength": 0.45
      }
    },
    "opening_hero": {
      "enabled": false,
      "ratio": "4:3",
      "placement": "before_intro"
    },
    "cover_prompt": {
      "enabled": false,
      "placement": "before_endcap",
      "title": "封面 Prompt"
    }
  }
}
```

`opening_hero` 与 `cover_prompt` 均默认关闭。只有当前请求或持久配置显式启用时写入正文；生成本地封面 Prompt 本身不视为公开授权。

`cover_composition` 只控制分享封面的视觉合成与艺术方向，不会启用正文首屏。默认组合为旧封面创作 skill 的 `hero/editorial` 艺术主图铺底、官方发布 Logo 居中叠加、无品牌面板；方形封面从已合成的宽版中心裁切。`text: none` 表示底图不绘制标题、Logo 或伪文字，品牌标识由后置合成层直接放置。

`wechat_article_branding.brand_profile` 优先于共享的通用 `brand.profile`。公众号品牌化必须从该文件解析 `publication`，避免把工作室或产品品牌误用为发布账号 Logo。
