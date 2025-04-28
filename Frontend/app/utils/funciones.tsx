import {  Bloque, bloques, Clase, Dia, dias, TablaHorario } from './constantes';

export function generarTablaHorario_old(horariosUsuario: Clase[]): TablaHorario {
  const tabla: TablaHorario = {};

  for (const bloque of bloques) {
    tabla[bloque] = {};
    for (const dia of dias) {
      tabla[bloque]![dia] = "";
    }
  }

  for (const clase of horariosUsuario) {
    const dia = clase.dia as Dia;
    const bloque = clase.bloque as Bloque;

    if (tabla[bloque]?.[dia]) {
      tabla[bloque]![dia]! += ` / ${clase.departamento.toUpperCase()} (Sala ${clase.sala}) `;
    } else {
      tabla[bloque]![dia] = `${clase.asignatura} (Sala ) \n ${clase.departamento.toUpperCase()}-${clase.sala}`;
    }
  }

  return tabla;
}

// Versión más simple que sobrescribe
export function generarTablaHorario(horarios: Clase[]): TablaHorario {
  const tabla: TablaHorario = {};

  for (const bloque of bloques) {
    tabla[bloque] = {};
  }

  for (const clase of horarios) {
    const dia = clase.dia as Dia;
    const bloque = clase.bloque as Bloque;

    if (!tabla[bloque]) {
      tabla[bloque] = {};
    }

    //tabla[bloque]![dia] = `${clase.asignatura} \n ${clase.departamento.toUpperCase()}-${clase.sala}`;
    tabla[bloque]![dia] = `${clase.asignatura}`
  }

  return tabla;
}