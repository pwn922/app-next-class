const BASE_URL = "https://tu-backend.com/api";

async function postAlBackend(endpoint, body) {
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

export function enviarCredencialesAlBackend(usuario, clave) {
  return postAlBackend(`${BASE_URL}/login`, { usuario, clave });
}

export function buscarHorariosPorUsuarioAlBackend(usuario, clave) {
  return postAlBackend(`${BASE_URL}/buscar_horario`, { usuario });
}

export function obtenerClasesConCoordenadasAlBackend(usuario, clave) {
  return postAlBackend(`${BASE_URL}/clases_coordenadas`, { usuario });
}

export function agregarCursoBackend(usuario, curso, clave) {
  return postAlBackend(`${BASE_URL}/buscar_horario`, { usuario });
}

export function eliminarCursoBackend (usuario, curso, clave) {
  return postAlBackend(`${BASE_URL}/clases_coordenadas`, { usuario });
}

export function obtenerNombresDepartamentosBackend (clave) {
  return postAlBackend(`${BASE_URL}/clases_coordenadas`, { usuario });
}
