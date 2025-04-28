import React, { useEffect, useState } from 'react';
import { View, Text, Image, ScrollView } from 'react-native';
import { Svg, Image as SvgImage } from 'react-native-svg';
import { bloquesHorario, bloques, ClaseConCoordenadas, ClaseConMinutos, Dia, Bloque } from '../utils/constantes';
import { obtenerClasesConCoordenadas } from '../src/validacion';

export default function MapaClases() {
  const [clasesCoordenadas, setClasesCoordenadas] = useState<ClaseConCoordenadas[]>([]);
  const [claseMasCercana, setClaseMasCercana] = useState<ClaseConMinutos | null>(null);
  const [claseActual, setClaseActual] = useState<ClaseConCoordenadas | null>(null);

  const escala = 2; // Factor de escala

  const hoy = new Date();
  const diaActual: Dia = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][hoy.getDay()] as Dia;
  const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes(); // Hora en minutos

  // Identificar el bloque actual
  const bloqueActual = bloques.find(b => {
    const { inicio, fin } = bloquesHorario[b];
    const inicioMin = parseInt(inicio.split(':')[0]) * 60 + parseInt(inicio.split(':')[1]);
    const finMin = parseInt(fin.split(':')[0]) * 60 + parseInt(fin.split(':')[1]);
    return horaActualMin >= inicioMin && horaActualMin < finMin; // Bloque actual si la hora está dentro del rango
  });

  // Si no hay bloque actual, lo ponemos en 'A' o en un bloque predeterminado
  const bloqueActualValido = bloqueActual ? bloqueActual : 'A';

  const indiceBloqueSiguiente = bloques.indexOf(bloqueActualValido) + 1;
  const siguienteBloque: Bloque | null = bloques[indiceBloqueSiguiente] || null;

  useEffect(() => {
    const cargarDatosMapa = async () => {
      try {
        const coordenadas = await obtenerClasesConCoordenadas();
        setClasesCoordenadas(coordenadas || []);

        // Filtrar solo las clases del día actual
        const clasesHoy = (coordenadas || [])
          .filter(c => c.dia === diaActual) // Solo las clases del día actual
          .map(c => {
            const bloque = bloquesHorario[c.bloque];
            const inicioMin = parseInt(bloque.inicio.split(':')[0]) * 60 + parseInt(bloque.inicio.split(':')[1]);
            return { ...c, minutosInicio: inicioMin };
          })
          .sort((a, b) => a.minutosInicio - b.minutosInicio);

        // Buscar la clase actual
        const claseActual = clasesHoy.find(c => c.minutosInicio <= horaActualMin && (bloques.indexOf(c.bloque) === bloques.indexOf(bloqueActualValido) || bloques.indexOf(c.bloque) < bloques.indexOf(bloqueActualValido)));
        setClaseActual(claseActual || null);

        // Buscar la siguiente clase
        const siguienteClase = clasesHoy.find(c => c.minutosInicio > horaActualMin);
        setClaseMasCercana(siguienteClase || null);
      } catch (err) {
        console.error("Error al cargar datos del mapa:", err);
      }
    };

    cargarDatosMapa();
  }, [diaActual, horaActualMin, bloqueActualValido]);

  return (
    <View style={{ flex: 1, marginTop: 10, borderWidth: 1, borderColor: 'white' }}>
      <Text style={{ color: 'white', fontWeight: 'bold', marginBottom: 5, textAlign: 'center' }}>
        Ubicación de clases
      </Text>

      <Text style={{ color: 'white', fontSize: 18, textAlign: 'center', marginBottom: 10 }}>
        {`Fecha: ${hoy.toLocaleDateString('es-ES', {
          weekday: 'long',
          year: 'numeric',
          month: 'long',
          day: 'numeric',
        })}`}
        {'\n'}
        {`Hora: ${hoy.toLocaleTimeString('es-ES', { hour: '2-digit', minute: '2-digit' })}`}
      </Text>

      <ScrollView 
        style={{ flex: 1 }}
        contentContainerStyle={{ alignItems: 'center', paddingVertical: 20 }}
        minimumZoomScale={1}
        maximumZoomScale={5}
        bouncesZoom={true}
        horizontal={true}
      >
        <View style={{ width: 928, height: 602 }}>
          <Svg height="100%" width="100%" style={{ position: 'absolute' }}>
            <SvgImage
              x="0"
              y="0"
              width="928"
              height="602"
              preserveAspectRatio="xMidYMid slice"
              href={require('../src/mapa.jpg')}
            />
          </Svg>

          {/* Marca la clase actual en verde */}
          {claseActual && (
            <Image
              key={claseActual.bloque}
              source={require('../src/verde.gif')} // Usamos verde.gif para la clase actual
              style={{
                width: 30,
                height: 30,
                position: 'absolute',
                top: 602 - claseActual.y * escala - 24,
                left: claseActual.x * escala - 12,
              }}
            />
          )}

          {/* Solo muestra la próxima clase en amarillo */}
          {claseMasCercana && (
            <Image
              key={claseMasCercana.bloque}
              source={require('../src/amarillo.gif')} // Usamos amarillo.gif para la próxima clase
              style={{
                width: 30,
                height: 30,
                position: 'absolute',
                top: 602 - claseMasCercana.y * escala - 24,
                left: claseMasCercana.x * escala - 12,
              }}
            />
          )}
        </View>
      </ScrollView>
    </View>
  );
}
