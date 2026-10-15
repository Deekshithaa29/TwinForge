from app.api.dependencies import get_application
from app.core.container import application


def test_get_application_returns_shared_instance():
    assert get_application() is application


def test_websocket_manager_is_shared():
    resolved_application = get_application()

    assert (
        resolved_application.websocket_manager
        is application.websocket_manager
    )