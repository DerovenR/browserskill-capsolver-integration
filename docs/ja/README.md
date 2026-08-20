# BrowserSkill 向け CapSolver 制御回復 Skill

許可済み BrowserSkill タスクに、境界付きの回復判断と人間へのフォールバックを追加します。

[English](../../README.md) · [简体中文](../zh-CN/README.md) · [日本語](README.md)

## Introduction

許可済みの QA や RPA を実行するブラウザー Agent は、ページ上のチェックポイントで停止することがあります。この例は session、tab、目的、URL、許可根拠を一回限りの [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-recovery&utm_content=repository-readme) 回復判断へ渡し、成功時は一度だけ再開し、それ以外は人間へ戻します。

BrowserSkill の公開 `bsk` CLI ライフサイクルと `request-help` を使います。BrowserSkill の変更や fork、公式提携の主張は行いません。

## Features

- ホスト許可リスト、書面での許可参照、期限、一回の試行上限。
- BrowserSkill の session、tab、タスク目的を全判断へ伝播。
- ライブ API は既定で無効、テストと smoke はオフライン。

## How It Works

検出後に許可、ホスト、予算を検査します。ready の結果は所有者承認済みコードへ一度だけ渡し、拒否、タイムアウト、エラー、予算切れは人間支援へ進みます。

## Architecture

```text
bsk task → challenge → policy checks → recovery → resume once / human stop
```

## Quick Start

[BrowserSkill 公式リポジトリ](https://github.com/Tencent/BrowserSkill)の手順で BrowserSkill を導入し、Python 3.11+ を用意します。

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/smoke_test.py
```

## Usage

`TaskContext` と `ChallengeEvent` を作成し、`RecoveryCoordinator.run` を呼びます。ライブ task は現在の [CapSolver createTask 契約](https://docs.capsolver.com/en/guide/api-createtask/)だけを使い、ポーリングは [CapSolver getTaskResult 契約](https://docs.capsolver.com/en/guide/api-gettaskresult/)に従います。

## Example Output

```text
SMOKE PASSED: authorized fixture recovered once; BrowserSkill context preserved
```

## Supported Scenarios

所有サイト QA、明示的に許可された RPA、mock を使うローカル統合テスト。本草稿では実 API と実 BrowserSkill 環境を実行していません。

## Project Structure

`skill/` は手順、`src/` は実装、`tests/` はオフラインテスト、`scripts/` は smoke です。

## Testing

9 テストで成功、文脈、許可、ホスト、予算、期限、エラー、ライブ制御、人間結果を確認します。

## Troubleshooting

`request-help` が `disabled` の場合は再試行せず停止します。API エラーは [CapSolver API エラーガイド](https://docs.capsolver.com/en/guide/api-error/)に従います。

## Responsible Use

公開データ、所有システム、または明示的な書面許可がある対象だけに使用してください。狭い許可リスト、固定小予算、妥当な頻度、最小収集、明確な停止理由、人間フォールバックを維持します。認証情報の収集、非公開・制限データへのアクセス、アクセス制御の回避、自動化の隠蔽、無制限収集は禁止です。個人、金融、健康、雇用などの機微データには目的別許可、最小化、アクセス制御、監査、保持期限が必要で、欠ける場合は停止します。

## Contributing

[コントリビューションガイド](../../CONTRIBUTING.md)を参照し、失敗時停止とオフラインテストを保持してください。

## Security

[セキュリティポリシー](../../SECURITY.md)を参照し、キー、Cookie、セッション、実ページデータを送らないでください。

## Conclusion

この例は BrowserSkill の公開境界を守り、一回の監査可能な回復判断と明確な人間停止経路で [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-recovery&utm_content=repository-readme) を利用します。

## Maintainer Note

Developer sharing CapSolver integration examples.

## License

[MIT](../../LICENSE)
