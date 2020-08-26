# opentelemetry-issue

## How to run

You need to run two applications: `A` and `B`. This can be done like that:

```
# Install dependencies
poetry install
```

Run a:

```
.venv/bin/uvicorn app_a:app --port=8000 --reload
```

Run b:

```
.venv/bin/uvicorn app_b:app --port=8001 --reload
```

Then navigate to `http://localhost:8000` in your browser. If everything okay you should see welcome message.
