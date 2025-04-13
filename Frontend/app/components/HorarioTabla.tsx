//Aqui se maneja la talba del horario, ademas se agregan cursos  o eliminan respectivamente
import React, { useState, useEffect } from 'react';
import { View, Text, Button, TextInput, Alert, TouchableOpacity, ScrollView } from 'react-native';
import { bloquesHorario, bloques, dias } from '../utils/constantes';
import { agregarCurso, eliminarCurso ,buscarHorariosPorUsuario, obtenerNombresDepartamentos} from '../src/validacion';
import { generarTablaHorario } from '../utils/funciones';

export default function HorarioTabla({ usuario, clave }) {
  const [tablaHorario, setTablaHorario] = useState({});
  const [msg, setMsg] = useState('');
  const [mostrarFormulario, setMostrarFormulario] = useState(false);
  const [mostrarEliminar, setMostrarEliminar] = useState(false);
  const [departamentos, setDepartamentos] = useState([]);

  const [nuevoCurso, setNuevoCurso] = useState({
    bloque: 'A',
    dia: 'lunes',
    asignatura: '',
    sala: 101,
    departamento: 'x',
  });
  useEffect(() => {
    const cargarHorario = async () => {
      if (!usuario) return;

      try {
        const horarios = await buscarHorariosPorUsuario(usuario, clave);
        const tabla = generarTablaHorario(horarios);
        setTablaHorario(tabla);
      } catch (err) {
        console.error('Error al cargar horario:', err);
        setMsg('Error al cargar horario');
      }
    };
    cargarHorario();
  }, [usuario]);
  useEffect(() => {
    const cargarDepartamentos = async () => {
      try {
        const departamentos = await obtenerNombresDepartamentos( clave);
        setDepartamentos(departamentos || []);
      } catch (err) {
        console.error('Error al cargar departamentos:', err);
      }
    };
  
    cargarDepartamentos();
  }, []);
  const handleAgregar = async () => {
    const res = await agregarCurso(usuario, nuevoCurso, clave);
    if (res.ok) {
      const horarios = await buscarHorariosPorUsuario(usuario, clave);
      setTablaHorario(generarTablaHorario(horarios));
      setMsg('Curso agregado!');
      setNuevoCurso({ ...nuevoCurso, asignatura: '' });
      setMostrarFormulario(false);
    } else {
      setMsg('Error al agregar el curso');
    }
  };
  const handleEliminarCurso = async (bloque, dia, asignatura) => {
    const curso = {
      bloque,
      dia,
      asignatura,
      sala: 999,
      departamento: 'test',
    };
    const res = await eliminarCurso(usuario, curso, clave);
    if (res.ok) {
      const horarios = await buscarHorariosPorUsuario(usuario, clave);
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

          <Text style={{ color: 'white', marginBottom: 4 }}>Departamento:</Text>
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
              const soloNumeros = text.replace(/[^0-9]/g, '');
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
