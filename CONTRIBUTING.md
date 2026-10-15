# Contribuir al proyecto

## Ramas

Utilizamos prefijos que identifican el propósito de cada rama:

- `FEATURE-xxx-descripcion`: incorporación de funcionalidades.
- `FIX-xxx-descripcion`: corrección de errores.
- `INTERNAL-xxx-descripcion`: configuración y mantenimiento interno del proyecto.

El identificador debe corresponder a la tarea asociada cuando proceda. Utiliza nombres breves, descriptivos y separados por guiones.

## Pull requests

El título del PR debe indicar su tipo y número:

- `[FEATURE-xxx] Descripción de la funcionalidad`
- `[FIX-xxx] Descripción de la corrección`
- `[INTERNAL-xxx] Descripción del cambio interno`

Los PR deben utilizar la plantilla correspondiente al tipo de cambio, enlazar los issues afectados y describir cómo se han verificado los cambios.

## Commits

Los commits deben tener mensajes breves y descriptivos. Como convención general:

- `feat: descripción de la funcionalidad`
- `fix: descripción de la corrección`
- `ci: descripción de la automatización`
- `docs: descripción de la documentación`
- `chore: descripción del mantenimiento`

Cuando corresponda, se pueden incluir referencias de cierre como `Closes #123`. El cierre efectivo depende de que el commit llegue a la rama predeterminada de GitHub.

## Issues y labels

Los issues deben utilizar la plantilla correspondiente y especificar:

1. El issue relacionado.
2. El contexto.
3. Qué hay que hacer.
4. Los criterios de cierre.

Labels acordadas:

- `documentation`: documentación.
- `tools`: herramientas.
- `development`: desarrollo del producto.
- `user-story`: historias de usuario.
- `internal-config`: configuración interna.
- `bug`: errores del proyecto.

Se pueden combinar varias labels cuando la tarea lo requiera.

## Milestones

Los milestones utilizan el formato:

`[MX]: Breve descripción del contenido del producto`

Por ejemplo: `[M00]: Preparación base`.

## Revisión e integración

Antes de integrar un PR, deben revisarse sus cambios y comprobarse los controles automáticos que correspondan. Los PR deben solicitar revisión al equipo.
