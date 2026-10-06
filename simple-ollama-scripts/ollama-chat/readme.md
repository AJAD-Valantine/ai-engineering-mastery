# Ollama Chat

A small collection of Python scripts for learning how to build a chat application using Ollama's `/api/chat` HTTP endpoint.

The scripts progressively introduce conversation history, streaming, system messages, and basic CLI chat functionality.

## What I Built

### `ask-and-answer.py`

A basic one-shot chat request.

```text
You → /api/chat → Ollama → Response
```

* Sends one user message.
* Receives one complete response.
* No conversation history.
* No streaming.

**Concepts:** API requests, `/api/chat`, `messages`, user/assistant roles.

---

### `chat-history.py`

A multi-turn conversation with manually maintained message history.

```text
You: My name is Alex.
AI: Nice to meet you, Alex!

You: What is my name?
AI: Your name is Alex.
```

The program stores both user and assistant messages and sends the complete conversation history with each request.

**Concepts:** conversation history, message roles, maintaining context.

---

### `streaming-chat.py`

A multi-turn chat that streams the model's response as it is generated.

Instead of waiting for the complete response:

```text
AI: [wait...]
AI: Here is the complete response...
```

the response appears progressively:

```text
AI: Here is the...
```

The streamed chunks are also combined into a complete assistant message before being added to the conversation history.

**Concepts:** streaming responses, JSON chunks, `iter_lines()`, maintaining streamed response history.

---

### `system-message.py`

Adds a system message that defines the model's behavior.

Example:

```text
System: You are a computer science professor.
```

The system message is kept at the beginning of the conversation while user and assistant messages are added afterward.

**Concepts:** system messages, model behavior, message roles, combining system prompts with conversation history.

---

### `cli-chatbot.py`

A simple terminal chatbot that combines the concepts from the previous scripts.

Supported commands:

```text
/new
/exit
```

Example:

```text
Welcome to a new chat!

You: What is Python?
Bot: Python is a programming language...

You: What is FastAPI?
Bot: FastAPI is a Python web framework...
```

`/new` starts a fresh conversation while preserving the system prompt.

`/exit` closes the application.

**Concepts:** CLI interaction, conversation state, streaming, system messages, starting new conversations.


## Main Idea
- Understand what happens underneath an LLM chat library before using higher-level abstractions.


## What I Learned

* How to call Ollama's `/api/chat` endpoint.
* How chat messages are represented using `role` and `content`.
* How conversation history provides context to the model.
* How streaming responses work.
* How streamed JSON chunks can be processed.
* How system messages influence model behavior.
* How to maintain basic chat state in a Python application.
* How a simple chatbot can be built directly on top of an HTTP API.