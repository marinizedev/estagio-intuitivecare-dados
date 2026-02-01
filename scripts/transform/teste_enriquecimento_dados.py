import pandas as pd
from pathlib import Path

# Configuração de caminhos
BASE_DIR = Path(__file__).resolve().parents[2]

INPUT_DIR = BASE_DIR / "data" / "processed"
CADASTRO_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

input_file = INPUT_DIR / "03_base_validada_2025.csv"
cadastro_file = CADASTRO_DIR / "operadoras_ativas.csv"
output_file = OUTPUT_DIR / "04_base1_enriquecida_2025.csv"

# Leitura dos arquivos
df_despesas = pd.read_csv(input_file, sep=";", encoding="latin1")
df_cadastro = pd.read_csv(cadastro_file, sep=";", encoding="latin1")

# Padronização dos nomes das colunas conforme enunciado
df_cadastro = df_cadastro.rename(columns={"REGISTRO_OPERADORA": "RegistroANS"})

# Seleção das colunas relevantes do cadastro
df_cadastro = df_cadastro[
    ["CNPJ", "RegistroANS",
    "Modalidade", "UF"]
]

# Tratamento de duplicidades no cadastro
df_cadastro = df_cadastro.drop_duplicates(subset="CNPJ")

# Join dos dados
df_final = df_despesas.merge(
    df_cadastro,
    on="CNPJ",
    how="left"
)

# Escrita do arquivo final
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

df_final.to_csv(output_file,
    index=False,
    sep=";",
    encoding="latin1"
)

print("Enriquecimento concluído com sucesso!")
print(f"Aruquivo gerado: {output_file}")