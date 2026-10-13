"""Ponto de entrada do App: traduz a configuração do HA em variáveis do wledadmin.

- Opções da aba "Configuração": /data/options.json (gravado pelo Supervisor).
- Portas: lidas da API do Supervisor (/addons/self/info), porque com host_network o
  Docker não aplica o mapeamento da seção "Rede":
  * network["8000/tcp"]: porta do acesso direto escolhida pelo usuário (None = desligado);
  * ingress_port: porta do painel da barra lateral, sorteada pelo HA.
/data é o volume persistente do App (e entra nos backups do Home Assistant).
"""

import json
import os
import sys
import time
import urllib.request

OPTIONS_FILE = "/data/options.json"
HEALTH_PORT_FILE = "/tmp/wledadmin-health-port"  # lido pelo healthcheck.py
SSL_DIR = "/ssl"
SUPERVISOR_INFO = "http://supervisor/addons/self/info"
DEFAULT_PORT = 8000


def log(msg: str) -> None:
    print(f"[wledadmin] {msg}", flush=True)


def load_options() -> dict:
    try:
        with open(OPTIONS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except ValueError as e:
        log(f"{OPTIONS_FILE} inválido ({e}); usando padrões")
        return {}


def supervisor_info() -> dict | None:
    token = os.environ.get("SUPERVISOR_TOKEN")
    if not token:
        log("SUPERVISOR_TOKEN ausente: não dá para ler as portas configuradas no HA")
        return None
    req = urllib.request.Request(SUPERVISOR_INFO, headers={"Authorization": f"Bearer {token}"})
    for attempt in range(1, 4):
        try:
            with urllib.request.urlopen(req, timeout=10) as resp:
                return json.load(resp).get("data") or {}
        except (OSError, ValueError) as e:
            log(f"consulta ao Supervisor falhou (tentativa {attempt}/3): {e}")
            time.sleep(2)
    return None


def resolve_ports(info: dict | None) -> tuple[int, int | None]:
    """(porta direta, porta do ingress). Porta direta 0 = acesso direto desligado."""
    if info is None:
        log(f"usando a porta {DEFAULT_PORT} para o acesso direto; o painel da barra lateral "
            "fica indisponível até o app conseguir falar com o Supervisor")
        return DEFAULT_PORT, None
    network = info.get("network") or {}
    direct = network.get(f"{DEFAULT_PORT}/tcp", DEFAULT_PORT)
    ingress_port = info.get("ingress_port") or None
    if not direct and not ingress_port:
        log(f"nenhuma porta configurada; usando {DEFAULT_PORT} para o acesso direto")
        return DEFAULT_PORT, None
    return int(direct or 0), (int(ingress_port) if ingress_port else None)


def main() -> None:
    opts = load_options()
    direct, ingress_port = resolve_ports(supervisor_info())

    env = os.environ
    env["WLEDADMIN_DATA_DIR"] = "/data"
    env["WLEDADMIN_HOST"] = "0.0.0.0"
    env["WLEDADMIN_PORT"] = str(direct)
    if ingress_port:
        env["WLEDADMIN_INGRESS_PORT"] = str(ingress_port)
    env["WLEDADMIN_INGRESS"] = "true" if opts.get("ingress", True) else "false"
    env["WLEDADMIN_LOG_LEVEL"] = str(opts.get("log_level") or "info").upper()
    if opts.get("scan_subnets"):
        env["WLEDADMIN_SCAN_SUBNETS"] = str(opts["scan_subnets"])
    if opts.get("github_token"):
        env["WLEDADMIN_GITHUB_TOKEN"] = str(opts["github_token"])
    use_ssl = bool(opts.get("ssl")) and bool(direct)
    if use_ssl:
        # Nomes validados pelo schema (sem barras); o wledadmin explica no log se faltar.
        env["WLEDADMIN_SSL_CERTFILE"] = os.path.join(SSL_DIR, opts.get("certfile") or
                                                     "fullchain.pem")
        env["WLEDADMIN_SSL_KEYFILE"] = os.path.join(SSL_DIR, opts.get("keyfile") or
                                                    "privkey.pem")

    log("acesso direto: " + (f"porta {direct}" + (" (https)" if use_ssl else "")
                             if direct else "desligado")
        + " · painel da barra lateral: "
        + ("desativado na opção ingress" if env["WLEDADMIN_INGRESS"] != "true"
           else f"porta {ingress_port}" if ingress_port else "indisponível"))
    # Uma linha "esquema porta" por porta: o healthcheck considera vivo se qualquer uma
    # responder (se o certificado for inválido, a porta direta nem sobe, e o painel basta).
    targets = []
    if direct:
        targets.append(f"{'https' if use_ssl else 'http'} {direct}")
    if ingress_port:
        targets.append(f"http {ingress_port}")
    with open(HEALTH_PORT_FILE, "w", encoding="ascii") as f:
        f.write("\n".join(targets) + "\n")
    exe = os.path.join(os.path.dirname(sys.executable), "wledadmin")
    os.execv(exe, [exe, "serve"])


if __name__ == "__main__":
    main()
