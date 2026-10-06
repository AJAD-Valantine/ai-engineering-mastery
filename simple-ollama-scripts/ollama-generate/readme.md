# Ollama Generate

A small Python project for learning how to interact with Ollama's local HTTP API using `requests`.

## What I Built

Two versions of the same basic LLM interaction:

* `without-stream.py` — waits for the complete response before printing it.
* `with-stream.py` — receives and prints the generated response progressively using streaming.

## How It Works

The Python program sends a `POST` request to Ollama's `/api/generate` endpoint:

### Without Streaming

The complete response is returned at once.

```text
Prompt → Ollama → Complete response
```

### With Streaming

Ollama sends the generated response in chunks, which are processed and printed as they arrive.

```text
Prompt → Ollama
             ↓
        chunk → print
        chunk → print
        chunk → print
             ↓
          complete
```

## Concepts Learned

* HTTP POST requests
* API endpoints
* JSON request bodies
* HTTP status codes
* Ollama's `/api/generate` endpoint
* Python `requests`
* JSON response parsing
* Streaming HTTP responses
* NDJSON-style streamed responses
* Difference between streaming and non-streaming LLM responses