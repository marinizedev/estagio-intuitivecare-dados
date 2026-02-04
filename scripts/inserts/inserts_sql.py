import pandas as pd
from sqlalchemy import create_engine

engine = create_engine(
    "mysql+pymysql://root:85731705VVAmv%25@localhost:3306/ans_despesas",
    echo=False,
    future=True
)

csv_enriquecido = r"C:\Users\Marinize\Desktop\estagio-intuitivecare-dados\data\processed\04_base_enriquecida_2025.csv"

df = pd.read_csv(csv_enriquecido, sep=";", encoding="utf-8-sig")

# Substituir NaN por None
df = df.where(pd.notnull(df), None)

# Para operadoras finais: seleciona apenas as colunas relevantes
df_operadoras = df[[
    "REGISTRO_OPERADORA", "CNPJ", "Razao_Social", "Modalidade", "UF"
]].drop_duplicates(subset=["REGISTRO_OPERADORA"])

df_operadoras.columns = ["registro_ans", "cnpj", "razao_social", "modalidade", "uf"]

# Garantir tipos corretos
df_operadoras["registro_ans"] = df_operadoras["registro_ans"].astype(int)

# Inserção em chunks menores
df_operadoras.to_sql(
    "operadoras",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000
)
