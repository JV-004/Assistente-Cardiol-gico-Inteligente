import requests

from backend.config import Config


class WatsonService:
    """
    Serviço responsável pela comunicação entre o backend
    CardioIA e a API REST do IBM Watson Assistant.
    """

    def __init__(self):
        """
        Inicializa o serviço utilizando exclusivamente
        variáveis de ambiente carregadas pela classe Config.
        """

        Config.validate_watson_config()

        self.api_key = Config.WATSON_API_KEY
        self.service_url = Config.WATSON_URL.rstrip("/")
        self.environment_id = Config.WATSON_ENVIRONMENT_ID
        self.version = Config.WATSON_VERSION

        self.auth = (
            "apikey",
            self.api_key
        )

        self.timeout = 15


    def create_session(self):
        """
        Cria uma nova sessão conversacional no
        IBM Watson Assistant.

        Returns:
            str: identificador da sessão criada.

        Raises:
            requests.exceptions.RequestException:
                caso ocorra falha de comunicação com a API.
        """

        url = (
            f"{self.service_url}/v2/assistants/"
            f"{self.environment_id}/sessions"
        )

        response = requests.post(
            url,
            params={
                "version": self.version
            },
            auth=self.auth,
            timeout=self.timeout
        )

        response.raise_for_status()

        data = response.json()

        session_id = data.get("session_id")

        if not session_id:
            raise RuntimeError(
                "O Watson Assistant não retornou um session_id."
            )

        return session_id


    def send_message(self, session_id, message):
        """
        Envia uma mensagem para uma sessão existente
        no IBM Watson Assistant.

        Args:
            session_id (str):
                identificador da sessão ativa.

            message (str):
                texto enviado pelo usuário.

        Returns:
            dict:
                resposta completa retornada pela API do Watson.

        Raises:
            ValueError:
                caso session_id ou message sejam inválidos.

            requests.exceptions.RequestException:
                caso ocorra falha de comunicação com a API.
        """

        if not isinstance(session_id, str) or not session_id.strip():
            raise ValueError(
                "session_id deve ser uma string válida."
            )

        if not isinstance(message, str) or not message.strip():
            raise ValueError(
                "message deve ser uma string válida."
            )

        url = (
            f"{self.service_url}/v2/assistants/"
            f"{self.environment_id}/sessions/"
            f"{session_id.strip()}/message"
        )

        payload = {
            "input": {
                "message_type": "text",
                "text": message.strip()
            }
        }

        response = requests.post(
            url,
            params={
                "version": self.version
            },
            json=payload,
            auth=self.auth,
            timeout=self.timeout
        )

        response.raise_for_status()

        return response.json()