from types import SimpleNamespace

import pytest
from fastapi import HTTPException

from app.services.media.validation import AdminMediaUploadRequestValidator


class _DummyRequest:
    def __init__(self, content_length: str | None) -> None:
        self.headers = {}
        if content_length is not None:
            self.headers['content-length'] = content_length


def test_validate_payload_rejects_empty_upload() -> None:
    validator = AdminMediaUploadRequestValidator()

    with pytest.raises(HTTPException) as error:
        validator.validate_payload(file_bytes=b'', original_filename='image.png')

    assert error.value.status_code == 400


def test_validate_payload_requires_filename() -> None:
    validator = AdminMediaUploadRequestValidator()

    with pytest.raises(HTTPException) as error:
        validator.validate_payload(file_bytes=b'123', original_filename='   ')

    assert error.value.status_code == 400


def test_validate_request_rejects_invalid_visibility(monkeypatch: pytest.MonkeyPatch) -> None:
    validator = AdminMediaUploadRequestValidator()
    monkeypatch.setattr(
        'app.services.media.validation.enforce_rate_limit_or_429',
        lambda **_: None,
    )

    with pytest.raises(HTTPException) as error:
        validator.validate_request(_DummyRequest(None), admin_identifier='admin-1', visibility='secret')

    assert error.value.status_code == 400
