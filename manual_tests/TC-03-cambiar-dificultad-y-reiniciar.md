# TC-03 — Cambiar de dificultad, reiniciar partida y reproducir una partida con `seed`

| Campo | Valor |
|---|---|
| **ID** | TC-03 |
| **Módulo** | Selector de dificultad y reinicio (`/api/reset`), reproducibilidad por `seed` |
| **Prioridad** | Media |
| **Tipo** | Funcional |
| **Autor** | Equipo QA Buscaminas |

## Objetivo

Verificar que cambiar de dificultad reconstruye el tablero con el tamaño y
cantidad de minas correctos, que el botón de reinicio vuelve la partida
actual a su estado inicial, y que compartir la misma URL con `?seed=` entre
dos sesiones distintas produce exactamente el mismo tablero.

## Precondiciones

- La aplicación está corriendo localmente (`python main.py`) y accesible en
  `http://localhost:5173`.
- No hay ninguna partida previa en curso que pueda interferir (si la hay,
  alcanza con recargar la página).

## Datos de prueba

| Dificultad | id | Tamaño | Minas esperadas |
|---|---|---|---|
| Principiante | `beginner` | 9×9 (81 celdas) | 010 |
| Intermedio | `intermediate` | 16×16 (256 celdas) | 040 |
| Experto | `expert` | 16×30 (480 celdas) | 099 |

| Parámetro | Valor |
|---|---|
| Seed de reproducibilidad | `123` |
| Primer click en ambas sesiones | fila 1, columna 1 → `cell-0-0` |
| Celdas que deben quedar reveladas tras ese click (17 en total) | fila 1: columnas 1 a 6 · fila 2: columnas 1 a 6 · fila 3: columnas 2 a 6 |

## Pasos

### Parte A — Selector de dificultad

| # | Acción | Resultado esperado |
|---|---|---|
| 1 | Navegar a `http://localhost:5173/`. | Carga la dificultad por defecto, "Principiante", con tablero de 9×9 y contador de minas `010`. El botón "Principiante" aparece marcado como seleccionado (`aria-checked="true"`). |
| 2 | Hacer click en el botón "Intermedio" (`data-testid="difficulty-intermediate"`). | El tablero se reconstruye a 16×16 (256 celdas). El contador de minas cambia a `040`. El estado vuelve a "Haz click en una casilla para empezar." El botón "Intermedio" queda marcado como seleccionado. |
| 3 | Hacer click en el botón "Experto" (`data-testid="difficulty-expert"`). | El tablero se reconstruye a 16×30 (480 celdas). El contador de minas cambia a `099`. El botón "Experto" queda marcado como seleccionado. |
| 4 | Hacer click en el botón "Principiante" (`data-testid="difficulty-beginner"`). | El tablero vuelve a 9×9 (81 celdas) y el contador de minas vuelve a `010`. |

### Parte B — Botón de reinicio

| # | Acción | Resultado esperado |
|---|---|---|
| 5 | Con la dificultad "Principiante" activa, hacer click en cualquier celda oculta para iniciar la partida. | El estado pasa a "playing" y el cronómetro empieza a avanzar. El botón de reinicio muestra 🙂. |
| 6 | Esperar unos segundos y luego hacer click en el botón de reinicio (`data-testid="reset-button"`). | La partida se reinicia **sin cambiar de dificultad**: todas las celdas vuelven a estar ocultas, el contador de minas vuelve a `010`, el cronómetro vuelve a `000` y el estado vuelve a "Haz click en una casilla para empezar." |

### Parte C — Reproducibilidad con `seed`

| # | Acción | Resultado esperado |
|---|---|---|
| 7 | Abrir `http://localhost:5173/?seed=123&difficulty=beginner` en una pestaña. Hacer click en `cell-0-0`. | Quedan reveladas exactamente las 17 celdas indicadas en **Datos de prueba** (fila 1 cols 1-6, fila 2 cols 1-6, fila 3 cols 2-6). Anotar o capturar el tablero resultante. |
| 8 | Abrir la **misma URL** `http://localhost:5173/?seed=123&difficulty=beginner` en una ventana nueva o de incógnito (sesión distinta). Hacer click en `cell-0-0`. | Se revela exactamente el **mismo** conjunto de 17 celdas que en el paso 7. El patrón del tablero es idéntico entre ambas sesiones. |
| 9 | Repetir el paso 7 usando una URL con un `seed` distinto, por ejemplo `?seed=456&difficulty=beginner`, y hacer click en `cell-0-0`. | El conjunto de celdas reveladas tras el primer click es **distinto** al de los pasos 7 y 8 (semillas distintas producen tableros distintos). |

## Resultado esperado (global)

Cambiar de dificultad reconstruye el tablero con el tamaño y número de minas
correctos sin afectar otras partidas; el botón de reinicio devuelve la
partida actual a su estado inicial conservando la dificultad vigente; y una
misma URL con `?seed=` fijo produce siempre el mismo tablero, permitiendo
compartir o reproducir una partida exacta.

## Registro de ejecución

| Campo | Detalle |
|---|---|
| **Resultado** | ☐ Aprobado&nbsp;&nbsp;☐ Fallido |
| **Ejecutado por** | |
| **Fecha** | |
| **Navegador / entorno** | |
| **Observaciones / bugs encontrados** | |
