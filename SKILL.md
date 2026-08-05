---
name: lovstudio-wechat-article-branding
description: >
  自动读取微信公众号文章并完成目录、封面、正文首屏、可公开封面 Prompt、结构优化和品牌内容应用；适用于“把当前公众号文章品牌化”“加上封面 Prompt”、"turn this WeChat article into branded content"。
license: MIT
metadata:
  author: lovstudio
  version: "0.4.0"
  tags:
    - wechat
    - article-branding
    - editorial-design
    - content-intelligence
  compatibility: "Agent runtime with authenticated browser automation; optional image generation or licensed-media research; Python 3.8+ for profile validation."
  dependencies: []
---

# 微信公众号文章品牌化

把一篇普通的微信公众号文章自动加工成结构专业、视觉成熟、具有品牌辨识度的可发布内容。文章自动化只是底座；用户得到的是经过内容理解、智能增强、品牌应用和真实页面验收的完整制品。

## Triggers

### Activate when

- 用户说“把当前公众号文章品牌化”“加上目录、封面和品牌收尾”“整体优化得更专业、更有审美”。
- 用户给出当前公众号文章、参考封面或品牌资料，要求直接完成内容与视觉包装。
- The user asks to "brand this WeChat article", "polish the whole article for publication", or "turn this WeChat article into professional branded content".

### Do not activate when

- 用户只要求读取、插入、替换或保存某个明确字段，使用 `lovstudio-wechat-article-operator`。
- 用户只需要一张独立封面或一次离线文案改写，不涉及完整公众号文章。
- 用户明确只要诊断报告而不允许修改时，选择 `audit` 管线，不执行写回。

## Product contract

- **Outcome over automation.** 不把浏览器、草稿、选择器或上传过程当成交付。
- **Article truth first.** 先取得真实文章，再决定 TOC、封面、摘要、润色和品牌区需要什么。
- **Context is not copy.** 人名、括号说明、沟通背景和内部定位默认不进入用户可见内容。
- **Brand is a profile.** Skill 不硬编码任何品牌；名称、Logo、产品、链接和设计规范来自可移植配置。
- **Publisher identity is first-class.** 封面与正文首图只使用 `publication` 中的发布主体名称和官方 Logo；工作室、母品牌或产品 Logo 不得自动替代。
- **One primary product link.** 品牌尾注默认只展示每个产品的一个主链接，不追加代码仓库、下载页或其他辅助链接。
- **One coherent edition.** TOC、标题、摘要和封面围绕同一文章命题；稳定品牌区保持自身定位，不借正文隐喻临时改写。
- **Artifacts are selectable.** 分享封面、正文首屏品牌图和面向读者的封面 Prompt 是三个独立选项；不因生成了本地 Prompt 就默认公开到文章。
- **Publisher voice matters.** 转载、采访与自述的标题必须匹配当前发布账号的叙事身份，不照搬来源媒体对发布者的第三人称命名。
- **Persisted acceptance.** 保存后重载、真实裁切和最终可见顺序是验收依据。

## User Configuration

通过 [用户配置](references/user-config.md) 与 [品牌 Profile](references/brand-profile.md) 解析持久设置。显式请求和当前文章事实优先；不得把用户的真实配置提交进 Skill 源码。

## Skill Kit Modules

执行所选管线前完整读取对应模块：

- `$SKILL_DIR/skills/article-access/SKILL.md` — 获取文章、调用公开 Operator 或使用自包含适配流程。
- `$SKILL_DIR/skills/content-intelligence/SKILL.md` — 文章结构、TOC、摘要与可选润色计划。
- `$SKILL_DIR/skills/cover-direction/SKILL.md` — 封面策略、素材来源、品牌完整性与双比例裁切。
- `$SKILL_DIR/skills/brand-application/SKILL.md` — 品牌文案、产品信息、可复制资产块与视觉预设。
- `$SKILL_DIR/skills/quality-gate/SKILL.md` — 内容、审美、品牌和保存持久化验收。

`kit.yaml` 是模块和管线的机器可读契约。

## Workflow (MANDATORY)

### Step 0: Resolve the Skill Kit and select a pipeline

检查 `kit.yaml`、所需模块、引用文件和脚本。根据用户结果选择：

| 用户结果 | 管线 |
|---|---|
| TOC、封面和品牌内容完整处理 | `full` |
| 只优化文章结构、目录或摘要 | `content` |
| 只重构封面并写回文章 | `cover` |
| 文章稳定，只应用品牌内容 | `brand` |
| 只检查当前文章是否专业、统一 | `audit` |

用户说“为什么不够专业/不好看”且没有禁止修改时，使用 `full`：先解释根因，再直接修复。

### Step 1: Resolve the article and brand profile

1. 从当前请求、环境、共享 Profile 和安全默认值解析配置；分别解析 `publication` 发布主体、`brand` 工作室品牌与 `products` 产品。
2. 必需的品牌事实仍缺失时，只问一个会改变最终用户可见结果的问题。
3. 运行：

```bash
python3 "$SKILL_DIR/scripts/validate_brand_profile.py" BRAND_PROFILE.json
```

