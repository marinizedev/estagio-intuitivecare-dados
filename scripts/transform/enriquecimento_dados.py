import pandas as pd
from pathlib import Path
import re

# Configuração de caminhos
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "data" / "processed"
RAW_DIR = BASE_DIR / "data" / "raw"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

# Arquivos
input_file = INPUT_DIR / "03_base_validada_2025.csv"
ans_file = RAW_DIR / "Relatorio_cadop.csv"
output_file = OUTPUT_DIR / "04_base_enriquecida_2025.csv"

# Leitura dos dados
df = pd.read_csv(input_file, sep=";", encoding="latin1")
df_ans = pd.read_csv(ans_file, sep=";", encoding="latin1")

# Limpeza e padronização dos CNPJs
# CSV consolidado
df["CNPJ_limpo"] = df["CNPJ"].apply(lambda x: re.sub(r"\D", "", str(x)) if pd.notnull(x) else "")

# CSV ANS - ajustar o nome da coluna do CNPJ conforme estiver no CSV
df_ans["CNPJ_limpo"] = df_ans["CNPJ"].apply(lambda x: re.sub(r"\D", "", str(x)) if pd.notnull(x) else "")

# Renomear colunas da ANS para o padrão desejado
df_ans.rename(columns={"REGISTRO_OPERADORA": "RegistroANS"}, inplace=True)

# Tratar duplicitas no cadastro ANS
df_ans = df_ans.drop_duplicates(subset="CNPJ_limpo", keep="first")

# Merge / Join para enriquecer dados
df_final = df.merge(df_ans[["CNPJ_limpo", 
    "RegistroANS", 
    "Modalidade", 
    "UF"]],
    on="CNPJ_limpo",    
    how="left"
)

# Tratar registros sem match
# Converte para string antes de preencher valores
df_final["RegistroANS"] = df_final["RegistroANS"].astype(str).replace("nan", "Não encontrado")
df_final["Modalidade"] = df_final["Modalidade"].astype(str).replace("nan", "Não encontrado")
df_final["UF"] = df_final["UF"].astype(str).replace("nan", "Não encontrado")

# Salvar CSV final
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df_final.to_csv(output_file, index=False, sep=";", encoding="latin1")

print("Enriquecimento concluído com sucesso!")
print(f"Arquivo gerado: {output_file}")