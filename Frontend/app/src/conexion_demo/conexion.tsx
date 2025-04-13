let usuariosPredeterminados = [
  { usuario: "demo1", clave: "demo2" }, // 15 de agosto de 1995
  { usuario: "marco.hernandez@alumnos.ucn.cl", clave: "15081995" }, // 15 de agosto de 1995
  { usuario: "lucia.morales@alumnos.ucn.cl", clave: "22041998" }, // 22 de abril de 1998
  { usuario: "diego.fuentes@alumnos.ucn.cl", clave: "05061992" }, // 5 de junio de 1992
  { usuario: "ana.torres@alumnos.ucn.cl", clave: "30071997" }, // 30 de julio de 1997
  { usuario: "carlos.romero@alumnos.ucn.cl", clave: "12031996" }, // 12 de marzo de 1996
  { usuario: "valentina.soto@alumnos.ucn.cl", clave: "18022000" }, // 18 de febrero de 2000
  { usuario: "fernando.guzman@alumnos.ucn.cl", clave: "25051994" }, // 25 de mayo de 1994
  { usuario: "martina.rios@alumnos.ucn.cl", clave: "08082001" }, // 8 de agosto de 2001
  { usuario: "sebastian.mendez@alumnos.ucn.cl", clave: "11071993" }, // 11 de julio de 1993
  { usuario: "paula.vera@alumnos.ucn.cl", clave: "03121999" } // 3 de diciembre de 1999
];

const departamentos = [
  { nombre: "x", x: 150, y: 340 },
  { nombre: "x1", x: 170, y: 373 },
  { nombre: "y", x: 165, y: 411 },
  { nombre: "g", x: 151, y: 198 },
  { nombre: "g1", x: 146, y: 217 },
  { nombre: "g2", x: 163, y: 213 },
  { nombre: "g3", x: 179, y: 199 },
  { nombre: "g4", x: 193, y: 244 },
  { nombre: "g5", x: 182, y: 367 },
  { nombre: "g6", x: 132, y: 435 },

  { nombre: "b1", x: 74, y: 372 },
  { nombre: "b2", x: 84, y: 363 },

  { nombre: "d1", x: 156, y: 281 },
  { nombre: "d2", x: 134, y: 304 },

  { nombre: "i", x: 224, y: 161 },
];

//nombre: "x", x: 150, y: 340 },

