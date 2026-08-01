from app.core.application import Application
from app.core.container import application


def get_application() -> Application:
    """
    Returns the shared TwinForge application.
    """

    return application