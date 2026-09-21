import pypandoc

readme = r"""# 🎵 SoundFlow

## Sistema de recomendación musical mediante búsqueda semántica

SoundFlow es una aplicación desarrollada en Python que permite buscar y recomendar canciones a partir de una descripción escrita por el usuario. La idea principal del proyecto es que el usuario no tenga que conocer necesariamente el nombre de una canción, artista o utilizar exactamente las mismas palabras que aparecen en la información almacenada.

En lugar de realizar una búsqueda tradicional por coincidencia de palabras, SoundFlow utiliza inteligencia artificial mediante **embeddings** para representar el significado de los textos como vectores numéricos. Posteriormente, estos vectores se comparan con los vectores almacenados en una base de datos para encontrar las canciones que tienen un significado más cercano a la consulta realizada.

Por ejemplo, si el usuario escribe:

> "Algo muy tranquilo para dormir"

el sistema puede encontrar una canción descrita como música relajante para dormir, aunque la consulta y la descripción no utilicen exactamente las mismas palabras.

---

## 🎯 Objetivo

El objetivo del proyecto es construir un sistema básico de recomendación musical utilizando búsqueda vectorial.

El proyecto permite demostrar cómo una base de datos puede trabajar junto con modelos de inteligencia artificial para realizar búsquedas basadas en el **significado y el contexto** de una consulta.

La aplicación recibe una descripción del usuario, genera un embedding de esa descripción y posteriormente consulta Supabase para encontrar las canciones cuyos embeddings presentan mayor similitud.

---

## 🧠 Funcionamiento del sistema

El funcionamiento de SoundFlow se puede dividir en varias etapas.

Primero, se dispone de un conjunto de canciones que contienen información como título, artista y descripción. Cada descripción es procesada mediante el modelo `all-MiniLM-L6-v2`.

Este modelo transforma el texto en un vector numérico de **384 dimensiones**. Ese vector representa semánticamente el contenido de la descripción.

Por ejemplo:

```text
"Música tranquila para dormir"
              ↓
      Sentence Transformer
              ↓
       Vector de 384 valores