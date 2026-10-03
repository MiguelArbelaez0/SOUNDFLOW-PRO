# SoundFlow AI

> Semantic music recommendation system using embeddings and vector similarity.

SoundFlow AI is a Python-based semantic music search and recommendation system that allows users to find music using natural-language descriptions.

Instead of relying exclusively on exact keyword matching, the system represents text as numerical embeddings and uses vector similarity to retrieve semantically relevant songs.

## Overview

The project combines:

- Python
- Sentence Transformers
- `all-MiniLM-L6-v2`
- Text embeddings
- Vector similarity
- PostgreSQL
- Supabase
- pgvector

The core idea is to transform a natural-language query into an embedding and compare it against stored song embeddings to retrieve semantically similar results.

## How It Works

The recommendation flow is:

```text
User query
    ↓
Sentence Transformer
    ↓
Text embedding
    ↓
Vector similarity search
    ↓
Supabase / PostgreSQL
    ↓
pgvector
    ↓
Relevant songs