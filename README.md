# lovstudio-wechat-article-branding

![Version](https://img.shields.io/badge/version-0.1.0-CC785C)

自动读取微信公众号文章，完成内容智能、封面指导和品牌预设应用，交付专业、有审美的品牌内容。

## 本地安装

在本仓库根目录执行：

```bash
export SKILL_SOURCE_DIR="$(pwd)"
mkdir -p "${LOVSTUDIO_SKILLS_INSTALL_DIR:?请设置本地 Skills 目录}"
ln -s "$SKILL_SOURCE_DIR" \
  "$LOVSTUDIO_SKILLS_INSTALL_DIR/lovstudio-wechat-article-branding"
```

## 用户配置

品牌名称、Logo、产品、链接、语气和设计指南通过共享 Profile 提供。真实配置不进入 Skill 源码。

默认共享配置：

```bash
${LOVSTUDIO_SKILLS_PROFILE:-$HOME/.lovstudio/skills/profile.json}
```

详见 `references/user-config.md` 与 `references/brand-profile.md`。

## 使用

```text
$lovstudio-wechat-article-branding 把当前公众号文章整体品牌化：生成目录、重构封面、增加专业的品牌收尾并保存验证。
```

```text
$lovstudio-wechat-article-branding audit 当前文章，只检查内容、审美和品牌一致性，不修改。
```

## 管线

- `full`：内容、封面、品牌和验收
- `content`：结构、TOC、摘要或明确要求的润色
- `cover`：封面策略、制作、上传和裁切验收
- `brand`：品牌内容与可复制资产块
- `audit`：只读质量检查

## 质量门

```bash
python3 scripts/validate_skill.py .
python3 scripts/validate_brand_profile.py --self-test
```

## 依赖

- 能复用用户登录状态的浏览器自动化适配器
- 封面任务按需使用图像或素材能力
- Python 3.8+
- PyYAML（源码结构校验）

## License

MIT
