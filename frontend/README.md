# 🫀 CardioIA — Front-end e Experiência do Usuário

Interface web desenvolvida para o projeto **CardioIA — Assistente Cardiológico Inteligente**, da FIAP.

Esta parte do projeto é responsável pela interação entre o usuário e o assistente conversacional, oferecendo uma interface simples, responsiva e integrada ao backend Flask e ao IBM Watson Assistant.

---

## 👨‍💻 Responsável

**Endrew Alves dos Santos**  
Área: **Interface e Experiência do Usuário — Front-end**

---

## 🎯 Objetivo

O objetivo do front-end é permitir que o usuário converse com o CardioIA utilizando linguagem natural por meio de uma interface web simples e intuitiva.

A interface foi desenvolvida para:

- receber mensagens digitadas pelo usuário;
- exibir as mensagens na conversa;
- enviar as mensagens ao backend Flask;
- receber e apresentar as respostas do CardioIA;
- manter a continuidade da conversa;
- exibir feedback visual durante o processamento;
- tratar erros de comunicação;
- apresentar avisos relacionados ao uso responsável do assistente em saúde;
- funcionar em diferentes tamanhos de tela.

---

## 🧩 Tecnologias Utilizadas

O front-end foi desenvolvido utilizando:

- **HTML5** — estrutura da interface;
- **CSS3** — estilização e responsividade;
- **JavaScript** — comportamento da aplicação;
- **Fetch API** — comunicação HTTP com o backend Flask.

O front-end não possui acesso direto às credenciais do IBM Watson Assistant.

Toda comunicação com o Watson é realizada através do backend.

---

## 📁 Estrutura do Front-end

```text
frontend/
│
├── index.html
├── style.css
├── script.js
└── README.md
```

### `index.html`

Responsável pela estrutura visual da aplicação.

Contém:

- cabeçalho do CardioIA;
- nome e identificação do assistente;
- indicador visual de disponibilidade;
- aviso médico;
- área da conversa;
- mensagem inicial;
- indicador de processamento;
- campo para digitação;
- botão de envio;
- contador de caracteres.

---

### `style.css`

Responsável pela identidade visual e experiência de uso.

Foram implementados:

- layout centralizado;
- identidade visual relacionada ao contexto de saúde;
- diferenciação entre mensagens do usuário e do CardioIA;
- balões de conversa;
- indicador animado de processamento;
- estilização do formulário;
- aviso médico em destaque;
- adaptação para telas menores;
- responsividade para desktop, tablet e smartphone.

---

### `script.js`

Responsável pelo comportamento da aplicação e integração com o backend.

Foram implementados:

- envio de mensagens;
- comunicação com a API;
- armazenamento do `session_id`;
- continuidade da conversa;
- criação dinâmica das mensagens;
- indicador de carregamento;
- tratamento de erros;
- contador de caracteres;
- ajuste automático do campo de texto;
- envio utilizando Enter;
- `Shift + Enter` para quebra de linha.

---

## 🔄 Arquitetura da Comunicação

O front-end não se comunica diretamente com o IBM Watson Assistant.

O fluxo utilizado é:

```text
Usuário
   │
   ▼
Interface Web
   │
   │ POST /api/chat
   ▼
Backend Flask
   │
   ▼
IBM Watson Assistant
   │
   ▼
Backend Flask
   │
   ▼
Resposta JSON
   │
   ▼
Interface Web
   │
   ▼
Usuário
```

Essa separação mantém as credenciais protegidas no backend e evita que informações sensíveis sejam expostas no navegador.

---

## 🔌 Integração com o Backend

O endpoint utilizado pelo front-end é:

```text
POST http://127.0.0.1:5000/api/chat
```

Na primeira mensagem, o front-end pode enviar um JSON semelhante a:

```json
{
  "message": "Estou sentindo dor no peito"
}
```

O backend retorna uma estrutura semelhante a:

```json
{
  "success": true,
  "session_id": "identificador-da-sessao",
  "response": "Entendi que você está sentindo algo. Pode me dizer a intensidade — leve, moderada ou forte?"
}
```

