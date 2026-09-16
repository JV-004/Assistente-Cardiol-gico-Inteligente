import logging
import time
from threading import Lock
from uuid import uuid4

from flask import Flask, jsonify, request
from flask_cors import CORS
from requests.exceptions import RequestException

from backend.config import Config
from backend.services.watson_service import WatsonService


# ============================================================
# APLICAÇÃO
# ============================================================

app = Flask(__name__)

CORS(
    app,
    resources={
        r"/api/*": {
            "origins": "*"
        }
    }
)

app.config["JSON_SORT_KEYS"] = False


# ============================================================
# LOGS
# ============================================================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s"
)

logger = logging.getLogger("cardioia.backend")


# ============================================================
# CONTEXTO CONVERSACIONAL LOCAL
# ============================================================

# O Watson utilizado pelo grupo reconhece corretamente frases completas
# como "estou sentindo uma dor forte no peito", mas o fluxo exportado
# não preserva sozinho a intenção anterior quando o usuário responde
# apenas "forte", "leve" ou "moderada".
#
# Esta estrutura mantém somente o contexto mínimo necessário para
# complementar esse tipo de resposta curta.
#
# Em uma aplicação de produção, esse estado poderia ser armazenado
# em Redis ou banco de dados.

SESSION_CONTEXT = {}
SESSION_CONTEXT_LOCK = Lock()

CONTEXT_TTL_SECONDS = 1800  # 30 minutos

INTENSITY_VALUES = {
    "leve",
    "moderada",
    "forte"
}


# ============================================================
# FUNÇÕES AUXILIARES
# ============================================================

def cleanup_expired_contexts():
    """
    Remove contextos locais antigos para evitar acúmulo
    desnecessário de dados em memória.
    """

    now = time.time()

    with SESSION_CONTEXT_LOCK:
        expired_sessions = [
            session_id
            for session_id, context in SESSION_CONTEXT.items()
            if now - context.get("updated_at", now)
            > CONTEXT_TTL_SECONDS
        ]

        for session_id in expired_sessions:
            SESSION_CONTEXT.pop(session_id, None)


def extract_response_text(watson_response):
    """
    Extrai somente respostas textuais retornadas pelo Watson.
    """

    output = watson_response.get("output", {})
    generic_responses = output.get("generic", [])

    texts = []

    for item in generic_responses:
        if item.get("response_type") == "text":
            text = item.get("text")

            if text:
                texts.append(text)

    return "\n".join(texts)


def extract_nlu_metadata(watson_response):
    """
    Extrai intenção, confiança e entidades identificadas
    pelo processamento de linguagem natural do Watson.
    """

    output = watson_response.get("output", {})

    intents = output.get("intents", [])
    entities = output.get("entities", [])

    detected_intent = None
    confidence = None

    if intents:
        detected_intent = intents[0].get("intent")
        confidence = intents[0].get("confidence")

    formatted_entities = []

    for entity in entities:
        formatted_entities.append({
            "entity": entity.get("entity"),
            "value": entity.get("value"),
            "confidence": entity.get("confidence")
        })

    return {
        "intent": detected_intent,
        "confidence": confidence,
        "entities": formatted_entities
    }


def has_entity(metadata, entity_name):
    """
    Verifica se determinada entidade foi identificada pelo Watson.
    """

    return any(
        entity.get("entity") == entity_name
        for entity in metadata.get("entities", [])
    )


def validate_message_payload(data):
    """
    Valida o JSON recebido pelo endpoint /api/chat.

    Retorna:
        message
        session_id
        validation_error
    """

    if data is None:
        return None, None, (
            "Corpo da requisição ausente ou JSON inválido."
        )

    if not isinstance(data, dict):
        return None, None, (
            "O corpo da requisição deve ser um objeto JSON."
        )

    message = data.get("message")
    session_id = data.get("session_id")

    if not isinstance(message, str) or not message.strip():
        return None, None, (
            "O campo 'message' é obrigatório e deve conter texto."
        )

    message = message.strip()

    if len(message) > 1000:
        return None, None, (
            "A mensagem excede o limite de 1000 caracteres."
        )

    if session_id is not None:
        if not isinstance(session_id, str) or not session_id.strip():
            return None, None, (
                "O campo 'session_id', quando informado, "
                "deve conter um identificador válido."
            )

        session_id = session_id.strip()

    return message, session_id, None


