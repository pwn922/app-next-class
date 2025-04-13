import { validarCredencialesOffline, buscarHorariosPorUsuarioOffline, obtenerClasesConCoordenadasOffline, agregarCursoOffline, eliminarCursoOffline ,obtenerNombresDepartamentosOffline } from './conexion_demo/conexion';
import { enviarCredencialesAlBackend, buscarHorariosPorUsuarioAlBackend, obtenerClasesConCoordenadasAlBackend , agregarCursoBackend, eliminarCursoBackend, obtenerNombresDepartamentosBackend } from './conexion_back/conexion';



export async function validarCredenciales(usuario, clave) {
  try {
    const data = await enviarCredencialesAlBackend(usuario, clave);
    return procesarRespuestaLogin(data, clave);
  } catch (error) {
    console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return validarCredencialesOffline(usuario, clave);
  }
}

export async function buscarHorariosPorUsuario(usuario, clave) {
  try {
    const data = await buscarHorariosPorUsuarioAlBackend(usuario, clave);
    return data;
  } catch (error) {
    console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return buscarHorariosPorUsuarioOffline(usuario);
  }
}

export async function obtenerClasesConCoordenadas(usuario, clave) {
  try {
    const data = await obtenerClasesConCoordenadasAlBackend(usuario, clave);
    return data;
  } catch (error) {
    console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return obtenerClasesConCoordenadasOffline(usuario);
  }
}

export async function agregarCurso(usuario, nuevoCurso, clave) {
  try {
    await agregarCursoBackend(usuario, nuevoCurso, clave);
    return { ok: true };
  } catch (error) {
    console.warn("Fallo en el backend, usando demo:", error);
    return agregarCursoOffline(usuario, nuevoCurso);
  }
}

export async function eliminarCurso(usuario, curso, clave) {
  try {
    await eliminarCursoBackend(usuario, curso, clave);
    return { ok: true };
  } catch (error) {
    console.warn("Fallo en el backend, usando demo:", error);
    return eliminarCursoOffline(usuario, curso);
  }
}

export async function obtenerNombresDepartamentos(clave) {
  try {
    await obtenerNombresDepartamentosBackend(clave);
    return { ok: true };
  } catch (error) {
    console.warn("Fallo en el backend, usando demo:", error);
    return obtenerNombresDepartamentosOffline;
  }
}

function procesarRespuestaLogin(data) {
  if (data && data.success) {
    return 1;
  }

  if (data && data.error) {
    if (data.error === "Usuario incorrecto") {
      return 2;
    } else if (data.error === "Contraseña incorrecta") {
      return 3;
    }
  }
  return 3;
}