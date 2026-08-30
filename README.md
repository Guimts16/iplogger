# IP Logger PoC em Python

Este repositório contém uma versão em Python do conceito original de envio de informações públicas de cliente para um webhook do Discord.

## Objetivo

A finalidade deste material é exclusivamente educacional e de demonstração de coleta de metadados de rede e ambiente, como:

- IP público
- Geolocalização
- Sistema operacional
- Navegador
- Idioma
- Resolução do terminal

## Aviso legal

Este projeto é uma prova de conceito (PoC) criada apenas para fins educacionais e de pesquisa em segurança da informação.

O uso indevido, sem consentimento, para rastrear usuários, invadir privacidade ou violar leis de proteção de dados é proibido e não é apoiado pelo autor.

## Instalação

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
.venv\Scripts\activate    # Windows
pip install -r requirements.txt
```

## Execução

```bash
python ip_logger.py --once
```

Para execução contínua:

```bash
python ip_logger.py --interval 30
```

## Observação importante

Esse script não coleta dados de uma página web em tempo real como no navegador. Ele reproduz a lógica em Python para fins de estudo e demonstração.

## Segurança e uso responsável

- Substitua a URL padrão do webhook antes de usar
- Não execute em ambientes públicos sem autorização
- Respeite leis locais de privacidade e proteção de dados, como LGPD e GDPR
- Use apenas para fins educacionais e de pesquisa em laboratório
