# Mini–Parser de Inglés (Fase 2)

Este proyecto implementa un **analizador léxico y un parser descendente recursivo** para un subconjunto muy limitado del inglés, orientado a la Fase 2 del proyecto de Teoría de Lenguajes de Programación.

Además, incluye un **runner de pruebas** que permite validar oraciones almacenadas en archivos de texto y comparar el resultado con un analizador moderno (spaCy).

---

## 1. Estructura de carpetas

La estructura recomendada del proyecto es la siguiente:

```text
PARSER-NLP/
├── .venv/                  # Entorno virtual de Python (opcional pero recomendado)
├── src/
│   ├── __init__.py
│   ├── lexico_en.py        # Analizador léxico y etiquetador (tagger simple)
│   └── parser_en.py        # Parser descendente recursivo sobre POS-tags
├── test/
│   ├── valid_1.txt         # Ejemplos de oraciones válidas
│   ├── valid_2.txt
│   ├── valid_3.txt
│   ├── valid_4.txt
│   ├── valid_5.txt
│   ├── invalid_1.txt       # Ejemplos de oraciones inválidas
│   ├── invalid_2.txt
│   ├── invalid_3.txt
│   ├── invalid_4.txt
│   └── invalid_5.txt
├── run_tests.py            # Script principal para ejecutar las pruebas
└── requirements.txt        # Dependencias de Python
```
 
> El vocabulario se define directamente en código dentro de `src/lexico_en.py`.

---

## 2. Configuración del entorno

### 2.1. Crear y activar el entorno virtual

Desde la carpeta raíz del proyecto (`PARSER-NLP`):

#### En Windows (PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Si usas `cmd.exe`:

```cmd
python -m venv .venv
.\.venv\Scripts\Activate.bat
```

#### En Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 2.2. Instalar dependencias

Con el entorno virtual activado, instala las dependencias:

```bash
pip install -r requirements.txt
```

### 2.3. Descargar el modelo de spaCy

El runner de pruebas puede mostrar, además del resultado del parser propio, un análisis de referencia usando **spaCy**.  
Si quieres habilitar esta comparación, instala el modelo inglés pequeño:

```bash
python -m spacy download en_core_web_sm
```

Si no instalas este modelo, el script seguirá funcionando; simplemente omitirá la parte de spaCy.

---

## 3. Léxico y etiquetas gramaticales

El archivo `src/lexico_en.py` define un **vocabulario reducido** directamente en código, usando un diccionario (`LEXICON`) con palabras frecuentes en inglés y su categoría gramatical gruesa:

- `N` – Sustantivo (noun)  
- `V` – Verbo (verb)  
- `ADJ` – Adjetivo (adjective)  
- `ADV` – Adverbio (adverb)

Adicionalmente, `src/parser_en.py` define conjuntos cerrados de:

- **Determinantes (`DET`)**: `a, an, the, this, that, my, your, his, her, our, their`
- **Pronombres (`PRON`)**: `i, you, he, she, it, we, they`
- **Preposiciones (`PREP`)**: `in, on, at, for, to, with, from, between, before, after`

Si una palabra no está en el vocabulario abierto (`LEXICON`) ni en los conjuntos anteriores:

- Si termina en `-ly` se etiqueta como `ADV`.
- En otro caso se etiqueta como `N` (sustantivo por defecto).

El archivo `parser_en.py` también declara un diccionario `TAG_DESCRIPTIONS` que asocia cada etiqueta con una breve descripción en español (por ejemplo, `N → "Sustantivo"`).  
Estas descripciones se muestran en la salida de consola al ejecutar las pruebas, para facilitar la interpretación de los tokens.

---

## 4. Gramática utilizada

El parser implementa un **análisis sintáctico descendente recursivo** sobre una gramática libre de contexto **limitada** que trabaja sobre secuencias de POS-tags (no sobre palabras directamente).

La gramática base es:

```text
S  → NP VP

NP → PRON
    | DET ADJ* N
    | ADJ* N

VP → V
    | V NP
    | V NP PP+
    | V PP+

PP → PREP NP
```

Lectura informal:

- Una **oración** (`S`) se compone de un **sintagma nominal** (`NP`) seguido de un **sintagma verbal** (`VP`).
- Un `NP` puede ser:
  - Un pronombre (`PRON`) como `she`, `they`.
  - Un determinante seguido de cero o más adjetivos y un sustantivo: `the big dog`.
  - Cero o más adjetivos seguidos de un sustantivo: `happy children`.
