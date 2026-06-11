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
        SELECT m.*, p.nome AS produto, u.nome AS usuario
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
        print("FORM DATA EDITAR:", dict(request.form))  # aqui dentro
        produto_id = int(float(request.form["produto_id"]))
        tipo       = request.form["tipo"]
        quantidade = int(float(request.form["quantidade"]))
        observacao = request.form.get("observacao", "")
        data       = datetime.now().strftime("%Y-%m-%d %H:%M")

        produto = conn.execute("SELECT * FROM produtos WHERE id=?", (produto_id,)).fetchone()

        if tipo == "saida" and quantidade > produto["quantidade"]:
            flash(f"Estoque insuficiente! Disponível: {produto['quantidade']}.", "danger")
            produtos = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
            conn.close()
            return render_template("movimentacoes/form.html", produtos=produtos)

        conn.execute("""
            INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, usuario_id, observacao)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (produto_id, tipo, quantidade, data, current_user.id, observacao))

        if tipo == "entrada":
            conn.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id=?", (quantidade, produto_id))
        elif tipo == "saida":
            conn.execute("UPDATE produtos SET quantidade = quantidade - ? WHERE id=?", (quantidade, produto_id))
        else:  # ajuste — sobrescreve o saldo direto
            conn.execute("UPDATE produtos SET quantidade = ? WHERE id=?", (quantidade, produto_id))

        conn.commit()
        conn.close()
        flash("Movimentação registrada!", "success")
        return redirect(url_for("movimentacoes.listar"))

    produtos = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    conn.close()
    return render_template("movimentacoes/form.html", produtos=produtos)
