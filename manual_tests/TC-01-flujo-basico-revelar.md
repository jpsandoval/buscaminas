# TC-01 — Flujo básico: primer click seguro, revelar celdas y perder la partida

| Campo | Valor |
|---|---|
| **ID** | TC-01 |
| **Módulo** | Tablero de juego (`/`, `/api/reveal`) |
| **Prioridad** | Alta |
| **Tipo** | Funcional |
| **Autor** | Equipo QA Buscaminas |

## Objetivo

Verificar que el primer click de una partida nunca cae sobre una mina (regla
de "primer click siempre seguro"), que revelar una celda vacía propaga el
revelado a sus vecinas (flood fill), y que al revelar una mina la partida
termina correctamente mostrando todas las minas del tablero.

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
| Primer click | fila 1, columna 1 → `data-testid="cell-0-0"` |
| Mina conocida (para el paso de pérdida) | fila 1, columna 7 → `data-testid="cell-0-6"` |

> Estos valores son deterministas: con `seed=123`, `beginner` y primer click
> en `(0,0)`, el motor del juego siempre coloca las mismas 10 minas, entre
> ellas la celda `(0,6)`.

## Pasos

| # | Acción | Resultado esperado |
|---|---|---|
| 1 | Navegar a `http://localhost:5173/?seed=123&difficulty=beginner`. | La página carga un tablero de 9×9 (81 celdas). El texto de estado (`data-testid="game-status"`) muestra "Haz click en una casilla para empezar." El contador de minas (`data-testid="mines-remaining"`) muestra `010`. |
| 2 | Hacer click izquierdo sobre la celda `cell-0-0` (fila 1, columna 1). | La celda se revela (no es una mina). El estado cambia a "Click izquierdo para revelar, click derecho para marcar." El cronómetro (`data-testid="elapsed-seconds"`) empieza a avanzar. |
| 3 | Observar el tablero completo tras el click anterior. | Quedan reveladas exactamente 17 celdas: toda la fila 1 y 2 completas (columnas 1 a 6), y la fila 3 en columnas 2 a 6. El resto de las celdas sigue oculta (`data-state="hidden"`). Ninguna celda revelada muestra el emoji de mina 💣. |
| 4 | Hacer click izquierdo sobre una celda ya revelada (por ejemplo `cell-0-0` de nuevo). | No ocurre ningún cambio visible: la celda ya revelada ignora el click (está deshabilitada). |
| 5 | Hacer click izquierdo sobre la celda `cell-0-6` (fila 1, columna 7), que contiene una mina. | La partida termina. El estado muestra "Perdiste. Inténtalo de nuevo." El emoji del botón de reinicio cambia de 🙂 a 😵. |
| 6 | Revisar el tablero completo. | Las 10 minas del tablero quedan reveladas y muestran el emoji 💣, incluyendo las que el jugador no clickeó directamente. Todas las celdas del tablero quedan deshabilitadas (no responden a más clicks). |
| 7 | Hacer click sobre cualquier celda oculta restante. | No sucede nada: con la partida terminada (`won`/`lost`), el tablero no acepta más jugadas. |

## Resultado esperado (global)

El primer click de toda partida revela una zona segura (nunca una mina), el
flood fill revela correctamente todas las celdas vacías conectadas, y al
revelar una mina la partida pasa a estado "perdido" mostrando todas las
minas y bloqueando el tablero.

## Registro de ejecución

| Campo | Detalle |
|---|---|
| **Resultado** | ☐ Aprobado&nbsp;&nbsp;☐ Fallido |
| **Ejecutado por** | |
| **Fecha** | |
| **Navegador / entorno** | |
| **Observaciones / bugs encontrados** | |
