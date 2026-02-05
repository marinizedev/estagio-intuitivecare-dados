import pandas as pd
from pathlib import Path

# -------------------------------
# Caminhos
# -------------------------------
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_PROCESSED = BASE_DIR / "data" / "processed"

csv_enriquecido = DATA_PROCESSED / "04_base_enriquecida_2025.csv"
csv_agregado = DATA_PROCESSED / "despesas_agregadas.csv"

# -------------------------------
# Leitura do CSV enriquecido
# -------------------------------
df = pd.read_csv(csv_enriquecido, sep=";", encoding="latin1")

# -------------------------------
# Seleção das colunas necessárias
# -------------------------------
df = df[[
    "Razao_Social",
    "UF",
    "Ano",
    "Trimestre",
    "ValorDespesas"
]]

# -------------------------------
# Limpeza e tipos
# -------------------------------
df["ValorDespesas"] = pd.to_numeric(df["ValorDespesas"], errors="coerce").fillna(0)

df["Razao_Social"] = df["Razao_Social"].astype(str).str.strip()
df["UF"] = df["UF"].astype(str).str.strip()

# Remover registros sem razão social ou UF
#df = df[(df["RazaoSocial"] != "") & (df["UF"] != "")]
print(df.head())
print("Linhas antes da agregação:", len(df))
# -------------------------------
# Agregação
# -------------------------------
df_agregado = (
    df.groupby(["Razao_Social", "UF"])
      .agg(
          total_despesas=("ValorDespesas", "sum"),
          media_trimestral=("ValorDespesas", "mean"),
          desvio_padrao=("ValorDespesas", "std")
      )
      .reset_index()
)

# Substituir NaN do desvio padrão (casos com apenas 1 trimestre)
df_agregado["desvio_padrao"] = df_agregado["desvio_padrao"].fillna(0)

# -------------------------------
# Exportação
# -------------------------------
df_agregado.to_csv(csv_agregado, sep=";", index=False, encoding="latin1")

print("despesas_agregadas.csv gerado com sucesso!")
print(df_agregado.head())
