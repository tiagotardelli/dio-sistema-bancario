from pathlib import Path
import os
import yaml

caminho = Path(__file__).resolve().parent
arquivo_yaml = caminho / "config.yaml"
config = ""
with arquivo_yaml.open('r', encoding='utf-8') as arquivo:
    config = yaml.safe_load(arquivo)