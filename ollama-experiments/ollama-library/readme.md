# Ollama Python

A collection of small Python scripts for learning how to interact with Ollama using the official Python library.
This project builds on the previous `ollama-generate` and `ollama-chat` projects, where the Ollama HTTP API was used directly with `requests`.

## What I Built

### `01_single_completion.py`

Makes a single request using `ollama.chat()` and prints the complete response.

```text"
Prompt
  ↓
ollama.chat()
  ↓
Complete response
```

**Concepts:** Ollama Python library, `ollama.chat()`, messages, model selection.

---

### `02_streaming.py`

Uses `stream=True` to receive and print the response progressively.

```text"
Prompt
  ↓
ollama.chat(stream=True)
  ↓
Chunk → print
Chunk → print
Chunk → print
```

**Concepts:** streaming with the Ollama Python library.

---

### `03_chat_loop.py`

Creates a basic multi-turn conversation by maintaining a `messages` list.

```text"
You: What is Python?
Bot: ...

You: What is FastAPI?
Bot: ...

You: Why use it?
Bot: ...
```

User and assistant messages are added to the conversation history after each turn.

**Concepts:** conversation history, message roles, streaming, chat loops.

---

### `04_system_prompt.py`

Adds a system message that defines the model's behavior.

Example:

```python"
{"role": "system", "content": "You are a computer science teacher"}
```

The system message remains in the conversation while user and assistant messages are added.

**Concepts:** system prompts, message roles, model behavior.

---

### `05_chatbot.py`

Combines the previous concepts into a simple terminal chatbot.

Supported commands:

```text"
/new  → clear the current conversation
/exit → exit the chatbot
```

The `/new` command resets the conversation while keeping the system prompt.

**Concepts:** chat state, conversation reset, system prompts, streaming, CLI interaction.


## Raw API vs Python Library

This project intentionally follows the previous raw HTTP projects.

### Raw HTTP

```text"
Python
  ↓
requests
  ↓
HTTP POST
  ↓
Ollama API
  ↓
Model
```

### Ollama Python Library

```text"
Python
  ↓
ollama library
  ↓
Ollama API
  ↓
Model
```

The Python library provides a higher-level interface so that HTTP request handling, response parsing, and other implementation details do not need to be handled manually.

## What I Learned

* How to use the Ollama Python library.
* How `ollama.chat()` works.
* How to pass chat messages to a model.
* How to stream model responses.
* How to maintain conversation history.
* How system messages affect model behavior.
* How to manage basic chat state.
* The difference between using an API directly and using an SDK/library abstraction.