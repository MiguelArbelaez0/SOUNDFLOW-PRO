# 🎵 SoundFlow AI

> Semantic music search and recommendation system using text embeddings and vector similarity.

SoundFlow AI is a Python application that uses **natural-language queries, sentence embeddings, PostgreSQL, Supabase and pgvector** to retrieve music that is semantically related to what the user describes.

Instead of depending only on exact keywords, the application converts text into numerical vectors and compares them against stored song embeddings to find semantically similar results.

## ✨ What the project demonstrates

- Natural-language music search
- Text embeddings with `Sentence Transformers`
- `all-MiniLM-L6-v2`
- Vector similarity search
- PostgreSQL + Supabase
- `pgvector`
- Supabase RPC functions
- Streamlit interface
- Environment-based configuration
- Python integration with a vector database

## 🧠 How it works

The main search flow is:

```text
User describes the music they want
              ↓
        Natural-language query
              ↓
     Sentence Transformer model
              ↓
        384-dimensional vector
              ↓
      Supabase RPC function
              ↓
        pgvector similarity
              ↓
       Top matching songs
              ↓
      Streamlit recommendations
```

### Example

A user can search for:

```text
I want an energetic song for working out
```

The query is transformed into an embedding using `all-MiniLM-L6-v2`. That vector is then compared with the embeddings stored for songs in Supabase.

The application requests the most relevant matches and displays the title, artist and similarity percentage.

## 🏗️ Architecture

The project is intentionally compact and organized around the main responsibilities of the application:

```text
SOUNDFLOW-PRO/
│
├── app.py
├── database.py
├── buscar_canciones.py
├── insertar_canciones.py
├── actualizar_vector.py
├── test_supabase.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Main components

| File | Responsibility |
|---|---|
| `app.py` | Streamlit user interface and semantic search flow |
| `database.py` | Supabase client configuration |
| `buscar_canciones.py` | Command-line semantic search |
| `insertar_canciones.py` | Generates embeddings and inserts songs |
| `actualizar_vector.py` | Re-generates and updates a song embedding |
| `test_supabase.py` | Basic Supabase connectivity test |
| `requirements.txt` | Python dependency versions |
| `.gitignore` | Excludes local environment and Python artifacts |

## 🔎 Semantic search

SoundFlow uses the `all-MiniLM-L6-v2` Sentence Transformer model to generate text embeddings.

For indexed songs, the project combines information such as:

```text
Title + Artist + Description
```

and generates an embedding from that text.

For a search, the user's natural-language query is converted into another embedding.

The application then calls the Supabase RPC function:

```text
buscar_canciones
```

with:

- `query_embedding`
- `match_threshold`
- `match_count`

The current Streamlit application uses:

```text
match_threshold = 0.5
match_count = 5
```

This allows the application to retrieve up to five semantically relevant results that satisfy the configured similarity threshold.

## 🗄️ Supabase + pgvector

Supabase provides the PostgreSQL database used by the project.

The song records contain information such as:

- Title
- Artist
- Description
- Embedding

The embeddings are stored as vectors and searched using **pgvector**.

The application does not perform the vector comparison entirely in Python. Instead, it sends the query embedding to a PostgreSQL/Supabase RPC function, allowing the database layer to perform the similarity search.

## 🖥️ Streamlit interface

The main interface is implemented in `app.py` with Streamlit.

It provides:

- Natural-language search input
- Search button
- Loading state
- Similarity results
- Artist and song information
- Similarity percentage
- Visual similarity progress bar
- Empty-result handling
- Error handling

The application also caches the Sentence Transformer model with Streamlit's resource cache so that the model does not need to be loaded again for every interaction.

## ⚙️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/MiguelArbelaez0/SOUNDFLOW-PRO.git
cd SOUNDFLOW-PRO
```

### 2. Create a virtual environment

Windows:

```powershell
python -m venv venv
venv\Scripts\activate
```

macOS / Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

## 🔐 Environment variables

Create a local `.env` file in the project root.

```env
SUPABASE_URL=your_supabase_project_url
SUPABASE_KEY=your_supabase_key
```

The repository intentionally does not include the local `.env` file.

The application loads these variables through `python-dotenv` in `database.py`.

> Never commit real credentials, API keys or database passwords to the repository.

## ▶️ Run the application

Start the Streamlit interface with:

```bash
streamlit run app.py
```

Streamlit will provide the local application URL in the terminal.

## 🧪 Utility scripts

### Search from the terminal

```bash
python buscar_canciones.py
```

This script asks for a natural-language query, generates its embedding and calls the same Supabase vector-search function.

### Insert songs

```bash
python insertar_canciones.py
```

This script:

1. Loads the Sentence Transformer model.
2. Builds the text representation of each song.
3. Generates an embedding.
4. Inserts the song data into Supabase.
5. Stores the generated vector.

### Update an embedding

```bash
python actualizar_vector.py
```

This utility retrieves a specific song, generates a new embedding and updates only its vector.

### Test Supabase connectivity

```bash
python test_supabase.py
```

This performs a basic query against the `canciones_vectoriales` table to verify connectivity.

## 🧰 Technologies

### Backend / Application

- Python
- Streamlit

### AI / NLP

- Sentence Transformers
- `all-MiniLM-L6-v2`
- Text embeddings
- Vector similarity

### Database

- PostgreSQL
- Supabase
- pgvector
- Supabase RPC

### Configuration

- python-dotenv

## 📌 Project status

SoundFlow AI is a functional academic/personal project focused on demonstrating the integration of **semantic search, embeddings and vector databases** in a Python application.

The repository currently focuses on the core semantic-search workflow rather than a production-scale recommendation platform.

## 🔒 Security

Configuration values are loaded from environment variables rather than being hard-coded in the application.

The repository's `.gitignore` excludes:

```text
.env
venv/
__pycache__/
*.pyc
```

For deployment or production use, credentials should be supplied through the hosting platform's secret/environment-variable mechanism.

## 👨‍💻 Author

**Miguel Arbeláez Vallejo**

Software Developer focused on Flutter/Dart, Full-Stack development, backend systems, databases and applied AI.

- GitHub: https://github.com/MiguelArbelaez0
- LinkedIn: https://www.linkedin.com/in/miguel-arbelaez-v-57719542b/
