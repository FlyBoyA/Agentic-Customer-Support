# Agentic Customer Support AI Assistant

An agentic AI-powered customer support assistant built using **Retrieval-Augmented Generation (RAG)**.  
The system retrieves relevant answers from a customer support knowledge base using semantic search and applies agentic decision-making to decide whether to:

- Answer directly from the knowledge base
- Ask the user for clarification
- Decline unsupported or out-of-scope requests

The project exposes a REST API using FastAPI and provides a simple React-based chat interface.

---

# Features

## Core Capabilities

-Retrieval-Augmented Generation (RAG) pipeline  
-Semantic search over customer support knowledge base  
-Local LLM inference using Ollama  
-Lightweight embedding model  
-Persistent vector database  
-Agentic decision-making logic  
-REST API interface  
-Web-based chat interface  
-Confidence-based response handling  
-Graceful fallback for unsupported queries  


---

# Architecture Overview


```
                    User
                     |
                     |
              React Frontend
                     |
                     |
              FastAPI REST API
                     |
                     |
            Agent Decision Engine
                     |
        +------------+-------------+
        |                          |
        |                          |
 Semantic Retrieval            Decision Logic
        |                          |
        |                          |
    ChromaDB                Answer / Clarify /Decline Decision
        |                 
        |
 BAAI/bge-small-en-v1.5
        |
 Knowledge Base


                     |
                     |
              Response Generator
                     |
                     |
             Ollama LLM Backend
                     |
                     |
             qwen2.5:0.5b
```

---

# Technology Stack

## Backend

| Component | Technology |
|---|---|
| API Framework | FastAPI |
| Programming Language | Python |
| Vector Database | ChromaDB |
| Embedding Model | BAAI/bge-small-en-v1.5 |
| LLM Runtime | Ollama |
| LLM Model | qwen2.5:0.5b |
| Data Validation | Pydantic |


## Frontend

| Component | Technology |
|-|-|
| Framework | React |
| Build Tool | Vite |
| Language | TypeScript |


---



# How the System Works

## 1. Knowledge Base Loading

At application startup:

1. The customer support dataset is loaded from:

```
data/knowledge_base.json
```

2. Documents are converted into vector embeddings.

3. Embeddings are stored inside ChromaDB.

---

## 2. Semantic Retrieval

When a user asks a question:

Example:

```
How can I reset my password?
```

The system:

1. Converts the query into an embedding.
2. Performs similarity search in ChromaDB.
3. Retrieves the most relevant knowledge base entries.

---

## 3. Agentic Decision Making

The assistant does not blindly answer every question.

The decision engine evaluates retrieval confidence.

### Decision Branch 1: Answer

If similarity score is above the confidence threshold:

```
similarity >= 0.55
```

The assistant generates an answer using retrieved context.

---

### Decision Branch 2: Clarification

If multiple results are similar or the query is ambiguous:

```
similarity between 0.40 - 0.55
```

The assistant asks a clarification question.


---

### Decision Branch 3: Decline

If the query is unsupported:

The assistant gracefully declines.


---

# Vector Database Choice

## ChromaDB

This project uses ChromaDB as the vector database.

### Why ChromaDB?

Advantages:

- Lightweight
- Easy local deployment
- Persistent storage support
- Native embedding function support
- Suitable for small and medium RAG applications


### Trade-offs

For larger production systems:

- Limited distributed scaling
- Less suitable for very large datasets
- Requires migration to systems such as:
  - Qdrant
  - Pinecone
  - Weaviate
  - pgvector


For this challenge, ChromaDB provides the right balance between simplicity and functionality.

---

# Embedding Model Choice

## BAAI/bge-small-en-v1.5

The project uses:

```
BAAI/bge-small-en-v1.5
```

Reasons:

- Open-source
- Lightweight
- Good semantic retrieval performance
- Small memory footprint
- Suitable for local execution


Embedding dimension:

```
384
```

---

# LLM Backend

## Ollama

The application uses Ollama for local LLM inference.

Model:

```
qwen2.5:0.5b
```

Reasons:

- Lightweight
- Runs locally
- No external API dependency
- Suitable for demonstration environments


---

# Installation and Setup

## Prerequisites

Install:

- Python 3.10+
- Node.js 18+
- Ollama


---

# Backend Setup

## 1. Create Python environment

```
python -m venv .venv
```

Activate:

Windows:

```
.venv\Scripts\activate
```

Linux/Mac:

```
source .venv/bin/activate
```


---

## 2. Install dependencies

```
pip install -r requirements.txt
```


---

## 3. Install Ollama model

Download Ollama model:

```
ollama pull qwen2.5:0.5b
```


Verify:

```
ollama list
```

---

# Frontend Setup

Navigate to frontend:

```
cd Frontend
```

Install packages:

```
npm install
```

Return to root:

```
cd ..
```

---

# Running the Application

The project provides a single command to run both frontend and backend.

From the root directory:

```
npm install
```

Then:

```
npm run dev
```


This starts:

Backend:

```
http://localhost:8000
```

Frontend:

```
http://localhost:5173
```


---

# API Documentation

FastAPI automatically provides interactive documentation:

Swagger UI:

```
http://localhost:8000/docs
```


ReDoc:

```
http://localhost:8000/redoc
```


---



# Design Decisions and Trade-offs

## Local LLM Instead of Cloud APIs

Chosen:

Ollama + qwen2.5:0.5b

Advantages:

- No API cost
- Privacy friendly
- Works offline

Trade-off:

- Smaller models provide lower reasoning ability compared with large cloud models


---

## Retrieval Before Generation

The assistant always retrieves knowledge base context before generating responses.

Benefits:

- Reduces hallucination
- Keeps responses grounded
- Makes answers traceable


---

## Rule-Based Agent Decision Layer

The agent decision layer uses retrieval confidence scores.

Advantages:

- Predictable behaviour
- Easy to debug
- Transparent decisions

Trade-off:

More advanced systems could use an LLM-based planner or tool-calling agent.

---

# Future Improvements

Possible production improvements:

- Add user authentication
- Add conversation memory
- Add evaluation metrics
- Add automated RAG testing
- Replace ChromaDB with distributed vector database
- Add streaming responses
- Add monitoring and logging dashboard


---


# Conclusion

This project demonstrates a complete agentic RAG customer support assistant with:

- Semantic retrieval
- Local embeddings
- Vector search
- Local LLM generation
- Agent decision-making
- REST API exposure
- Frontend interaction

The architecture is designed to be lightweight, explainable, and easily extendable toward a production support system.