- Un `VP` puede ser:
  - Solo un verbo: `sleep`.
  - Verbo + `NP`: `eat bread`, `read the book`.
  - Verbo + `NP` + uno o más sintagmas preposicionales: `play the game in the street`.
  - Verbo + uno o más sintagmas preposicionales: `sleep in the house`.
- Un `PP` es una preposición seguida de un `NP`: `in the house`, `with the friend`.

Esta gramática está diseñada para cubrir patrones simples de tipo **Sujeto – Verbo – (Objeto) – (Modificadores)** con un vocabulario controlado.

---

## 5. Ejecución del runner de pruebas

El script principal es `run_tests.py` y está construido con **Typer**, por lo que ofrece una pequeña interfaz de línea de comandos.

### 5.1. Ejecutar las pruebas sobre la carpeta `test/` (por defecto)

Con el entorno virtual activado y desde la carpeta raíz:

```bash
python -m run_tests run
```

El comando:

- Lee todos los archivos `*.txt` dentro de la carpeta `test/`.
- Cada archivo debe contener **una sola oración**.
- Para cada archivo:
  - Muestra el texto de entrada.
  - Tokeniza y etiqueta las palabras según el léxico reducido.
  - Imprime una tabla con:
    - El token,
    - Su etiqueta (`POS`),
    - Una breve descripción en español de esa etiqueta.
  - Ejecuta el **parser descendente recursivo**.
    - Si la oración es aceptada, muestra un mensaje en verde y el árbol sintáctico.
    - Si es rechazada, muestra el motivo del error (qué se esperaba y qué se encontró).
  - Si spaCy está disponible, imprime también una tabla con POS, dependencia y cabeza léxica para cada token.

### 5.2. Ejecutar pruebas sobre otra carpeta

Puedes indicar una carpeta distinta (por ejemplo `mis_pruebas/`) con:

```bash
python -m run_tests mis_pruebas
```

La carpeta debe existir y contener archivos `.txt`.

---

## 6. Ejemplo de salida en consola

Ejemplo simplificado para un archivo `valid_2.txt` con el texto:

```text
She read the book
```

Salida aproximada:

```text
──────────────────────────────────────────── valid_2.txt ─────────────────────────────────────────────
┌─ Texto de entrada ─┐
│ She read the book  │
└────────────────────┘

Tokens y POS usados por el parser
┏━━━━━━━┳━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Token ┃ Etiqueta (POS) ┃ Descripción                   ┃
┡━━━━━━━╇━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ She   │ PRON           │ Pronombre                     │
│ read  │ V              │ Verbo                         │
│ the   │ DET            │ Determinante / artículo       │
│ book  │ N              │ Sustantivo                    │
└───────┴────────────────┴───────────────────────────────┘

✓ Oración ACEPTADA por el parser recursivo
┌─ Árbol sintáctico (SVO simplificado) ┐
│ S                                    │
│   NP                                 │
│     She/PRON                         │
│   VP                                 │
│     read/V                           │
│     NP                               │
│       the/DET                        │
│       book/N                         │
└──────────────────────────────────────┘
```

Si el modelo de spaCy está instalado, a continuación aparecería una segunda tabla con el análisis `POS/Dep/Head` de spaCy.

---

## 7. Conjunto de pruebas sugerido

Para cumplir con la parte de “probar el parser con ejemplos válidos e inválidos”, se incluyen 10 archivos de ejemplo en la carpeta `test/`:

### 7.1. Oraciones válidas (aceptadas por la gramática)

- `valid_1.txt`  
  ```text
  The big dog sleep
  ```

- `valid_2.txt`  
  ```text
  She read the book
  ```

- `valid_3.txt`  
  ```text
  Happy child play in the street
  ```

- `valid_4.txt`  
  ```text
  They eat bread
  ```

- `valid_5.txt`  
  ```text
  Our teacher talk with the friend
  ```

### 7.2. Oraciones inválidas (rechazadas por la gramática)

- `invalid_1.txt`  
  ```text
  The dog
  ```

- `invalid_2.txt`  
  ```text
  Eat bread
  ```

- `invalid_3.txt`  
  ```text
  The red
  ```

- `invalid_4.txt`  
  ```text
  She is happy
  ```

- `invalid_5.txt`  
  ```text
  In the house the dog sleep
  ```

Cada una de estas oraciones provoca un mensaje de error diferente (por ejemplo, “esperaba un verbo y se encontró fin de entrada”, “esperaba un sustantivo y se encontró un verbo”, etc.), lo cual resulta útil para documentar y analizar las limitaciones de la gramática.