4. 通过文章访问模块取得真实文章状态，不从聊天摘要重建文章。

### Step 2: Build an internal truth ledger

将输入分为：

- `article truth`：正文明确表达的主题、证据和语气；
- `publishable brand fact`：Profile 中允许公开的品牌、产品和链接；
- `internal context`：帮助判断但不应公开的背景；
- `evidence gap`：不得写成事实的缺口。

先形成简短的文章命题、读者收益和期望行动，再生成任何可见内容。

### Step 3: Plan one coherent branded edition

生成内部变更计划：

- 哪些章节进入 TOC；
- 标题是否符合当前发布账号、文章体裁和转载关系；
- 是否需要结构、摘要或语言调整；
- 封面应采用生成式画面、摄影或授权/公共领域作品；
- 哪些稳定品牌区块直接复用，哪些只需调整位置与视觉层级；
- 是否启用正文首屏品牌图与可公开封面 Prompt，以及各自的锚点；
- 哪些字段和段落必须保持不变；
- 每个新增区块的锚点、唯一标记和验收信号。

初版中润色默认关闭；只有用户明确要求时启用，并在报告中标记为尚未经过本轮基准验证的模块。

### Step 4: Run content intelligence

使用内容智能模块：

1. 从真实标题与章节生成可扫描的 TOC；
2. 单独评估标题：先判断发布账号是采访者、受访者还是转载者，再决定保留、第一人称化或主题化；
3. 保留原作者观点、事实和语气；
4. 避免重复解释、模板化过渡和功能清单；
5. 将 Prompt、代码或清单组织成“章节标题 + 可复制内容块”；
6. 只把用户真正需要看到的信息放入成品。

### Step 5: Direct the cover

使用封面模块把文章命题变成一个视觉世界：

- 先分析参考图的信息层级和审美语法，不逐元素照抄；
- 根据题材选择真实素材或生成式画面；
- 只使用 `publication.logo` 指向的发布主体官方 Logo，保留字形、间距和拼写；不得从 `brand.name`、工作室资产目录或产品名称猜测 Logo；
- 同时验证 `2.35:1` 消息列表与中心 `1:1` 分享裁切；
- 保存完整 Prompt、素材来源、PNG 与上传用 JPG；
- 同时生成制作 Prompt 与经过清理的读者可复制 Prompt；只有显式启用 `cover_prompt` 时才把后者写入正文；
- 启用 `opening_hero` 时，另做适合正文阅读的首屏比例并放在导语之前；不得直接把分享封面当作未经设计的普通插图；
- 真实上传后检查平台 CDN 成品。

### Step 6: Apply the brand

使用品牌应用模块：

- 只引用 Profile 中允许公开的事实；
- 以“读者获得什么”介绍品牌和产品；
- 优先复用稳定品牌文案，不从当前文章的比喻、结论或人物经历临时推演品牌口号；
- 通过位置、长度和视觉层级避免突兀，而不是强行把品牌文案写成正文续篇；
- 控制品牌区长度和视觉权重；
- 每个产品仅展示 `products[].url` 这一主链接；`blocks.endcap.links` 只承载工作室等非产品链接；
- 将启用的封面 Prompt 组织为“封面 Prompt + 单一可复制内容块”，默认放在正文结论之后、品牌尾注之前；
- 链接、Logo、产品名和口号必须与 Profile 一致。

### Step 7: Write back through the article operator

优先调用公开的 `lovstudio-wechat-article-operator`。若不可用，使用文章访问模块中的自包含操作契约：

1. 保存变更前快照；
2. 按计划执行最小写入；
3. 使用唯一标记检查 `opening-hero`、`cover-prompt`、TOC 与品牌尾注的重复、错位、测试文字和空壳节点；
4. 预览正文与封面；
5. 保存并重新加载。

### Step 8: Run the quality gate

按 [验收标准](references/acceptance.md) 验证：

1. **内容：** 文章命题、事实和语气未被破坏；
2. **结构：** TOC、标题和新增区块顺序正确且只出现一次；
3. **审美：** 封面、版式和品牌区形成统一层级；
4. **品牌：** 发布主体 Logo、工作室名称、产品承诺和主链接角色准确；
5. **机械：** 保存后重载仍存在，非目标字段保持不变。

发现因果问题时直接修复并重复完整验收，不把“已生成”或“已上传”当成完成。

### Step 9: Report the edition

用用户语言说明：

- 文章增加或调整了什么；
- 标题如何匹配发布账号与文章体裁；
- 封面策略与素材类型；
- 应用了哪些品牌预设；
- 保存、重载和裁切观察结果；
- 哪些可选模块未运行或仍缺证据。

## References

- [用户配置](references/user-config.md)
- [品牌 Profile](references/brand-profile.md)
- [验收标准](references/acceptance.md)
- [封面 Prompt 选项](references/cover-prompt.md)

## Dependencies

- 可操作用户已登录微信公众号页面的浏览器自动化能力。
- 封面任务需要时使用图像生成、图像编辑或有来源的素材检索能力。
- Python 3.8+；PyYAML 仅用于源码结构校验。
