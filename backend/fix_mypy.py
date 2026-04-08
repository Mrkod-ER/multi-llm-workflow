import os

def replace_in_file(path, old, new):
    if not os.path.exists(path): return
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace(old, new)
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)

# memory.py
replace_in_file('app/engine/memory.py', 'def __init__(self):', 'def __init__(self) -> None:')

# test_api.py
replace_in_file('tests/test_api.py', 'def test_health_check(client: TestClient):', 'def test_health_check(client: TestClient) -> None:')
replace_in_file('tests/test_api.py', 'def test_validate_cyclic_workflow(client: TestClient):', 'def test_validate_cyclic_workflow(client: TestClient) -> None:')
replace_in_file('tests/test_api.py', 'def test_validate_invalid_workflow(client: TestClient):', 'def test_validate_invalid_workflow(client: TestClient) -> None:')
replace_in_file('tests/test_api.py', 'def test_run_workflow(client: TestClient):', 'def test_run_workflow(client: TestClient) -> None:')
replace_in_file('tests/test_api.py', 'def test_list_models(client: TestClient):', 'def test_list_models(client: TestClient) -> None:')
replace_in_file('tests/test_api.py', 'def test_sync_models(client: TestClient):', 'def test_sync_models(client: TestClient) -> None:')

# middleware.py
replace_in_file('app/middleware.py', 'async def dispatch(self, request: Request, call_next: RequestResponseEndpoint):', 'async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:')

# redis_client.py
replace_in_file('app/services/redis_client.py', 'def __new__(cls):', 'def __new__(cls) -> "RedisClient":')
replace_in_file('app/services/redis_client.py', 'async def connect(self):', 'async def connect(self) -> None:')

# providers
replace_in_file('app/providers/openai.py', 'def __init__(self, model_name: str = "gpt-3.5-turbo"):', 'def __init__(self, model_name: str = "gpt-3.5-turbo") -> None:')
replace_in_file('app/providers/ollama.py', 'def __init__(self, model_name: str = "llama3"):', 'def __init__(self, model_name: str = "llama3") -> None:')

# factory.py abstract Error (this happens because mock.py inherits BaseLLMProvider but base.py yields). It's complaining we are instantiating abstract class directly? No, Factory returns MockProvider which has generate_stream returning async generator. Wait, MockProvider generates correctly right? My previous regex didn\'t catch that.
replace_in_file('app/providers/mock.py', 'async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:\n        yield "mock"\n', 'async def generate_stream(self, request: LLMRequest) -> AsyncGenerator[str, None]:\n        yield "mock"\n')

# models.py
replace_in_file('app/api/v1/models.py', 'async def sync_models():', 'async def sync_models() -> dict:')

# runners
replace_in_file('app/engine/runner.py', 'async def _execute_graph(self, queue):', 'async def _execute_graph(self, queue: asyncio.Queue) -> None:')
replace_in_file('app/engine/executors.py', 'stream_queue: asyncio.Queue | None = None', 'stream_queue: asyncio.Queue | None = None')

# workflows.py
replace_in_file('app/api/v1/workflows.py', 'async def validate_workflow(workflow: Workflow):', 'async def validate_workflow(workflow: Workflow) -> dict:')
replace_in_file('app/api/v1/workflows.py', '-> dict:', '-> dict:') # fixing any
