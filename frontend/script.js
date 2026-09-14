const API_URL = "http://127.0.0.1:5000/api/chat";

let sessionId = null;

// Elementos da interface
const chat = document.getElementById("chat");
const chatForm = document.getElementById("chatForm");
const messageInput = document.getElementById("messageInput");
const sendButton = document.getElementById("sendButton");
const typingIndicator = document.getElementById("typingIndicator");
const characterCount = document.getElementById("characterCount");


// ============================================================
// COMUNICAÇÃO COM O BACKEND
// ============================================================

async function enviarMensagem(message) {
    const payload = {
        message: message
    };

    // Mantém a mesma sessão durante a conversa
    if (sessionId) {
        payload.session_id = sessionId;
    }

    const response = await fetch(API_URL, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    let data;

    try {
        data = await response.json();
    } catch {
        throw new Error(
            "O servidor retornou uma resposta inválida."
        );
    }

    if (!response.ok || !data.success) {
        throw new Error(
            data.error || "Não foi possível enviar a mensagem."
        );
    }

    // Guarda a sessão para as próximas mensagens
    sessionId = data.session_id;

    return data.response;
}


// ============================================================
// MENSAGENS NA TELA
// ============================================================

function adicionarMensagem(texto, tipo) {
    const message = document.createElement("div");

    message.classList.add(
        "message",
        tipo === "user"
            ? "user-message"
            : "bot-message"
    );

    const messageContent = document.createElement("div");
    messageContent.classList.add("message-content");

    const author = document.createElement("span");
    author.classList.add("message-author");

    const bubble = document.createElement("div");
    bubble.classList.add("message-bubble");

    // textContent evita interpretar HTML enviado nas mensagens
    bubble.textContent = texto;

    if (tipo === "user") {
        author.textContent = "Você";

        messageContent.appendChild(author);
        messageContent.appendChild(bubble);
        message.appendChild(messageContent);
    } else {
        const avatar = document.createElement("div");

        avatar.classList.add(
            "avatar",
            "bot-avatar"
        );

        avatar.textContent = "♥";
        author.textContent = "CardioIA";

        messageContent.appendChild(author);
        messageContent.appendChild(bubble);

        message.appendChild(avatar);
        message.appendChild(messageContent);
    }

    chat.appendChild(message);

    rolarParaFinal();
}


// ============================================================
// LOADING
// ============================================================

function mostrarCarregamento() {
    typingIndicator.classList.remove("hidden");
    rolarParaFinal();
}

function esconderCarregamento() {
    typingIndicator.classList.add("hidden");
}


// ============================================================
// CONTROLE DO FORMULÁRIO
// ============================================================

function alterarEstadoEnvio(enviando) {
    sendButton.disabled = enviando;
    messageInput.disabled = enviando;

    sendButton.textContent = enviando
        ? "Enviando..."
        : "Enviar";
}


// ============================================================
// ROLAGEM DO CHAT
// ============================================================

function rolarParaFinal() {
    requestAnimationFrame(() => {
        chat.scrollTop = chat.scrollHeight;
    });
}


// ============================================================
// CONTADOR DE CARACTERES
// ============================================================

function atualizarContador() {
    const quantidade = messageInput.value.length;

    characterCount.textContent =
        `${quantidade} / 1000`;
}


// ============================================================
// AJUSTE AUTOMÁTICO DO TEXTAREA
// ============================================================

function ajustarAlturaCampo() {
    messageInput.style.height = "auto";

    messageInput.style.height =
        `${Math.min(messageInput.scrollHeight, 130)}px`;
}


// ============================================================
// ENVIO DO FORMULÁRIO
// ============================================================

chatForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const message = messageInput.value.trim();

    if (!message) {
        return;
    }

    if (message.length > 1000) {
        adicionarMensagem(
            "A mensagem deve possuir no máximo 1000 caracteres.",
            "bot"
        );

        return;
    }

    // Mostra imediatamente a mensagem do usuário
    adicionarMensagem(message, "user");

    // Limpa o campo
    messageInput.value = "";

    atualizarContador();
    ajustarAlturaCampo();

    alterarEstadoEnvio(true);
    mostrarCarregamento();

    try {
        const resposta = await enviarMensagem(message);

        esconderCarregamento();

        adicionarMensagem(
            resposta,
            "bot"
        );

    } catch (error) {
        esconderCarregamento();

        console.error(
            "Erro ao comunicar com o CardioIA:",
            error
        );

        adicionarMensagem(
            `Não foi possível obter uma resposta do CardioIA. ${error.message}`,
            "bot"
        );

    } finally {
        alterarEstadoEnvio(false);

        messageInput.focus();
    }
});


// ============================================================
// ENTER PARA ENVIAR
// SHIFT + ENTER PARA QUEBRA DE LINHA
// ============================================================

messageInput.addEventListener("keydown", (event) => {
    if (
        event.key === "Enter" &&
        !event.shiftKey
    ) {
        event.preventDefault();

        if (!sendButton.disabled) {
            chatForm.requestSubmit();
        }
    }
});


// ============================================================
// ALTERAÇÕES NO CAMPO
// ============================================================

messageInput.addEventListener("input", () => {
    atualizarContador();
    ajustarAlturaCampo();
});


// ============================================================
// INICIALIZAÇÃO
// ============================================================

atualizarContador();
messageInput.focus();
