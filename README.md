# Bria Python SDK

A lightweight Python SDK for the [Bria API](https://bria.ai).  
It provides simple methods to remove image backgrounds, check job statuses, and handle API responses.

---

## Installation

Using [uv](https://docs.astral.sh/uv/):

```bash
uv add bria-sdk
```

Or with pip:

```bash
pip install bria-sdk
```

---

## Authentication

You need an API token from Bria.

Set it as an environment variable:

```bash
export BRIA_API_TOKEN="your_api_token_here"
```

Or pass it directly when creating the client:

```python
from bria.client import Bria

client = Bria(api_token="your_api_token_here")
```

---

## Usage

### 1. Remove Background (Sync)

```python
from bria.client import Bria

client = Bria(api_token="your_api_token_here")

result = client.rmbg.remove_background(
    "https://example.com/image.png",
    sync=True
)

print("Processed image:", result.url)
print("Full response:", result.raw_json)
```

---

### 2. Remove Background (Async + Polling)

```python
import time
from bria.client import Bria

client = Bria(api_token="your_api_token_here")

# Submit async job
job = client.rmbg.remove_background(
    "https://example.com/image.png",
    sync=False
)

print("Job submitted:", job.request_id)

# Poll for completion
while True:
    status = client.status.get_status(job.request_id)

    if status.status == "COMPLETED":
        print("Done:", status.url)
        break
    elif status.status == "ERROR":
        print("Failed:", status.error)
        break
    else:
        print("In progress...")
        time.sleep(2)
```

---

### 3. Check Job Status

```python
from bria.client import Bria

client = Bria(api_token="your_api_token_here")

status = client.status.get_status("req_123")

if status.status == "COMPLETED":
    print("Done:", status.url)
elif status.status == "ERROR":
    print("Failed:", status.error)
else:
    print("Still running...")
```

---

### 4. Error Handling

```python
from bria.exceptions import BriaError, NotFoundError
from bria.client import Bria

client = Bria(api_token="your_api_token_here")

try:
    client.status.get_status("invalid_id")
except NotFoundError as e:
    print("Request not found:", e)
except BriaError as e:
    print("API error:", e)
```

---

## Testing

Run all tests with:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=bria --cov-report=term-missing
```

---

## Contributing

1. Clone this repo  
2. Install dependencies:

   ```bash
   uv sync
   ```

3. Run checks:

   ```bash
   uv run black .
   uv run ruff check .
   uv run mypy src
   ```

4. Open a pull request 🎉

---

## License

MIT – see [LICENSE](LICENSE) for details.
