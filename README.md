# 📦 StockMaster

> Sistema de Controle de Estoque desenvolvido para a **Monticoifas LTDA** como projeto acadêmico da disciplina de Prática Profissional — Engenharia de Software.

---

## Sobre o Projeto

O StockMaster é um sistema web de gerenciamento de estoque que substitui o controle manual por planilhas, oferecendo uma interface centralizada para registro de produtos, movimentações, fornecedores e geração de relatórios.

---

## Funcionalidades

- **Autenticação** — Login seguro com senha criptografada
- **Dashboard** — Visão geral do estoque com alertas de itens críticos
- **Produtos** — Cadastro, edição e exclusão de produtos
- **Movimentações** — Registro de entradas, saídas e ajustes de estoque
- **Fornecedores** — Cadastro e gerenciamento de fornecedores
- **Pedidos de Compra** — Emissão e controle de pedidos com confirmação de recebimento
- **Relatórios** — Posição do estoque, itens críticos e histórico com filtro por data

---

## Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| Python | Linguagem principal |
| Flask | Framework web |
| Flask-Login | Autenticação e sessão |
| SQLite | Banco de dados local |
| Bootstrap 5 | Interface visual |
| Werkzeug | Criptografia de senhas |


---

## Como Executar

### Executável 

1. Certifique-se que o arquivo `StockMaster.exe` está na pasta do projeto
2. Dê dois cliques em `StockMaster.exe`
3. Abra o navegador e acesse:
```
http://localhost:5000
```

---

### OU Pelo terminal

**Pré-requisitos:** Python instalado

**1. Clone o repositório:**
```bash
git clone https://github.com/Feduzo/PP-Projeto-de-Software.git
cd PP-Projeto-de-Software
```

**2. Instale as dependências:**
```bash
pip install -r requirements.txt
```

**3. Execute o sistema:**
```bash
py app.py
```

**4. Acesse no navegador:**
```
http://localhost:5000
```

---

## Acesso Padrão

| Campo | Valor |
|---|---|
| Email | admin@stockmaster.com |
| Senha | admin123 |

---

## Estrutura do Projeto

```
stockmaster/
├── app.py                        # Arquivo principal — inicia o Flask
├── database.py                   # Conexão e criação do banco de dados
├── requirements.txt              # Dependências Python
├── StockMaster.exe               # Executável (gerado pelo PyInstaller)
│
├── routes/                       # Rotas separadas por módulo
│   ├── auth.py                   # Login e logout
│   ├── produtos.py               # CRUD de produtos
│   ├── movimentacoes.py          # Entradas, saídas e ajustes
│   ├── fornecedores.py           # CRUD de fornecedores
│   ├── compras.py                # Pedidos de compra
│   └── relatorios.py             # Relatórios e filtros
│
└── templates/                    # Telas HTML
    ├── base.html                 # Layout base com menu lateral
    ├── login.html                # Tela de login
    ├── dashboard.html            # Painel principal
    ├── produtos/                 # Telas de produtos
    ├── movimentacoes/            # Telas de movimentações
    ├── fornecedores/             # Telas de fornecedores
    ├── compras/                  # Telas de pedidos
    └── relatorios/               # Telas de relatórios
```

---

## Banco de Dados

O sistema usa **SQLite** — um banco de dados em arquivo local, sem necessidade de instalação de servidor.

**Tabelas:**

| Tabela | Descrição |
|---|---|
| `usuarios` | Usuários do sistema com perfil de acesso |
| `produtos` | Cadastro de produtos com estoque |
| `fornecedores` | Fornecedores vinculados aos produtos |
| `movimentacoes` | Histórico de entradas, saídas e ajustes |
| `compras` | Pedidos de compra e status de recebimento |

---

## Equipe

Mayara de Oliveira           RA: 202444484
Matheus do Prado Fais        RA: 202454284
Jefferson Costa da Silva     RA: 202416050
Lucas Barboza Leandro        RA: 202454106
Poliana Araujo Oliveira      RA: 202447398
Ane Yumie Matsumoto Rolim    RA: 202446892
Felipe de Sousa Duzo         RA: 202320905

---

## Licença

Este projeto é de uso acadêmico.
