---
name: sgc-wechat-branding-cover-direction
description: >
  将文章主题和参考图转为成熟的公众号品牌封面，管理素材来源、Logo 完整性与双比例裁切；用于“重做封面”“不要 AI 味”、"create an editorial WeChat cover"。
license: MIT
metadata:
  author: lovstudio
  version: "0.5.1"
  tags:
    - cover-design
    - editorial-art-direction
    - brand-integrity
  compatibility: "Embedded module; image generation, editing, or licensed-media retrieval is selected per task."
  dependencies: []
---

# Cover Direction

把文章命题翻译为一个克制、可辨认并适合公众号真实裁切的视觉世界。

## Triggers

### Activate when

- 用户说“参考这个成熟账号重做封面”“封面不要像 AI”“加入品牌 Logo”。
- Branding 管线启用封面生成、重构或替换。
- The user asks to "create an editorial WeChat cover" or improve an AI-looking cover.

### Do not activate when

- 用户只要求提取参考图 Design DNA，不需要封面成品。
- 当前封面已经通过审美、品牌和裁切验收且用户未要求变化。

## Workflow (MANDATORY)

1. 读取文章命题、参考图和品牌 Profile。
2. 读取 `$KIT_DIR/prompts/cover-hero-editorial-painterly.md`，先用文章事实填充 `ARTICLE_THESIS`、`CORE_RELATIONSHIP`、`PRIMARY_FORMS`、`MATERIAL_LANGUAGE` 和 `PALETTE`，再生成本次完整制作 Prompt。
3. 提取参考图的信息层级、焦点、留白、色彩、素材类型和品牌权重，不照抄其身份元素。
4. 解析 `wechat_article_branding.cover_composition.art_direction`；优先继承旧封面创作 skill 的 `source_skill`、`style`、`type`、`palette`、`rendering`、`text` 和 `mood`，再选择素材策略：真实摄影、授权或公共领域作品、生成式画面。选择理由必须服务文章而非工具偏好。
5. 需要外部素材时记录作品、作者、来源、使用状态和原始 URL。
6. 从 `publication.logo` 加载发布主体的官方 Logo；保持字形、字距、拼写和透明区域，不用生成模型重画品牌标识。`brand` 工作室、母品牌与 `products` 产品资产均不得作为默认替代。
7. 先构图 `2.35:1`，同时保护中心 `1:1` 安全区。
8. 控制视觉焦点；默认避免模板化蓝紫渐变、机器人、代码 UI、霓虹和无意义科技粒子。
9. 在生成或合成前保存完整制作 Prompt，并派生不含本地路径、内部备注和工具步骤的读者可复制 Prompt。
10. 启用 `opening_hero` 时，基于同一视觉世界制作独立正文首屏；默认采用 `4:3`、Logo 下方居中、导语之前，并避免继承导语卡片或正文容器样式。
11. 输出 PNG、上传用 JPG、裁切预览、制作 Prompt 和读者可复制 Prompt。
12. 上传后检查平台实际预览和 CDN 成品，而不是只检查本地文件。

## Art direction contract

- `type: hero` 需要一个可识别的主视觉隐喻和宽画幅张力，不用零散装饰拼出“看起来像封面”。
- `style: editorial` 需要有作者感的构图、材质和留白；`rendering: painterly` 使用绘画、纸艺或版画肌理，避免未经选择的暖色桌面静物和图库式产品摄影。
- `palette: elegant` 可使用克制的珊瑚、灰蓝、墨色、奶油色和少量金属色，但不把整张图压成单一橙棕色。
- `text: none` 时，底图不得出现标题、字母、数字、伪文字、Logo 或水印；官方 Logo 由 `cover-composition` 在生成后直接居中叠加。
- `center_safe_zone: true` 时，中心区域保持低细节和足够对比度，供官方 Logo 居中使用；宽版完成后再派生方形裁切。

## Prompt publication option

完整读取 `$KIT_DIR/references/cover-prompt.md` 与 `$KIT_DIR/prompts/cover-hero-editorial-painterly.md`。始终保留制作 Prompt 作为内部产物；只有配置或当前请求显式启用 `cover_prompt` 时，才把读者可复制版交给品牌模块写入文章。涉及公共领域或授权素材时，写清必需的输入素材或来源，不把合成流程伪装成纯文本生成。

## Decision rule

当“生成得更精细”仍然保留明显模型审美时，优先改变素材策略和信息层级，不继续堆叠 Prompt。确定性裁切、调色和官方 Logo 合成可以优于再次生成。

## Validation

- 封面只有一个主要视觉焦点。
- 横版与方形裁切都保留主题和品牌。
- Logo 高对比且不变形。
- Logo 对应 `publication.name` 的发布主体，而不是工作室、母品牌或产品。
- 素材来源可回溯。
- 制作 Prompt 与公开 Prompt 分离，公开版本可复制且不泄漏本地路径或内部上下文。
- 启用正文首屏时，首图位于导语之前并保持独立视觉容器。
- 文章标题由平台叠加时，画面仍留有可读区域。

## Dependencies

按任务选择图像生成、图像编辑、公共素材检索和真实页面预览能力。
