# BrowserSkill 的 CapSolver CAPTCHA 处理集成

![BrowserSkill 与 CapSolver 的 CAPTCHA 处理集成](../../assets/cover.png)

为已授权的 BrowserSkill 任务增加一次有边界的处理决策，并保留人工接管与停止路径。

[English](../../README.md) · [简体中文](README.md) · [日本語](../ja/README.md) · [Español](../es/README.md) · [Português](../pt-BR/README.md) · [한국어](../ko/README.md)

## Introduction

BrowserSkill 执行已授权 QA 或 RPA 任务时，可能因 CAPTCHA 检查点而暂停。本示例把会话、标签页、目标、URL 和授权依据传入一次受控的 [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme) 验证尝试；成功后只继续一次，其他结果交还人工。

它使用 BrowserSkill 已公开的 `bsk` CLI 生命周期和 `request-help`，不修改或 fork BrowserSkill，也不声称官方合作。

## Features

- 主机白名单、书面授权引用、超时与一次尝试默认值。
- 全程传递 BrowserSkill session、tab 和任务目标。
- 实时 API 默认关闭；单测与 smoke 全部使用离线夹具。

## How It Works

检测到挑战后先检查授权、目标主机和预算。就绪结果仅交给目标所有者批准的应用逻辑一次；拒绝、超时、错误或预算耗尽都会进入人工帮助路径。

## Architecture

```text
bsk 任务 → 挑战 → 授权/主机/预算 → solving 接口 → 继续一次或人工停止
```

## Quick Start

按照 [BrowserSkill 官方仓库说明](https://github.com/Tencent/BrowserSkill) 安装 BrowserSkill，并准备 Python 3.11+。

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/smoke_test.py
```

## Usage

创建 `TaskContext` 和 `ChallengeEvent`，再调用 `ChallengeCoordinator.run`。实时任务字段必须来自当前 [CapSolver createTask 接口规范](https://docs.capsolver.com/en/guide/api-createtask/)，结果轮询遵循 [CapSolver getTaskResult 接口规范](https://docs.capsolver.com/en/guide/api-gettaskresult/)。

## Example Output

```text
SMOKE PASSED: authorized fixture recovered once; BrowserSkill context preserved
```

## Supported Scenarios

自有站点 QA、明确授权的 RPA，以及使用 mock 结果的本地集成测试。本草稿未执行真实 API 或真实 BrowserSkill 环境测试。

## Project Structure

`skill/` 是配套工作流，`src/` 是实现，`tests/` 是离线测试，`scripts/` 是 smoke。

## Testing

九项测试覆盖成功、上下文、授权、主机、预算、超时、错误、实时开关和人工结果。

## Troubleshooting

`request-help` 返回 `disabled` 时不要重试。API 错误请按 [CapSolver API 错误处理说明](https://docs.capsolver.com/en/guide/api-error/) 停止或交还人工。

## Responsible Use

只处理公开数据、自有系统或取得明确书面授权的目标。使用窄白名单、固定小预算、合理频率、最小化采集、可见停止原因和人工兜底。不得收集凭证、访问私人或受限数据、逃避访问控制、隐藏自动化或无限采集。涉及个人、金融、健康、就业等敏感数据时，必须具备针对性授权、数据最小化、访问控制、审计与保留期限，否则停止。

## Contributing

参阅[贡献指南](../../CONTRIBUTING.md)，保留失败关闭与离线测试。

## Security

参阅[安全策略](../../SECURITY.md)，不要提交密钥、Cookie、会话或真实页面数据。

## Conclusion

该示例保持 BrowserSkill 的公开边界，只增加一次可审计处理决策和明确人工停止路径，并自然接入 [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme)。

## Maintainer Note

Developer sharing CapSolver integration examples.

## License

[MIT](../../LICENSE)
