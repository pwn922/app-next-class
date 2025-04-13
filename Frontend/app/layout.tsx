import React, { useState, useEffect } from 'react';
import { ScrollView, View, Text, Button } from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';

import { buscarHorariosPorUsuario, obtenerClasesConCoordenadas } from './src/validacion';

import HorarioTabla from './components/HorarioTabla';
import MapaClases from './components/MapaClases';
import SelectorPantalla from './components/SelectorPantalla';
import { bloquesHorario, bloques } from './utils/constantes';
import { generarTablaHorario } from './utils/funciones';





export default function Menu_de_usuario() {//aqui manejamos donde se controlaran las pantallas de horarios y mapa
  const router = useRouter();
  const { usuario, clave } = useLocalSearchParams();

  const [pantalla, setPantalla] = useState('horario');
  const [clasesCoordenadas, setClasesCoordenadas] = useState([]);
  const [claseMasCercana, setClaseMasCercana] = useState(null);

  const hoy = new Date();
  const diaActual = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][hoy.getDay()];
  const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes();

  useEffect(() => {
    if (!usuario) return;

    const cargarDatos = async () => {
      try {
        const horarios = await buscarHorariosPorUsuario(usuario,clave);
        // setHorarioUsuario(horarios || []);
        // setTablaHorario(generarTablaHorario(horarios || []));

        const coordenadas = await obtenerClasesConCoordenadas(usuario,clave);
        setClasesCoordenadas(coordenadas || []);

        const clasesHoy = (coordenadas || [])
          .filter(c => c.dia === diaActual)
          .map(c => {
            const bloque = bloquesHorario[c.bloque];
            const inicioMin = parseInt(bloque.inicio.split(':')[0]) * 60 + parseInt(bloque.inicio.split(':')[1]);
            return { ...c, minutosInicio: inicioMin };
          })
          .sort((a, b) => a.minutosInicio - b.minutosInicio);

        const siguienteClase = clasesHoy.find(c => c.minutosInicio >= horaActualMin);
        setClaseMasCercana(siguienteClase || null);
      } catch (err) {
        console.error("Error al cargar datos:", err);
      }
    };

    cargarDatos();
  }, [usuario]);

  const bloqueActual = bloques.find(b => {
    const { inicio, fin } = bloquesHorario[b];
    const inicioMin = parseInt(inicio.split(':')[0]) * 60 + parseInt(inicio.split(':')[1]);
    const finMin = parseInt(fin.split(':')[0]) * 60 + parseInt(fin.split(':')[1]);
    return horaActualMin >= inicioMin && horaActualMin < finMin;
  });

  const indiceBloqueSiguiente = bloqueActual ? bloques.indexOf(bloqueActual) + 1 : -1;
  const siguienteBloque = bloques[indiceBloqueSiguiente] || null;

  return (
    <ScrollView contentContainerStyle={{ flexGrow: 1, backgroundColor: '#8B4000', padding: 20, alignItems: 'center' }}>
      <View style={{ alignItems: 'center', marginBottom: 20 }}>
        <Text style={{ fontSize: 24, fontWeight: 'bold', color: 'white' }}>Datos de BlackBox</Text>
        <Text style={{ fontSize: 18, color: 'white' }}>Usuario: {usuario}</Text>

        <SelectorPantalla pantalla={pantalla} setPantalla={setPantalla} />
      </View>

      {pantalla === 'horario' && (
        <ScrollView horizontal contentContainerStyle={{ alignItems: 'center', justifyContent: 'center' }}>
          <HorarioTabla usuario={usuario} clave={clave} />
        </ScrollView>
      )}

      {pantalla === 'mapa' && (
        <MapaClases usuario={usuario} clave={clave} />
      )}

      <View style={{ marginTop: 20 }}>
        <Button title="CERRAR SESIÓN" onPress={() => router.push('/')} />
      </View>
    </ScrollView>
  );
}
