# CardioIA — Contrato da API

Este documento define o contrato de comunicação entre o front-end do CardioIA e o backend desenvolvido em Flask, responsável pela integração segura com o IBM Watson Assistant.

---

## 1. Base URL

Durante o desenvolvimento local:

```text
http://127.0.0.1:5000
```

Todas as rotas descritas neste documento utilizam essa URL como base.

---

## 2. Health Check

### Endpoint

```http
GET /health
```

Verifica se o backend está disponível e se a configuração necessária para comunicação com o IBM Watson Assistant foi carregada.

### Exemplo de resposta

```json
{
  "service": "CardioIA Backend API",
  "status": "healthy",
  "version": "1.0.0",
  "watson_configured": true
}
```

### Status HTTP

- `200 OK` — serviço disponível.

---

## 3. Criar sessão

### Endpoint

```http
POST /api/session
```

Cria manualmente uma nova sessão conversacional no IBM Watson Assistant.

O front-end não é obrigado a utilizar este endpoint antes de iniciar uma conversa, pois `/api/chat` também pode criar automaticamente uma sessão quando nenhum `session_id` é informado.

### Exemplo de resposta

```json
{
  "success": true,
  "session_id": "exemplo-de-session-id",
  "request_id": "exemplo-de-request-id"
}
```

### Possíveis status HTTP

- `201 Created` — sessão criada com sucesso.
- `500 Internal Server Error` — configuração necessária indisponível.
- `502 Bad Gateway` — falha de comunicação com o serviço externo.

---

## 4. Enviar mensagem

### Endpoint

```http
POST /api/chat
```

Este é o principal endpoint de comunicação entre o front-end e o assistente.

### Header

```http
Content-Type: application/json
```

### Corpo da requisição

O campo `message` é obrigatório.

O campo `session_id` é opcional na primeira mensagem e deve ser reutilizado nas mensagens seguintes.

---

## 5. Primeira mensagem da conversa

Na primeira interação, o front-end pode enviar somente a mensagem:

```json
{
  "message": "Estou sentindo dor no peito"
}
```

Quando nenhum `session_id` é informado, o backend cria automaticamente uma sessão para a conversa.

### Exemplo de resposta

```json
{
  "success": true,
  "session_id": "exemplo-de-session-id",
  "response": "Entendi que você está sentindo algo. Pode me dizer a intensidade — leve, moderada ou forte?",
  "analysis": {
    "intent": "relatar_sintoma",
    "confidence": 1,
    "entities": [
      {
        "entity": "sintoma",
        "value": "dor no peito",
        "confidence": 1
      }
    ]
  },
  "context": {
    "applied": false,
    "session_created": true
  },
  "request_id": "exemplo-de-request-id"
}
```

---

## 6. Continuação da conversa

Após a primeira resposta, o front-end deve armazenar o valor retornado em:

```text
session_id
```

Esse identificador deve ser enviado nas mensagens seguintes para manter a continuidade da conversa.

### Exemplo

```json
{
  "message": "forte",
  "session_id": "exemplo-de-session-id"
}
```

### Exemplo de resposta

```json
{
  "success": true,
  "session_id": "exemplo-de-session-id",
  "response": "Isso que você descreveu pode ser sério. Recomendo buscar atendimento médico imediatamente ou procurar o pronto-socorro mais próximo. Não estou apto a fazer diagnósticos.",
  "analysis": {
    "intent": "relatar_sintoma",
    "confidence": 0.93,
    "entities": []
  },
  "context": {
    "applied": true,
    "session_created": false
  },
  "request_id": "exemplo-de-request-id"
}
```

---

## 7. Estrutura da resposta de `/api/chat`

Uma resposta bem-sucedida possui a seguinte estrutura principal:

```json
{
  "success": true,
  "session_id": "identificador-da-sessao",
  "response": "Resposta apresentada ao usuário",
  "analysis": {
    "intent": "intencao_identificada",
    "confidence": 0.95,
    "entities": []
  },
  "context": {
    "applied": false,
    "session_created": true
  },
  "request_id": "identificador-da-requisicao"
}
```

### `success`

Indica se a operação foi concluída com sucesso.

```json
"success": true
```

### `session_id`

Identificador da sessão conversacional.

O front-end deve armazenar esse valor e reutilizá-lo durante a conversa.

### `response`

Texto produzido pelo fluxo conversacional e que pode ser apresentado ao usuário.

### `analysis`

Contém metadados do processamento de linguagem natural.

Pode apresentar:

- intenção identificada;
- confiança da intenção;
- entidades reconhecidas.

Exemplo:

```json
{
  "intent": "relatar_sintoma",
  "confidence": 0.97,
  "entities": [
    {
      "entity": "sintoma",
      "value": "dor no peito",
      "confidence": 1
    }
  ]
}
```

Essas informações são destinadas principalmente à camada técnica e não precisam ser exibidas diretamente ao usuário.

### `context`

Apresenta informações relacionadas ao gerenciamento do contexto conversacional.

Exemplo:

```json
{
  "applied": true,
  "session_created": false
}
```

#### `applied`

Indica se houve aplicação de contexto para auxiliar a continuidade da interação.

