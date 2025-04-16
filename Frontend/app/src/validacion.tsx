import { validarCredencialesOffline, buscarHorariosPorUsuarioOffline, obtenerClasesConCoordenadasOffline, agregarCursoOffline, eliminarCursoOffline ,obtenerNombresDepartamentosOffline } from './conexion_demo/conexion';
import { enviarCredencialesAlBackend, buscarHorariosPorUsuarioAlBackend, obtenerClasesConCoordenadasAlBackend , agregarCursoBackend, eliminarCursoBackend, obtenerNombresDepartamentosBackend } from './conexion_back/conexion';
import { getTokens } from "@/storage/storage";
import { BACKEND_URL } from '@env';

export async function validarCredenciales() {
  try {
    // Intentamos obtener el access_token desde AsyncStorage
    const { accessToken } = await getTokens();

    if (accessToken) {
      // Si tenemos un access_token, lo usamos para validar al usuario con el backend
      const data = await enviarCredencialesAlBackendConToken(accessToken);
      return procesarRespuestaLogin(data);
    } else {
      // Si no tenemos el token, simplemente lanzamos un error
      throw new Error("Token no encontrado.");
    }
  } catch (error) {
    console.error("Fallo en la conexión con el backend, no se puede usar el modo demo:", error);
    // En lugar de intentar un fallback, retornamos un error claro
    return 3; // Error: no se pudo autenticar, no hay token disponible
  }
}

async function enviarCredencialesAlBackendConToken(accessToken: string) {
  const response = await fetch(`${BACKEND_URL}/validate_token`, {
    method: "GET",
    headers: {
      "Authorization": `Bearer ${accessToken}`,  // Enviamos el token para validación
    },
  });

  if (!response.ok) {
    throw new Error(`Error validando el token: ${response.status}`);
  }

  const data = await response.json();
  return data;
}

export async function buscarHorariosPorUsuario() {
  try {
    const data = await buscarHorariosPorUsuarioAlBackend( );
    return data;
  } catch (error) {
    console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return 
  }
}

export async function obtenerClasesConCoordenadas( ) {
  try {
    const data = await obtenerClasesConCoordenadasAlBackend( );
    return data;
  } catch (error) {
    const usuario= "a";
    console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return obtenerClasesConCoordenadasOffline(usuario);
  }
}

export async function agregarCurso(nuevoCurso:string) {
  try {
    await agregarCursoBackend(nuevoCurso);
    return { ok: true };
  } catch (error) {
    const usuario ="a";
    console.warn("Fallo en el backend, usando demo:", error);
    return agregarCursoOffline(usuario,nuevoCurso);
  }
}

export async function eliminarCurso(curso: string) {
  try {
    await eliminarCursoBackend(curso);
    return { ok: true };
  } catch (error) {
    const usuario = "offline";
    console.warn("Fallo en el backend, usando demo:", error);
    return eliminarCursoOffline(usuario, curso);
  }
}

export async function obtenerNombresDepartamentos() {
  try {
    //await obtenerNombresDepartamentosBackend(clave);
    await obtenerNombresDepartamentosBackend();
    return { ok: true };
  } catch (error) {
    console.warn("Fallo en el backend, usando demo:", error);
    return obtenerNombresDepartamentosOffline;
  }
}

function procesarRespuestaLogin(data:any) {
  if (data && data.success) {
    return 1; // Sesión válida
  }

  if (data && data.error) {
    if (data.error === "Token inválido") {
      return 3; // Token inválido
    }
  }
  return 3; // Token no válido o error desconocido
}
