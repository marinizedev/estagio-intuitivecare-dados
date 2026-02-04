import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco (PyMySQL)
engine = create_engine(
"mysql+pymysql://root:85731705VVAmv%25@localhost:3306/ans_despesas",
echo=False,
future=True
)

# Caminho do CSV
csv_path = r"C:\Users\Marinize\Desktop\estagio-intuitivecare-dados\data\processed\04_base_enriquecida_2025.csv"
print("Iniciando leitura do CSV...")

df = pd.read_csv(
    csv_path,
    sep=";", 
    encoding="latin1")

print(f"CSV lido com sucesso! Total de linhas: {len(df)}")

df.columns = [
    "data",
    "reg_ans",
    "cd_conta_contabil",
    "descricao",
    "vl_saldo_inicial",
    "vl_saldo_final",
    "cnpj",
    "razaoSocial",
    "trimestre",
    "ano",
    "valorDespesas",
    "registro_operadora",
    "razao_social",
    "modalidade",
    "uf"
]

# Inserção no banco (em chunks)
print("Iniciando inserção no banco...")

with engine.begin() as conn:
    df.to_sql(
        name="str_base_enriquecida",
        con=conn,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
)
    
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM str_base_enriquecida"))
    print(result.fetchone())


print("Carga concluída com sucesso!")
