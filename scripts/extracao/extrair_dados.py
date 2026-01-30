import pandas as pd
from pathlib import Path

# Diretórios base
BASE_DIR = Path(__file__).resolve().parents[2]
DATA_RAW = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

# Leitura dos arquivos
dataframes = []

for csv_file in DATA_RAW.glob("*.csv"):
    df = pd.read_csv(csv_file, sep=";", encoding="latin1")
    dataframes.append(df)

print(f"Quantidade de arquivos lidos: {len(dataframes)}")

# Validação de estrutura
for i, df in  enumerate(dataframes, 1):
    print(f"Trimestre {i}: shape = {df.shape}") 

colunas_ref = dataframes[0].columns
for i, df in enumerate(dataframes, 1):
    if not df.columns.equals(colunas_ref):
        raise ValueError(f"Estrutura difirente encontrada no arquivo {i}")

# Consolidação
base_df = pd.concat(dataframes, ignore_index=True)

# Escrita do arquivo final
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
output_file = OUTPUT_DIR / "base_2025_consolidada.csv"

base_df.to_csv(output_file, index=False, sep=";", encoding="latin1")