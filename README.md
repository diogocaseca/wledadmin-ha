# wledadmin-ha

Repositório de **App** do Home Assistant para o
[wledadmin](https://github.com/diogocaseca/wledadmin), um painel para administrar vários
dispositivos WLED: descoberta, status, ações em massa, backup e restauração, e atualização
de firmware em lote.

Requer **Home Assistant OS** ou **Supervised** (as instalações Container e Core não têm
Apps; nesse caso, use o Docker descrito no repositório do wledadmin).

## Instalação

1. No Home Assistant: **Configurações → Apps → Loja de Apps**.
2. No menu **⋮** (canto superior direito), escolha **Repositórios** e adicione:
   `https://github.com/diogocaseca/wledadmin-ha`
3. Procure **WLED Admin** na loja, instale e inicie.
4. Abra pela barra lateral. Depois, troque a senha do acesso direto (porta 8000, login
   inicial `admin`/`admin`) em **Configurações → Conta de administrador**.

O build é feito no próprio Home Assistant na instalação e nas atualizações (alguns minutos
num Raspberry Pi).

## Arquiteturas

`amd64` (PCs, NUC, máquinas virtuais) e `aarch64` (Raspberry Pi 4/5 com sistema 64 bits,
ODROID, Home Assistant Green/Yellow).

## Como funciona

| | |
|---|---|
| Rede | Rede do host, necessária para a descoberta mDNS dos dispositivos |
| Acesso | Barra lateral (Ingress, login do HA, porta própria escolhida pelo HA) e acesso direto (login do wledadmin, porta 8000 configurável na seção Rede, ou desligado) |
| Dados | Pasta de dados do app (`/data`), incluída nos backups do Home Assistant |
| Código | O Dockerfile baixa a versão marcada (tag) do wledadmin e instala as dependências travadas no `uv.lock` dela |

## Lançando uma versão nova

1. No repositório do wledadmin: suba a versão, crie a tag `vX.Y.Z` e faça o push.
2. Aqui: atualize `WLEDADMIN_VERSION` em `wledadmin/Dockerfile`, a `version` em
   `wledadmin/config.yaml` e o `wledadmin/CHANGELOG.md`.
3. Faça o push. O Home Assistant mostra a atualização disponível.

## Licença

[MIT](LICENSE)