Exemplo conceitual:

```text
Usuário: Estou sentindo dor no peito.
CardioIA: Pode me dizer a intensidade?
Usuário: forte.
```

A última mensagem depende do contexto da interação anterior para ser interpretada adequadamente.

#### `session_created`

Indica se uma nova sessão foi criada durante a requisição atual.

### `request_id`

Identificador exclusivo associado à requisição.

Exemplo:

```json
{
  "request_id": "568afcdc-e75f-4a39-8d3f-c7b36779f250"
}
```

Esse identificador facilita rastreabilidade e análise técnica de falhas sem exigir a exposição de credenciais.

---

## 8. Validação de entrada

O campo `message` é obrigatório e deve conter texto válido.

### Requisição inválida

```json
{}
```

### Exemplo de resposta

```json
{
  "success": false,
  "error": "O campo 'message' é obrigatório e deve conter texto.",
  "request_id": "exemplo-de-request-id"
}
```

### Status HTTP

```text
400 Bad Request
```

---

## 9. Corpo ausente ou JSON inválido

Caso o corpo da requisição esteja ausente ou não seja um JSON válido, a API retorna uma resposta de erro controlada.

### Exemplo

```json
{
  "success": false,
  "error": "Corpo da requisição ausente ou JSON inválido.",
  "request_id": "exemplo-de-request-id"
}
```

### Status HTTP

```text
400 Bad Request
```

---

## 10. Limite de tamanho da mensagem

Para evitar entradas excessivamente grandes, mensagens acima do limite definido pelo backend são rejeitadas.

O limite adotado pela API é de 1000 caracteres por mensagem.

### Exemplo de resposta

```json
{
  "success": false,
  "error": "A mensagem excede o limite de 1000 caracteres.",
  "request_id": "exemplo-de-request-id"
}
```

### Status HTTP

```text
400 Bad Request
```

---

## 11. Falha de comunicação com o IBM Watson Assistant

Caso o backend não consiga se comunicar corretamente com o IBM Watson Assistant, a API retorna uma falha controlada.

### Exemplo

```json
{
  "success": false,
  "error": "Não foi possível comunicar com o Watson Assistant no momento.",
  "request_id": "exemplo-de-request-id"
}
```

### Status HTTP

```text
502 Bad Gateway
```

A utilização do status `502` diferencia uma falha de dependência externa de uma falha interna da aplicação.

---

## 12. Endpoint inexistente

Caso seja solicitada uma rota que não existe na API:

```json
{
  "success": false,
  "error": "Endpoint não encontrado."
}
```

### Status HTTP

```text
404 Not Found
```

---

## 13. Método HTTP não permitido

Quando um endpoint existente recebe um método HTTP incompatível:

```json
{
  "success": false,
  "error": "Método HTTP não permitido para este endpoint."
}
```

### Status HTTP

```text
405 Method Not Allowed
```

---

## 14. Erro interno

Caso ocorra uma falha interna inesperada, a API retorna uma resposta genérica sem expor detalhes internos da aplicação.

```json
{
  "success": false,
  "error": "Erro interno do servidor."
}
```

### Status HTTP

```text
500 Internal Server Error
```

Detalhes técnicos devem permanecer restritos aos logs do backend.

---

## 15. Regras de integração com o front-end

O front-end deve:

1. enviar mensagens por meio de `POST /api/chat`;
2. utilizar `Content-Type: application/json`;
3. enviar o texto do usuário no campo `message`;
4. armazenar o `session_id` retornado na primeira interação;
5. reutilizar o mesmo `session_id` nas mensagens seguintes;
6. verificar o campo `success` antes de processar a resposta;
7. apresentar ao usuário o conteúdo apropriado do campo `response`;
8. tratar adequadamente respostas de erro;
9. não armazenar credenciais do IBM Watson Assistant;
10. não realizar autenticação diretamente com a IBM Cloud.

---

## 16. Fluxo de comunicação

O fluxo principal da aplicação é:

```text
Usuário
   |
   v
Interface Web
   |
   | POST /api/chat
   v
Backend Flask
   |
   v
Validação da requisição
   |
   v
Gerenciamento de sessão e contexto
   |
   v
IBM Watson Assistant
   |
   v
Processamento de linguagem natural
   |
   v
Backend Flask
   |
   v
Normalização da resposta
   |
   v
JSON estruturado
   |
   v
Interface Web
   |
   v
Usuário
```

Essa arquitetura mantém a interface desacoplada do serviço externo e centraliza no backend as regras de integração.

---

## 17. Segurança

As credenciais utilizadas para acessar o IBM Watson Assistant pertencem exclusivamente ao backend.

As seguintes informações nunca devem ser enviadas ao front-end:

- API Key do IBM Watson;
- credenciais da IBM Cloud;
- conteúdo do arquivo `.env`;
- parâmetros internos de autenticação.

As credenciais são carregadas por meio de variáveis de ambiente.

O arquivo real:

```text
backend/.env
```

contém informações sensíveis e não deve ser versionado.

O arquivo:

```text
backend/.env.example
```

