import pandas as pd
from pathlib import Path

# Definição dos caminhos do projeto
BASE_DIR = Path(__file__).resolve(). parents[2]
DATA_RAW = BASE_DIR / "data" / "raw"
DATA_PROCESSED = BASE_DIR / "data" / "processed"

DATA_PROCESSED.mkdir(parents=True, exist_ok=True)

# Leitura dos arquivos trimestrais
dataframes = []

for csv_file in DATA_RAW.glob("*.csv"):
    df = pd.read_csv(csv_file, sep=";", encoding="latin1")
    dataframes.append(df)

if not dataframes:
    raise ValueError("Nenhum arquivo CSV encontrado em data/raw")

# Verificação de consistência estrutural
colunas_referencia = dataframes[0].columns

for i, df in enumerate(dataframes, start=1):
    if not df.columns.equals(colunas_referencia):
        raise ValueError(f"Estrutura diferente encontrada no arquivo {i}")
    
    # Consolidação dos dados
    base_df = pd.concat(dataframes, ignore_index=True)

    # Padronização dos dados
    colunas_dominio = [
        "CNPJ",
        "RazaoSocial",
        "Trimestre",
        "Ano",
        "ValorDespesas"
    ]

    for coluna in colunas_dominio:
        if coluna not in base_df.columns:
            base_df[coluna] = pd.NA

# Exportação do CSV consolidado
output_file = DATA_PROCESSED / "02_base_consolidada_2025.csv"

base_df.to_csv(
    output_file, 
    index=False, 
    sep=";", 
    encoding="latin1"
    )

print("Arquivo consolidado gerado com sucesso:")
print(output_file)
print(f"Total de registros: {len(base_df)}")