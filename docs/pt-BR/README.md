# Tratamento de CAPTCHA no BrowserSkill com CapSolver

![Tratamento de CAPTCHA no BrowserSkill com CapSolver](../../assets/cover.png)

[English](../../README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Español](../es/README.md) · [Português](README.md) · [한국어](../ko/README.md)

## Introduction

Quando o BrowserSkill executa uma tarefa autorizada de QA ou RPA, um CAPTCHA pode interromper o fluxo. Este exemplo preserva sessão, aba, objetivo e autorização antes de permitir uma única tentativa limitada com [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme).

## Quick Start

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/smoke_test.py
```

## Features

- Hosts autorizados, referência escrita, prazo e uma tentativa.
- Fixtures offline e caminho humano com `bsk request-help`.
- O modo de API real fica desativado por padrão.

## Responsible Use

Use somente dados públicos, sistemas próprios ou autorização explícita. Respeite termos, limites, minimização, retenção e paradas humanas. Não processe credenciais, dados privados ou ações irreversíveis.

## Conclusion

A integração mantém o contexto e uma parada humana clara antes de usar [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme) em uma tarefa autorizada.

## Maintainer Note

Developer sharing CapSolver integration examples.

## License

[MIT](../../LICENSE)
