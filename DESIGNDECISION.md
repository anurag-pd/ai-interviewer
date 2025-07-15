# Design Decisions

## Time Constraint

This project was completed under a strict 2-day deadline. All technology and tool choices were made to maximize productivity, leverage existing knowledge, and ensure rapid delivery of a robust, full-stack AI-powered interview platform.

## Technology Choices & Rationale

### Backend: Python (FastAPI)

- **Why:** FastAPI is one of the fastest ways to build modern, async REST APIs in Python. It has excellent documentation, automatic OpenAPI docs, and is easy to use for rapid prototyping.
- **Alternatives considered:** Flask (slower for async, less modern), Django (overkill for API-only, slower to set up).
- **Result:** Allowed quick API development and easy integration with AI/ML libraries.

### Vector Store: ChromaDB (via LangChain)

- **Why:** ChromaDB is a simple, open-source vector database that integrates seamlessly with LangChain and HuggingFace. It is easy to set up locally and requires no cloud account or complex infra.
- **Alternatives considered:** Pinecone, Weaviate (require cloud setup, more time to configure).
- **Result:** Enabled fast, local semantic search for interview questions.

### Embeddings: HuggingFace (sentence-transformers)

- **Why:** HuggingFace provides high-quality, open-source embedding models that work out-of-the-box. No API key or cloud setup required.
- **Alternatives considered:** OpenAI embeddings (require API key, cost, and network latency).
- **Result:** Local, fast, and free embeddings for semantic search.

### AI Follow-up: Groq API

- **Why:** Groq API provides fast, reliable LLM completions and is easy to use as a drop-in replacement for OpenAI. The API key was available and setup was minimal.
- **Alternatives considered:** OpenAI (rate limits, cost), local LLMs (not feasible in 2 days).
- **Result:** Enabled AI-powered follow-up questions with minimal integration effort.

### Frontend: Vue 3 (Vite, Pinia)

- **Why:** Vue 3 with Vite offers a fast, modern SPA development experience. Pinia is the recommended state management for Vue 3. Vue is easy to learn, has great documentation, and is productive for rapid UI development.
- **Alternatives considered:** React (more boilerplate, slower to scaffold), Angular (steeper learning curve).
- **Result:** Allowed building a clean, modern UI quickly.

### Admin Panel: SPA Route

- **Why:** Building the admin panel as a route in the same Vue SPA allowed code reuse, fast development, and a consistent look and feel.
- **Alternatives considered:** Separate app (more setup, more time).
- **Result:** Fastest way to deliver required admin features.

### Tooling: Vite, npm, PowerShell/Bash scripts

- **Why:** Vite is the fastest way to scaffold and build Vue 3 apps. npm is standard for JS dependencies. PowerShell and Bash scripts automate setup and running, saving time and reducing manual errors.
- **Alternatives considered:** Manual setup (slower, error-prone).
- **Result:** Enabled quick onboarding and repeatable setup for any user.

### Summary

All tools and frameworks were chosen for their speed, ease of use, and minimal setup, allowing delivery of a robust, full-stack AI interviewer platform within 2 days.
