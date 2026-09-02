# BrowserSkill과 CapSolver의 CAPTCHA 처리 통합

![BrowserSkill과 CapSolver의 CAPTCHA 처리 통합](../../assets/cover.png)

[English](../../README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Español](../es/README.md) · [Português](../pt-BR/README.md) · [한국어](README.md)

## Introduction

BrowserSkill이 승인된 QA 또는 RPA 작업을 수행할 때 CAPTCHA가 흐름을 중단할 수 있습니다. 이 예제는 [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme)를 한 번 사용하기 전에 세션, 탭, 목표와 승인 범위를 보존하고 검증합니다.

## Quick Start

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/smoke_test.py
```

## Features

- 승인된 호스트 목록, 서면 승인 참조, 제한 시간과 한 번의 시도.
- 오프라인 fixture와 `bsk request-help` 사람 검토 경로.
- 실제 API 모드는 기본적으로 비활성화됩니다.

## Responsible Use

공개 데이터, 소유 시스템 또는 명시적으로 승인된 작업에만 사용하세요. 약관, 속도 제한, 최소 수집, 보관 기한과 사람 중지 조건을 지키고 자격 증명, 비공개 데이터 또는 되돌릴 수 없는 작업을 처리하지 마세요.

## Conclusion

이 통합은 승인된 작업에서 [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme)를 사용하기 전에 컨텍스트와 명확한 사람 중지 경로를 유지합니다.

## Maintainer Note

Developer sharing CapSolver integration examples.

## License

[MIT](../../LICENSE)