O `session_id` retornado é armazenado pelo JavaScript.

Nas próximas mensagens, esse identificador é enviado novamente:

```json
{
  "message": "forte",
  "session_id": "identificador-da-sessao"
}
```

Isso permite que o assistente mantenha a continuidade da conversa.

---

## 🧠 Controle da Sessão

O front-end inicia sem uma sessão armazenada:

```javascript
let sessionId = null;
```

Após a primeira resposta do backend, o identificador da sessão é armazenado:

```javascript
sessionId = data.session_id;
```

Nas próximas mensagens:

```javascript
if (sessionId) {
    payload.session_id = sessionId;
}
```

Dessa forma, mensagens curtas podem ser interpretadas considerando o contexto da interação anterior.

Exemplo:

```text
Usuário:
Estou sentindo dor no peito

CardioIA:
Entendi que você está sentindo algo.
Pode me dizer a intensidade — leve, moderada ou forte?

Usuário:
Forte

CardioIA:
Isso que você descreveu pode ser sério.
Recomendo buscar atendimento médico imediatamente
ou procurar o pronto-socorro mais próximo.
```

Esse teste confirmou que o contexto da conversa é preservado entre as mensagens.

---

## 💬 Experiência da Conversa

Quando o usuário envia uma mensagem, o sistema executa o seguinte fluxo:

1. captura o texto digitado;
2. adiciona imediatamente a mensagem do usuário na interface;
3. limpa o campo de texto;
4. atualiza o contador de caracteres;
5. exibe um indicador de processamento;
6. envia a mensagem ao backend;
7. aguarda a resposta;
8. apresenta a resposta do CardioIA;
9. libera novamente o campo de mensagem;
10. mantém a sessão para a próxima interação.

---

## ⏳ Feedback Visual

Durante o processamento da mensagem, a interface apresenta um indicador animado.

Exemplo:

```text
● ● ● CardioIA está analisando...
```

Enquanto a requisição está sendo processada:

- o botão de envio é temporariamente desabilitado;
- o campo de mensagem é temporariamente bloqueado;
- o botão apresenta o texto `Enviando...`.

Depois que a resposta é recebida, os controles são habilitados novamente.

Isso evita múltiplos envios enquanto a requisição anterior ainda está sendo processada.

---

## ⚠️ Tratamento de Erros

O front-end possui tratamento para falhas na comunicação com o backend.

Caso o backend esteja indisponível ou ocorra algum problema durante a requisição, o usuário recebe uma mensagem diretamente no chat.

Exemplo:

```text
Não foi possível obter uma resposta do CardioIA.
```

Durante os testes, quando o backend não estava iniciado, a interface também identificou corretamente a falha de comunicação.

O tratamento contempla situações como:

- backend desligado;
- falha de comunicação;
- resposta inválida;
- erro retornado pela API;
- falha na integração externa.

---

## ⌨️ Recursos de Usabilidade

A interface possui recursos adicionais para melhorar a experiência do usuário.

### Envio com Enter

Pressionar:

```text
Enter
```

envia a mensagem.

### Quebra de Linha

Pressionar:

```text
Shift + Enter
```

permite inserir uma nova linha sem enviar a mensagem.

### Limite de Caracteres

O campo de mensagem aceita no máximo:

```text
1000 caracteres
```

Esse limite acompanha a validação existente no backend.

### Contador de Caracteres

A quantidade de caracteres digitada é atualizada automaticamente.

Exemplo:

```text
250 / 1000
```

### Ajuste Automático do Campo

O campo de texto aumenta de tamanho de acordo com a quantidade de conteúdo digitado, respeitando um limite máximo de altura.

---

## 🩺 Comunicação Responsável em Saúde

A interface apresenta permanentemente o aviso:

> **Importante:** O CardioIA oferece orientações iniciais e não substitui avaliação, diagnóstico ou atendimento realizado por profissionais de saúde.

Também é apresentada uma recomendação para que o usuário evite compartilhar informações pessoais sensíveis.

