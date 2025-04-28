import React, { useState, useEffect } from 'react';
import { ScrollView, View, Text, Button } from 'react-native';
import { useRouter } from 'expo-router';




import HorarioTabla from './components/HorarioTabla';
import MapaClases from './components/MapaClases';
import SelectorPantalla from './components/SelectorPantalla';
import { bloquesHorario, bloques } from './utils/constantes';
import { obtenerClasesConCoordenadas } from './src/validacion';
import { GET_USER } from '@/constant';
import { getTokens } from '@/storage/storage';

type Clase = {
  dia: string;
  bloque: keyof typeof bloquesHorario;
  minutosInicio?: number;
  [key: string]: any; 
};

export default function Menu_de_usuario(): JSX.Element {
  const router = useRouter();

  const [pantalla, setPantalla] = useState<'horario' | 'mapa'>('horario');
  const [clasesCoordenadas, setClasesCoordenadas] = useState<Clase[]>([]);
  const [claseMasCercana, setClaseMasCercana] = useState<Clase | null>(null);
  const [email, setEmail] = useState<string>(''); // Estado para almacenar el email

  const hoy = new Date();
  const diaActual = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][hoy.getDay()];
  const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes();

  useEffect(() => {
    // Función para cargar los datos del usuario
    const cargarDatos = async () => {
      try {
        const { accessToken } = await getTokens();
        if (!accessToken) {
          console.error('Token de acceso no encontrado');
          return;
        }

        // Realizar la solicitud para obtener los datos del usuario
        const response = await fetch(GET_USER, {
          method: 'GET',
          headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        });

        const data = await response.json();

        if (data.success) {
          setEmail(data.data.email); // Asignar el email del usuario al estado
        } else {
          console.error('Error al obtener los datos del usuario:', data.message);
        }

        // Cargar las coordenadas de las clases
        const coordenadas: Clase[] = await obtenerClasesConCoordenadas();
        setClasesCoordenadas(coordenadas || []);

        const clasesHoy = (coordenadas || [])
          .filter(c => c.dia === diaActual)
          .map(c => {
            const bloque = bloquesHorario[c.bloque];
            const inicioMin = parseInt(bloque.inicio.split(':')[0]) * 60 + parseInt(bloque.inicio.split(':')[1]);
            return { ...c, minutosInicio: inicioMin };
          })
          .sort((a, b) => (a.minutosInicio ?? 0) - (b.minutosInicio ?? 0));

        const siguienteClase = clasesHoy.find(c => (c.minutosInicio ?? 0) >= horaActualMin);
        setClaseMasCercana(siguienteClase || null);
      } catch (err) {
        console.error("Error al cargar datos:", err);
      }
    };

    cargarDatos();
  }, []);

  const bloqueActual = bloques.find(b => {
    const { inicio, fin } = bloquesHorario[b as keyof typeof bloquesHorario];
    const inicioMin = parseInt(inicio.split(':')[0]) * 60 + parseInt(inicio.split(':')[1]);
    const finMin = parseInt(fin.split(':')[0]) * 60 + parseInt(fin.split(':')[1]);
    return horaActualMin >= inicioMin && horaActualMin < finMin;
  });

  const indiceBloqueSiguiente = bloqueActual ? bloques.indexOf(bloqueActual) + 1 : -1;
  const siguienteBloque = bloques[indiceBloqueSiguiente] || null;

  return (
    <ScrollView contentContainerStyle={{ flexGrow: 1, backgroundColor: '#8B4000', padding: 20, alignItems: 'center' }}>
      <View style={{ alignItems: 'center', marginBottom: 20 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', color: 'white' }}>Horario</Text>
        <Text style={{ fontSize: 18, color: 'white' }}>Usuario: {email || "Cargando..."}</Text>

        <SelectorPantalla pantalla={pantalla} setPantalla={setPantalla} />
      </View>

      {pantalla === 'horario' && (
        <ScrollView horizontal contentContainerStyle={{ alignItems: 'center', justifyContent: 'center' }}>
          <HorarioTabla />
        </ScrollView>
      )}

      {pantalla === 'mapa' && (
        <MapaClases />
      )}

      <View style={{ marginTop: 20 }}>
        <Button title="CERRAR SESIÓN" onPress={() => router.push('/')} />
      </View>
    </ScrollView>
  );
}