def apply_conversation_context(session_id, message):
    """
    Aplica continuidade contextual para respostas curtas.

    Exemplo:

        Usuário:
        "Estou sentindo dor no peito"

        Watson:
        "Qual a intensidade?"

        Usuário:
        "forte"

    O backend transforma internamente a segunda mensagem em algo
    equivalente a:

        "Estou sentindo dor no peito. A intensidade é forte."

    A mensagem original enviada pelo usuário não é alterada
    na resposta da API.
    """

    normalized_message = message.strip().lower()

    if normalized_message not in INTENSITY_VALUES:
        return message, False

    with SESSION_CONTEXT_LOCK:
        context = SESSION_CONTEXT.get(session_id)

    if not context:
        return message, False

    if context.get("awaiting") != "intensidade":
        return message, False

    previous_message = context.get("previous_message")

    if not previous_message:
        return message, False

    contextualized_message = (
        f"{previous_message}. "
        f"A intensidade é {normalized_message}."
    )

    return contextualized_message, True


def update_conversation_context(
    session_id,
    original_message,
    response_text,
    metadata
):
    """
    Atualiza somente o contexto mínimo necessário
    para continuidade da conversa.
    """

    intent = metadata.get("intent")
    intensity_detected = has_entity(
        metadata,
        "intensidade"
    )

    waiting_for_intensity = (
        intent == "relatar_sintoma"
        and not intensity_detected
        and "intensidade" in response_text.lower()
    )

    with SESSION_CONTEXT_LOCK:

        if waiting_for_intensity:
            SESSION_CONTEXT[session_id] = {
                "awaiting": "intensidade",
                "previous_message": original_message,
                "updated_at": time.time()
            }

        elif intensity_detected:
            SESSION_CONTEXT.pop(
                session_id,
                None
            )


# ============================================================
# INFORMAÇÕES DA API
# ============================================================

@app.route("/", methods=["GET"])
def home():
    """
    Retorna informações públicas sobre o backend CardioIA.
    """

    return jsonify({
        "service": "CardioIA Backend API",
        "version": "1.0.0",
        "status": "online",
        "description": (
            "API responsável pela integração entre "
            "a interface do CardioIA e o IBM Watson Assistant."
        ),
        "features": [
            "Integração com IBM Watson Assistant",
            "Gerenciamento de sessão conversacional",
            "Extração de intenção e entidades NLP",
            "Validação de requisições",
            "Tratamento de falhas da API externa",
            "Continuidade contextual de respostas curtas"
        ],
        "endpoints": {
            "health": "GET /health",
            "create_session": "POST /api/session",
            "chat": "POST /api/chat"
        }
    }), 200


@app.route("/health", methods=["GET"])
def health():
    """
    Health check do backend.

    Não expõe API Key nem outros dados sensíveis.
    """

    watson_configured = all([
        Config.WATSON_API_KEY,
        Config.WATSON_URL,
        Config.WATSON_ENVIRONMENT_ID
    ])

    return jsonify({
        "status": "healthy",
        "service": "CardioIA Backend API",
        "version": "1.0.0",
        "watson_configured": watson_configured
    }), 200


# ============================================================
# SESSÃO
# ============================================================

