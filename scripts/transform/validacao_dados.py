import pandas as pd
from pathlib import Path
import re

# Configuração de caminhos
BASE_DIR = Path(__file__).resolve().parents[2]
INPUT_DIR = BASE_DIR / "data" / "processed"
OUTPUT_DIR = BASE_DIR / "data" / "processed"

input_file = INPUT_DIR / "02_base_consolidada_2025.csv"
output_file = OUTPUT_DIR / "03_base_validada_2025.csv"

# Funções auxiliares
def validar_cnpj(cnpj: str) -> bool:
    if not isinstance(cnpj, str):
        return False
    
    cnpj = re.sub(r"\D", "", cnpj)

    if len(cnpj) != 14:
        return False
    
    if cnpj == cnpj[0] * 14:
        return False
    
    def calcular_digito(cnpj, pesos):
        soma = sum(int(d) * p for d, p in zip(cnpj, pesos))
        resto = soma % 11
        return "0" if resto < 2 else str(11 - resto)
    pesos_1 = [5, 4, 3, 2, 9, 8, 7, 6, 5, 4, 3, 2]
    pesos_2 = [6] + pesos_1

    digito_1 = calcular_digito(cnpj[: 12], pesos_1)
    digito_2 = calcular_digito(cnpj[: 12] + digito_1, pesos_2)

    return cnpj[-2:] == digito_1 + digito_2

# Leitura dos dados
df = pd.read_csv(input_file, sep=";", encoding="latin1")

# Validações
# CNPJ
df["cnpj_valido"] = df["CNPJ"].apply(validar_cnpj)

# Razão Social
df["razao_social_valida"] = (
    df["RazaoSocial"]
    .fillna("")
    .str.strip()
    .ne("")
)

# Valor de Despesas
df["valor_despesas_valido"] = df["ValorDespesas"].apply(lambda x: isinstance(x, (int, float)) and x > 0)

# Escrita do arquivo validado
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
df.to_csv(output_file, index=False, sep=";", encoding="latin1")

print("Validação concluída com sucesso.")
print(f"Arquivo gerado: {output_file}")