from fastapi import APIRouter
from sqlalchemy import text
from backend.database import engine

router = APIRouter(prefix="/estatisticas", tags=["Estatísticas"])


@router.get("")
def estatisticas_gerais():
    with engine.connect() as conn:
        totais = conn.execute(text("""
            SELECT
                SUM(valor_despesas) AS total,
                AVG(valor_despesas) AS media
            FROM despesas_consolidadas
        """)).fetchone()

        top5 = conn.execute(text("""
            SELECT
                o.razao_social,
                SUM(dc.valor_despesas) AS total_despesas
            FROM despesas_consolidadas dc
            JOIN operadoras o
                ON o.id_operadora = dc.id_operadora
            GROUP BY o.razao_social
            ORDER BY total_despesas DESC
            LIMIT 5
        """))

        top5_operadoras = [dict(row._mapping) for row in top5]

    return {
        "total_despesas": float(totais.total or 0),
        "media_despesas": float(totais.media or 0),
        "top_5_operadoras": top5_operadoras
    }
