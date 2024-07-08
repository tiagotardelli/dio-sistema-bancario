from datetime import datetime
from pathlib import Path

LOG_FILE = Path(__file__).resolve().parent / "log.txt"
CSV_FILE = Path(__file__).resolve().parent / "usuario.csv"

try:
    data_hora = datetime.now(datetime.UTC).strftime('%d-%m-%Y %H:%M:%S')
    with LOG_FILE.open('a', encoding='utf-8') as arquivo:
        arquivo.write(f"[{data_hora}] Sistema Iniciado\n")
except IOError as exc: 
    print("Erro ao abrir o arquivo {exc}")

try:
    with CSV_FILE.open('a', newline='', encoding="utf-8") as arquivo:
        pass
except IOError as exc:
    print(f"Erro ao criar o arquivo: {exc}")
