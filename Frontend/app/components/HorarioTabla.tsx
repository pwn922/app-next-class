//Aqui se maneja la talba del horario, ademas se agregan cursos  o eliminan respectivamente
import React, { useState, useEffect } from 'react';
import { View, Text, Button, TextInput, Alert, TouchableOpacity, ScrollView } from 'react-native';
import { bloquesHorario, bloques, dias, TablaHorario } from '../utils/constantes';
import { agregarCurso, eliminarCurso ,buscarHorariosPorUsuario, obtenerNombresDepartamentos} from '../src/validacion';
import { generarTablaHorario } from '../utils/funciones';
import { agregarCursoBackend, obtenerNombresDepartamentosBackend } from '../src/conexion_back/conexion';

export default function HorarioTabla({  }) {

  const [tablaHorario, setTablaHorario] = useState<TablaHorario>({});
  const [msg, setMsg] = useState('');
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [mostrarEliminar, setMostrarEliminar] = useState(false);
  const [departamentos, setDepartamentos] = useState<string[]>([]);
  const [usuario, setUsuario] = useState("");
  const [asignatura, setAsignatura] = useState("");
  const [nuevoCurso, setNuevoCurso] = useState({
    bloque: 'A',
    dia: 'lunes',
    asignatura: '',
    sala: 101,
    departamento: '',
  });

  useEffect(() => {
    const cargarHorario = async () => {
      //if (!usuario) return;

      try {
        const horarios = await buscarHorariosPorUsuario();
        const tabla = generarTablaHorario(horarios);
        setTablaHorario(tabla);
      } catch (err) {
        console.error('Error al cargar horario:', err);
        setMsg('Error al cargar horario');
      }
    };
    cargarHorario();

  }, []);
  
  useEffect(() => {
    const cargarPabellones = async () => {
      try {
        const pabellonesCompletos = await obtenerNombresDepartamentosBackend(); 
  
        
        const nombresPabellones = pabellonesCompletos.map((pabellon: { name: string }) => pabellon.name);
  
        
        setDepartamentos(nombresPabellones || []);
      } catch (err) {
        console.error('Error al cargar pabellones:', err);
      }
    };
  
    cargarPabellones();
  }, []);


  const handleAgregar = async () => {
    if (!nuevoCurso.departamento) {
      setMsg('Por favor, selecciona un pabellón.');
      return; // Asegura que el usuario haya seleccionado un pabellón
    }
  
    // Preparamos el objeto con los nombres correctos
    const cursoData = {
      block: nuevoCurso.bloque,         // 'A', 'B', etc.
      classroom: String(nuevoCurso.sala), // Aseguramos que sea un string
      day: nuevoCurso.dia,              // 'lunes', 'martes', etc.
      pavilion: nuevoCurso.departamento, // Nombre del pabellón
      subject: nuevoCurso.asignatura    // Nombre de la asignatura
    };
  
    try {
      // Llamada a la función que envía el curso al backend
      const res = await agregarCursoBackend(cursoData);
  
      if (res) {
        // Refetch (Reconsulta) los horarios actualizados del servidor
        const horariosActualizados = await buscarHorariosPorUsuario();
        setTablaHorario(generarTablaHorario(horariosActualizados)); // Actualizamos el estado con los nuevos horarios
        
        setMsg('Curso agregado!');
        setNuevoCurso({ 
          bloque: 'A',
          dia: 'lunes',
          asignatura: '',
          sala: 101,
          departamento: ''
        });
        setMostrarFormulario(false); // Ocultar el formulario después de agregar el curso
      } else {
        setMsg('Error al agregar el curso: ' + (res.message || "No se recibieron datos"));
      }
    } catch (error) {
      console.error('Error al agregar el curso:', error);
      setMsg('Hubo un problema al agregar el curso. Intenta nuevamente.');
    }
  };

  const handleEliminarCurso = async (bloque:string, dia:string, asignatura:string) => {

      const curso = {
        bloque,
        dia,
        asignatura,
        sala: 999,
        departamento: 'test',
      };
    console.log("curso eliminado",curso)
    const res = await eliminarCurso(curso);
    if (res.ok) {
      const horarios = await buscarHorariosPorUsuario();
      setTablaHorario(generarTablaHorario(horarios));
      setMsg(`Curso "${asignatura}" eliminado`);
    } else {
      setMsg('Error al eliminar el curso');
    }
  };
  return (
    <ScrollView contentContainerStyle={{ alignItems: 'center', paddingBottom: 50 }}>
      <Text style={{ color: 'white', marginBottom: 8 }}>{msg}</Text>
      {/* Esta es la tabla de horario ########################################################*/}
      <View style={{ flexDirection: 'row', backgroundColor: '#333', marginTop: 10 }}>
        <View style={{ width: 200, padding: 8, borderWidth: 1, borderColor: 'white' }}>
          <Text style={{ color: 'white', fontWeight: 'bold', textAlign: 'center' }}>Bloque</Text>
        </View>
        {dias.map((dia) => (
          <View key={dia} style={{ width: 100, padding: 8, borderWidth: 1, borderColor: 'white' }}>
            <Text style={{ color: 'white', fontWeight: 'bold', textAlign: 'center' }}>
              {dia.charAt(0).toUpperCase() + dia.slice(1)}
            </Text>
          </View>
        ))}
      </View>
      {bloques.map((bloque) => (
        <View key={bloque} style={{ flexDirection: 'row' }}>
          <View style={{ width: 200, padding: 8, borderWidth: 1, borderColor: 'white' }}>
            <Text style={{ color: 'white', fontWeight: 'bold', textAlign: 'center' }}>{bloque}</Text>
            <Text style={{ color: 'white', fontWeight: 'bold', textAlign: 'center' }}>
              ({bloquesHorario[bloque]?.inicio} - {bloquesHorario[bloque]?.fin})
            </Text>
          </View>
          {dias.map((dia) => (
            <View
              key={dia}
              style={{
                width: 100,
                height: 60,
                padding: 4,
                borderWidth: 1,
                borderColor: 'white',
                justifyContent: 'center',
              }}>
                <Text style={{ color: 'white', fontSize: 12, textAlign: 'center' }}>
                {tablaHorario?.[bloque]?.[dia] || '-'}
              </Text>
            </View>
          ))}
        </View>
      ))}
      <Button
        title={mostrarFormulario ? 'Ocultar Formulario' : 'Agregar Curso'}
        onPress={() => {
          setMostrarFormulario(!mostrarFormulario);
          setMostrarEliminar(false);
        }}
      />
      {mostrarFormulario && (
        <View style={{
          marginVertical: 10,
          padding: 16,
          borderColor: 'white',
          borderWidth: 1,
          borderRadius: 8,
          backgroundColor: '#222'
        }}>
          <Text style={{ color: 'white', fontWeight: 'bold', marginBottom: 8 }}>Agregar Curso</Text>
          <Text style={{ color: 'white', marginBottom: 4 }}>Asignatura:</Text>
          <TextInput
            style={{
              backgroundColor: 'white',
              marginBottom: 12,
              padding: 8,
              borderRadius: 4
            }}
            value={nuevoCurso.asignatura}
            onChangeText={(text) => setNuevoCurso({ ...nuevoCurso, asignatura: text })}
            placeholder="Nombre de la asignatura"
            placeholderTextColor="#888"
          />
          <Text style={{ color: 'white', marginBottom: 4 }}>Bloque:</Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', marginBottom: 12 }}>
            {['A', 'B', 'C', 'C2', 'D', 'E', 'F'].map((bloque) => (
              <TouchableOpacity
                key={bloque}
                style={{
                  backgroundColor: nuevoCurso.bloque === bloque ? '#ffaa00' : '#444',
                  paddingHorizontal: 12,
                  paddingVertical: 6,
                  margin: 4,
                  borderRadius: 4
                }}
                onPress={() => setNuevoCurso({ ...nuevoCurso, bloque })}
              >
                <Text style={{ color: 'white' }}>{bloque}</Text>
              </TouchableOpacity>
            ))}
          </View>
          <Text style={{ color: 'white', marginBottom: 4 }}>Día:</Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', marginBottom: 12 }}>
            {['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'].map((dia) => (
              <TouchableOpacity
                key={dia}
                style={{
                  backgroundColor: nuevoCurso.dia === dia ? '#ffaa00' : '#444',
                  paddingHorizontal: 12,
                  paddingVertical: 6,
                  margin: 4,
                  borderRadius: 4
                }}
                onPress={() => setNuevoCurso({ ...nuevoCurso, dia })}
              >
                <Text style={{ color: 'white' }}>{dia.charAt(0).toUpperCase() + dia.slice(1)}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={{ color: 'white', marginBottom: 4 }}>Pabellón:</Text>
          <View style={{ flexDirection: 'row', flexWrap: 'wrap', marginBottom: 12 }}>
            {departamentos.map((departamento) => (
              <TouchableOpacity
                key={departamento}
                style={{
                  backgroundColor: nuevoCurso.departamento === departamento ? '#ffaa00' : '#444',
                  paddingHorizontal: 12,
                  paddingVertical: 6,
                  margin: 4,
                  borderRadius: 4
                }}
                onPress={() => setNuevoCurso({ ...nuevoCurso, departamento })}
              >
                <Text style={{ color: 'white' }}>{departamento}</Text>
              </TouchableOpacity>
            ))}
          </View>

          <Text style={{ color: 'white', marginBottom: 4 }}>Sala (solo número):</Text>
          <TextInput
            style={{
              backgroundColor: 'white',
              marginBottom: 12,
              padding: 8,
              borderRadius: 4
            }}
            value={String(nuevoCurso.sala)}
            onChangeText={(text) => {
              const soloNumeros = parseInt(text.replace(/[^0-9]/g, ''), 10) || 0;

              setNuevoCurso({ ...nuevoCurso, sala: soloNumeros });
            }}
            placeholder="Número de sala"
            keyboardType="numeric"
            placeholderTextColor="#888"
          />
          <Button title="Confirmar Agregar" onPress={handleAgregar} />
        </View>
      )}

      <Button
        title={mostrarEliminar ? 'Ocultar Lista de Eliminación' : 'Eliminar Curso'}
        onPress={() => {
          setMostrarEliminar(!mostrarEliminar);
          setMostrarFormulario(false);
        }}
      />
      {mostrarEliminar && (
        <View style={{
          marginVertical: 10,
          padding: 16,
          borderColor: 'white',
          borderWidth: 1,
          borderRadius: 8,
          backgroundColor: '#222'
        }}>
          <Text style={{ color: 'white', fontWeight: 'bold', marginBottom: 12 }}>Cursos actuales</Text>

          {dias.map(dia => (
            <View key={dia} style={{ marginBottom: 10 }}>
              <Text style={{ color: '#ffaa00', fontWeight: 'bold', fontSize: 16, marginBottom: 6 }}>
                {dia.charAt(0).toUpperCase() + dia.slice(1)}
              </Text>

              {bloques.map(bloque => {
                const asignatura = tablaHorario?.[bloque]?.[dia];
                if (!asignatura) return null;

                return (
                  <View
                    key={`${bloque}-${dia}`}
                    style={{
                      flexDirection: 'row',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      backgroundColor: '#333',
                      marginBottom: 8,
                      padding: 10,
                      borderRadius: 6,
                      width: 700
                    }}
                  >
                    <Text style={{ color: 'white' }}>
                      {`${asignatura} (${bloque})`}
                    </Text>
                    <TouchableOpacity onPress={() => handleEliminarCurso(bloque, dia, asignatura)}>
                      <Text style={{ color: 'red', fontWeight: 'bold', fontSize: 18 }}>❌</Text>
                    </TouchableOpacity>
                  </View>
                );
              })}
            </View>
          ))}
        </View>
      )}
    </ScrollView>
  );
}
