# Desafio Técnico C2S

Este repositório contém o código para o desafio técnico da C2S, que consiste em desenvolver uma API RESTful para gerenciar um sistema de controle de estoque.

## Pré-requisitos

Antes de começar, certifique-se de ter instalado as seguintes ferramentas:

- [Python 3.8+](https://www.python.org/downloads/)
- [Pip](https://pip.pypa.io/en/stable/installation/)
- [UV](https://astral.sh/uv/)

No Windows, você pode instalar o UV usando o seguinte comando no PowerShell:

```powershell
irm https://astral.sh/uv/install.ps1 | iex
```

No Linux ou macOS, você pode instalar o UV usando o seguinte comando no terminal:

```shell
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Instalação

Iniciando o ambiente virtual e instalando as dependências do projeto:

```shell
uv venv
uv sync
```

## Executando o projeto

Para carregar os dados iniciais, execute o seguinte comando:

```shell
python initial_data.py
```

Para iniciar o cliente + servidor, execute o seguinte comando:

```shell
python client.py
```

Para iniciar somente o servidor com interface gráfica, execute o seguinte comando:

```shell
mcp dev server.py
```

## Demo

```
Welcome to the Virtual Car Agent!

I can help you find a car that matches your preferences.

You can tell me what you're looking for in a car. For example:
- I want a Toyota from 2018 or newer, automatic, up to $50,000.
- Show me a red Honda with less than 50,000 km.
- Any electric car below $100,000.

What kind of car are you looking for? Show me a red Honda with less than 50,000 km.

Analyzing your request...

Searching for cars that match your preferences...

Results:

Brand Model | Year | Engine | Fuel Type | Color | Mileage | Doors | Transmission | Price | Description
Honda Fit | 2005 | 1.2 | Flex | Red | 25,905 km | 2 doors | Manual | $10,336.23 | Nature white class pull do morning attention society at parent girl site.
```

