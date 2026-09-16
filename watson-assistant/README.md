# Watson Assistant — CardioIA

## O que é este arquivo

`cardioia-dialog-skill.json` é a exportação do **Dialog skill** do IBM Watson Assistant usado pelo assistente CardioIA. Ele contém a definição completa da conversa:

| Conteúdo | Quantidade |
| --- | --- |
| Intents | 23 (ex.: `relatar_sintoma`, `duvida_medicacao`, `pedir_orientacao`, `agendar_contato`, além dos `General_*` e `Bot_Control_*` do template) |
| Entities | 5 (`sintoma`, `medicacao`, `intensidade`, `sys-number`, `sys-time`) |
| Dialog nodes | 8 |

Idioma: `pt-br`. Exportado pela API `v2` (`2018-11-08`).

## Como reimportar no Watson Assistant

1. Abra o **Assistant** no IBM Cloud.
2. Vá em **Dialog**.
3. Abra **Options**.
4. Em **Upload/Download**, escolha **Upload**.
5. Selecione `cardioia-dialog-skill.json`.

O upload **substitui** o conteúdo do skill atual (intents, entities e nós de diálogo). Faça um Download do skill existente antes, se quiser preservar o estado anterior.

## Credenciais

Este arquivo **não contém API Key, URL de serviço nem qualquer segredo de autenticação**. Essas credenciais ficam fora do repositório, em `.env`, sob responsabilidade do backend.

Uma ressalva: o campo `description` da exportação traz o texto gerado pelo próprio Watson — `"created for assistant c91f0bdf-887a-4dc6-8fce-3664509919d3"` — ou seja, o **Assistant ID está presente no arquivo**. Ele é apenas um identificador de recurso, inútil sem a API Key, mas não é correto afirmar que o arquivo está livre de identificadores. Se a exposição do ID for indesejada, edite esse campo antes de tornar o repositório público.
