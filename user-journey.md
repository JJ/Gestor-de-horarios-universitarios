# User Journey - Gestor de Horarios Universitarios

Este documento describe la experiencia de los distintos perfiles de estudiantes al interactuar con el Gestor de Horarios Universitarios.

---

## Perfiles de Usuario

1. **Estudiante de 1º de Nuevo Ingreso**
   - **Contexto:** Viene de fuera (ej. Toledo) a estudiar a Granada. 
   - **Problema:** No conoce la nomenclatura de la universidad, no sabe qué grupos o subgrupos le tocan tras la EBAU y le abruma la cantidad de PDFs dispersos. *(Basado en HU001)*

2. **Estudiante de asignaturas de varios cursos**
   - **Contexto:** Se va a matricular o ya está matriculado en asignaturas de 1º, 2º, 3º o 4º mezcladas (asignaturas pendientes y adelantadas).
   - **Problema:** Alto riesgo de solapamiento horario. Revisar a mano es inviable y genera dolores de cabeza. *(Basado en HU002 y HU003)*

3. **Estudiante de Doble Grado / Distintos Campus**
   - **Contexto:** Cursa dos carreras a la vez en facultades físicamente separadas (ej. ETSIIT y Ciencias).
   - **Problema:** Carga lectiva masiva. Las colisiones no solo son de hora, sino físicas (imposible estar en dos campus a la vez). Necesita margen de maniobra para llegar de un campus a otro. *(Basado en HU004)*

---

## User Journey

El viaje del usuario se divide en tres fases principales respecto al proceso académico de la universidad.

### Fase 1: Pre-Matriculación 
*Corresponde a los estudiantes preparando su curso académico (HU003, HU004).*

- **Objetivo del usuario:** Saber qué grupos le convienen más antes de confirmar su matrícula.
- **Problemas:** Tiene que abrir 5 o 6 PDFs de horarios diferentes y cruzar días, horas y asignaturas mentalmente o en un papel. Si se equivoca, perderá clases durante todo el cuatrimestre.
- **Interacción con la aplicación:** 
  1. Entra a la aplicación y selecciona las asignaturas y grados que desea cursar.
  2. La aplicación genera posibles combinaciones de grupos.
  3. El sistema alerta visualmente de las colisiones inevitables, permitiendo al usuario elegir el mal menor (el horario que le permite asistir al mayor número de horas).

### Fase 2: Post-Matriculación 
*Corresponde al inicio del cuatrimestre y alumnos de nuevo ingreso (HU001).*

- **Objetivo del usuario:** Entender a qué hora, qué día y en qué aula/facultad tiene clase según los grupos que le han asignado.
- **Problemas:** El estudiante (especialmente el de primero) está perdido. Las fuentes de datos son PDFs que pueden resultar confusos.
- **Interacción con la aplicación:**
  1. El usuario introduce su grado y el grupo general que le han asignado.
  2. El sistema procesa los datos subyacentes de la ETSIIT y le devuelve un horario visual, limpio y centralizado.
  3. Muestra claramente la ubicación física y los subgrupos (prácticas, teoría, seminarios).

### Fase 3: Detección y Resolución de Conflictos
*Corresponde a estudiantes ya matriculados con problemas inminentes (HU002, HU004).*

- **Objetivo del usuario:** Detectar colisiones que no pudo evitar en la matrícula (o de las que no se dio cuenta) para hablar con los profesores cuanto antes.
- **Problemas:** Enterarse tarde de que dos exámenes o clases obligatorias de distintos cursos (o distintos campus) coinciden el mismo día. Imposibilidad física de desdoblarse.
- **Interacción con la aplicación:**
  1. Al generar su horario final en la app, salta una "Alerta de Colisión Severa".
  2. La app detalla qué asignatura pisa a cuál y si es una colisión de campus (requiere tiempo de desplazamiento).
  3. El usuario exporta este reporte de solapamiento de forma sencilla.