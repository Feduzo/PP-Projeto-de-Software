from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import get_connection
from datetime import datetime

mov_bp = Blueprint("movimentacoes", __name__, url_prefix="/movimentacoes")

@mov_bp.route("/")
@login_required
def listar():
    conn = get_connection()
    movs = conn.execute("""
        SELECT m.*, p.nome as produto, u.nome as usuario
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
        ORDER BY m.id DESC
    """).fetchall()
    conn.close()
    return render_template("movimentacoes/listar.html", movimentacoes=movs)

@mov_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    conn = get_connection()

    if request.method == "POST":
        produto_id = int(request.form["produto_id"])
        tipo       = request.form["tipo"]           # 'entrada' ou 'saida'
        quantidade = int(request.form["quantidade"])
        data       = datetime.now().strftime("%Y-%m-%d %H:%M")

        produto = conn.execute("SELECT * FROM produtos WHERE id = ?", (produto_id,)).fetchone()

        # Valida saída: não pode tirar mais do que tem
        if tipo == "saida" and quantidade > produto["quantidade"]:
            flash(f"Estoque insuficiente! Disponível: {produto['quantidade']} unidades.", "danger")
            produtos = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
            conn.close()
            return render_template("movimentacoes/form.html", produtos=produtos)

        # Registra a movimentação
        conn.execute("""
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, usuario_id)
            VALUES (?, ?, ?, ?, ?)
        """, (produto_id, tipo, quantidade, data, current_user.id))

        # Atualiza o estoque do produto
        if tipo == "entrada":
            conn.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id = ?", (quantidade, produto_id))
        else:
            conn.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id = ?", (quantidade, produto_id))

        conn.commit()
        conn.close()

        flash("Movimentação registrada!", "success")
        return redirect(url_for("movimentacoes.listar"))

    produtos = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    conn.close()
    return render_template("movimentacoes/form.html", produtos=produtos)
