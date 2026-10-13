"""HEALTHCHECK do contêiner: o wledadmin está respondendo?

Roda dentro do contêiner (rede do host), então independe da porta configurada na seção
Rede. O run.py grava em PORT_FILE as portas em uso ("esquema porta", uma por linha), e o
app está vivo se qualquer uma responder. Qualquer resposta HTTP conta, inclusive o 403
que a porta do painel dá para conexões que não vêm do proxy do HA: o que importa é o
servidor responder. Com o Watchdog ligado, o Supervisor reinicia o app quando o Docker o
marca como "unhealthy".
"""

import ssl
import sys
import urllib.error
import urllib.request

PORT_FILE = "/tmp/wledadmin-health-port"


def responds(scheme: str, port: int) -> bool:
    # HTTPS: o certificado é do domínio e aqui o acesso é por 127.0.0.1, então não se
    # valida o nome nem a cadeia (só importa o servidor responder).
    ctx = ssl._create_unverified_context() if scheme == "https" else None
    try:
        with urllib.request.urlopen(f"{scheme}://127.0.0.1:{port}/healthz", timeout=8,
                                    context=ctx):
            return True
    except urllib.error.HTTPError:
        return True  # respondeu (ex.: 403 na porta do painel)
    except (urllib.error.URLError, OSError) as e:
        print(f"sem resposta em {scheme}://127.0.0.1:{port}: {e}", file=sys.stderr)
        return False


def main() -> int:
    try:
        with open(PORT_FILE, encoding="ascii") as f:
            targets = [(s, int(p)) for s, p in (line.split() for line in f if line.strip())]
    except (OSError, ValueError):
        targets = []
    if not targets:
        print("portas ainda não definidas", file=sys.stderr)
        return 1
    # Vivo se qualquer porta responder.
    return 0 if any(responds(scheme, port) for scheme, port in targets) else 1


if __name__ == "__main__":
    sys.exit(main())
