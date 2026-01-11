## Monitor de Lives da Twitch

Este script monitora streamers da Twitch e abre automaticamente a live
quando o streamer entra ao vivo.

### Requisitos
- Python 3.9+
- requests

### Configuração
Defina as variáveis de ambiente:

Windows:
setx TWITCH_CLIENT_ID "SEU_CLIENT_ID"
setx TWITCH_CLIENT_SECRET "SEU_CLIENT_SECRET"

Depois reinicie o terminal.

### Execução
python main.py
