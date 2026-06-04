from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from database import get_connection

produtos_bp = Blueprint("produtos", __name__, url_prefix="/produtos")

@produtos_bp.route("/")
@login_required
def listar():
    conn = get_connection()
    produtos = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    conn.close()
    return render_template("produtos/listar.html", produtos=produtos)

@produtos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        nome         = request.form["nome"]
        categoria    = request.form["categoria"]
        quantidade   = int(request.form["quantidade"])
        est_minimo   = int(request.form["estoque_minimo"])
        preco        = float(request.form["preco"])

        conn = get_connection()
        conn.execute("""
            INSERT INTO produtos (nome, categoria, quantidade, estoque_minimo, preco)
            VALUES (?, ?, ?, ?, ?)
        """, (nome, categoria, quantidade, est_minimo, preco))
        conn.commit()
        conn.close()

        flash("Produto cadastrado com sucesso!", "success")
        return redirect(url_for("produtos.listar"))

    return render_template("produtos/form.html", produto=None)

@produtos_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    conn = get_connection()

    if request.method == "POST":
        nome       = request.form["nome"]
        categoria  = request.form["categoria"]
        est_minimo = int(request.form["estoque_minimo"])
        preco      = float(request.form["preco"])

        conn.execute("""
            UPDATE produtos SET nome=?, categoria=?, estoque_minimo=?, preco=?
            WHERE id=?
        """, (nome, categoria, est_minimo, preco, id))
        conn.commit()
        conn.close()

        flash("Produto atualizado!", "success")
        return redirect(url_for("produtos.listar"))

    produto = conn.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()
    conn.close()
    return render_template("produtos/form.html", produto=produto)

@produtos_bp.route("/excluir/<int:id>")
@login_required
def excluir(id):
    conn = get_connection()
    conn.execute("DELETE FROM produtos WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    flash("Produto excluído.", "warning")
    return redirect(url_for("produtos.listar"))