pode ser versionado porque contém somente os nomes das variáveis necessárias, sem os respectivos valores secretos.

---

## 18. Sessões conversacionais

Cada conversa utiliza um `session_id`.

Na primeira interação, o backend pode criar automaticamente uma nova sessão.

Nas mensagens posteriores, o cliente reutiliza o mesmo identificador para preservar a continuidade da conversa.

A aplicação evita expor ao usuário detalhes internos relacionados à criação e manutenção dessas sessões.

---

## 19. Tratamento de contexto

Além da sessão fornecida pelo IBM Watson Assistant, o backend possui mecanismos para auxiliar a continuidade de determinadas interações.

Isso é especialmente relevante quando uma mensagem isolada possui pouco significado sem a interação anterior.

Exemplo:

```text
Mensagem 1: Estou sentindo dor no peito.
Mensagem 2: forte.
```

A palavra `forte`, isoladamente, possui contexto insuficiente. A camada de backend pode utilizar informações da interação anterior para preservar a coerência da conversa.

O campo `context.applied` informa se esse mecanismo foi aplicado durante a requisição.

---

## 20. Observabilidade e rastreabilidade

Cada requisição processada pode receber um `request_id` exclusivo.

Esse identificador permite:

- localizar uma requisição específica nos logs;
- investigar falhas;
- correlacionar eventos;
- melhorar a manutenção da aplicação;
- evitar a exposição desnecessária de informações sensíveis ao cliente.

O `request_id` não substitui o `session_id`.

Enquanto o `session_id` identifica uma conversa, o `request_id` identifica uma requisição específica.

---

## 21. Responsabilidades do backend

O backend do CardioIA é responsável por:

- proteger credenciais;
- autenticar-se com o IBM Watson Assistant;
- criar e gerenciar sessões;
- encaminhar mensagens;
- validar dados recebidos;
- estruturar respostas;
- tratar falhas;
- preservar o contrato da API;
- oferecer continuidade contextual quando aplicável;
- fornecer informações técnicas de rastreabilidade.

---

## 22. Responsabilidades do front-end

O front-end é responsável por:

- coletar a mensagem do usuário;
- enviar requisições válidas ao backend;
- manter o `session_id` durante a conversa;
- apresentar respostas ao usuário;
- oferecer feedback visual durante o processamento;
- tratar erros de comunicação;
- não expor dados técnicos ou credenciais desnecessárias.

---

## 23. Princípio de separação de responsabilidades

O CardioIA utiliza separação entre apresentação, integração e processamento conversacional.

```text
FRONT-END
Apresentação e interação com o usuário
        |
        v
BACKEND FLASK
Segurança, validação, contexto e integração
        |
        v
IBM WATSON ASSISTANT
Processamento conversacional e linguagem natural
```

Essa separação reduz o acoplamento entre componentes e permite evolução independente da interface e da integração com o serviço de inteligência artificial.

---

## 24. Considerações de segurança no domínio da aplicação

O CardioIA possui finalidade educacional e de apoio conversacional.

A aplicação não deve ser utilizada como substituta de avaliação realizada por profissional de saúde.

As respostas relacionadas a situações potencialmente graves devem priorizar orientação para busca de atendimento profissional, sem apresentar diagnóstico médico como conclusão do sistema.

---

## 25. Resumo dos endpoints

| Método | Endpoint | Finalidade |
|---|---|---|
| `GET` | `/health` | Verificar disponibilidade do backend |
| `POST` | `/api/session` | Criar uma sessão manualmente |
| `POST` | `/api/chat` | Enviar mensagem ao assistente |
| `DELETE` | `/api/session/<session_id>` | Solicitar encerramento de uma sessão |

---

## 26. Códigos HTTP utilizados

| Código | Significado | Utilização |
|---|---|---|
| `200` | OK | Requisição processada com sucesso |
| `201` | Created | Recurso ou sessão criado com sucesso |
| `400` | Bad Request | Dados de entrada inválidos |
| `404` | Not Found | Endpoint não encontrado |
| `405` | Method Not Allowed | Método HTTP não permitido |
| `500` | Internal Server Error | Falha interna inesperada |
| `502` | Bad Gateway | Falha de comunicação com serviço externo |

---

## 27. Tecnologias envolvidas

A integração descrita neste contrato utiliza:

- Python;
- Flask;
- IBM Watson Assistant;
- API REST;
- JSON;
- variáveis de ambiente para proteção de credenciais.

---

## 28. Objetivo arquitetural

O contrato foi projetado para permitir que diferentes interfaces possam consumir o CardioIA sem conhecer detalhes internos da integração com o IBM Watson Assistant.

Dessa forma, a aplicação mantém:

- baixo acoplamento entre front-end e serviço de IA;
- proteção das credenciais;
- respostas padronizadas;
- tratamento centralizado de erros;
- rastreabilidade das requisições;
- continuidade das sessões conversacionais;
- facilidade de manutenção e evolução.

---

## 29. Observação final

Este documento representa o contrato técnico entre a camada de apresentação e o backend do CardioIA.

Alterações futuras na implementação interna não devem quebrar este contrato sem que a versão da API e sua respectiva documentação sejam atualizadas.