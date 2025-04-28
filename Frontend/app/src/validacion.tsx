import { validarCredencialesOffline, buscarHorariosPorUsuarioOffline, obtenerClasesConCoordenadasOffline, agregarCursoOffline, eliminarCursoOffline ,obtenerNombresDepartamentosOffline } from './conexion_demo/conexion';
import { enviarCredencialesAlBackend, buscarHorariosPorUsuarioAlBackend, obtenerClasesConCoordenadasAlBackend , agregarCursoBackend, eliminarCursoBackend, obtenerNombresDepartamentosBackend } from './conexion_back/conexion';
import { getTokens } from "@/storage/storage";
import { BACKEND_URL } from '@env';
import { ClaseConCoordenadas } from '../utils/constantes';
import { HORARIO_POR_USUARIO_URL } from '@/constant';

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
    method: "POST",
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
    const { accessToken } = await getTokens();

    if (!accessToken) {
      throw new Error("No se encontró el token.");
    }

    console.log("entrando al metodo buscarHorariosPorUsuario");
    
    // Llamada GET para obtener los horarios del usuario
    const response = await fetch(`${HORARIO_POR_USUARIO_URL}`, {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        "Authorization": `Bearer ${accessToken}`,
      },
    });

    if (!response.ok) {
      throw new Error("Error en la conexión con el backend.");
    }

    const data_horario = await response.json();

    if (!Array.isArray(data_horario.data)) {
      throw new Error("Formato inesperado en la respuesta de los horarios.");
    }

    // Solo devolvemos la información del usuario (sin pabellones)
    const horariosUsuario = data_horario.data.map((clase: any) => ({
      departamento: clase.pavilion,
      bloque: clase.block,
      sala: parseInt(clase.classroom),
      dia: clase.day.toLowerCase(),
      asignatura: clase.subject,
    }));

    console.log(horariosUsuario);
    return horariosUsuario;

  } catch (error) {
    //console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return [];
  }
}


export async function obtenerClasesConCoordenadas(): Promise<ClaseConCoordenadas[]> {
  try {
    const data: ClaseConCoordenadas[] = await obtenerClasesConCoordenadasAlBackend();
    return data;
  } catch (error) {
    const usuario = 'a'; // puedes parametrizarlo si se necesita más adelante
    //console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    //return obtenerClasesConCoordenadasOffline(usuario);
    return [];
    
  }
}

export async function agregarCurso(nuevoCurso:any) {
  try {
    await agregarCursoBackend(nuevoCurso);
    return { ok: true };
  } catch (error) {
    const usuario ="a";
    console.warn("Fallo en el backend, usando demo:", error);
    return agregarCursoOffline(usuario,nuevoCurso);
  }
}

export async function eliminarCurso(curso: any) {
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
    return [];
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
