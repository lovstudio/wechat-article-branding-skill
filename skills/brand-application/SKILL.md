---
name: sgc-wechat-branding-brand-application
description: >
  从可移植品牌 Profile 生成专业且不突兀的作者、工作室、产品和资源内容块；用于“增加品牌收尾”“加入产品介绍”、"apply this brand to the article"。
license: MIT
metadata:
  author: lovstudio
  version: "0.4.0"
  tags:
    - brand-content
    - article-endcap
    - product-copy
  compatibility: "Embedded module for sgc-wechat-article-branding-skill."
  dependencies: []
---

# Brand Application

把品牌作为稳定、独立的出版组件应用到文章中。它可以在视觉上与文章协调，但不把正文的隐喻、结论或临时话题改写成品牌口号。

## Triggers

### Activate when

- 用户说“结尾做一些专业且不违和的 PR”“加入工作室和产品介绍”。
- 用户说“把封面 Prompt 放进文章”“公开这张封面的提示词”或要求正文首屏品牌图。
- Branding 管线需要应用 Logo、品牌语言、产品事实、链接或可复制资源块。
- The user asks to "apply this brand to the article" or add a subtle branded endcap.

### Do not activate when

- 没有经过验证的品牌 Profile，且用户没有提供可公开事实。
- 用户要强销售落地页或广告投放文案，而不是文章品牌化。

## Workflow (MANDATORY)

1. 完整读取根级品牌 Profile、批准的固定品牌区块与当前文章结构；明确区分 `publication` 发布主体、`brand` 工作室品牌和 `products` 产品。
2. 只使用 `public_facts`、产品名称、结果承诺、公开 URL 和批准的视觉字段。
3. Profile 已提供批准文案时直接复用；不要为了“呼应文章”临时创造口号、比喻或新的品牌定位。
4. 没有批准文案时，用稳定品牌主张和“为读者带来什么结果”描述产品，不罗列内部能力和技术数量。
5. 构建必要内容块：品牌尾注、产品介绍、作者信息、链接、可复制 Prompt 或代码。每个产品只输出 `products[].url` 这一主链接；不从正文、代码仓库或其他资料追加辅助链接。
6. 启用 `cover_prompt` 时，完整读取 `$KIT_DIR/references/cover-prompt.md`，使用封面模块产出的读者可复制版本；默认锚点为正文结论之后、品牌尾注之前，唯一标记为 `data-sgc-block="cover-prompt"`。
7. 可复制资产只保留章节标题和内容块；删除本地路径、内部背景、工具步骤、制作过程和复用说明。
8. 根据 Profile 应用 Logo、品牌色和层级；封面与正文首图只认 `publication.logo`，品牌尾注使用 `brand` 和 `products`；文章主题只影响摆放与视觉权重，不改写品牌内容主体。
9. 检查名称、链接、拼写、承诺和 `forbidden_context`。

## Editorial test

把品牌区复制到另一篇不同主题的文章末尾：若核心文案仍成立，说明它保持了稳定品牌身份；若依赖当前正文的人物、隐喻或结论才成立，回退到批准的固定品牌文案。是否突兀由位置、长度和视觉层级解决。

## Validation

- 品牌内容比文章结论短且层级更低。
- 没有内部背景、私人说明和未验证主张。
- 产品承诺来自 Profile，且不依赖当前文章主题才能成立。
- Prompt、代码或清单是直接可复制的内容块。
- 封面 Prompt 只出现一次，位于正文结论与品牌尾注之间，并与制作 Prompt 的实际方法一致。
- 链接和品牌资产准确。
- 每个产品最多一个链接，等于其 `products[].url`，且未在 `blocks.endcap.links` 中重复。

## Dependencies

Root brand Profile from `$KIT_DIR/references/brand-profile.md`.
