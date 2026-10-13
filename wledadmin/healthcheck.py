"""HEALTHCHECK do contêiner: o wledadmin está respondendo?

Roda dentro do contêiner (rede do host), então independe da porta configurada na seção
Rede. O run.py grava em PORT_FILE a porta a verificar: a do acesso direto ou, se ele estiver
desligado, a do painel do HA. Qualquer resposta HTTP conta como saudável, inclusive o 403
que a porta do painel dá para conexões que não vêm do proxy do HA: o que importa é o
servidor responder. Com o Watchdog ligado, o Supervisor reinicia o app quando o Docker o
marca como "unhealthy".
"""

import sys
import urllib.error
import urllib.request

PORT_FILE = "/tmp/wledadmin-health-port"


def main() -> int:
    try:
        with open(PORT_FILE, encoding="ascii") as f:
            port = int(f.read().strip())
    except (OSError, ValueError):
        print("porta ainda não definida", file=sys.stderr)
        return 1
    try:
        with urllib.request.urlopen(f"http://127.0.0.1:{port}/healthz", timeout=8):
            return 0
    except urllib.error.HTTPError:
        return 0  # respondeu (ex.: 403 na porta do painel)
    except (urllib.error.URLError, OSError) as e:
        print(f"wledadmin não respondeu na porta {port}: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
