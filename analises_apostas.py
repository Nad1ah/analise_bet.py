import os
from dotenv import load_dotenv
import requests
import pandas as pd

# Carregar variáveis de ambiente
load_dotenv(dotenv_path=".env")
API_KEY = os.getenv("API_KEY")

if API_KEY is None:
    raise ValueError("A chave da API não foi encontrada. Verifique o arquivo .env.")

COMPETICAO = "BSA"
url = f"http://api.football-data.org/v4/competitions/{COMPETICAO}/matches"
headers = {"X-Auth-Token": API_KEY}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    dados = response.json()
except requests.exceptions.RequestException as e:
    print(f"Erro na requisição: {e}")
    exit()

jogos_sugeridos = []

for jogo in dados.get("matches", []):  # Usar get para evitar KeyError
    if jogo["status"] != "FINISHED":
        time_casa = jogo["homeTeam"]["shortName"]
        time_fora = jogo["awayTeam"]["shortName"]

        # Aqui você pode calcular ou definir as médias de gols
        media_gols_casa = 1.8  # Substitua por dados reais
        media_gols_sofridos_fora = 1.2  # Substitua por dados reais

        # Verifique se as médias são válidas
        if media_gols_casa > 0 and media_gols_sofridos_fora > 0:
            if (media_gols_casa + media_gols_sofridos_fora) > 2.5:
                jogos_sugeridos.append(
                    {
                        "Jogo": f"{time_casa} vs {time_fora}",
                        "Over 2.5 Gols": "✅",
                        "Data": jogo["utcDate"],  # Adiciona a data do jogo
                    }
                )
            else:
                jogos_sugeridos.append(
                    {
                        "Jogo": f"{time_casa} vs {time_fora}",
                        "Over 2.5 Gols": "❌",
                        "Data": jogo["utcDate"],  # Adiciona a data do jogo
                    }
                )

# Exibir resultados em uma tabela
if jogos_sugeridos:
    df = pd.DataFrame(jogos_sugeridos)
    print("\nJogos sugeridos para Over 2.5 gols:")
    print(df.to_string(index=False))
else:
    print("Nenhum jogo encontrado com os critérios atuais.")
