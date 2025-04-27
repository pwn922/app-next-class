import React, { useEffect, useState } from 'react';
import { View, Text, Image, ScrollView } from 'react-native';
import { Svg, Image as SvgImage } from 'react-native-svg';
import { bloquesHorario, bloques, ClaseConCoordenadas, ClaseConMinutos, Dia, Bloque } from '../utils/constantes';
import { obtenerClasesConCoordenadas } from '../src/validacion';

export default function MapaClases() {
  const [clasesCoordenadas, setClasesCoordenadas] = useState<ClaseConCoordenadas[]>([]);
  const [claseMasCercana, setClaseMasCercana] = useState<ClaseConMinutos | null>(null);

  //const escalaX = 3;
  //const escalaY = 3;
  const escala = 2;

  const hoy = new Date();
  const diaActual: Dia = ['domingo', 'lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'][hoy.getDay()] as Dia;
  const dias: Dia[] = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'];
  const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes();
  let horarioA_rojo = 'null';
  horarioA_rojo = 'Dato de actualizado horario rojo prueba';
  
  useEffect(() => {
    const cargarDatosMapa = async () => {
      try {
        const coordenadas = await obtenerClasesConCoordenadas();
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
  }, []);

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

      {/*<View style={{ marginBottom: 10 }}>
        {claseMasCercana ? (
          <Text style={{ color: 'white', fontSize: 16, textAlign: 'center' }}>
            {`Próxima clase: ${claseMasCercana.asignatura} en el pabellón ${claseMasCercana.departamento} (Sala ${claseMasCercana.sala})`}
          </Text>
        ) : (
          <Text style={{ color: 'white', fontSize: 16, textAlign: 'center' }}>
            Terminó el periodo académico de esta semana
          </Text>
        )}
      </View>*/}

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
              width="928"//"903"
              height="602"//"1394"
              preserveAspectRatio="xMidYMid slice"
              href={require('../src/mapa.jpg')}
            />
          </Svg>

          {clasesCoordenadas.map((clase, index) => {
            let gif = require('../src/verde.gif'); 
            const diaClase = clase.dia;

            const hoy = new Date();
            const diaActual: Dia = dias[hoy.getDay()];
            const horaActualMin = hoy.getHours() * 60 + hoy.getMinutes();

            const bloque = bloquesHorario[clase.bloque];
            const minutosInicio = parseInt(bloque.inicio.split(':')[0]) * 60 + parseInt(bloque.inicio.split(':')[1]);
            const minutosFin = parseInt(bloque.fin.split(':')[0]) * 60 + parseInt(bloque.fin.split(':')[1]);

            const diaActualIndex = dias.indexOf(diaActual); 
            const diaClaseIndex = dias.indexOf(diaClase);   
            const diaSiguienteIndex = (diaActualIndex + 1) % 7;  

            if (diaClaseIndex === diaActualIndex) {
              if (horaActualMin >= minutosInicio && horaActualMin < minutosFin) {
                gif = require('../src/rojo.gif');
              } else {
                gif = require('../src/amarillo.gif');
              }
            } else if (diaClaseIndex === diaSiguienteIndex) {
              gif = require('../src/naranja.gif');
            } else if ((diaClaseIndex + 7 - diaActualIndex) % 7 < 3) {
              gif = require('../src/amarillo.gif');
            } else if (diaClaseIndex < diaActualIndex) {
              gif = require('../src/verde.gif');
            }

            return (
              <Image
                key={index}
                source={gif}
                style={{
                  width: 30,
                  height: 30,
                  position: 'absolute',
                  top: 602 - clase.x * escala - 24,
                  left: clase.y * escala - 12,
                }}
              />
            );
          })}
        </View>
      </ScrollView>
    </View>
  );
}
