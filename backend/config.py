import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent

load_dotenv(BASE_DIR / ".env")


class Config:
    """
    Configurações centralizadas do backend CardioIA.

    As credenciais do IBM Watson Assistant são carregadas
    exclusivamente por variáveis de ambiente.
    """

    WATSON_API_KEY = os.getenv("WATSON_API_KEY")
    WATSON_URL = os.getenv("WATSON_URL")
    WATSON_ENVIRONMENT_ID = os.getenv("WATSON_ENVIRONMENT_ID")
    WATSON_VERSION = os.getenv(
        "WATSON_VERSION",
        "2021-11-27"
    )

    FLASK_ENV = os.getenv(
        "FLASK_ENV",
        "development"
    )

    @classmethod
    def validate_watson_config(cls):
        """
        Valida as configurações necessárias para comunicação
        com o IBM Watson Assistant.
        """

        required_variables = {
            "WATSON_API_KEY": cls.WATSON_API_KEY,
            "WATSON_URL": cls.WATSON_URL,
            "WATSON_ENVIRONMENT_ID": cls.WATSON_ENVIRONMENT_ID,
        }

        missing_variables = [
            name
            for name, value in required_variables.items()
            if not value
        ]

        if missing_variables:
            raise ValueError(
                "Variáveis de ambiente ausentes: "
                + ", ".join(missing_variables)
            )

        return True