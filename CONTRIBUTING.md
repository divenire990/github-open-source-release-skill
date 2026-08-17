# 贡献指南 (Contributing Guide)

感谢您对 **github-open-source-release-skill** 的关注与贡献！本项目是一个用于指导与约束 AI 智能体（如 Codex, Claude Code, Oh My Pi 等）安全、合规发布开源项目的标准化技能库。

---

## 贡献原则与准则

1. **规范与结构一致性**
   - 技能主文件 `SKILL.md` 必须遵循标准的 Agent Skill 格式（包含 YAML Front Matter，定义清晰的 `name` 与 `description`）。
   - 核心工作流小节必须保持完整、结构清晰，包含分层验收清单（Layered Verification Checklist）。

2. **文档同步要求**
   - 默认主文档为中文 `README.md`，配套提供英文文档 `README.en.md`。
   - 任何涉及功能、工作流、参数或规范的修改，**必须同时更新中英文文档**，并确保首屏双向互链正常。

3. **真实自包含多媒体资产**
   - 演示动图（GIF）与示意图必须存放在仓库内 `./assets/` 目录，并在 Markdown 中使用相对路径引用。
   - 动图必须为真实多帧动画，严禁使用单帧静态图片伪装动图，严禁伪造虚假数据或包含敏感机器路径。

4. **敏感信息与隐私红线**
   - 严格杜绝在代码、文档、配置中包含任何硬编码 API Key、Token、私有凭据或内部网络地址。
   - 严禁包含开发者本地绝对文件路径（如真实机器用户路径）；示例与模板中仅允许使用通用相对路径或规范占位符。
   - 提交前请确认 Git Author Name 与 Author Email 符合公开开源规范（推荐使用 GitHub No-Reply 邮箱）。

5. **纯文档型仓库定位**
   - 本项目属于纯文档与规范型 Skill 仓库（Documentation-only Skill repository），**不包含且不适用 Python 软件包构建与打包**（Python packaging is not applicable）。

---

## 本地验证门禁

在提交 Pull Request 前，请确保本地通过离线结构与安全验证：

```bash
# 安装轻量验证依赖（Pillow 与 PyYAML 用于解析与动图核验）
pip install pillow pyyaml

# 运行自动化验证门禁
python scripts/validate.py
```

CI 门禁将对上述各项规范进行自动化离线检查，确保所有检查项全部通过（PASS）后方可合并。