O CardioIA foi desenvolvido como um assistente de orientação inicial e não deve ser utilizado como substituto de profissionais de saúde.

---

## 📱 Responsividade

A interface foi preparada para funcionar em diferentes tamanhos de tela.

Foram adicionadas adaptações para:

- desktop;
- notebook;
- tablet;
- smartphone.

Em telas menores:

- a aplicação utiliza toda a área disponível;
- os espaçamentos são reduzidos;
- os balões das mensagens são ajustados;
- informações secundárias podem ser ocultadas;
- o botão de envio é redimensionado;
- a área do chat se adapta ao espaço disponível.

---

## 🔒 Segurança no Front-end

O front-end não contém credenciais do IBM Watson Assistant.

Informações como:

```text
WATSON_API_KEY
WATSON_URL
WATSON_ENVIRONMENT_ID
```

permanecem exclusivamente no backend.

As credenciais reais são configuradas através do arquivo:

```text
backend/.env
```

Esse arquivo não deve ser enviado para o GitHub.

O projeto utiliza:

```text
backend/.env.example
```

apenas como modelo para informar quais variáveis precisam ser configuradas.

Dessa forma, o navegador se comunica somente com o backend Flask e não recebe diretamente as credenciais do Watson.

---

## ▶️ Como Executar o Projeto

Para testar a interface completa, é necessário iniciar o backend e o front-end simultaneamente.

### 1. Ativar o ambiente virtual

No Windows PowerShell, caso a execução do ambiente virtual esteja bloqueada, pode ser necessário utilizar:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
```

Depois, ative o ambiente virtual do projeto:

```powershell
.\.venv\Scripts\Activate.ps1
```

Quando estiver ativo, o terminal deverá apresentar algo semelhante a:

```text
(.venv)
```

---

### 2. Entrar na pasta raiz correta do projeto

É necessário estar na pasta que contém:

```text
backend
frontend
watson-assistant
README.md
```

Caso o projeto tenha sido baixado como ZIP e exista uma pasta interna com o mesmo nome, entre nela antes de executar o backend.

Exemplo:

```powershell
cd .\Assistente-Cardiol-gico-Inteligente-main
```

---

### 3. Instalar as dependências do backend

Na raiz do projeto:

```bash
pip install -r backend/requirements.txt
```

---

### 4. Iniciar o Backend

Ainda na raiz do projeto:

```bash
python -m backend.app
```

O backend ficará disponível em:

```text
http://127.0.0.1:5000
```

O terminal deverá permanecer aberto enquanto o projeto estiver sendo utilizado.

---

### 5. Verificar o Backend

O health check pode ser acessado em:

```text
http://127.0.0.1:5000/health
```

Quando o backend está funcionando e o IBM Watson está configurado, a resposta apresenta:

```json
{
  "service": "CardioIA Backend API",
  "status": "healthy",
  "version": "1.0.0",
  "watson_configured": true
}
```

O campo:

```text
"watson_configured": true
```

indica que as configurações necessárias para a integração com o Watson foram carregadas pelo backend.

---

### 6. Iniciar o Front-end

O backend deve continuar funcionando no primeiro terminal.

Abra um segundo terminal e entre na pasta:

```bash
cd frontend
```

Depois execute:

```bash
python -m http.server 5500
```

O front-end ficará disponível em:

```text
http://127.0.0.1:5500
```

---

## 🖥️ Terminais Necessários

Durante a execução local, são utilizados dois terminais.

### Terminal 1 — Backend

```bash
python -m backend.app
```

Executando em:

```text
http://127.0.0.1:5000
```

### Terminal 2 — Front-end

```bash
cd frontend
python -m http.server 5500
```

Executando em:

```text
http://127.0.0.1:5500
```

Os dois devem permanecer abertos durante o teste.

---

## 🧪 Teste Funcional Realizado

A integração foi validada utilizando uma interação real com o sistema.

Fluxo utilizado:

```text
Usuário:
Olá

CardioIA:
Eu não entendi. Você pode tentar reformular a frase.

