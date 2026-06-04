from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from database import get_connection
from datetime import datetime

compras_bp = Blueprint("compras", __name__, url_prefix="/compras")

@compras_bp.route("/")
@login_required
def listar():
    conn = get_connection()
    compras = conn.execute("""
        SELECT c.*, p.nome AS produto, f.nome AS fornecedor
        FROM compras c
        JOIN produtos p ON c.produto_id = p.id
        JOIN fornecedores f ON c.fornecedor_id = f.id
        ORDER BY c.id DESC
    """).fetchall()
    conn.close()
    return render_template("compras/listar.html", compras=compras)

@compras_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    conn = get_connection()

    if request.method == "POST":
        produto_id    = int(request.form["produto_id"])
        fornecedor_id = int(request.form["fornecedor_id"])
        quantidade    = float(request.form["quantidade"])
        data_pedido   = datetime.now().strftime("%Y-%m-%d %H:%M")

        conn.execute("""
            INSERT INTO compras (produto_id, fornecedor_id, quantidade, data_pedido, status)
            VALUES (?, ?, ?, ?, 'pendente')
        """, (produto_id, fornecedor_id, quantidade, data_pedido))
        conn.commit()
        conn.close()

        flash("Pedido de compra registrado!", "success")
        return redirect(url_for("compras.listar"))

    produtos     = conn.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
    fornecedores = conn.execute("SELECT * FROM fornecedores ORDER BY nome").fetchall()
    conn.close()
    return render_template("compras/form.html", produtos=produtos, fornecedores=fornecedores)

@compras_bp.route("/receber/<int:id>")
@login_required
def receber(id):
    conn = get_connection()
    compra = conn.execute(
        "SELECT * FROM compras WHERE id=? AND status='pendente'", (id,)
    ).fetchone()

    if not compra:
        flash("Pedido não encontrado ou já processado.", "danger")
        conn.close()
        return redirect(url_for("compras.listar"))

    # Registra entrada no estoque
    data = datetime.now().strftime("%Y-%m-%d %H:%M")
    conn.execute("""
        INSERT INTO movimentacoes (produto_id, tipo, quantidade, data, usuario_id, observacao)
        VALUES (?, 'entrada', ?, ?, ?, ?)
    """, (compra["produto_id"], compra["quantidade"], data, current_user.id,
          f"Recebimento do pedido #{id}"))

    conn.execute("UPDATE produtos SET quantidade = quantidade + ? WHERE id=?",
                 (compra["quantidade"], compra["produto_id"]))
    conn.execute("UPDATE compras SET status='recebido' WHERE id=?", (id,))
    conn.commit()
    conn.close()

    flash("Recebimento confirmado! Estoque atualizado.", "success")
    return redirect(url_for("compras.listar"))

@compras_bp.route("/cancelar/<int:id>")
@login_required
def cancelar(id):
    conn = get_connection()
    conn.execute(
        "UPDATE compras SET status='cancelado' WHERE id=? AND status='pendente'", (id,)
    )
    conn.commit()
    conn.close()
    flash("Pedido cancelado.", "warning")
    return redirect(url_for("compras.listar"))
