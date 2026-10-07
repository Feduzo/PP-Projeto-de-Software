# StockMaster

Inventory management system built for **Monticoifas LTDA**, a real company that controlled its stock with spreadsheets. Academic project for the Professional Practice course of the Software Engineering program at USF.

<!-- Screenshots: add the images to docs/screenshots/ and remove this comment
![Dashboard](docs/screenshots/dashboard.png)
![Products](docs/screenshots/products.png)
![Reports](docs/screenshots/reports.png)
-->

## Features

- **Authentication:** login with hashed passwords and user profiles.
- **Dashboard:** stock overview with alerts for items below the minimum level.
- **Products:** create, edit and delete products.
- **Stock movements:** record inbound, outbound and adjustment entries.
- **Suppliers:** manage suppliers linked to products.
- **Purchase orders:** issue orders and confirm receipt.
- **Reports:** current stock, critical items and history filtered by date.

## Tech stack

| Technology | Purpose |
| --- | --- |
| Python | Main language |
| Flask | Web framework, split into Blueprints per module |
| Flask-Login | Authentication and sessions |
| SQLite | Local file database, no server needed |
| Bootstrap 5 | User interface |
| Werkzeug | Password hashing |
| PyInstaller | Windows executable |

## Running it

### Windows executable

Download [`StockMaster.exe`](https://github.com/Feduzo/PP-Projeto-de-Software/raw/main/StockMaster.exe), run it and open http://localhost:5000.

### From source

Requirements: Python 3.10+.

```bash
git clone https://github.com/Feduzo/PP-Projeto-de-Software.git
cd PP-Projeto-de-Software
pip install -r requirements.txt
python app.py
```

Open http://localhost:5000. The database is created automatically on first run.

To build the executable yourself, run `build.bat` (requires `pip install pyinstaller`).

**Demo login** (created locally on first run):

| Field | Value |
| --- | --- |
| Email | admin@stockmaster.com |
| Password | admin123 |

## Project structure

```text
├── app.py              # Starts Flask, login manager and dashboard
├── database.py         # Connection and table creation
├── requirements.txt
├── routes/             # One Blueprint per module
│   ├── auth.py         # Login and logout
│   ├── produtos.py     # Products CRUD
│   ├── movimentacoes.py  # Inbound, outbound and adjustments
│   ├── fornecedores.py # Suppliers CRUD
│   ├── compras.py      # Purchase orders
│   └── relatorios.py   # Reports and filters
└── templates/          # HTML pages (Jinja2 + Bootstrap)
```

## Database

| Table | Description |
| --- | --- |
| `usuarios` | System users and their access profile |
| `produtos` | Products with current and minimum stock |
| `fornecedores` | Suppliers linked to products |
| `movimentacoes` | History of inbound, outbound and adjustments |
| `compras` | Purchase orders and receipt status |

## My role

I built most of the application (around 90%): I designed the structure, chose the backend stack, implemented the modules and tested the system.

## Team

Mayara de Oliveira, Matheus do Prado Fais, Jefferson Costa da Silva, Lucas Barboza Leandro, Poliana Araujo Oliveira, Ane Yumie Matsumoto Rolim and Felipe de Sousa Duzo.

## License

[MIT](LICENSE)
