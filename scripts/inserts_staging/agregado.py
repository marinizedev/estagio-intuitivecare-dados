import pandas as pd
from sqlalchemy import create_engine, text

# Conexão com o banco (PyMySQL)
engine = create_engine(
"mysql+pymysql://root:85731705VVAmv%25@localhost:3306/ans_despesas",
echo=False,
future=True
)

# Caminho do CSV
csv_path = r"C:\Users\Marinize\Desktop\estagio-intuitivecare-dados\data\processed\despesas_agregadas.csv"
print("Iniciando leitura do CSV...")

df = pd.read_csv(
    csv_path,
    sep=";", 
    encoding="latin1")

print(f"CSV lido com sucesso! Total de linhas: {len(df)}")

df.columns = [
    "Razao_Social",
    "UF",
    "total_despesas",
    "media_trimestral",
    "desvio_padrao"
]

# Inserção no banco (em chunks)
print("Iniciando inserção no banco...")

with engine.begin() as conn:
    df.to_sql(
        name="stg_despesas_agregadas",
        con=conn,
        if_exists="append",
        index=False,
        chunksize=5000,
        method="multi"
)
    
with engine.connect() as conn:
    result = conn.execute(text("SELECT COUNT(*) FROM stg_despesas_agregadas"))
    print(result.fetchone())


print("Carga concluída com sucesso!")
