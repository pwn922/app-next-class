import { HORARIO_POR_USUARIO_URL, INFO_PAVILION_BY_NAME_URL, LOGIN_V1 } from "@/constant";
import { getTokens } from "@/storage/storage";
import { BACKEND_URL } from "@env";


export async function enviarCredencialesAlBackend(usuario: string, clave: string) {
  console.log("Enviando credenciales al backend:", { email: usuario, password: clave });
  console.log(LOGIN_V1);
  const response = await fetch(`${LOGIN_V1}`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ email: usuario, password: clave }),
  });

  if (!response.ok) {
    const errorText = true;
    //console.log(errorText);
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText}`);
  }

  const tokens = await response.json();
  //console.log("Tokens recibidos:", tokens);
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



export async function obtenerClasesConCoordenadasAlBackend() {
  try {
    const { accessToken } = await getTokens();

    if (!accessToken) {
      throw new Error("No se encontró el token.");
    }

    console.log("entrando al metodo");
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
      throw new Error("Formato inesperado en la respuesta del horario.");
    }

    // Usamos Promise.all para esperar todas las consultas de pabellones
    const clases = await Promise.all(
      data_horario.data.map(async (clase: any) => {
        const response_pavilion = await fetch(`${INFO_PAVILION_BY_NAME_URL}${clase.pavilion}`);

        if (!response_pavilion.ok) {
          throw new Error(`Error al obtener datos del pabellón ${clase.pavilion}`);
        }

        const data_pavilion = await response_pavilion.json();

        return {
          departamento: data_pavilion.data.name.toUpperCase(),
          bloque: clase.block,
          sala: parseInt(clase.classroom),
          dia: clase.day.toLowerCase(),
          asignatura: clase.subject,
          x: data_pavilion.data.x,
          y: data_pavilion.data.y,
        };
      })
    );

    console.log(clases);
    return clases;

  } catch (error) {
    console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return [];
  }
}

/*
export function obtenerClasesConCoordenadasOffline(usuario:string) {
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
*/

export function agregarCursoBackend(curso:string) {
  console.log("agrego un curso")
  //return postAlBackend(`${BACKEND_URL}/buscar_horario`, {  });
}

export function eliminarCursoBackend (curso:string) {
  //return postAlBackend(`${BACKEND_URL}/clases_coordenadas`, {  });
}

export function obtenerNombresDepartamentosBackend() {
  //return postAlBackend(`${BACKEND_URL}/clases_coordenadas`, {  });
}
