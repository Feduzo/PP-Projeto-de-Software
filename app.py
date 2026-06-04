from flask import Flask, render_template, redirect, url_for
from flask_login import LoginManager, UserMixin, login_required, current_user
from database import criar_tabelas, get_connection

app = Flask(__name__)
app.secret_key = "stockmaster_chave_secreta_2024"

# ── Flask-Login setup ──────────────────────────────────────────────────────────
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "auth.login"
login_manager.login_message = "Faça login para acessar o sistema."

class User(UserMixin):
    def __init__(self, id, nome, email, perfil):
        self.id = id
        self.nome = nome
        self.email = email
        self.perfil = perfil

@login_manager.user_loader
def load_user(user_id):
    conn = get_connection()
    user = conn.execute("SELECT * FROM usuarios WHERE id = ?", (user_id,)).fetchone()
    conn.close()
    if user:
        return User(user["id"], user["nome"], user["email"], user["perfil"])
    return None

# ── Blueprints ─────────────────────────────────────────────────────────────────
from routes.auth import auth_bp
from routes.produtos import produtos_bp
from routes.movimentacoes import mov_bp

app.register_blueprint(auth_bp)
app.register_blueprint(produtos_bp)
app.register_blueprint(mov_bp)

# ── Dashboard ──────────────────────────────────────────────────────────────────
@app.route("/")
@login_required
def index():
    conn = get_connection()
    total_produtos = conn.execute("SELECT COUNT(*) FROM produtos").fetchone()[0]
    total_estoque  = conn.execute("SELECT SUM(quantidade) FROM produtos").fetchone()[0] or 0
    alertas = conn.execute("""
        SELECT nome, quantidade, estoque_minimo
        FROM produtos WHERE quantidade <= estoque_minimo
    """).fetchall()
    ultimas_mov = conn.execute("""
        SELECT m.tipo, m.quantidade, m.data, p.nome as produto, u.nome as usuario
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.id DESC LIMIT 10
    """).fetchall()
    conn.close()
    return render_template("dashboard.html",
        total_produtos=total_produtos,
        total_estoque=total_estoque,
        alertas=alertas,
        ultimas_mov=ultimas_mov
    )

if __name__ == "__main__":
    with app.app_context():
        criar_tabelas()
    app.run(debug=True)
