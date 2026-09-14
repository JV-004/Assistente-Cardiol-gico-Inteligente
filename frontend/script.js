const API_URL = "http://127.0.0.1:5000/api/chat";

let sessionId = null;

async function enviarMensagem(message) {
    const payload = {
        message: message
    };

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

    const data = await response.json();

    if (!response.ok || !data.success) {
        throw new Error(
            data.error || "Não foi possível enviar a mensagem."
        );
    }

    sessionId = data.session_id;

    return data.response;
}
