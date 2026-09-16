<p align="center">
  <a href="https://www.fiap.com.br/">
    <img src="https://github.com/JV-004/Assistente-Cardiol-gico-Inteligente/docs/images/logo-fiap.png" alt="FIAP" width="35%"/>
  </a>
</p>


<![CDATA[# 🫀 CardioIA — Assistente Cardiológico Inteligente

<div align="center">

**Projeto acadêmico — FIAP | 2º Semestre | Fase 5**

*Assistente conversacional inteligente para orientação cardiológica inicial, integrando Processamento de Linguagem Natural (PLN), IBM Watson Assistant e interface web responsiva.*

![Python](https://img.shields.io/badge/Python-3.12+-3776AB?logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-3.1.3-000000?logo=flask&logoColor=white)
![Watson](https://img.shields.io/badge/IBM_Watson-Assistant-052FAD?logo=ibm&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-ES6+-F7DF1E?logo=javascript&logoColor=black)
![License](https://img.shields.io/badge/Licença-Acadêmica-gray)

</div>

---

## 📋 Índice

- [Visão Geral](#-visão-geral)
- [Arquitetura](#-arquitetura)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Projeto](#-estrutura-do-projeto)
- [Pré-requisitos](#-pré-requisitos)
- [Como Executar](#-como-executar)
- [Endpoints da API](#-endpoints-da-api)
- [Fluxo Conversacional](#-fluxo-conversacional)
- [Watson Assistant — Configuração](#-watson-assistant--configuração)
- [Interface do Usuário](#-interface-do-usuário)
- [Segurança](#-segurança)
- [Testes e Validação](#-testes-e-validação)
- [Equipe e Divisão de Responsabilidades](#-equipe-e-divisão-de-responsabilidades)
- [Demonstração](#-demonstração)

---

## 🎯 Visão Geral

O **CardioIA** é um protótipo funcional de assistente cardiológico conversacional (chatbot) desenvolvido como projeto acadêmico da FIAP. O sistema:

- **Interage** com o usuário por meio de linguagem natural, simulando um atendimento inicial em saúde cardiovascular.
- **Integra** serviços de NLP através do IBM Watson Assistant para reconhecimento de intenções e entidades clínicas.
- **Organiza** e apresenta informações de saúde de forma estruturada e compreensível.
- **Alerta** para situações de urgência, orientando o paciente a buscar atendimento médico quando necessário.

> ⚠️ **Importante:** O CardioIA oferece orientações iniciais e **não substitui** avaliação, diagnóstico ou atendimento realizado por profissionais de saúde.

---

## 🏗 Arquitetura

O sistema segue uma arquitetura em três camadas com comunicação via API REST:

```
┌──────────────────┐      HTTP POST       ┌───────────────────┐      REST API      ┌──────────────────────┐
│                  │    /api/chat          │                   │                    │                      │
│   Frontend Web   │ ──────────────────►   │  Backend Flask    │ ────────────────►  │  IBM Watson          │
│   (HTML/CSS/JS)  │                       │  (Python)         │                    │  Assistant (NLP)     │
│                  │ ◄──────────────────   │                   │ ◄────────────────  │                      │
│                  │    JSON Response      │                   │    JSON Response   │                      │
└──────────────────┘                       └───────────────────┘                    └──────────────────────┘
     Porta 5500                                 Porta 5000                             IBM Cloud
```

**Fluxo completo:**

1. O **usuário** digita uma mensagem na interface web.
2. O **frontend** envia a mensagem via `POST /api/chat` para o backend Flask.
3. O **backend** valida a requisição, aplica contexto conversacional e encaminha ao Watson Assistant.
4. O **Watson** processa a intenção e as entidades configuradas (PLN).
5. O **backend** organiza a resposta, extrai metadados de NLP e retorna JSON estruturado.
6. O **frontend** exibe a resposta ao usuário, mantendo o histórico da conversa.

---

## 🛠 Tecnologias Utilizadas

### Backend
| Tecnologia | Versão | Finalidade |
|---|---|---|
| **Python** | 3.12+ | Linguagem principal do backend |
| **Flask** | 3.1.3 | Framework web para API REST |
| **Flask-CORS** | 6.0.5 | Controle de acesso cross-origin |
| **Requests** | 2.34.2 | Comunicação HTTP com a API do Watson |
| **python-dotenv** | 1.2.3 | Carregamento de variáveis de ambiente |

### Frontend
| Tecnologia | Finalidade |
|---|---|
| **HTML5** | Estrutura semântica da interface |
| **CSS3** | Estilização, layout responsivo e animações |
| **JavaScript (ES6+)** | Lógica da aplicação e integração com API |
| **Fetch API** | Comunicação HTTP assíncrona com o backend |

### Inteligência Artificial
| Tecnologia | Finalidade |
|---|---|
| **IBM Watson Assistant** | Motor de PLN (intents, entities, dialog) |
| **API REST v2** | Integração programática com o Watson |

---

## 📁 Estrutura do Projeto

```text
Assistente-Cardiologico-Inteligente/
│
├── 📄 README.md                          ← Este arquivo
├── 📄 .gitignore                         ← Regras de exclusão do Git
├── 📄 CardioIA_Fase5_Divisao_Equipe.docx ← Divisão de responsabilidades
├── 📄 Relatorio_Tecnico_CardioIA_Fase5_Aprimorado.docx
│
├── 📂 backend/                           ← API REST (Python/Flask)
│   ├── 📄 app.py                         ← Aplicação Flask (rotas e lógica)
│   ├── 📄 config.py                      ← Configurações e variáveis de ambiente
│   ├── 📄 requirements.txt               ← Dependências Python
│   ├── 📄 .env.example                   ← Modelo de variáveis de ambiente
│   ├── 📄 API_CONTRACT.md                ← Contrato formal da API REST
│   └── 📂 services/
│       └── 📄 watson_service.py          ← Camada de serviço do Watson
│
├── 📂 frontend/                          ← Interface Web
│   ├── 📄 index.html                     ← Estrutura da página
│   ├── 📄 style.css                      ← Estilos e responsividade
│   ├── 📄 script.js                      ← Lógica do chat e integração API
│   └── 📄 README.md                      ← Documentação do frontend
│
└── 📂 watson-assistant/                  ← Configuração do Watson
    ├── 📄 cardioia-dialog-skill.json     ← Exportação do Dialog Skill
    └── 📄 README.md                      ← Documentação da configuração Watson
```

---

## ✅ Pré-requisitos

Antes de executar o projeto, certifique-se de ter:

- **Python 3.12+** instalado ([python.org](https://www.python.org/downloads/))
- **pip** (gerenciador de pacotes Python)
- **Conta IBM Cloud** com instância do Watson Assistant configurada
- **Credenciais do Watson Assistant:**
  - `WATSON_API_KEY` — Chave de autenticação
  - `WATSON_URL` — URL do serviço Watson
  - `WATSON_ENVIRONMENT_ID` — ID do ambiente/assistente

---

## 🚀 Como Executar

### 1. Clonar o repositório

```bash
git clone https://github.com/<seu-usuario>/Assistente-Cardiologico-Inteligente.git
cd Assistente-Cardiologico-Inteligente
```

### 2. Configurar variáveis de ambiente

Crie o arquivo `backend/.env` baseado no modelo fornecido:

```bash
cp backend/.env.example backend/.env
```

Edite `backend/.env` e preencha com suas credenciais:

```env
WATSON_API_KEY=sua-api-key-aqui
WATSON_URL=https://api.us-south.assistant.watson.cloud.ibm.com
WATSON_ENVIRONMENT_ID=seu-environment-id-aqui
WATSON_VERSION=2021-11-27
FLASK_ENV=development
```

### 3. Instalar dependências do backend

```bash
pip install -r backend/requirements.txt
```

### 4. Importar o Dialog Skill no Watson Assistant

1. Acesse o [IBM Watson Assistant](https://cloud.ibm.com/catalog/services/watson-assistant).
2. Navegue até **Dialog** → **Options** → **Upload/Download**.
3. Faça upload do arquivo `watson-assistant/cardioia-dialog-skill.json`.

> ⚠️ A importação sobrescreve intents, entities e dialog nodes existentes no skill.

### 5. Iniciar o backend (Terminal 1)

Na **raiz do projeto**:

```bash
python -m backend.app
```

O backend estará disponível em: `http://127.0.0.1:5000`

### 6. Verificar o backend

Acesse no navegador ou via curl:

```bash
curl http://127.0.0.1:5000/health
```

Resposta esperada:

```json
{
  "service": "CardioIA Backend API",
  "status": "healthy",
  "version": "1.0.0",
  "watson_configured": true
}

```

### 7. Iniciar o frontend (Terminal 2)

Em um **segundo terminal**, entre na pasta `frontend/` e inicie o servidor:

```bash
cd frontend
python -m http.server 5500
```

O frontend estará disponível em: `http://127.0.0.1:5500`

### 8. Acessar o CardioIA

Abra o navegador e acesse **http://127.0.0.1:5500** para interagir com o assistente.

> 💡 **Nota (Windows PowerShell):** Caso encontre problemas com a execução do ambiente virtual, execute antes:
> ```powershell
> Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
> ```

---

## 📡 Endpoints da API

| Método | Endpoint | Descrição | Status HTTP |
|---|---|---|---|
| `GET` | `/` | Informações da API | `200` |
| `GET` | `/health` | Health check do backend | `200` |
| `POST` | `/api/session` | Criar sessão manualmente | `201` / `500` / `502` |
| `POST` | `/api/chat` | Enviar mensagem ao assistente | `200` / `400` / `500` / `502` |

### Exemplo — Enviar mensagem

**Requisição:**
```json
{
  "message": "Estou sentindo dor no peito",
  "session_id": "opcional-na-primeira-mensagem"
}
```

**Resposta:**
```json
{
  "success": true,
  "session_id": "id-da-sessao",
  "response": "Entendi que você está sentindo algo. Pode me dizer a intensidade — leve, moderada ou forte?",
  "analysis": {
    "intent": "relatar_sintoma",
    "confidence": 1.0,
    "entities": [
      {
        "entity": "sintoma",
        "value": "dor no peito",
        "confidence": 1.0
      }
    ]
  },
  "context": {
    "applied": false,
    "session_created": true
  },
  "request_id": "uuid-da-requisicao"
}
```

> 📄 Para detalhes completos do contrato da API, consulte [`backend/API_CONTRACT.md`](backend/API_CONTRACT.md).

---

## 💬 Fluxo Conversacional

O Watson Assistant foi configurado com um fluxo de triagem cardiológica em 3 níveis:

```text
                        ┌─ Intensidade FORTE ──► 🚨 Alerta de emergência
                        │                           "Buscar pronto-socorro imediatamente"
                        │
Usuário relata ────────►├─ Intensidade LEVE/   ──► ⚠️ Orientação de observação
   sintoma              │   MODERADA                "Observar e procurar médico se persistir"
                        │
                        └─ Sem intensidade ────► ❓ Solicita intensidade
                                                    "Pode me dizer: leve, moderada ou forte?"
```

### Intenções clínicas reconhecidas

| Intenção | Descrição | Exemplos |
|---|---|---|
| `relatar_sintoma` | Relato de sintoma cardiovascular | "dor no peito", "coração acelerado", "falta de ar" |
| `duvida_medicacao` | Dúvida sobre medicamentos | "esqueci meu remédio", "posso tomar com café?" |
| `pedir_orientacao` | Orientação geral de saúde | "como cuido da pressão?", "preciso ir ao PS?" |
| `agendar_contato` | Contato com profissional | "quero falar com um médico" |

### Entidades reconhecidas

| Entidade | Valores | Sinônimos |
|---|---|---|
| `@sintoma` | dor no peito, falta de ar, palpitação, tontura | aperto no peito, batedeira, vertigem... |
| `@intensidade` | forte, moderada, leve | insuportável, média, fraca... |
| `@medicacao` | AAS, losartana, sinvastatina | aspirina, remédio de pressão... |

### Contexto conversacional inteligente

O backend implementa uma camada de **continuidade contextual** que resolve uma limitação do dialog flow exportado. Quando o Watson pergunta a intensidade e o usuário responde apenas "forte", o backend reconstrói internamente a mensagem completa antes de reenviar:

```text
Entrada original:  "forte"
Mensagem enviada:  "Estou sentindo dor no peito. A intensidade é forte."
```

Isso garante que o Watson classifique corretamente a resposta curta no contexto da conversa anterior.

---

## ⚙ Watson Assistant — Configuração

O projeto utiliza o **IBM Watson Assistant** com a API v2, configurado com:

| Componente | Quantidade |
|---|---|
| **Intents** | 23 (4 clínicos + 19 do template IBM) |
| **Entities** | 5 (3 customizadas + 2 de sistema) |
| **Dialog Nodes** | 8 nós raiz |
| **Idioma** | `pt-br` |

O arquivo de exportação [`cardioia-dialog-skill.json`](watson-assistant/cardioia-dialog-skill.json) pode ser reimportado em qualquer instância do Watson Assistant.

> 📖 Para instruções detalhadas de reimportação, consulte [`watson-assistant/README.md`](watson-assistant/README.md).

---

## 🖥 Interface do Usuário

A interface web oferece uma experiência de chat completa:

### Funcionalidades implementadas

- ✅ Chat conversacional com balões de mensagem
- ✅ Mensagem de boas-vindas automática
- ✅ Indicador animado "CardioIA está analisando..."
- ✅ Bloqueio de envio durante processamento (evita duplicação)
- ✅ Contador de caracteres em tempo real (limite: 1000)
- ✅ Auto-resize do campo de texto
- ✅ Enter para enviar / Shift+Enter para quebra de linha
- ✅ Tratamento de erros com mensagem visual no chat
- ✅ Aviso médico permanente no topo
- ✅ Layout responsivo (desktop, tablet e smartphone)
- ✅ Prevenção contra XSS (uso de `textContent`)
- ✅ Aviso sobre compartilhamento de dados sensíveis

### Identidade Visual

A interface utiliza uma paleta de cores inspirada na cardiologia:
- **Vermelho carmesim** (`#b4232f`) para a marca e mensagens do usuário
- **Neutros suaves** para o fundo e balões do assistente
- **Âmbar** para alertas médicos
- **Verde** para indicador de status online

---

## 🔒 Segurança

O projeto implementa diversas medidas de segurança:

- ✅ **Credenciais isoladas** — API keys ficam exclusivamente no arquivo `backend/.env`, nunca no código-fonte
- ✅ **`.env` no `.gitignore`** — Variáveis sensíveis não são versionadas
- ✅ **Frontend sem acesso direto ao Watson** — Toda comunicação passa pelo backend
- ✅ **Validação de entrada** — Verificação de tipo, conteúdo e tamanho das mensagens
- ✅ **Tratamento de erros estruturado** — Respostas de erro padronizadas sem expor stack traces
- ✅ **CORS configurado** — Controle de origens permitidas
- ✅ **Prevenção XSS** — Uso de `textContent` em vez de `innerHTML`

---

## 🧪 Testes e Validação

### Validação do backend

| Teste | Resultado |
|---|---|
| `GET /health` | ✅ Retorna status `healthy` e estado da configuração Watson |
| `GET /` | ✅ Retorna metadados da API e lista de endpoints |
| `POST /api/chat` (mensagem válida) | ✅ Processa e retorna resposta estruturada |
| `POST /api/chat` (sem mensagem) | ✅ Retorna erro `400` com mensagem clara |
| `POST /api/chat` (> 1000 caracteres) | ✅ Rejeita com erro `400` |
| `GET /endpoint-inexistente` | ✅ Retorna `404` com JSON padronizado |
| `PUT /api/chat` (método errado) | ✅ Retorna `405` com JSON padronizado |

### Teste de integração ponta a ponta

```text
Usuário:   "Estou sentindo dor no peito"
CardioIA:  "Entendi que você está sentindo algo.
            Pode me dizer a intensidade — leve, moderada ou forte?"

Usuário:   "Forte"
CardioIA:  "Isso que você descreveu pode ser sério.
            Recomendo buscar atendimento médico imediatamente
            ou procurar o pronto-socorro mais próximo.
            Não estou apto a fazer diagnósticos."
```

✅ O teste confirmou: envio de mensagem, integração backend ↔ Watson, continuidade de sessão, contexto conversacional e exibição de resposta.

---

## 👥 Equipe e Divisão de Responsabilidades

O projeto foi dividido em **4 frentes de trabalho**, cada uma com um responsável:


## 👨‍🎓 Equipe

| Nome | RM | Papel — Sprint 3 |
|---|---:|---|
| João | RM565999 |1 - Modelagem Conversacional |
| Tayná Esteves | RM562491 | 2 - Backend e Integração |
| Endrew Alves | RM563646 | 3 - Interface e Experiência do Usuário |
| Carlos Eduardo | RM566487 | Video & Documentação |

### 👩‍🏫 Professores

**Tutor turma A:** [Caique Nonato da Silva Bezerra](https://www.linkedin.com/in/caique-nonato/) — profcaique.bezerra@fiap.com.br  
**Tutor turma R:** [Leonardo Ruiz Orabona](https://www.linkedin.com/in/leonardoorabona/) — profleonardo.orabona@fiap.com.br  
**Coordenador:** [André Godoi Chiovato](https://www.linkedin.com/in/andregodoichiovato/) - profandre.chiovato@fiap.com.br


---

## 🎬 Demonstração

> *Vídeo de demonstração (até 3 minutos) mostrando o fluxo completo de interação.*
>
> 📹 [Link para o vídeo de demonstração](#) *(inserir link)*

---

## 📚 Documentação Adicional

- [Contrato da API](backend/API_CONTRACT.md) — Especificação formal de todos os endpoints
- [Documentação do Frontend](frontend/README.md) — Detalhes da interface e experiência do usuário
- [Configuração Watson](watson-assistant/README.md) — Instruções de reimportação do Dialog Skill

---

<div align="center">

**CardioIA** — Projeto acadêmico FIAP | Fase 5 — Assistente Conversacional com NLP

*Desenvolvido com 🫀 pela equipe CardioIA*

</div>
]]>
