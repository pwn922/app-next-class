import { getTokens } from "@/storage/storage";

const BASE_URL = "https://tu-backend.com/api";


async function getBackend(endpoint: string) {
  const { accessToken } = await getTokens();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    method: "GET",
    headers,
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText}`);
  }

  return await response.json();
}

async function postAlBackend(endpoint:string, body:any) {
  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(body)
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText}`);
  }

  return await response.json();
}
/*
export function enviarCredencialesAlBackend(usuario, clave) {
  return postAlBackend(`${BASE_URL}/login`, { usuario, clave });
}
*/
export function buscarHorariosPorUsuarioAlBackend(usuario:string, clave:string) {
  return postAlBackend(`${BASE_URL}/buscar_horario`, { usuario });
}

export function obtenerClasesConCoordenadasAlBackend(usuario:string, clave:string) {
  return postAlBackend(`${BASE_URL}/clases_coordenadas`, { usuario });
}

export function agregarCursoBackend(usuario:string, curso:string, clave:string) {
  return postAlBackend(`${BASE_URL}/buscar_horario`, { usuario });
}

export function eliminarCursoBackend (usuario:string, curso:string, clave:string) {
  return postAlBackend(`${BASE_URL}/clases_coordenadas`, { usuario });
}

export function obtenerNombresDepartamentosBackend (clave:string) {
  return postAlBackend(`${BASE_URL}/clases_coordenadas`, { usuario });
}
