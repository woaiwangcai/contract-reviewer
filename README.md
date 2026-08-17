**  
> 一键打通 `DOCX 结构化解析` → `Prompt 协议隔离` → `大模型深度研判` → `独立 HTML/MD 报告交付`。

[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://github.com/woaiwangcai/contract-reviewer/actions/workflows/tests.yml/badge.svg)](https://github.com/woaiwangcai/contract-reviewer/actions/workflows/tests.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-2F6F4E.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/woaiwangcai/contract-reviewer)](../../releases/latest)

---

**Contract Reviewer** 专为追求**可靠性与审查深度**的法律科技场景设计。它将复杂的合同文件转化为标准结构化 Markdown，结合工业级可复用审查协议（Skill），接入任意兼容 OpenAI 接口的大模型，最终自动化交付可继续二次编辑的 Markdown 分析记录与**开箱即用、支持直接打印/离线阅读的独立 HTML 报告**。

![HTML report preview](docs/report-preview.png)

---

## ✨ 核心亮点

* 🎯 **确定性工程管线**：格式转换、结构保真、报告渲染 100% 由代码确定性执行，模型仅聚焦风险识别与法理判断。
* 🛡️ **严格的数据与指令分离**：将合同全文视为纯文本输入，通过协议防御 Prompt 注入与幻觉，严禁模型虚构条款。
* 🔍 **证据链精准溯源**：审查报告强制要求每一项法律风险关联合同原文字句，杜绝空泛结论。
* 🔌 **零厂商锁定（Vendor-Agnostic）**：标准 OpenAI-compatible 协议，无缝适配 DeepSeek、Qwen、Claude、GPT 等各大主流模型。
* 📄 **高颜值离线报告**：单文件 HTML 独立封装，零外部 CSS/JS CDN 依赖，断网也能秒开并支持直接打印排版。

---

## 🔄 架构与工作流

```mermaid
flowchart LR
    A[📄 DOCX 合同] -->|结构化清洗| B[📑 标准 Markdown]
    B --> C{🛡️ 审查 Skill 协议}
    C -->|API 调用| D[🧠 Model API]
    D -->|结构化输出| E[📝 Markdown 报告]
    E -->|模板渲染| F[📊 独立 HTML 报告]
分工理念：让代码做确定的事，让 AI 做深度的判断模块文件职责说明文档解析src/docx_to_md.py严格保留标题层级、段落、列表、复杂表格顺序，剔除干扰格式审查协议skills/contract_review.md规定审查边界、证据要求、风险等级定义（高/中/低）与结构规范通用驱动src/model_client.py极简高效的 API 客户端，专注标准化调用，安全校验端点与密钥专业排版src/md_to_html.py清洗潜在危险标签（XSS 防护），注入专属阅读样式，渲染单文件报告⚡ 快速开始1. 克隆与下载从 Releases 下载预打包版本，或直接克隆仓库：Bashgit clone [https://github.com/woaiwangcai/contract-reviewer.git](https://github.com/woaiwangcai/contract-reviewer.git)
cd contract-reviewer
2. 环境准备Windows (PowerShell):PowerShellpy -m venv .venv
.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
macOS / Linux:Bashpython3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
3. 配置模型参数复制环境变量示例文件：Bashcp .env.example .env
在 .env 中配置你的模型服务凭证（兼容任意 OpenAI 格式服务商）：代码段MODEL_API_KEY=your-api-key
MODEL_BASE_URL=[https://api.deepseek.com/v1](https://api.deepseek.com/v1)
MODEL_NAME=deepseek-chat
注：生产环境强制要求 HTTPS 远程接口；HTTP 仅允许本机回环地址（Localhost）用于本地模型测试。4. 一键执行审查Bashpython main.py --input examples/sample_contract.docx
执行完毕后，终端将输出生成的文件路径：Plaintext✅ 审查完成！已生成双格式报告：
output/sample_contract-review.md
output/sample_contract-review.html
💡 防覆盖机制：若同名报告已存在，系统自动递增命名（如 -2.html、-3.html），保障历史记录安全。🛠️ 进阶用法与参数Plaintext参数说明：
  --input      [必填] 待审查的 DOCX 文件路径
  --skill      [可选] 审查协议路径（默认: skills/contract_review.md）
  --output     [可选] 报告输出目录（默认: output/）
  --env-file   [可选] 环境变量文件路径（默认: .env）
  --version    [可选] 查看当前版本
加载自定义审查协议（如采购合同专项审查）：Bashpython main.py \
  --input "contracts/service-agreement.docx" \
  --skill "skills/procurement-review.md" \
  --output "reports/2026-Q1"
🧩 为什么是 “Skill（审查协议）”？在本项目中，Skill 绝不仅是一句简单的系统提示词，而是一份具备工业级约束的审查执行标准与接口契约。它从机制上锁定了模型行为：上下文隔离：合同全文仅作为只读分析目标，不可覆写系统审查指令。严禁无据推论：模型必须做到“凡提风险，必引原条”，没有依据则视为不存在该风险。量化风险评级：统一度量标准（核心履约风险 / 合规瑕疵 / 商务友好建议）。确定性输出结构：严格约束 Markdown 报告的章节层级，保障下游解析与 HTML 渲染的百分之百稳定性。默认协议位于 skills/contract_review.md，你可以根据业务需求自由阅读、修改或为特定合同类型定制专项 Skill。📁 目录结构Plaintextcontract-reviewer/
├── main.py                    # CLI 命令行入口
├── src/
│   ├── docx_to_md.py          # DOCX → Markdown 结构化提取器
│   ├── model_client.py        # 标准 Model API 适配层
│   ├── md_to_html.py          # Markdown → 独立 HTML 渲染引擎
│   └── workflow.py            # 主干工作流调度编排
├── skills/
│   └── contract_review.md     # 默认通用合同审查协议
├── templates/
│   └── report.html            # 独立 HTML 报告模板
├── examples/                  # 虚构示例：输入、转换中间态与最终报告
└── tests/                     # 自动化测试套件（无需联网消耗 Token）
🔒 隐私与合规安全合同数据具有高度敏感性，本项目在架构层面贯彻严格的安全设计：🛡️ 无外部泄露风险：本地代码不上传任何统计信息，不设中间转发服务器，仅与你显式配置的 MODEL_BASE_URL 通信。🔐 凭证隔离：.env、output/ 与本地日志全部纳入 .gitignore；异常捕获均对 API Key 做了脱敏过滤。🧼 XSS 深度清洗：HTML 渲染引擎内置严格的标签与属性白名单机制，防范潜在注入风险。⚠️ 免责与复核：AI 审查结果旨在提供辅助参考与盲点排查，涉及重大交易及法律责任事项请务必由持牌专业人员复核。更多安全策略与建议请查阅 SECURITY.md。🧪 开发与测试本项目内置了完备的 Mock 测试，无需调用真实 API 产生费用即可验证全部逻辑链路：Bashpython -m pip install -r requirements-dev.txt
python -m pytest
📄 开源协议本项目基于 MIT License 开源。
---

### 💡 润色说明
* **Slogan & 概述升维**：修复了原句重复的“将...将...”小语病，将项目定义升维为“高可控、零依赖锁定的中文合同 AI 智能审查工作流”。
* **亮点模块提炼**：新增 `✨ 核心亮点` 和清晰的对照表格，让技术同行或非技术用户一眼看懂“为什么它比普通 Prompt 靠谱”。
* **强化 Skill 概念**：把“Prompt 隔离”、“强制原文证据溯源”这些法务 AI 领域极其看重的痛点明确标出。
* **排版层级优化**：增加了清晰的 emoji 分区与跨平台命令高亮，视觉上更具现代开源项目的精美质感。
