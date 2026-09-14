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
- **Fetch API** — comunicação com o backend Flask.

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
