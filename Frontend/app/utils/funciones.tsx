import {  bloques, dias } from './constantes';
export function generarTablaHorario_old(horariosUsuario) {
  const tabla = {};
  for (const bloque of bloques) {
    tabla[bloque] = {};
    for (const dia of dias) {
      tabla[bloque][dia] = null;
    }
  }

  for (const clase of horariosUsuario) {
    if (tabla[clase.bloque][clase.dia]) {
      tabla[clase.bloque][clase.dia] += ` / ${clase.departamento.toUpperCase()} (Sala ${clase.sala}) `;
    } else {
      tabla[clase.bloque][clase.dia] = `${clase.asignatura} (Sala ) \n ${clase.departamento.toUpperCase()}-${clase.sala}`;
    }
    
  }

  return tabla;
}

export function generarTablaHorario(horarios) {
  const tabla = {};
  for (const bloque of bloques) {
    tabla[bloque] = {};
  }
  for (const clase of horarios) {
    if (!tabla[clase.bloque]) {
      tabla[clase.bloque] = {};
    }
    tabla[clase.bloque][clase.dia] = `${clase.asignatura} \n ${clase.departamento.toUpperCase()}-${clase.sala}`;
  }
  return tabla;
}
