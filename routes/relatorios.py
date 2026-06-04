from flask import Blueprint, render_template, request
from flask_login import login_required
from database import get_connection
from datetime import datetime

relatorios_bp = Blueprint("relatorios", __name__, url_prefix="/relatorios")

@relatorios_bp.route("/")
@login_required
def index():
    conn = get_connection()

    # Filtros de data opcionais
    data_ini = request.args.get("data_ini", "")
    data_fim = request.args.get("data_fim", "")

    # Estoque atual completo
    produtos = conn.execute("""
        SELECT p.*, f.nome AS fornecedor
        FROM produtos p
        LEFT JOIN fornecedores f ON p.fornecedor_id = f.id
        ORDER BY p.nome
    """).fetchall()

    # Itens críticos
    criticos = conn.execute("""
        SELECT * FROM produtos WHERE quantidade <= estoque_minimo ORDER BY nome
    """).fetchall()

    # Movimentações com filtro de data
    query = """
        SELECT m.*, p.nome AS produto, u.nome AS usuario
        FROM movimentacoes m
        JOIN produtos p ON m.produto_id = p.id
        JOIN usuarios u ON m.usuario_id = u.id
    """
    params = []
    if data_ini and data_fim:
        query += " WHERE m.data BETWEEN ? AND ?"
        params = [data_ini, data_fim + " 23:59"]

    query += " ORDER BY m.id DESC LIMIT 100"
    movimentacoes = conn.execute(query, params).fetchall()

    # Totais
    total_entrada = conn.execute(
        "SELECT COALESCE(SUM(quantidade),0) FROM movimentacoes WHERE tipo='entrada'"
    ).fetchone()[0]
    total_saida = conn.execute(
        "SELECT COALESCE(SUM(quantidade),0) FROM movimentacoes WHERE tipo='saida'"
    ).fetchone()[0]

    conn.close()

    return render_template("relatorios/index.html",
        produtos=produtos,
        criticos=criticos,
        movimentacoes=movimentacoes,
        total_entrada=total_entrada,
        total_saida=total_saida,
        data_ini=data_ini,
        data_fim=data_fim,
        gerado_em=datetime.now().strftime("%d/%m/%Y %H:%M")
    )
