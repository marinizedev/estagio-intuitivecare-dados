from pathlib import Path
import re

input_file = Path("data/processed/04_base_enriquecida_2025.csv")
output_file = Path("data/processed/04_base_enriquecida_2025_mysql.csv")

with open(input_file, "r", encoding="latin1", errors="ignore") as f:
    content = f.read()

# Remove caracteres de controle (ASCII 0-31 e 127)
content = re.sub(r"[\x00-\x1F\x7F]", "", content)

with open(output_file, "w", encoding="utf-8", newline="") as f:
    f.write(content)

print("Arquivo limpo para importação no MySQL!")