Usuário:
Estou sentindo dor no peito

CardioIA:
Entendi que você está sentindo algo.
Pode me dizer a intensidade — leve, moderada ou forte?

Usuário:
Forte

CardioIA:
Isso que você descreveu pode ser sério.
Recomendo buscar atendimento médico imediatamente
ou procurar o pronto-socorro mais próximo.
Não estou apto a fazer diagnósticos.
```

O primeiro retorno para a mensagem `Olá` está relacionado à configuração conversacional do assistente e não representa uma falha do front-end.

O fluxo de sintomas foi concluído corretamente.

---

## ✅ O Que o Teste Confirmou

O teste funcional confirmou:

- envio da mensagem pelo front-end;
- comunicação HTTP com o backend Flask;
- funcionamento do endpoint `/api/chat`;
- integração do backend com o IBM Watson Assistant;
- recebimento da resposta;
- armazenamento do `session_id`;
- continuidade da conversa;
- interpretação da mensagem `Forte` dentro do contexto anterior;
- exibição da resposta na interface;
- funcionamento do indicador de carregamento;
- funcionamento do tratamento de erros.

O fluxo completo validado foi:

```text
Front-end
    ↓
Backend Flask
    ↓
IBM Watson Assistant
    ↓
Backend Flask
    ↓
Front-end
```

---

## ✅ Funcionalidades Implementadas

- [x] Interface web do CardioIA
- [x] Área de conversa
- [x] Mensagem inicial do assistente
- [x] Campo para digitação
- [x] Botão de envio
- [x] Exibição das mensagens do usuário
- [x] Exibição das respostas do CardioIA
- [x] Integração com backend Flask
- [x] Comunicação indireta com IBM Watson Assistant
- [x] Envio através de `POST /api/chat`
- [x] Recebimento de respostas em JSON
- [x] Armazenamento do `session_id`
- [x] Continuidade da conversa
- [x] Indicador de processamento
- [x] Estado `Enviando...`
- [x] Bloqueio temporário durante o processamento
- [x] Tratamento de erros
- [x] Limite de 1000 caracteres
- [x] Contador de caracteres
- [x] Ajuste automático do campo de texto
- [x] Enter para envio
- [x] Shift + Enter para quebra de linha
- [x] Aviso médico
- [x] Aviso sobre informações pessoais sensíveis
- [x] Interface responsiva
- [x] Adaptação para dispositivos móveis
- [x] Teste funcional de ponta a ponta

---

## 📌 Responsabilidade no Projeto

A responsabilidade desta etapa foi desenvolver a área de **Interface e Experiência do Usuário**.

O trabalho realizado concentrou-se principalmente nos arquivos:

```text
frontend/index.html
frontend/style.css
frontend/script.js
```

As atividades incluíram:

- desenvolvimento da estrutura da página;
- criação da identidade visual;
- construção do chat;
- experiência de interação;
- integração da interface com a API;
- gerenciamento de sessão no front-end;
- tratamento de carregamento e erros;
- responsividade;
- realização de testes de integração.

A configuração dos fluxos e intenções do IBM Watson Assistant e o desenvolvimento principal da API Flask pertencem às demais áreas do projeto, porém foram utilizados e testados durante a integração do front-end.

---

## 📌 Resultado Final

O front-end desenvolvido transforma o CardioIA em uma aplicação acessível ao usuário final, permitindo uma interação conversacional simples, organizada e funcional.

A solução integra:

```text
Experiência do Usuário
        +
HTML
        +
CSS
        +
JavaScript
        +
Fetch API
        +
Backend Flask
        +
IBM Watson Assistant
```

O resultado é um protótipo funcional de **Assistente Cardiológico Conversacional**, permitindo que o usuário envie mensagens em linguagem natural e visualize as respostas processadas pelo sistema.

A integração foi testada com sucesso, incluindo uma conversa contextual na qual o usuário informou um sintoma e, em seguida, apenas sua intensidade, demonstrando a manutenção da sessão e da continuidade da interação.
