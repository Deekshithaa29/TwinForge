from unittest.mock import MagicMock, patch

import pytest

from app.core.application import Application


@pytest.fixture
def app():
    with (
        patch(
            "app.core.application.RULModelPersistence.load",
            return_value=MagicMock(),
        ),
        patch(
            "app.core.application.MQTTPublisher",
        ),
        patch(
            "app.core.application.SQLiteDatabase",
        ),
        patch(
            "app.core.application.create_schema",
        ),
    ):
        application = Application()

    application.simulation.start = MagicMock()
    application.publisher = MagicMock()
    application.database = MagicMock()

    return application


def test_application_start_is_idempotent(app):
    app.start()
    app.start()

    assert app.publisher.connect.call_count == 1

    app.stop()


def test_application_stop_is_idempotent(app):
    app.start()
    app.stop()
    app.stop()

    assert app.publisher.disconnect.call_count == 1
    assert app.database.close.call_count == 1


def test_closed_application_cannot_restart(app):
    app.start()
    app.stop()

    with pytest.raises(RuntimeError):
        app.start()