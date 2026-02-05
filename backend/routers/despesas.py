from fastapi import APIRouter
from sqlalchemy import text
from backend.database import engine

router = APIRouter(tags=["Despesas"])


@router.get("/operadoras/{reg_ans}/despesas")
def historico_despesas(reg_ans: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                dc.ano,
                dc.trimestre,
                dc.valor_despesas
            FROM despesas_consolidadas dc
            JOIN operadoras o
                ON o.id_operadora = dc.id_operadora
            WHERE o.reg_ans = :reg_ans
            ORDER BY dc.ano, dc.trimestre
        """), {"reg_ans": reg_ans})

        data = [dict(row) for row in result.mappings().all()]

    return {
        "reg_ans": reg_ans,
        "despesas": data
    }
