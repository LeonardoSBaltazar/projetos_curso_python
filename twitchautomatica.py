import os
import requests
import time
import subprocess

# =========================================================
# CONFIGURAÇÃO DO USUÁRIO
# =========================================================
# O USUÁRIO DEVE DEFINIR AS VARIÁVEIS DE AMBIENTE NO SISTEMA:
#
# Windows (PowerShell):
#   setx TWITCH_CLIENT_ID "SEU_CLIENT_ID_AQUI"
#   setx TWITCH_CLIENT_SECRET "SEU_CLIENT_SECRET_AQUI"
#
# Linux / macOS:
#   export TWITCH_CLIENT_ID="SEU_CLIENT_ID_AQUI"
#   export TWITCH_CLIENT_SECRET="SEU_CLIENT_SECRET_AQUI"
#
# Depois de definir, FECHAR e ABRIR o terminal novamente.
# =========================================================

CLIENT_ID = os.getenv("TWITCH_CLIENT_ID")
CLIENT_SECRET = os.getenv("TWITCH_CLIENT_SECRET")

if not CLIENT_ID or not CLIENT_SECRET:
    raise RuntimeError(
        "TWITCH_CLIENT_ID e TWITCH_CLIENT_SECRET não estão configurados "
        "como variáveis de ambiente."
    )

# Lista de streamers que o usuário deseja monitorar
STREAMERS = [
    "guerreirotetra"  # substitua ou adicione outros nomes
]

# Intervalo de verificação em segundos
CHECK_INTERVAL = 60

# Caminho do navegador (ajuste se necessário)
EDGE_PATH = r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"

# Controle interno para não abrir várias abas do mesmo streamer
ja_aberto = set()


def obter_token():
    """
    Obtém um token de acesso OAuth da Twitch usando Client Credentials.
    """
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }

    response = requests.post(url, params=params)
    response.raise_for_status()
    return response.json()["access_token"]


ACCESS_TOKEN = obter_token()

headers = {
    "Client-ID": CLIENT_ID,
    "Authorization": f"Bearer {ACCESS_TOKEN}"
}


def esta_ao_vivo(streamer):
    """
    Verifica se o streamer está ao vivo.
    """
    global ACCESS_TOKEN

    url = f"https://api.twitch.tv/helix/streams?user_login={streamer}"
    response = requests.get(url, headers=headers)

    # Token expirado → gera outro automaticamente
    if response.status_code == 401:
        ACCESS_TOKEN = obter_token()
        headers["Authorization"] = f"Bearer {ACCESS_TOKEN}"
        response = requests.get(url, headers=headers)

    if response.status_code != 200:
        return False

    data = response.json()
    return len(data.get("data", [])) > 0


# =========================================================
# LOOP PRINCIPAL
# =========================================================
while True:
    for streamer in STREAMERS:
        if esta_ao_vivo(streamer):
            if streamer not in ja_aberto:
                subprocess.Popen([
                    EDGE_PATH,
                    "--new-tab",
                    "--mute-audio",
                    f"https://www.twitch.tv/{streamer}"
                ])
                ja_aberto.add(streamer)
        else:
            ja_aberto.discard(streamer)

    time.sleep(CHECK_INTERVAL)
