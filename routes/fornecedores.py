from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required
from database import get_connection

fornecedores_bp = Blueprint("fornecedores", __name__, url_prefix="/fornecedores")

@fornecedores_bp.route("/")
@login_required
def listar():
    conn = get_connection()
    fornecedores = conn.execute("SELECT * FROM fornecedores ORDER BY nome").fetchall()
    conn.close()
    return render_template("fornecedores/listar.html", fornecedores=fornecedores)

@fornecedores_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    if request.method == "POST":
        nome    = request.form["nome"]
        contato = request.form.get("contato", "")
        cnpj    = request.form.get("cnpj", "") or None

        try:
            conn = get_connection()
            conn.execute(
                "INSERT INTO fornecedores (nome, contato, cnpj) VALUES (?, ?, ?)",
                (nome, contato, cnpj)
            )
            conn.commit()
            conn.close()
            flash("Fornecedor cadastrado com sucesso!", "success")
            return redirect(url_for("fornecedores.listar"))
        except Exception:
            flash("Erro: CNPJ já cadastrado.", "danger")

    return render_template("fornecedores/form.html", fornecedor=None)

@fornecedores_bp.route("/editar/<int:id>", methods=["GET", "POST"])
@login_required
def editar(id):
    conn = get_connection()

    if request.method == "POST":
        nome    = request.form["nome"]
        contato = request.form.get("contato", "")
        cnpj    = request.form.get("cnpj", "") or None

        conn.execute(
            "UPDATE fornecedores SET nome=?, contato=?, cnpj=? WHERE id=?",
            (nome, contato, cnpj, id)
        )
        conn.commit()
        conn.close()
        flash("Fornecedor atualizado!", "success")
        return redirect(url_for("fornecedores.listar"))

    fornecedor = conn.execute("SELECT * FROM fornecedores WHERE id=?", (id,)).fetchone()
    conn.close()
    return render_template("fornecedores/form.html", fornecedor=fornecedor)

@fornecedores_bp.route("/excluir/<int:id>")
@login_required
def excluir(id):
    try:
        conn = get_connection()
        conn.execute("DELETE FROM fornecedores WHERE id=?", (id,))
        conn.commit()
        conn.close()
        flash("Fornecedor excluído.", "warning")
    except Exception:
        flash("Não é possível excluir: fornecedor vinculado a produtos.", "danger")
    return redirect(url_for("fornecedores.listar"))
