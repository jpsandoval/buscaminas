# Pruebas manuales

Esta carpeta contiene los casos de prueba manuales del proyecto Buscaminas.
Cada archivo `TC-XX-*.md` es un caso de prueba independiente, listo para que
cualquier persona (QA, docente, compañero de equipo) lo ejecute sin más
contexto que el que trae el propio documento.

## Cómo ejecutar un caso de prueba

1. Levanta la aplicación localmente:

   ```bash
   source .venv/bin/activate
   python main.py        # http://localhost:5173
   ```

2. Abre el archivo del caso de prueba que vas a ejecutar.
3. Sigue los pasos de la tabla **en orden**, sin saltarte ninguno.
4. Para cada paso, compara el **resultado esperado** contra lo que realmente
   ocurre en la aplicación.
5. Al terminar, completa la sección **Registro de ejecución** al final del
   documento:
   - **Resultado**: `Aprobado` si todos los pasos cumplieron lo esperado,
     `Fallido` si alguno no cumplió (indica cuál en **Observaciones**).
   - **Ejecutado por** y **Fecha**.
   - **Observaciones**: cualquier desviación, captura de pantalla adjunta,
     o bug encontrado (idealmente con su número de issue).

## Plantilla

Todos los casos siguen la misma estructura:

| Sección | Contenido |
|---|---|
| **ID / Título** | Identificador único y nombre descriptivo del caso |
| **Objetivo** | Qué comportamiento del sistema se está verificando |
| **Prioridad** | Alta / Media / Baja |
| **Precondiciones** | Estado necesario antes de empezar a ejecutar los pasos |
| **Datos de prueba** | URLs, seeds, dificultades u otros valores a usar |
| **Pasos** | Tabla numerada: acción → resultado esperado |
| **Resultado esperado (global)** | Criterio de aceptación del caso completo |
| **Registro de ejecución** | Se completa al ejecutar: resultado, autor, fecha, observaciones |

## Casos disponibles

| Caso | Título | Prioridad |
|---|---|---|
| [TC-01](./TC-01-flujo-basico-revelar.md) | Flujo básico: primer click seguro, revelar celdas y ganar la partida | Alta |
| [TC-02](./TC-02-marcar-banderas.md) | Marcar y desmarcar banderas, y contador de minas restantes | Alta |
| [TC-03](./TC-03-cambiar-dificultad-y-reiniciar.md) | Cambiar de dificultad, reiniciar partida y reproducir una partida con `seed` | Media |
