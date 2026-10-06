# SoundFlow AI

> Semantic music search application built with Python, Streamlit, Sentence Transformers, PostgreSQL, Supabase and pgvector.

SoundFlow AI is an **AI/Data-oriented application** that allows users to explore a music library and find songs based on the meaning of a description, genre, or mood.

The project implements a semantic search workflow based on **embeddings**, vector similarity, and PostgreSQL with **pgvector**, while keeping configuration, embedding generation, data access, business logic, and presentation responsibilities separated.

## 🧩 Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Streamlit | Web interface and application runtime |
| Sentence Transformers | Embedding generation |
| `all-MiniLM-L6-v2` | 384-dimensional embedding model |
| PostgreSQL | Data persistence and queries |
| Supabase | PostgreSQL platform and data access |
| pgvector | Vector similarity search |
| Supabase RPC | Execution of `buscar_canciones()` |
| python-dotenv | Local environment variable loading |

## 📂 Project Structure

```text
SOUNDFLOW-PRO/
├── app.py
├── config/
│   └── settings.py
├── core/
│   └── embeddings.py
├── data/
│   └── supabase_client.py
├── repositories/
│   └── song_repository.py
├── services/
│   └── song_service.py
├── ui/
│   ├── styles.py
│   ├── home.py
│   ├── search.py
│   └── add_song.py
├── scripts/
│   ├── buscar_canciones.py
│   ├── insertar_canciones.py
│   ├── actualizar_vector.py
│   └── test_supabase.py
├── requirements.txt
└── README.md
```

## 🧠 Semantic Search Workflow

```text
User Query
    ↓
Embedding Generation
(all-MiniLM-L6-v2)
    ↓
384-dimensional Vector
    ↓
SongService
    ↓
SongRepository
    ↓
Supabase RPC: buscar_canciones()
    ↓
PostgreSQL + pgvector
    ↓
Results Ranked by Similarity
    ↓
Streamlit
```

The application transforms the user's text query into a vector and uses semantic similarity to retrieve songs related to its meaning rather than relying only on literal keyword matches.

## 🏗️ Architecture

The project separates presentation, business logic, embedding generation, and data access:

```text
ui/
  ↓
app.py
  ↓
services/
  ↓
repositories/
  ↓
Supabase / PostgreSQL / pgvector

core/embeddings.py
  ↓
Sentence Transformers
```

This separation improves maintainability and allows the search logic to be reused by both the user interface and command-line utilities.

## 🔧 Responsibilities

- `config/`: shared model, embedding dimension, and search parameters.
- `core/`: song-text construction and cached embedding generation.
- `data/`: `.env` loading and creation of the Supabase client.
- `repositories/`: queries and inserts into `canciones_vectoriales` and calls to the RPC.
- `services/`: business logic for listing, searching, adding, and updating songs.
- `ui/`: home, categories, library, search, form, and styling presentation.
- `scripts/`: terminal utilities that reuse the same services and repository.
- `app.py`: Streamlit configuration and navigation between views.

## ⚙️ Configuration and Installation

Python compatible with the dependencies specified in `requirements.txt` is required.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the project root with the credentials for your Supabase project:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

The `.env` file is local and excluded from Git. Do not add credentials to the source code.

## ▶️ Running the Application

```powershell
streamlit run app.py
```

The command-line utilities can be executed as modules from the project root:

```powershell
python -m scripts.buscar_canciones
python -m scripts.insertar_canciones
python -m scripts.actualizar_vector
python -m scripts.test_supabase
```

`insertar_canciones` adds the sample songs each time it is executed. `actualizar_vector` regenerates and stores the embedding for Rain Sounds. Run them only when you want to perform those write operations.

## 🔎 Semantic Search and Embeddings

The search workflow converts the user's text into a **384-dimensional embedding** using `all-MiniLM-L6-v2`. The service passes that vector and the original text to the repository, which calls `buscar_canciones()` with `query_embedding`, `query_text`, `match_threshold`, and `match_count`. PostgreSQL and pgvector perform the similarity search, while Streamlit displays the results and their similarity scores.

The current central configuration is:

| Setting | Value |
|---|---|
| Model | `all-MiniLM-L6-v2` |
| Dimensions | `384` |
| Threshold | `0.35` |
| Maximum results | `5` |
| Table | `public.canciones_vectoriales` |
| RPC | `buscar_canciones()` |

For new songs, the embedding text is built from **Title + Artist + Genre + Description**. The model is kept in Streamlit's resource cache to avoid reloading it on every interaction.

The application assumes that the table, vector column, and RPC already exist in Supabase. This project does not create or modify the remote schema.

## 🎯 What This Project Demonstrates

SoundFlow AI demonstrates practical integration between software development and AI/Data techniques through:

- Text embedding generation.
- Semantic search using vector similarity.
- Sentence Transformers integration with PostgreSQL.
- pgvector and Supabase RPC usage.
- Layered separation between UI, services, repositories, and AI components.
- Music data persistence and retrieval.
- Secure local configuration through environment variables.

## 📌 Project Status

**Completed portfolio project.**

## 👨‍💻 Author

**Miguel Arbeláez Vallejo**

Software Developer | Flutter & Dart | Full-Stack | Backend | AI/Data

- GitHub: https://github.com/MiguelArbelaez0
- LinkedIn: https://www.linkedin.com/in/miguel-arbelaez-v-57719542b/
