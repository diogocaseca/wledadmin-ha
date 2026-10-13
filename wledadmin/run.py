"""Ponto de entrada do App: traduz as opções do HA em variáveis do wledadmin.

O Supervisor grava as opções da aba "Configuração" em /data/options.json. /data é o
volume persistente do App (e entra nos backups do Home Assistant).
"""

import json
import os
import sys

OPTIONS_FILE = "/data/options.json"


def load_options() -> dict:
    try:
        with open(OPTIONS_FILE, encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return {}
    except ValueError as e:
        print(f"[wledadmin] {OPTIONS_FILE} inválido ({e}); usando padrões", file=sys.stderr)
        return {}


def main() -> None:
    opts = load_options()
    env = os.environ
    env["WLEDADMIN_DATA_DIR"] = "/data"
    env["WLEDADMIN_HOST"] = "0.0.0.0"
    env["WLEDADMIN_PORT"] = "8000"  # fixa: é a mesma do ingress_port no config.yaml
    env["WLEDADMIN_INGRESS"] = "true" if opts.get("ingress", True) else "false"
    env["WLEDADMIN_LOG_LEVEL"] = str(opts.get("log_level") or "info").upper()
    if opts.get("scan_subnets"):
        env["WLEDADMIN_SCAN_SUBNETS"] = str(opts["scan_subnets"])
    if opts.get("github_token"):
        env["WLEDADMIN_GITHUB_TOKEN"] = str(opts["github_token"])

    print(
        "[wledadmin] iniciando: porta 8000, ingress "
        + ("ligado" if env["WLEDADMIN_INGRESS"] == "true" else "desligado"),
        flush=True,
    )
    exe = os.path.join(os.path.dirname(sys.executable), "wledadmin")
    os.execv(exe, [exe, "serve"])


if __name__ == "__main__":
    main()
