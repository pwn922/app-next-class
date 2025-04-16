import { LOGIN_V1 } from "@/constant";
import { getTokens } from "@/storage/storage";
import { BACKEND_URL } from "@env";




async function getBackend(endpoint: string) {
  const { accessToken } = await getTokens();

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (accessToken) {
    headers["Authorization"] = `Bearer ${accessToken}`;
  }

  const response = await fetch(`${BACKEND_URL}${endpoint}`, {
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

export async function enviarCredencialesAlBackend(usuario: string, clave: string) {

  const response = await fetch(`${LOGIN_V1}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email: usuario, password: clave }),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText}`);
  }

  const tokens = await response.json();
  console.log("token: ", tokens);
  return tokens;
}

export async function buscarHorariosPorUsuarioAlBackend() {
  // Asumimos que siempre tenemos el token
  const { accessToken } = await getTokens();
  const response = await fetch(`${BACKEND_URL}/buscar_horario`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`,  // Enviamos el access_token en el encabezado
    },
    body: JSON.stringify({}),
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText}`);
  }

  return await response.json();
}

export function obtenerClasesConCoordenadasAlBackend() {
  return postAlBackend(`${BACKEND_URL}/clases_coordenadas`, {  });
}

export function agregarCursoBackend(curso:string) {
  return postAlBackend(`${BACKEND_URL}/buscar_horario`, {  });
}

export function eliminarCursoBackend (curso:string) {
  return postAlBackend(`${BACKEND_URL}/clases_coordenadas`, {  });
}

export function obtenerNombresDepartamentosBackend() {
  return postAlBackend(`${BACKEND_URL}/clases_coordenadas`, {  });
}