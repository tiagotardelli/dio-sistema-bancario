from pathlib import Path
import os
import yaml

CONFIG = ""

try:
    arquivo_yaml = Path(__file__).resolve().parent / "config.yaml"
    with arquivo_yaml.open('r', encoding='utf-8') as arquivo:
        CONFIG = yaml.safe_load(arquivo)
except IOError as exc:
    print(f"Erro ao ler o arquivo: {exc}")
