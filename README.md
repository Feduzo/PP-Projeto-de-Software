# StockMaster 📦

Sistema de controle de estoque — Monticoifas LTDA

## Como rodar

1. Instale as dependências:
```
pip install -r requirements.txt
```

2. Inicie o sistema:
```
python app.py
```

3. Acesse no navegador: http://localhost:5000

## Login padrão
- Email: admin@stockmaster.com
- Senha: admin123

## Estrutura do projeto
```
stockmaster/
├── app.py                  → Arquivo principal, inicia o Flask
├── database.py             → Conexão e criação do banco SQLite
├── requirements.txt        → Dependências Python
├── routes/
│   ├── auth.py             → Login e logout
│   ├── produtos.py         → CRUD de produtos
│   └── movimentacoes.py    → Entradas e saídas de estoque
└── templates/
    ├── base.html           → Layout base (sidebar, menu)
    ├── login.html          → Tela de login
    ├── dashboard.html      → Painel principal
    ├── produtos/           → Telas de produtos
    └── movimentacoes/      → Telas de movimentações
```

## Funcionalidades
- Login com autenticação segura
- Dashboard com resumo e alertas de estoque baixo
- Cadastro, edição e exclusão de produtos
- Registro de entradas e saídas com validação
- Histórico completo de movimentações
