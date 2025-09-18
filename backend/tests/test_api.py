import asyncio
from unittest.mock import MagicMock, patch
import uuid
import pytest
from httpx import AsyncClient, ASGITransport
from main import app
from main import celery_app

@pytest.fixture(scope="session", autouse=True)
def configure_celery_for_tests():
    celery_app.conf.update(
        broker_url="memory://",
        result_backend="cache+memory://",
        task_always_eager=True,
    )

async def run_full_scan(ac: AsyncClient, url: str, suite: str):
    def mock_delay(*args, **kwargs):
        mock_result = MagicMock()
        mock_result.id = str(uuid.uuid4()) 
        return mock_result

    with patch("main.run_prompt.delay", side_effect=mock_delay) as mock_task, \
        patch("main.AsyncResult") as mock_async_result:

        # mocking the AsyncResult 
        mock_instance = MagicMock()
        mock_instance.ready.return_value = True
        mock_instance.result = {
            "response": {"agent_activity": [{"response": "mocked response"}]}
        }
        mock_async_result.return_value = mock_instance
        
        scan_request = await ac.post("/scan", json={"url": url, "suite": suite})
        assert scan_request.status_code == 200
        scan_id = scan_request.json()["scanId"]

        # wait until status is Finished
        for _ in range(80):
            scan_status = await ac.get(f"/status/{scan_id}")
            assert scan_status.status_code == 200
            status_data = scan_status.json()
            completed = float(status_data.get("completed", "0%").replace("%",""))
            if completed >= 100.0:
                break
            await asyncio.sleep(0.1)

        # only after status=Finished, get results
        scan_results = await ac.get(f"/results/{scan_id}")
        assert scan_results.status_code == 200
        results_data = scan_results.json()

        for result in results_data["results"]:
            assert result.get("status") == "Finished"
            assert isinstance(result.get("response"), str)
            assert result["response"] != ""

@pytest.mark.asyncio
async def test_scans():
    transport = ASGITransport(app=app)
    # run 3 tests async
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        await asyncio.gather(
            run_full_scan(ac, "https://tryme.tendry.net/chat", "Data Leak"),
            run_full_scan(ac, "https://tryme.tendry.net/chat", "Jail Break"),
            run_full_scan(ac, "https://tryme.tendry.net/chat", "Persuasion"),
        )

@pytest.mark.asyncio
async def test_get_all_scans_and_suites():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        scans = await ac.get("/scans")
        assert scans.status_code == 200
        assert isinstance(scans.json(), list)

        suites = await ac.get("/suites")
        assert suites.status_code == 200
        assert isinstance(suites.json(), list)