# Manejo de CAPTCHA en BrowserSkill con CapSolver

![Manejo de CAPTCHA en BrowserSkill con CapSolver](../../assets/cover.png)

[English](../../README.md) · [简体中文](../zh-CN/README.md) · [日本語](../ja/README.md) · [Español](README.md) · [Português](../pt-BR/README.md) · [한국어](../ko/README.md)

## Introduction

Cuando BrowserSkill ejecuta una tarea autorizada de QA o RPA, un CAPTCHA puede interrumpir el flujo. Este ejemplo conserva la sesión, pestaña, objetivo y autorización antes de permitir un único intento limitado con [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme).

## Quick Start

```bash
python -m pip install -e .
PYTHONPATH=src python -m unittest discover -s tests -v
PYTHONPATH=src python scripts/smoke_test.py
```

## Features

- Lista de hosts autorizados, referencia escrita, plazo y un intento.
- Fixtures offline y ruta humana con `bsk request-help`.
- El modo de API real está desactivado por defecto.

## Responsible Use

Úselo solo con datos públicos, sistemas propios o autorización explícita. Respete términos, límites, minimización, retención y paradas humanas. No procese credenciales, datos privados o acciones irreversibles.

## Conclusion

La integración mantiene el contexto y una parada humana clara antes de usar [CapSolver](https://www.capsolver.com/?utm_source=github&utm_medium=referral&utm_campaign=browserskill-capsolver-integration&utm_content=repository-readme) en una tarea autorizada.

## Maintainer Note

Developer sharing CapSolver integration examples.

## License

[MIT](../../LICENSE)
