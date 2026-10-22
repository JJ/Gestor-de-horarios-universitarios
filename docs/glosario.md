Lenguaje común del dominio

Relacionado con [DC001]Definir un lenguaje común del dominio

En este archivo se llevará a cabo el establecimiento del glosario común.
Se va a definir los siguientes objetos, atributos y restricciones relacionadas con Gestor de Horarios Universitarios:

Objetos:
- Asignatura: Enseñanza perteneciente al plan de estudios de un grado.
  Tipo: entidad. Se identifica por su código; aunque cambie su horario sigue siendo la misma asignatura.
  Atributos: código de asignatura, profesor que imparte la asignatura, cŕeditos asignados, horas lectivas, guia docente.
  
- Curso: Año acádemico de un Grado, tiene la restricción de establecerse los cursos según los crréditos del grado.
  Si un grado es de 240 créditos compondrá 4 cursos, y si es de 300 créditos compondrá 5 cursos.
  Tipo: objeto de valor. "2º" no tiene identidad propia; dos cursos con el mismo número son el mismo.
  
- Matriula: Una matrícula es el resultado del proceso de inscripción de un alumno en un curso acádemico dado un grado. 
  Tipo: agregado (raíz). Agrupa las asignaturas, grupos y subgrupos elegidos por un alumno; sobre ese conjunto se detectan las colisiones.
  Atributos: código de matrícula.
  
- Grupo: Conjunto de alumnos matriculados en el mismo curso que imparten las clases de teoría de una asignatura.
  Tipo: entidad. El grupo A de una asignatura sigue siendo el mismo aunque cambie su horario.

- Grado: Titulación oficial de una enseñaza superior que se imparte en una Universidad.
  Tipo: entidad. Se identifica por su código de titulación.
  
- Subgrupo: Un subgrupo es un conjunto de alumnos de un grupo, es decir, aquel que tiene la restricción de pertenecer a un grupo y que se imparte dentro de una hora legal, dando enseñanza de la parte práctica de una asignatura.
  Tipo: entidad. El subgrupo A1 sigue siendo el mismo aunque cambie su hora legal.
  
- Colisión: Es el resultado de un solapamiento entre dos subgrupos, un subgrupo y un grupo, o dos grupos.
  Tipo: objeto de valor. Es un resultado calculado; si se recalcula con los mismos datos, es la misma colisión.
  
- Campus: Conjunto de universidades donde se dan grados universitarios relacionados.
  Tipo: objeto de valor. Solo nos interesa su nombre y ubicación; no cambia ni tiene ciclo de vida.

- Hora legal: Una hora con la restriccción de legal el aquella que esta dentro de los siguientes intervalos de tiempo, de 8:00-14:30 y de 15:30 a 21:30.
  Tipo: objeto de valor. Una franja se define solo por su día, su inicio y su fin.
