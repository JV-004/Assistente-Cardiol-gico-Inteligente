<![CDATA[# 🫀 CardioIA — Resumo Técnico e Propostas de Melhoria

## 1. Resumo Técnico do Projeto

### 1.1 Visão Geral

O **CardioIA** é um assistente cardiológico conversacional composto por três camadas desacopladas: **Frontend** (HTML/CSS/JS), **Backend** (Python/Flask) e **Motor Cognitivo** (IBM Watson Assistant). O projeto foi desenvolvido para a Fase 5 da disciplina da FIAP, com foco em Processamento de Linguagem Natural (PLN), integração via API REST e interface de chat para interação com pacientes.

### 1.2 Análise por Componente

---

#### 🔧 Backend (Python/Flask)

| Aspecto | Status | Detalhes |
|---|---|---|
| **Estrutura do código** | ✅ Excelente | Separação clara: `app.py` (rotas), `config.py` (configuração), `services/watson_service.py` (integração Watson) |
| **Endpoints da API** | ✅ Funcionais | 4 rotas implementadas: `GET /`, `GET /health`, `POST /api/session`, `POST /api/chat` |
| **Validação de entrada** | ✅ Robusta | Verifica tipo, conteúdo, tamanho (1000 chars), corpo ausente/inválido |
| **Tratamento de erros** | ✅ Completo | Handlers para 400, 404, 405, 500, 502 — todos retornam JSON padronizado |
| **Rastreabilidade** | ✅ Implementada | `request_id` (UUID4) em cada requisição + logging estruturado |
| **Contexto conversacional** | ✅ Funcional | `SESSION_CONTEXT` com Lock e TTL de 30min resolve respostas curtas de intensidade |
| **Segurança** | ✅ Adequada | Credenciais via `.env`, CORS configurado, sem exposição de stack traces |
| **Contrato da API** | ✅ Documentado | `API_CONTRACT.md` com 29 seções detalhando cada aspecto do contrato REST |

**Execução verificada:**
- `GET /health` → Status 200, `watson_configured: false` (sem `.env` configurado — esperado)
- `POST /api/chat {}` → Status 400, erro de validação correto
- `POST /api/chat {"message":"..."}` → Status 500, erro controlado (Watson não configurado — esperado)
- `GET /nonexistent` → Status 404, JSON padronizado

---

#### 🖥️ Frontend (HTML/CSS/JS)

| Aspecto | Status | Detalhes |
|---|---|---|
| **Layout e UX** | ✅ Excelente | Chat limpo, balões diferenciados (usuário vs bot), identidade visual cardiológica |
| **Responsividade** | ✅ Implementada | 3 breakpoints (desktop, tablet ≤700px, mobile ≤440px) |
| **Integração com API** | ✅ Funcional | `fetch` para `POST /api/chat`, gerenciamento de `session_id` |
| **Feedback visual** | ✅ Completo | Indicador animado "analisando...", botão "Enviando...", bloqueio de duplo envio |
| **Segurança frontend** | ✅ Segura | `textContent` (anti-XSS), sem credenciais no browser |
| **Acessibilidade** | ⚠️ Parcial | `aria-live` presente mas com limitações (vide melhorias) |

---

#### 🤖 Watson Assistant (Dialog Skill)

| Aspecto | Status | Detalhes |
|---|---|---|
| **Intents** | ✅ Definidos | 4 intents clínicos + 19 de controle (23 total), mín. 10 exemplos cada |
| **Entities** | ⚠️ Parcial | 3 customizadas (`sintoma`, `intensidade`, `medicacao`) + 2 de sistema — mas `@sintoma` e `@medicacao` não são usadas nas respostas condicionais |
| **Dialog nodes** | ⚠️ Funcional | 8 nós raiz com triagem por intensidade, mas sem sub-nós ou slots nativos |
| **Cobertura** | ⚠️ Limitada | 4 sintomas, 3 medicações — cobertura clínica mínima viável |
| **Fallback** | ✅ Implementado | Nó `anything_else` com orientação de emergência |

---

### 1.3 Estado Geral do Projeto

```
┌──────────────────────────────────────────────────────────────┐
│  COMPONENTE          │  INTEGRIDADE  │  FUNCIONAL  │  NOTA  │
├──────────────────────┼───────────────┼─────────────┼────────┤
│  Backend Flask       │     ✅        │     ✅*     │  9/10  │
│  Frontend Web        │     ✅        │     ✅*     │  9/10  │
│  Watson Dialog Skill │     ✅        │     ✅*     │  7/10  │
│  Documentação        │     ✅        │     ✅      │  9/10  │
│  Segurança           │     ✅        │     ✅      │  9/10  │
│  Contrato da API     │     ⚠️        │     ⚠️      │  8/10  │
└──────────────────────┴───────────────┴─────────────┴────────┘

* Funcional condicionado à configuração de credenciais Watson no arquivo .env
```

> [!IMPORTANT]
> O projeto está **íntegro e pronto para uso**. Todos os componentes importam corretamente, as rotas respondem adequadamente e os tratamentos de erro funcionam. A única dependência externa é a configuração de credenciais do IBM Watson Assistant no arquivo `backend/.env`.

---

## 2. Problemas Identificados

### 🔴 Problemas Críticos (impedem uso em determinados cenários)

| # | Problema | Localização | Impacto |
|---|---|---|---|
| 1 | **`requirements.txt` em UTF-16LE** | [requirements.txt](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/backend/requirements.txt) | `pip install -r` falha em Linux, Docker e ambientes CI/CD |
| 2 | **Ausência de `__init__.py`** | `backend/` e `backend/services/` | Pode causar `ModuleNotFoundError` em certas versões/ambientes Python |
| 3 | **Endpoint DELETE não implementado** | [API_CONTRACT.md](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/backend/API_CONTRACT.md) vs [app.py](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/backend/app.py) | Contrato documenta `DELETE /api/session/<id>` mas a rota não existe no código |

### 🟡 Problemas Moderados (afetam robustez/UX)

| # | Problema | Localização | Impacto |
|---|---|---|---|
| 4 | **URL da API hardcoded** | [script.js L1](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/frontend/script.js) | `http://127.0.0.1:5000/api/chat` impede deploy em outros ambientes/HTTPS |
| 5 | **Sem timeout/AbortController no fetch** | [script.js](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/frontend/script.js) | Se Watson travar, interface fica em "Enviando..." permanentemente |
| 6 | **Sem tratamento de sessão expirada** | [script.js](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/frontend/script.js) | Watson expira sessões inativas; frontend não limpa `sessionId` ao receber erro de sessão |
| 7 | **19 intents sem nós de diálogo** | [cardioia-dialog-skill.json](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/watson-assistant/cardioia-dialog-skill.json) | "Olá", "Tchau", "O que você faz?" caem no fallback genérico |
| 8 | **Entidades definidas mas não utilizadas** | [cardioia-dialog-skill.json](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/watson-assistant/cardioia-dialog-skill.json) | `@sintoma` e `@medicacao` são reconhecidas mas as respostas não variam por tipo |
| 9 | **Dependências não utilizadas** | [requirements.txt](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/backend/requirements.txt) | `ibm-watson` e `ibm-cloud-sdk-core` instalados mas o código usa `requests` puro |

### 🟢 Problemas Menores (estéticos/boas práticas)

| # | Problema | Localização | Impacto |
|---|---|---|---|
| 10 | **`100vh` em mobile** | [style.css](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/frontend/style.css) | Barras dinâmicas do navegador mobile causam overflow — migrar para `100dvh` |
| 11 | **Ícone `♥` sem `aria-hidden`** | [index.html](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/frontend/index.html) | Screen readers verbalizam "coração de naipe preto" |
| 12 | **`FLASK_ENV` deprecated** | [.env.example](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/backend/.env.example) | Flask 3.x removeu `FLASK_ENV` em favor de `FLASK_DEBUG` |
| 13 | **Sem botão de "nova conversa"** | [index.html](file:///c:/FIAP_TRABALHOS/2%C2%BA%20SEMESTRE/Assistente-Cardiol-gico-Inteligente-main/frontend/index.html) | Usuário precisa recarregar a página para iniciar nova conversa |

---

## 3. Propostas de Melhoria

### 3.1 Correções Imediatas (Quick Wins)

> [!TIP]
> Estas correções podem ser implementadas em poucas horas e resolvem os problemas mais impactantes.

#### 1. Converter `requirements.txt` para UTF-8

```powershell
# PowerShell
$content = Get-Content backend/requirements.txt -Encoding Unicode
$content | Out-File backend/requirements.txt -Encoding UTF8NoBOM
```

#### 2. Adicionar arquivos `__init__.py`

```bash
touch backend/__init__.py
touch backend/services/__init__.py
```

#### 3. Resolver discrepância do endpoint DELETE

**Opção A** — Implementar a rota no `app.py`:
```python
@app.route("/api/session/<session_id>", methods=["DELETE"])
def delete_session(session_id):
    request_id = str(uuid4())
    try:
        watson = WatsonService()
        watson.delete_session(session_id)  # implementar no WatsonService
        return jsonify({"success": True, "request_id": request_id}), 200
    except RequestException:
        return jsonify({"success": False, "error": "Falha ao encerrar sessão.", "request_id": request_id}), 502
```

**Opção B** — Remover da tabela do `API_CONTRACT.md` (seção 25).

#### 4. Adicionar nós de diálogo para saudações e despedidas

No Watson Assistant, criar nós para:
- `General_Greetings` → "Olá! Sou o CardioIA. Como posso ajudar?"
- `General_Ending` → "Até logo! Lembre-se de procurar um médico se necessário."
- `General_About_You` → "Sou um assistente virtual para orientação cardiológica inicial."

---

### 3.2 Melhorias de Robustez

#### 5. Timeout no frontend com AbortController

```javascript
async function enviarMensagem(message) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 30000); // 30s

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload),
            signal: controller.signal
        });
        // ...
    } finally {
        clearTimeout(timeoutId);
    }
}
```

#### 6. Tratamento de sessão expirada

```javascript
// No catch do enviarMensagem
if (error.message.includes("sessão") || response.status === 502) {
    sessionId = null; // Limpa sessão expirada
    // Opcionalmente, reenvia automaticamente
}
```

#### 7. URL da API configurável

```javascript
const API_URL = window.location.hostname === "127.0.0.1"
    ? "http://127.0.0.1:5000/api/chat"
    : "/api/chat";
```

---

### 3.3 Melhorias Funcionais (Watson Assistant)

#### 8. Respostas contextualizadas por tipo de sintoma

Modificar o dialog node de `#relatar_sintoma` para condicionar respostas ao `@sintoma` detectado:

| Condição | Resposta |
|---|---|
| `@sintoma:dor no peito` | "Dor no peito pode ter diversas causas. Irradia para braço ou mandíbula?" |
| `@sintoma:palpitacao` | "Palpitações podem ser benignas ou indicar arritmia. Com que frequência ocorrem?" |
| `@sintoma:falta de ar` | "Falta de ar pode estar associada a problemas cardíacos. Ocorre em repouso ou ao esforço?" |

#### 9. Usar Slots nativos do Watson (em vez de contexto Python)

Substituir o mecanismo `SESSION_CONTEXT` do backend por **Slots** nativos no Watson Assistant para capturar `@intensidade` de forma declarativa:

```
Dialog Node: #relatar_sintoma
  Slot 1: @intensidade (obrigatório)
    Prompt: "Pode me dizer a intensidade — leve, moderada ou forte?"
```

Isso elimina a dependência do estado em memória do backend e permite escalabilidade horizontal.

#### 10. Expandir vocabulário clínico

**Sintomas adicionais sugeridos:**
- Irradiação de dor para braço/mandíbula/dorso
- Sudorese fria
- Edema de membros inferiores
- Síncope (desmaio)
- Náusea associada a dor torácica

**Medicamentos adicionais sugeridos:**
- Betabloqueadores: atenolol, metoprolol, carvedilol
- Diuréticos: hidroclorotiazida, furosemida
- Anticoagulantes: varfarina, rivaroxabana
- Antiarrítmicos: amiodarona

---

### 3.4 Melhorias Avançadas (Ir Além)

#### 11. Connection Pooling no WatsonService

Utilizar `requests.Session()` para reutilizar conexões TLS/TCP:

```python
class WatsonService:
    _session = None

    @classmethod
    def _get_session(cls):
        if cls._session is None:
            cls._session = requests.Session()
            cls._session.auth = ("apikey", Config.WATSON_API_KEY)
        return cls._session
```

#### 12. Botão "Nova Conversa" no frontend

Adicionar botão no cabeçalho para reiniciar a conversa sem recarregar a página:

```javascript
function novaConversa() {
    sessionId = null;
    chat.innerHTML = ""; // Limpa histórico
    adicionarMensagemInicial(); // Reinsere saudação
}
```

#### 13. Modo offline / demonstração

Implementar um modo de demonstração que funcione sem Watson, usando respostas pré-definidas para apresentações e testes:

```python
if not Config.WATSON_API_KEY:
    # Modo demonstração com respostas simuladas
    return DEMO_RESPONSES.get(intent, "Resposta padrão de demonstração")
```

#### 14. Persistência de sessão com Redis (produção)

Para ambiente de produção ou multi-worker:

```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Substituir SESSION_CONTEXT por Redis
r.setex(f"session:{session_id}", CONTEXT_TTL_SECONDS, json.dumps(context))
```

---

### 3.5 Priorização das Melhorias

| Prioridade | Melhoria | Esforço | Impacto |
|---|---|---|---|
| 🔴 P0 | Converter `requirements.txt` UTF-8 | 5 min | Compatibilidade multi-plataforma |
| 🔴 P0 | Adicionar `__init__.py` | 2 min | Evita `ModuleNotFoundError` |
| 🟠 P1 | Resolver endpoint DELETE | 30 min | Consistência contrato ↔ código |
| 🟠 P1 | Nós de diálogo para saudações | 30 min | UX do chatbot |
| 🟡 P2 | Timeout no frontend | 15 min | Robustez |
| 🟡 P2 | Sessão expirada | 15 min | Robustez |
| 🟡 P2 | Respostas por tipo de sintoma | 1h | Riqueza clínica |
| 🔵 P3 | Expandir vocabulário clínico | 2h | Cobertura |
| 🔵 P3 | Botão nova conversa | 30 min | UX |
| ⚪ P4 | Slots nativos Watson | 2h | Arquitetura |
| ⚪ P4 | Connection pooling | 30 min | Performance |
| ⚪ P4 | Modo demonstração | 2h | Apresentação |
]]>
