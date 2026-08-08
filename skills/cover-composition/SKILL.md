---
name: sgc-wechat-branding-cover-composition
description: >
  按既有公众号封面裁切器的确定性规则合成品牌封面：艺术图片打底、底部轻微调暗、官方发布 Logo 居中叠加，并从宽版派生方形裁切。
license: MIT
metadata:
  author: lovstudio
  version: "0.5.0"
  tags:
    - cover-composition
    - centered-logo
    - wechat
  compatibility: "Embedded module; requires a raster image compositor or the existing local WeChat cover editor."
  dependencies: []
---

# Cover Composition

本模块负责分享封面的最终合成，不负责生成新的 Logo，也不把正文首屏规则混入分享封面。

## Triggers

### Activate when

- `cover-direction` 已产出公众号分享封面的艺术底图，需要叠加发布主体 Logo 并输出双比例制品。
- 用户要求复用“艺术图片打底、Logo 居中”的既有封面风格。
- Branding 管线启用分享封面制作或重构。
- The user asks to "center the Logo over the artistic WeChat cover background".

### Do not activate when

- 当前请求只需要正文首屏品牌图，不需要分享封面。
- 当前请求只做封面审计，不允许生成或合成新制品。

## Composition contract

1. 使用 `cover-direction` 产出的艺术主图作为底图；先铺满 `2.35:1` 画布，再处理品牌层。
2. 按 `wechat_article_branding.cover_composition.background_dimming` 添加从约 38% 画面高度开始的底部渐变调暗，默认强度为 `0.45`。
3. 直接读取 `publication.logo`，保留原始字形、比例、透明区域和颜色；默认最大宽度为画布宽度的 `24%`，最大高度为画布高度的 `45%`。
4. Logo 以画布几何中心居中叠加。不要加左下角面板、圆角卡片、贴纸、胶囊底或额外品牌文字。
5. 从已经完成 Logo 合成的宽版中心裁切 `1:1`，不要分别生成一张位置不同的方版封面；这样两个比例中的 Logo 都保持居中。
6. 输出未叠加 Logo 的艺术底图、宽版合成图、方版合成图以及上传用 JPG；保留合成前后的本地文件便于回滚和比较。

## Existing editor compatibility

如果当前环境可用旧的公众号封面裁切器，复用它的“Logo 覆盖 / 居中叠加品牌标识”路径。其等价实现是：底图居中填满、底部渐变调暗、Logo 按上述限制缩放后以 `(画布宽度 - Logo 宽度) / 2` 和 `(画布高度 - Logo 高度) / 2` 定位。

## Validation

- 宽版和方版 Logo 的几何中心与画布中心一致。
- Logo 来自 `publication.logo`，没有被图像模型重画或变形。
- 两个比例均只有一个主视觉焦点，且没有品牌面板遮挡艺术主体。
- 上传前先查看宽版和中心方形裁切；上传后检查平台 CDN 成品。
