import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR =BASE_DIR / "data" / "processed"

input_file = INPUT_DIR / "04_base_enriquecida_2025.csv"
output_file = OUTPUT_DIR / "despesas_agregadas.csv"

# Leitura do CSV enriquecido
df = pd.read_csv(input_file, sep=";", encoding="latin1")

# Garantir que VallorDespesas seja numérico
df["ValorDespesas"] = pd.to_numeric(df["ValorDespesas"], errors="coerce").fillna(0)

# Agregação por RazaoSocial e UF
df_agg = df.groupby(["RazaoSocial", "UF"]).agg (

    total_despesas=pd.NamedAgg(column="ValorDespesas", aggfunc="sum"),

    media_trimestral=pd.NamedAgg(column="ValorDespesas", aggfunc="mean"),

    desvio_padrao=pd.NamedAgg(column="ValorDespesas", aggfunc="std")
).reset_index()

# Ordenação do maior para o menor total de despesas
df_agg = df_agg.sort_values(by="total_despesas", ascending=False)

# Salvando o CSV final
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df_agg.to_csv(output_file, index=False, sep=";", encoding="latin1")

print("Agregação concluída com sucesso!")
print(f"Arquivo CSV gerado: {output_file}")