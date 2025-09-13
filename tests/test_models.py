import pytest
from bria.models import (
    BaseResult,
    RemoveBackgroundResult,
    StatusResult,
    StatusSuccessResult,
    StatusErrorResult,
)
from bria.constants import (
    STATUS_KEY,
    REQUEST_ID_KEY,
    RESULT_KEY,
    IMAGE_URL_KEY,
    ERROR_KEY,
    SEED_KEY,
    PROMPT_KEY,
    REFINED_PROMPT_KEY,
)


def test_base_result_stores_raw_json():
    raw = {"foo": "bar"}
    result = BaseResult(raw_json=raw)
    assert result.raw_json == raw


def test_remove_background_result_fields():
    raw = {
        RESULT_KEY: {IMAGE_URL_KEY: "http://image.png"},
        REQUEST_ID_KEY: "123",
    }
    result = RemoveBackgroundResult(
        raw_json=raw,
        url=raw[RESULT_KEY][IMAGE_URL_KEY],
        request_id=raw[REQUEST_ID_KEY],
    )
    assert result.url == "http://image.png"
    assert result.request_id == "123"
    assert result.raw_json == raw


def test_status_result_fields():
    raw = {
        STATUS_KEY: "processing",
        REQUEST_ID_KEY: "abc123",
    }
    result = StatusResult(
        raw_json=raw,
        status=raw[STATUS_KEY],
        request_id=raw[REQUEST_ID_KEY],
    )
    assert result.status == "processing"
    assert result.request_id == "abc123"


def test_status_success_result_fields():
    raw = {
        STATUS_KEY: "success",
        REQUEST_ID_KEY: "req-1",
        RESULT_KEY: {IMAGE_URL_KEY: "http://img.png"},
        SEED_KEY: 42,
        PROMPT_KEY: "a cat",
        REFINED_PROMPT_KEY: "a cute cat",
    }
    result = StatusSuccessResult(
        raw_json=raw,
        status=raw[STATUS_KEY],
        request_id=raw[REQUEST_ID_KEY],
        url=raw[RESULT_KEY][IMAGE_URL_KEY],
        seed=raw[SEED_KEY],
        prompt=raw[PROMPT_KEY],
        refined_prompt=raw[REFINED_PROMPT_KEY],
    )
    assert result.status == "success"
    assert result.url == "http://img.png"
    assert result.seed == 42
    assert result.prompt == "a cat"
    assert result.refined_prompt == "a cute cat"


def test_status_error_result_fields():
    raw = {
        STATUS_KEY: "error",
        REQUEST_ID_KEY: "req-err",
        ERROR_KEY: {"message": "something went wrong"},
    }
    result = StatusErrorResult(
        raw_json=raw,
        status=raw[STATUS_KEY],
        request_id=raw[REQUEST_ID_KEY],
        error=raw[ERROR_KEY],
    )
    assert result.status == "error"
    assert result.error["message"] == "something went wrong"
    assert result.request_id == "req-err"
