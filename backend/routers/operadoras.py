from fastapi import APIRouter, Query
from sqlalchemy import text
from backend.database import engine

router = APIRouter(prefix="/operadoras", tags=["Operadoras"])


@router.get("")
def listar_operadoras(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1)
):
    offset = (page - 1) * limit

    with engine.connect() as conn:
        total = conn.execute(
            text("SELECT COUNT(*) FROM operadoras")
        ).scalar()

        result = conn.execute(text("""
            SELECT
                reg_ans,
                cnpj,
                razao_social,
                modalidade,
                uf
            FROM operadoras
            ORDER BY razao_social
            LIMIT :limit OFFSET :offset
        """), {"limit": limit, "offset": offset})

        data = [dict(row) for row in result.mappings().all()]

    return {
        "data": data,
        "page": page,
        "limit": limit,
        "total": total
    }


@router.get("/{reg_ans}")
def detalhe_operadora(reg_ans: str):
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT
                reg_ans,
                cnpj,
                razao_social,
                modalidade,
                uf
            FROM operadoras
            WHERE reg_ans = :reg_ans
        """), {"reg_ans": reg_ans}).fetchone()

    if not result:
        return {"detail": "Operadora não encontrada"}

    return dict(result)
