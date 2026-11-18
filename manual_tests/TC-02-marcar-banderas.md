# TC-02 — Marcar y desmarcar banderas, y contador de minas restantes

| Campo | Valor |
|---|---|
| **ID** | TC-02 |
| **Módulo** | Banderas (`/api/flag`) |
| **Prioridad** | Alta |
| **Tipo** | Funcional |
| **Autor** | Equipo QA Buscaminas |

## Objetivo

Verificar que el click derecho marca y desmarca una celda oculta con una
bandera, que el contador de minas restantes se actualiza en consecuencia, y
que una celda ya revelada no puede marcarse con bandera.

## Precondiciones

- La aplicación está corriendo localmente (`python main.py`) y accesible en
  `http://localhost:5173`.
- No hay ninguna partida previa en curso que pueda interferir (si la hay,
  alcanza con recargar la página).

## Datos de prueba

| Parámetro | Valor |
|---|---|
| Seed | `123` |
| Dificultad | `beginner` (9×9, 10 minas) |
| URL de entrada | `http://localhost:5173/?seed=123&difficulty=beginner` |
| Primer click (para empezar la partida) | fila 1, columna 1 → `data-testid="cell-0-0"` |
| Celda oculta a marcar | fila 9, columna 9 → `data-testid="cell-8-8"` |
| Celda ya revelada (control negativo) | fila 1, columna 1 → `data-testid="cell-0-0"` |

## Pasos

| # | Acción | Resultado esperado |
|---|---|---|
| 1 | Navegar a `http://localhost:5173/?seed=123&difficulty=beginner`. | El contador de minas (`data-testid="mines-remaining"`) muestra `010`. |
| 2 | Hacer click izquierdo sobre `cell-0-0` para iniciar la partida. | La celda se revela y el estado pasa a "playing" (texto "Click izquierdo para revelar, click derecho para marcar."). |
| 3 | Hacer click derecho (contextmenu) sobre la celda oculta `cell-8-8`. | No se abre el menú contextual del navegador. La celda muestra la bandera 🚩 y su atributo `data-state` pasa a `flagged`. El contador de minas restantes baja a `009`. |
| 4 | Hacer click izquierdo sobre la celda recién marcada (`cell-8-8`). | No ocurre nada: una celda con bandera no se revela con click izquierdo (sigue marcada, sigue oculta para el juego). |
| 5 | Hacer click derecho nuevamente sobre `cell-8-8`. | La bandera se quita. `data-state` vuelve a `hidden` y la celda no muestra ningún contenido. El contador de minas restantes vuelve a `010`. |
| 6 | Hacer click derecho sobre una celda ya revelada (`cell-0-0`). | No pasa nada: la celda revelada no se puede marcar con bandera (sigue revelada, sin 🚩, el contador de minas no cambia). |
| 7 | Marcar con bandera 3 celdas ocultas distintas (por ejemplo `cell-8-8`, `cell-8-7`, `cell-8-6`). | Cada marcado resta 1 al contador de minas restantes: `009`, `008`, `007` en ese orden. Las 3 celdas muestran 🚩. |
| 8 | Hacer click derecho sobre el botón de reinicio (🙂) — *no aplica, el reinicio es con click izquierdo*; en su lugar, hacer click izquierdo sobre el botón de reinicio (`data-testid="reset-button"`). | La partida se reinicia: todas las banderas desaparecen, el contador de minas vuelve a `010` y el estado vuelve a "Haz click en una casilla para empezar." |

## Resultado esperado (global)

El click derecho alterna correctamente el estado de bandera únicamente sobre
celdas ocultas, el contador de minas restantes refleja en todo momento
`minas totales - banderas colocadas`, y ni el click izquierdo sobre una
celda marcada ni el click derecho sobre una celda revelada producen ningún
cambio de estado indebido.

## Registro de ejecución

| Campo | Detalle |
|---|---|
| **Resultado** | ☐ Aprobado&nbsp;&nbsp;☐ Fallido |
| **Ejecutado por** | |
| **Fecha** | |
| **Navegador / entorno** | |
| **Observaciones / bugs encontrados** | |
