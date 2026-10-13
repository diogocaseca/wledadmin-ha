# WLED Admin

Painel para administrar vários dispositivos [WLED](https://kno.wled.ge) da sua rede:
descoberta automática, status, ações em massa, backup e restauração de configuração e
presets, e atualização de firmware em lote. Documentação completa do painel:
<https://github.com/diogocaseca/wledadmin>.

## Primeiro acesso

1. Inicie o app e abra **WLED Admin** na barra lateral do Home Assistant.
2. Os dispositivos são encontrados sozinhos por mDNS. Se algum não aparecer, use
   **Varrer rede** ou adicione pelo IP.
3. **Troque a senha do acesso direto.** O WLED Admin também atende na porta 8000 da sua
   rede local (configurável, veja abaixo), com o login inicial **admin / admin**. Troque
   em **Configurações → Conta de administrador**. Pela barra lateral o login não é pedido:
   quem já entrou no Home Assistant está autenticado.

## Duas formas de acesso

| Acesso | Endereço | Login |
|---|---|---|
| Barra lateral (Ingress) | Menu do Home Assistant | O do Home Assistant |
| Direto | `http://<endereço-do-home-assistant>:<porta>` (botão **Abrir interface web** na página do app; porta padrão 8000) | Usuário e senha do WLED Admin |

O acesso direto é útil para a API JSON e scripts (`curl -u usuario:senha ...`).

### Desativar o acesso pela barra lateral

- Desligue a opção **ingress** na aba **Configuração** do app e reinicie. O painel passa a
  mostrar uma página avisando que o acesso foi desativado, e só o acesso direto funciona.
- Para apenas esconder o atalho da barra lateral, sem desativar, use a chave **Mostrar na
  barra lateral** na página do app.

### Porta do acesso direto

Na aba **Configuração** do app, seção **Rede**:

- troque o número para usar outra porta (ex.: 8090) e reinicie o app. O botão **Abrir
  interface web** acompanha a mudança;
- **apague o número** para desligar o acesso direto. Aí só o painel da barra lateral
  funciona, e nenhuma porta do WLED Admin fica aberta para a rede local.

O painel da barra lateral usa uma porta própria, escolhida automaticamente pelo Home
Assistant, que só aceita conexões do próprio Home Assistant.

### HTTPS no acesso direto

Ligue a opção **ssl** para usar `https://` na porta do acesso direto, com o certificado
que o Home Assistant já tem na pasta `/ssl` (por exemplo, o do App DuckDNS). Os nomes
padrão (`fullchain.pem` e `privkey.pem`) são os que o App DuckDNS usa.

- Acesse pelo **nome do domínio** (ex.: `https://seudominio.duckdns.org:8000`). Pelo IP, o
  navegador mostra aviso, porque o certificado é do domínio.
- Com o HTTPS ligado, `http://` nessa porta deixa de funcionar.
- Quando o certificado é renovado, o WLED Admin passa a usar o novo sozinho (verifica a
  cada hora), sem reiniciar.
- Se o certificado não for encontrado ou for inválido, o acesso direto não sobe, o painel
  da barra lateral continua funcionando, e a aba **Log** explica o motivo.

## Opções

| Opção | Padrão | Descrição |
|---|---|---|
| `ingress` | ligado | Aceita o acesso pela barra lateral |
| `ssl` | desligado | HTTPS na porta do acesso direto |
| `certfile` / `keyfile` | `fullchain.pem` / `privkey.pem` | Arquivos em `/ssl` |
| `log_level` | `info` | Detalhe do log |
| `scan_subnets` | vazio | Faixas sugeridas para a varredura (ex.: `192.168.1.0/24`) |
| `github_token` | vazio | Token do GitHub, só se a lista de versões de firmware atingir o limite da API |

O intervalo do backup automático, a retenção e as opções de firmware ficam na tela
**Configurações** do próprio WLED Admin.

## Rede e porta

- O app usa a **rede do host** (necessária para o mDNS). Por isso a porta do acesso direto
  é aberta diretamente no Home Assistant e precisa estar livre. Se estiver ocupada, o app
  não inicia, e a aba **Log** mostra qual porta e por quê.
- Os dispositivos WLED precisam estar alcançáveis a partir do Home Assistant.

## Watchdog

Ligue a chave **Watchdog** na página do app. Com ela, o Home Assistant reinicia o WLED
Admin quando o processo cai e também quando ele para de responder: o contêiner verifica a
cada minuto se o painel responde e, depois de 3 falhas seguidas, é marcado como "unhealthy".
Os primeiros 2 minutos após a inicialização não contam.

## Dados e backups

Tudo fica na pasta de dados do app (banco SQLite com o cadastro, as versões de backup dos
dispositivos e o histórico de atualizações, além do cache de firmware). Ela entra nos
backups do Home Assistant. Os backups de `cfg.json` não contêm senhas: o WLED guarda as
senhas em outro arquivo, que nunca é servido pela rede.

## Esqueceu a senha do acesso direto?

Abra o painel pela barra lateral (não pede senha) e troque em **Configurações**. Se o
Ingress estiver desligado, ligue a opção, reinicie o app e faça a troca.
