# SoundFlow AI

> Semantic music search application built with Python, Streamlit, Sentence Transformers, PostgreSQL, Supabase and pgvector.

SoundFlow AI es una aplicación orientada a **AI/Data** que permite explorar una biblioteca musical y encontrar canciones a partir del significado de una descripción, un género o un estado de ánimo.

El proyecto implementa un flujo de búsqueda semántica basado en **embeddings**, similitud vectorial y PostgreSQL con **pgvector**, manteniendo separadas las responsabilidades de configuración, generación de embeddings, acceso a datos, lógica de negocio y presentación.

## 🧩 Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Streamlit | Interfaz web y ejecución de la aplicación |
| Sentence Transformers | Generación de embeddings |
| `all-MiniLM-L6-v2` | Modelo de embeddings de 384 dimensiones |
| PostgreSQL | Persistencia y consultas de datos |
| Supabase | Plataforma de PostgreSQL y acceso a datos |
| pgvector | Búsqueda por similitud vectorial |
| Supabase RPC | Ejecución de `buscar_canciones()` |
| python-dotenv | Carga local de variables de entorno |

## 📂 Estructura

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

## 🧠 Flujo de búsqueda semántica

```text
Consulta de la persona
        ↓
Generación del embedding
(all-MiniLM-L6-v2)
        ↓
Vector de 384 dimensiones
        ↓
SongService
        ↓
SongRepository
        ↓
Supabase RPC: buscar_canciones()
        ↓
PostgreSQL + pgvector
        ↓
Resultados ordenados por similitud
        ↓
Streamlit
```

La aplicación transforma la consulta de texto en un vector y utiliza la similitud semántica para recuperar canciones relacionadas con su significado, no únicamente con coincidencias literales de palabras.

## 🏗️ Arquitectura

El proyecto separa presentación, lógica de negocio, generación de embeddings y acceso a datos:

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

Esta separación facilita el mantenimiento y permite reutilizar la lógica de búsqueda desde la interfaz y las utilidades de terminal.

## Responsabilidades

- `config/`: modelo, dimensión del embedding y parámetros de búsqueda compartidos.
- `core/`: construcción del texto de canciones y generación cacheada de embeddings.
- `data/`: carga de `.env` y creación del único cliente Supabase.
- `repositories/`: consultas e inserciones en `canciones_vectoriales` y llamada a la RPC.
- `services/`: flujo de negocio para listar, buscar, agregar y actualizar canciones.
- `ui/`: presentación de inicio, categorías, biblioteca, búsqueda, formulario y estilos.
- `scripts/`: utilidades de terminal que reutilizan los mismos servicios y repositorio.
- `app.py`: configuración de Streamlit y navegación entre vistas.

## ⚙️ Configuración e instalación

Se requiere Python compatible con las dependencias fijadas en `requirements.txt`.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crea `.env` en la raíz del proyecto con las credenciales de tu proyecto Supabase:

```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
```

El archivo `.env` es local y está excluido de Git. No añadas credenciales al código.

## ▶️ Ejecutar

```powershell
streamlit run app.py
```

Las herramientas de terminal se ejecutan como módulos desde la raíz:

```powershell
python -m scripts.buscar_canciones
python -m scripts.insertar_canciones
python -m scripts.actualizar_vector
python -m scripts.test_supabase
```

`insertar_canciones` agrega las canciones de ejemplo cada vez que se ejecuta. `actualizar_vector` vuelve a generar y guardar el embedding de Rain Sounds. Ejecútalos solo cuando quieras realizar esas escrituras.

## 🔎 Búsqueda semántica y embeddings

El flujo de búsqueda convierte el texto escrito por la persona en un embedding de 384 dimensiones con `all-MiniLM-L6-v2`. El servicio pasa ese vector y el texto original al repositorio, que llama a `buscar_canciones()` con `query_embedding`, `query_text`, `match_threshold` y `match_count`. PostgreSQL y pgvector realizan la búsqueda de similitud; Streamlit presenta los resultados y su similitud.

La configuración central actual es:

| Ajuste | Valor |
|---|---|
| Modelo | `all-MiniLM-L6-v2` |
| Dimensiones | `384` |
| Umbral | `0.35` |
| Máximo de resultados | `5` |
| Tabla | `public.canciones_vectoriales` |
| RPC | `buscar_canciones()` |

Para nuevas canciones, el texto común del embedding se construye como **Título + Artista + Género + Descripción**. El modelo se conserva en cache de recursos de Streamlit para evitar recargarlo en cada interacción.

La aplicación asume que la tabla, la columna vectorial y la RPC ya existen en Supabase. Este proyecto no crea ni modifica el esquema remoto.

## 🎯 Qué demuestra este proyecto

SoundFlow AI demuestra integración práctica entre desarrollo de software y técnicas de AI/Data mediante:

- Generación de embeddings para texto.
- Búsqueda semántica con similitud vectorial.
- Integración de Sentence Transformers con PostgreSQL.
- Uso de pgvector y funciones RPC de Supabase.
- Separación por capas entre UI, servicios, repositorios y componentes de IA.
- Persistencia y consulta de información musical.
- Configuración segura mediante variables de entorno.

## 📌 Estado del proyecto

**Proyecto completado para portafolio.**

## 👨‍💻 Autor

**Miguel Arbeláez Vallejo**

Software Developer | Flutter & Dart | Full-Stack | Backend | AI/Data

- GitHub: https://github.com/MiguelArbelaez0
- LinkedIn: https://www.linkedin.com/in/miguel-arbelaez-v-57719542b/