let  horarios = [
  { usuario: "demo1", departamento: "x", bloque: "A", sala: 11, dia: "lunes", asignatura: "Matemáticas" },
  { usuario: "demo1", departamento: "g1", bloque: "B", sala: 211, dia: "martes", asignatura: "Física" },
  { usuario: "demo1", departamento: "g2", bloque: "C", sala: 3111, dia: "miércoles", asignatura: "Química" },
  { usuario: "demo1", departamento: "g", bloque: "A", sala: 3111, dia: "sábado", asignatura: "Química" },
  { usuario: "demo1", departamento: "g1", bloque: "B", sala: 3111, dia: "sábado", asignatura: "Química" },
  { usuario: "demo1", departamento: "g2", bloque: "C", sala: 3111, dia: "sábado", asignatura: "Química" },
  { usuario: "demo1", departamento: "g3", bloque: "C2", sala: 3111, dia: "sábado", asignatura: "Química" },
  { usuario: "demo1", departamento: "g4", bloque: "D", sala: 3111, dia: "sábado", asignatura: "Química" },
  { usuario: "demo1", departamento: "g5", bloque: "E", sala: 3111, dia: "sábado", asignatura: "Química" },
  { usuario: "demo1", departamento: "g6", bloque: "F", sala: 3111, dia: "sábado", asignatura: "Química" },

  { usuario: "marco.hernandez@alumnos.ucn.cl", departamento: "x", bloque: "A", sala: 101, dia: "lunes", asignatura: "Matemáticas" },
  { usuario: "marco.hernandez@alumnos.ucn.cl", departamento: "g1", bloque: "B", sala: 102, dia: "martes", asignatura: "Física" },
  { usuario: "marco.hernandez@alumnos.ucn.cl", departamento: "g2", bloque: "C", sala: 103, dia: "miércoles", asignatura: "Química" },

  { usuario: "lucia.morales@alumnos.ucn.cl", departamento: "g3", bloque: "D", sala: 201, dia: "jueves", asignatura: "Biología" },
  { usuario: "lucia.morales@alumnos.ucn.cl", departamento: "g4", bloque: "E", sala: 202, dia: "viernes", asignatura: "Historia" },
  { usuario: "lucia.morales@alumnos.ucn.cl", departamento: "x", bloque: "F", sala: 203, dia: "sábado", asignatura: "Arte" },
  { usuario: "lucia.morales@alumnos.ucn.cl", departamento: "g6", bloque: "C2", sala: 204, dia: "lunes", asignatura: "Lenguaje" },

  { usuario: "diego.fuentes@alumnos.ucn.cl", departamento: "y", bloque: "A", sala: 301, dia: "martes", asignatura: "Música" },
  { usuario: "diego.fuentes@alumnos.ucn.cl", departamento: "g1", bloque: "B", sala: 302, dia: "miércoles", asignatura: "Educación Física" },

  { usuario: "ana.torres@alumnos.ucn.cl", departamento: "g2", bloque: "C", sala: 401, dia: "jueves", asignatura: "Ciencias" },
  { usuario: "ana.torres@alumnos.ucn.cl", departamento: "g3", bloque: "D", sala: 402, dia: "viernes", asignatura: "Inglés" },
  { usuario: "ana.torres@alumnos.ucn.cl", departamento: "g4", bloque: "E", sala: 403, dia: "sábado", asignatura: "Religión" },
  { usuario: "ana.torres@alumnos.ucn.cl", departamento: "g5", bloque: "F", sala: 404, dia: "lunes", asignatura: "Lenguaje" },

  { usuario: "carlos.romero@alumnos.ucn.cl", departamento: "g6", bloque: "C2", sala: 501, dia: "martes", asignatura: "Matemáticas" },
  { usuario: "carlos.romero@alumnos.ucn.cl", departamento: "x", bloque: "A", sala: 502, dia: "miércoles", asignatura: "Física" },
  { usuario: "carlos.romero@alumnos.ucn.cl", departamento: "y", bloque: "B", sala: 503, dia: "jueves", asignatura: "Química" },

  { usuario: "valentina.soto@alumnos.ucn.cl", departamento: "g1", bloque: "C", sala: 601, dia: "viernes", asignatura: "Historia" },
  { usuario: "valentina.soto@alumnos.ucn.cl", departamento: "g2", bloque: "D", sala: 602, dia: "sábado", asignatura: "Ciencias" },

  { usuario: "fernando.guzman@alumnos.ucn.cl", departamento: "g3", bloque: "E", sala: 701, dia: "lunes", asignatura: "Arte" },
  { usuario: "fernando.guzman@alumnos.ucn.cl", departamento: "g4", bloque: "F", sala: 702, dia: "martes", asignatura: "Música" },
  { usuario: "fernando.guzman@alumnos.ucn.cl", departamento: "g5", bloque: "C2", sala: 703, dia: "miércoles", asignatura: "Filosofía" },
  { usuario: "fernando.guzman@alumnos.ucn.cl", departamento: "x", bloque: "A", sala: 704, dia: "jueves", asignatura: "Lenguaje" },

  { usuario: "martina.rios@alumnos.ucn.cl", departamento: "y", bloque: "B", sala: 801, dia: "viernes", asignatura: "Matemáticas" },
  { usuario: "martina.rios@alumnos.ucn.cl", departamento: "g6", bloque: "C", sala: 802, dia: "sábado", asignatura: "Educación Física" },
  { usuario: "martina.rios@alumnos.ucn.cl", departamento: "x", bloque: "D", sala: 803, dia: "lunes", asignatura: "Biología" },

  { usuario: "sebastian.mendez@alumnos.ucn.cl", departamento: "g1", bloque: "E", sala: 901, dia: "martes", asignatura: "Química" },
  { usuario: "sebastian.mendez@alumnos.ucn.cl", departamento: "g2", bloque: "F", sala: 902, dia: "miércoles", asignatura: "Historia" },

  { usuario: "paula.vera@alumnos.ucn.cl", departamento: "g3", bloque: "C2", sala: 1001, dia: "jueves", asignatura: "Lenguaje" },
  { usuario: "paula.vera@alumnos.ucn.cl", departamento: "g4", bloque: "A", sala: 1002, dia: "viernes", asignatura: "Matemáticas" },
  { usuario: "paula.vera@alumnos.ucn.cl", departamento: "g5", bloque: "B", sala: 1003, dia: "sábado", asignatura: "Física" },
  { usuario: "paula.vera@alumnos.ucn.cl", departamento: "g6", bloque: "C", sala: 1004, dia: "lunes", asignatura: "Ciencias" }
];

export function validarCredencialesOffline(usuario, clave) {
  const usuarioEncontrado = usuariosPredeterminados.find(u => u.usuario === usuario);

  if (!usuarioEncontrado) return 2; // Usuario incorrecto
  if (usuarioEncontrado.clave !== clave) return 3; // Contraseña incorrecta
  
  return 1; // Credenciales correctas, el usuario es el correcto
}

export function buscarHorariosPorUsuarioOffline(usuario) {
  return horarios.filter(h => h.usuario === usuario);
}

export function obtenerClasesConCoordenadasOffline(usuario) {
  return horarios
    .filter(h => h.usuario === usuario)
    .map(h => {
      const depto = departamentos.find(d => d.nombre === h.departamento);
      return {
        departamento: h.departamento.toUpperCase(),
        bloque: h.bloque,
        sala: h.sala,
        dia: h.dia,
        asignatura: h.asignatura,
        x: depto?.x || null,
        y: depto?.y || null
      };
    });
}

export function agregarCursoOffline(usuario, curso) {
  horarios.push({ usuario, ...curso });  
  return { ok: true };
}

export function eliminarCursoOffline(usuario, curso) {
  horarios = horarios.filter(
    h => !(h.usuario === usuario && h.dia === curso.dia && h.bloque === curso.bloque)
  );
  return { ok: true };
}

export function obtenerNombresDepartamentosOffline() {
  const nombres = departamentos.map((d) => d.nombre);
  return nombres;
}



