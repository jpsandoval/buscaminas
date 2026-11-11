# Buscaminas

Buscaminas (Minesweeper) jugable en el navegador, construido con React, TypeScript y Vite.

## Arquitectura

El código está organizado por capas, de más independiente a más acoplada a la UI:

```
src/
  domain/minesweeper/   Lógica pura del juego (sin React, sin DOM)
    types.ts              Tipos: Cell, Board, Difficulty, GameStatus...
    board.ts              Creación del tablero y colocación de minas
    gameplay.ts           Revelar celdas (flood fill), marcar banderas, condición de victoria
    MinesweeperEngine.ts  Orquesta una partida completa (estado + reglas)
    randomSource.ts       PRNG determinístico (seed) para partidas reproducibles
    difficulty.ts         Niveles de dificultad predefinidos

  application/
    useMinesweeper.ts     Hook de React que conecta el motor de dominio con el estado de la UI

  ui/
    components/           Board, Cell, GameHeader, DifficultySelector
    App/                   Composición de la pantalla principal

  shared/
    gameUrlParams.ts      Lee ?difficulty= y ?seed= de la URL
```

La regla de "primer click siempre seguro" se implementa colocando las minas recién
después del primer click, excluyendo esa celda y sus vecinas.

## Cómo correr el proyecto

```bash
npm install
npm run dev        # http://localhost:5173
```

Se puede compartir o reproducir una partida exacta agregando `?seed=123` a la URL
(y opcionalmente `?difficulty=beginner|intermediate|expert`).

## Tests

Hay tres niveles de pruebas:

```bash
npm run test        # Unitarios (dominio) + integración (hooks/componentes) — Vitest
npm run test:watch  # Igual, en modo watch
npm run test:e2e    # End-to-end en navegador real — Playwright
```

- **Unitarios** (`tests/unit`): funciones puras del dominio (colocación de minas,
  flood fill, condición de victoria, motor del juego), sin React ni DOM.
- **Integración** (`tests/integration`): el hook `useMinesweeper` y los componentes
  React renderizados juntos con Testing Library.
- **End-to-end** (`e2e/`): flujo completo en un navegador real con Playwright,
  incluyendo escenarios determinísticos de "ganar" y "perder" gracias al seed del PRNG.

## Otros scripts

```bash
npm run build       # tsc -b && vite build
npm run preview     # sirve el build de producción
npm run lint        # oxlint
npm run typecheck   # tsc -b --noEmit
```