@app.route("/api/session", methods=["POST"])
def create_session():
    """
    Cria uma nova sessão no IBM Watson Assistant.
    """

    request_id = str(uuid4())

    try:
        watson = WatsonService()

        session_id = watson.create_session()

        logger.info(
            "Sessão Watson criada | request_id=%s",
            request_id
        )

        return jsonify({
            "success": True,
            "session_id": session_id,
            "request_id": request_id
        }), 201

    except ValueError:

        logger.exception(
            "Configuração do Watson inválida | request_id=%s",
            request_id
        )

        return jsonify({
            "success": False,
            "error": (
                "Configuração do Watson Assistant incompleta."
            ),
            "request_id": request_id
        }), 500

    except RequestException:

        logger.exception(
            "Falha na criação da sessão Watson | request_id=%s",
            request_id
        )

        return jsonify({
            "success": False,
            "error": (
                "Não foi possível iniciar uma sessão "
                "com o Watson Assistant."
            ),
            "request_id": request_id
        }), 502

    except Exception:

        logger.exception(
            "Erro inesperado ao criar sessão | request_id=%s",
            request_id
        )

        return jsonify({
            "success": False,
            "error": "Erro interno do servidor.",
            "request_id": request_id
        }), 500


# ============================================================
# CHAT
# ============================================================

@app.route("/api/chat", methods=["POST"])
def chat():
    """
    Endpoint principal da aplicação.

    Fluxo:
        Front-end
        -> Flask
        -> validação
        -> contexto conversacional
        -> IBM Watson Assistant
        -> NLP
        -> resposta estruturada
        -> Front-end
    """

    request_id = str(uuid4())

    cleanup_expired_contexts()

    data = request.get_json(
        silent=True
    )

    message, session_id, validation_error = (
        validate_message_payload(data)
    )

    if validation_error:
        return jsonify({
            "success": False,
            "error": validation_error,
            "request_id": request_id
        }), 400

    try:
        watson = WatsonService()

        session_created = False

        if not session_id:
            session_id = watson.create_session()
            session_created = True

        watson_message, context_applied = (
            apply_conversation_context(
                session_id,
                message
            )
        )

        watson_response = watson.send_message(
            session_id,
            watson_message
        )

        response_text = extract_response_text(
            watson_response
        )

        metadata = extract_nlu_metadata(
            watson_response
        )

        if not response_text:
            response_text = (
                "O assistente processou a mensagem, "
                "mas não retornou uma resposta textual."
            )

        update_conversation_context(
            session_id=session_id,
            original_message=message,
            response_text=response_text,
            metadata=metadata
        )

        logger.info(
            (
                "Mensagem processada | "
                "request_id=%s | "
                "intent=%s | "
                "context_applied=%s"
            ),
            request_id,
            metadata["intent"],
            context_applied
        )

        return jsonify({
            "success": True,
            "session_id": session_id,
            "response": response_text,
            "analysis": {
                "intent": metadata["intent"],
                "confidence": metadata["confidence"],
                "entities": metadata["entities"]
            },
            "context": {
                "applied": context_applied,
                "session_created": session_created
            },
            "request_id": request_id
        }), 200

    except ValueError:

        logger.exception(
            "Configuração inválida | request_id=%s",
            request_id
        )

        return jsonify({
            "success": False,
            "error": (
                "Configuração do Watson Assistant incompleta."
            ),
            "request_id": request_id
        }), 500

    except RequestException:

        logger.exception(
            "Falha de comunicação com Watson | request_id=%s",
            request_id
        )

        return jsonify({
            "success": False,
            "error": (
                "Não foi possível comunicar com "
                "o Watson Assistant no momento."
            ),
            "request_id": request_id
        }), 502

    except Exception:

        logger.exception(
            "Erro inesperado no chat | request_id=%s",
            request_id
        )

        return jsonify({
            "success": False,
            "error": "Erro interno do servidor.",
            "request_id": request_id
        }), 500


# ============================================================
# ERROS HTTP
# ============================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": "Endpoint não encontrado."
    }), 404


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": (
            "Método HTTP não permitido para este endpoint."
        )
    }), 405


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": "Erro interno do servidor."
    }), 500


# ============================================================
# EXECUÇÃO LOCAL
# ============================================================

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=(Config.FLASK_ENV == "development")
    )