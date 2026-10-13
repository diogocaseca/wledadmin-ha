# Changelog

## 0.7.0

- Opção **ssl**: HTTPS na porta do acesso direto, com o certificado da pasta `/ssl` do
  Home Assistant (padrão `fullchain.pem`/`privkey.pem`, os nomes do App DuckDNS). O
  certificado renovado é aplicado sozinho, sem reiniciar. Se o certificado estiver ausente
  ou inválido, o acesso direto não sobe e o painel da barra lateral continua funcionando.
- O botão **Abrir interface web** usa https quando a opção estiver ligada.
- O app passa a encerrar com código 0 ao ser parado (antes saía com 143, e o Supervisor
  registrava um aviso).
- wledadmin 0.7.0.

## 0.6.1

- HEALTHCHECK no contêiner: com a chave **Watchdog** ligada, o Home Assistant reinicia o
  app também quando ele para de responder (não só quando cai). Funciona com qualquer
  porta configurada, inclusive com o acesso direto desligado.

## 0.6.0

- Porta do acesso direto configurável na seção **Rede** do app; apagar o número desliga o
  acesso direto.
- O painel da barra lateral passa a usar uma porta própria, escolhida pelo Home Assistant,
  que só aceita conexões do Home Assistant.
- Removida a verificação de saúde por URL (o Supervisor ainda reinicia o app se o
  processo parar, com a chave Watchdog ligada).
- wledadmin 0.6.0.

## 0.5.0

- Primeira versão do app, com o wledadmin 0.5.0: descoberta (mDNS, varredura, manual),
  painel e ações em massa, backup e restauração de `cfg.json`/`presets.json`, atualização
  de firmware em lote (com trava de OTA e recuperação após falha).
- Acesso pela barra lateral (Ingress, sem login extra), que pode ser desligado, e acesso
  direto pela porta 8000.
