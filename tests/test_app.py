import asyncio
import time

from fastapi.testclient import TestClient

import main


class FakeMessage:
    content = "Generated ad copy"


class FakeChoice:
    message = FakeMessage()


class FakeCompletion:
    choices = [FakeChoice()]


class FakeCompletions:
    async def create(self, **kwargs):
        await asyncio.sleep(0.1)
        return FakeCompletion()


class FakeChat:
    completions = FakeCompletions()


class FakeOpenAIClient:
    chat = FakeChat()

    async def close(self):
        return None


client = TestClient(main.app)


def test_homepage_is_served():
    response = client.get("/")

    assert response.status_code == 200
    assert "AdGenius" in response.text


def test_health_check():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_validates_empty_inputs():
    response = client.post(
        "/generate",
        json={"business_name": "", "product": "", "language": "az"},
    )

    assert response.status_code == 422


def test_generate_runs_platform_calls_concurrently(monkeypatch):
    monkeypatch.setattr(main, "get_openai_client", lambda: FakeOpenAIClient())

    started_at = time.perf_counter()
    response = client.post(
        "/generate",
        json={
            "business_name": "Luna Coffee",
            "product": "Yulaf südlü latte",
            "language": "az",
        },
    )
    elapsed = time.perf_counter() - started_at

    assert response.status_code == 200
    assert response.json() == {
        "instagram": "Generated ad copy",
        "facebook": "Generated ad copy",
        "tiktok": "Generated ad copy",
    }
    assert elapsed < 0.25
