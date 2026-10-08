# StockMaster

Sistema de controle de estoque feito para a **Monticoifas LTDA**, uma empresa real que controlava o estoque em planilhas. Projeto acadêmico da disciplina de Prática Profissional do curso de Engenharia de Software da USF.

<!-- Prints: adicione as imagens em docs/screenshots/ e apague este comentário
![Dashboard](docs/screenshots/dashboard.png)
![Produtos](docs/screenshots/produtos.png)
![Relatórios](docs/screenshots/relatorios.png)
-->

## Funcionalidades

- **Autenticação:** login com senha criptografada e perfis de usuário.
- **Dashboard:** visão geral do estoque com alertas de itens abaixo do mínimo.
- **Produtos:** cadastro, edição e exclusão.
- **Movimentações:** registro de entradas, saídas e ajustes.
- **Fornecedores:** cadastro de fornecedores vinculados aos produtos.
- **Pedidos de compra:** emissão de pedidos e confirmação de recebimento.
- **Relatórios:** posição do estoque, itens críticos e histórico com filtro por data.

## Stack

| Tecnologia | Uso |
| --- | --- |
| Python | Linguagem principal |
| Flask | Framework web, dividido em Blueprints por módulo |
| Flask-Login | Autenticação e sessão |
| SQLite | Banco em arquivo local, sem servidor |
| Bootstrap 5 | Interface |
| Werkzeug | Criptografia de senhas |
| PyInstaller | Executável para Windows |

## Como rodar

### Executável para Windows

Baixe o [`StockMaster.exe`](https://github.com/Feduzo/PP-Projeto-de-Software/raw/main/StockMaster.exe), execute e acesse http://localhost:5000.

### Pelo código

Requisitos: Python 3.10+.

```bash
git clone https://github.com/Feduzo/PP-Projeto-de-Software.git
cd PP-Projeto-de-Software
pip install -r requirements.txt
python app.py
```

Acesse http://localhost:5000. O banco é criado automaticamente na primeira execução.

Para gerar o executável, rode `build.bat` (precisa de `pip install pyinstaller`).

**Login de demonstração** (criado localmente na primeira execução):

| Campo | Valor |
| --- | --- |
| Email | admin@stockmaster.com |
| Senha | admin123 |

## Estrutura do projeto

```text
├── app.py              # Inicia o Flask, o login e o dashboard
├── database.py         # Conexão e criação das tabelas
├── requirements.txt
├── routes/             # Um Blueprint por módulo
│   ├── auth.py         # Login e logout
│   ├── produtos.py     # CRUD de produtos
│   ├── movimentacoes.py  # Entradas, saídas e ajustes
│   ├── fornecedores.py # CRUD de fornecedores
│   ├── compras.py      # Pedidos de compra
│   └── relatorios.py   # Relatórios e filtros
└── templates/          # Telas HTML (Jinja2 + Bootstrap)
```

## Banco de dados

| Tabela | Descrição |
| --- | --- |
| `usuarios` | Usuários do sistema e perfil de acesso |
| `produtos` | Produtos com estoque atual e mínimo |
| `fornecedores` | Fornecedores vinculados aos produtos |
| `movimentacoes` | Histórico de entradas, saídas e ajustes |
| `compras` | Pedidos de compra e status de recebimento |

## Minha parte

Desenvolvi a maior parte do sistema (cerca de 90%): defini a estrutura, escolhi a stack do backend, implementei os módulos e testei o sistema.

## Equipe

Mayara de Oliveira, Matheus do Prado Fais, Jefferson Costa da Silva, Lucas Barboza Leandro, Poliana Araujo Oliveira, Ane Yumie Matsumoto Rolim e Felipe de Sousa Duzo.

## Licença

[MIT](LICENSE)
