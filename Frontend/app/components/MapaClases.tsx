//Aqui es donde se maneja la pantalla del mapa
import React, { useEffect, useState } from 'react';
import { View, Text, Image } from 'react-native';
import { Svg, Image as SvgImage } from 'react-native-svg';
import { bloquesHorario, bloques } from '../utils/constantes';
import { obtenerClasesConCoordenadas } from '../src/validacion';

export default function MapaClases({ usuario, clave }) {
  const [clasesCoordenadas, setClasesCoordenadas] = useState([]);
  const [claseMasCercana, setClaseMasCercana] = useState(null);
  const escalaX = 3;
  const escalaY = 3;
  useEffect(() => {
    const hoy = new Date();
    const diaActual = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][hoy.getDay()];
    const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes();
    const cargarDatosMapa = async () => {
      try {
        const coordenadas = await obtenerClasesConCoordenadas(usuario, clave);
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
        console.error("Error al cargar datos del mapa:", err);
      }
    };

    cargarDatosMapa();
  }, [usuario]);
  const hoy = new Date();
  const diaActual = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][hoy.getDay()];
  const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes();
  const bloqueActual = bloques.find(b => {
    const { inicio, fin } = bloquesHorario[b];
    const inicioMin = parseInt(inicio.split(':')[0]) * 60 + parseInt(inicio.split(':')[1]);
    const finMin = parseInt(fin.split(':')[0]) * 60 + parseInt(fin.split(':')[1]);
    return horaActualMin >= inicioMin && horaActualMin < finMin;
  });
  const indiceBloqueSiguiente = bloqueActual ? bloques.indexOf(bloqueActual) + 1 : -1;
  const siguienteBloque = bloques[indiceBloqueSiguiente] || null;
  return (
    <View style={{ marginTop: 10, borderWidth: 1, borderColor: 'white' }}>
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

      <View style={{ width: 903, height: 1394 }}>
        <Svg height="100%" width="100%" style={{ position: 'absolute' }}>
          <SvgImage
            x="0"
            y="0"
            width="1394"
            height="903"
            preserveAspectRatio="xMidYMid slice"
            href={require('../src/mapa.jpg')}
            transform="rotate(90, 451, 451)"
          />
        </Svg>

        {clasesCoordenadas.map((clase, index) => {
          let gif = require('../src/verde.gif');
          const bloque = bloquesHorario[clase.bloque];
          if (bloque && clase.dia === diaActual) {
            const minutosInicio =
              parseInt(bloque.inicio.split(':')[0]) * 60 + parseInt(bloque.inicio.split(':')[1]);
            const esClaseMasCercana =
              claseMasCercana &&
              clase.bloque === claseMasCercana.bloque &&
              clase.x === claseMasCercana.x &&
              clase.y === claseMasCercana.y;
            const esSiguienteBloque = clase.bloque === siguienteBloque;
            if (esClaseMasCercana) {
              gif = require('../src/rojo.gif');
            } else if (esSiguienteBloque) {
              gif = require('../src/naranja.gif');
            } else if (minutosInicio < horaActualMin) {
              gif = require('../src/verde.gif');
            } else if (minutosInicio > horaActualMin && minutosInicio < horaActualMin + 30) {
              gif = require('../src/naranja.gif');
            } else if (minutosInicio > horaActualMin) {
              gif = require('../src/amarillo.gif');
            }
          }

          return (
            <Image
              key={index}
              source={gif}
              style={{
                width: 50,
                height: 50,
                position: 'absolute',
                left: clase.x * escalaX - 12,
                top: clase.y * escalaY - 12,
                transform: [{ rotate: '90deg' }],
              }}
            />
          );
        })}
      </View>
    </View>
  );
}
