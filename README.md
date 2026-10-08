# SoundFlow AI

> Aplicación de búsqueda semántica de música desarrollada con Python, Streamlit, Sentence Transformers, PostgreSQL, Supabase y pgvector.

SoundFlow AI es una aplicación orientada a inteligencia artificial y datos que permite explorar una biblioteca musical y encontrar canciones según el significado de una descripción, género o estado de ánimo.

El proyecto implementa búsqueda semántica mediante embeddings, similitud vectorial y PostgreSQL con pgvector, separando configuración, generación de embeddings, acceso a datos, lógica de negocio y presentación.

## 🧩 Tecnologías

| Tecnología | Uso |
|---|---|
| Python | Lenguaje principal |
| Streamlit | Interfaz web y ejecución de la aplicación |
| Sentence Transformers | Generación de embeddings |
| `all-MiniLM-L6-v2` | Modelo de embeddings de 384 dimensiones |
| PostgreSQL | Persistencia y consultas |
| Supabase | Plataforma PostgreSQL y acceso a datos |
| pgvector | Búsqueda por similitud vectorial |
| RPC de Supabase | Ejecución de `buscar_canciones()` |
| python-dotenv | Carga local de variables de entorno |

## 📂 Estructura del proyecto

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
Consulta del usuario
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
RPC de Supabase: buscar_canciones()
    ↓
PostgreSQL + pgvector
    ↓
Resultados ordenados por similitud
    ↓
Streamlit
```

La aplicación transforma la consulta de texto en un vector y utiliza similitud semántica para recuperar canciones relacionadas con su significado, no únicamente con palabras literales.

## 🏗️ Arquitectura

Se separan la presentación, la lógica de negocio, la generación de embeddings y el acceso a datos:

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

Esta separación mejora el mantenimiento y permite reutilizar la lógica de búsqueda desde la interfaz y las utilidades de terminal.

## 🔧 Responsabilidades

- `config/`: modelo, dimensiones y parámetros de búsqueda.
- `core/`: construcción del texto de las canciones y generación de embeddings.
- `data/`: carga de `.env` y creación del cliente de Supabase.
- `repositories/`: consultas e inserciones en `canciones_vectoriales` y llamadas a la RPC.
- `services/`: lógica para listar, buscar, agregar y actualizar canciones.
- `ui/`: presentación de inicio, categorías, biblioteca, búsqueda, formularios y estilos.
- `scripts/`: utilidades de terminal que reutilizan servicios y repositorios.
- `app.py`: configuración de Streamlit y navegación entre vistas.

## ⚙️ Configuración e instalación

Se requiere una versión de Python compatible con las dependencias de `requirements.txt`.

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Crear un archivo `.env` en la raíz con las credenciales del proyecto de Supabase:

```env
SUPABASE_URL=tu_url_de_supabase
SUPABASE_KEY=tu_clave_de_supabase
```

El archivo `.env` es local y está excluido de Git. No agregues credenciales directamente al código fuente.

## ▶️ Ejecución

```powershell
streamlit run app.py
```

Las utilidades de terminal pueden ejecutarse desde la raíz:

```powershell
python -m scripts.buscar_canciones
python -m scripts.insertar_canciones
python -m scripts.actualizar_vector
python -m scripts.test_supabase
```

`insertar_canciones` agrega las canciones de ejemplo cada vez que se ejecuta. `actualizar_vector` regenera y almacena el embedding de Rain Sounds. Ejecútalos únicamente cuando quieras realizar esas operaciones de escritura.

## 🔎 Búsqueda semántica y embeddings

La consulta se convierte en un embedding de **384 dimensiones** mediante `all-MiniLM-L6-v2`.

El servicio envía el vector y el texto original al repositorio, que ejecuta `buscar_canciones()` con `query_embedding`, `query_text`, `match_threshold` y `match_count`.

PostgreSQL y pgvector realizan la búsqueda por similitud, mientras Streamlit muestra los resultados y sus puntuaciones.

Configuración principal:

| Parámetro | Valor |
|---|---|
| Modelo | `all-MiniLM-L6-v2` |
| Dimensiones | `384` |
| Umbral | `0.35` |
| Máximo de resultados | `5` |
| Tabla | `public.canciones_vectoriales` |
| RPC | `buscar_canciones()` |

Para las canciones nuevas, el texto utilizado para generar el embedding se construye con **título + artista + género + descripción**.

El modelo se mantiene en la caché de recursos de Streamlit para evitar cargarlo nuevamente en cada interacción.

La aplicación asume que la tabla, la columna vectorial y la RPC ya existen en Supabase. Este proyecto no crea ni modifica el esquema remoto.

## 🎯 Qué demuestra este proyecto

- Generación de embeddings de texto.
- Búsqueda semántica mediante similitud vectorial.
- Integración de Sentence Transformers con PostgreSQL.
- Uso de pgvector y RPC de Supabase.
- Separación entre interfaz, servicios, repositorios y componentes de IA.
- Persistencia y recuperación de datos musicales.
- Configuración segura mediante variables de entorno.

## 📌 Estado del proyecto

**Proyecto de portafolio terminado.**

## 👨‍💻 Autor

**Miguel Arbeláez Vallejo**

Desarrollador de Software | Flutter y Dart | Desarrollo integral | Backend | IA y Datos

- GitHub: https://github.com/MiguelArbelaez0
- LinkedIn: https://www.linkedin.com/in/miguel-arbelaez-v-57719542b/
