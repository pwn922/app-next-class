import { DELETE_USER_SCHEDULE_BY_ID, GET_ALL_PAVILIONS, HORARIO_POR_USUARIO_URL, INFO_PAVILION_BY_NAME_URL, LOGIN_V1, POST_SCHEDULE } from "@/constant";
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
    const errorText = await response.json();
    if (errorText.error_code === 'INVALID_CREDENTIALS') {
      throw new Error("Credenciales inválidas. Por favor, revisa tu correo o contraseña.");
    }
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText.message}`);
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
    //console.error("Fallo en la conexión con el backend, usando respaldo local:", error);
    return [];
  }
}


export async function agregarCursoBackend(curso: { block: string, classroom: string, day: string, pavilion: string, subject: string }) {
  const { accessToken } = await getTokens(); // Obtener el token de acceso

  // Datos que vamos a enviar en el body de la solicitud
  const cursoData = {
    schedules: [
      {
        block: curso.block,           // 'A', 'B', etc.
        classroom: String(curso.classroom), // Aseguramos que sea un string
        day: curso.day,               // 'lunes', 'martes', etc.
        pavilion: curso.pavilion,     // El nombre del pabellón
        subject: curso.subject       // El nombre de la asignatura
      }
    ]
  };

  try {
    // Enviamos la solicitud POST al backend
    const response = await fetch(`${POST_SCHEDULE}`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}` // Añadimos el token de autorización
      },
      body: JSON.stringify(cursoData) // Convertimos el objeto a JSON
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Error al agregar el curso: ${response.status} - ${errorText}`);
    }

    // Si todo está bien, recibimos los datos del backend
    const result = await response.json();
    console.log("Curso agregado correctamente:", result);
    return result; // Devuelve la respuesta del backend

  } catch (error) {
    console.error('Error al enviar el curso:', error);
    throw new Error('Error al agregar el curso');
  }
}

export async function eliminarCursoBackend(curso: { bloque: string, dia: string, asignatura: string, sala: number, departamento: string }) {
  const { accessToken } = await getTokens();  

  try {
    // Primero, obtenemos todos los horarios del usuario
    const horariosResponse = await fetch(`${HORARIO_POR_USUARIO_URL}`, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!horariosResponse.ok) {
      const errorText = await horariosResponse.text();
      throw new Error(`Error al obtener los horarios: ${horariosResponse.status} - ${errorText}`);
    }

    const horariosData = await horariosResponse.json();
    console.log("Horarios del usuario:", horariosData);
    console.log("curso", curso);
    // Filtramos los horarios para encontrar el que coincida con el bloque, día y asignatura del curso
    const cursoEncontrado = horariosData.data.find((horario: any) => {
      console.log("horario:", horario);
      return horario.block === curso.bloque && 
             horario.day.toLowerCase() === curso.dia.toLowerCase() && 
             horario.subject === curso.asignatura;
    });

    if (!cursoEncontrado) {
      throw new Error('No se encontró el curso en los horarios del usuario');
    }

    // Obtener la ID del curso encontrado
    const cursoId = cursoEncontrado.id;
    console.log('ID del curso encontrado:', cursoId);

    // Ahora llamamos a la función para eliminar el curso usando la ID obtenida
    const deleteResponse = await fetch(`${DELETE_USER_SCHEDULE_BY_ID}/${cursoId}`, {
      method: 'DELETE',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${accessToken}`,
      },
    });

    if (!deleteResponse.ok) {
      const errorText = await deleteResponse.text();
      throw new Error(`Error al eliminar el curso: ${deleteResponse.status} - ${errorText}`);
    }

    const result = await deleteResponse.json();
    console.log("Curso eliminado correctamente:", result);
    return result;

  } catch (error) {
    console.error('Error al eliminar el curso:', error);
    throw new Error('Error al eliminar el curso');
  }
}


export async function obtenerNombresDepartamentosBackend() {
  const { accessToken } = await getTokens();

  // Hacemos una solicitud al backend para obtener los pabellones completos
  const response = await fetch(`${GET_ALL_PAVILIONS}`, {
    method: "GET",
    headers: {
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`,
    },
  });

  if (!response.ok) {
    const errorText = await response.text();
    throw new Error(`Error en la conexión al backend: ${response.status} - ${errorText}`);
  }

  const data = await response.json();

  if (data.success && Array.isArray(data.data)) {
    // Retornamos toda la información del pabellón sin procesar
    return data.data;
  } else {
    throw new Error("No se encontraron pabellones disponibles.");
  }
}
