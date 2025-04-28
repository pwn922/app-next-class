import { useState, useEffect } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { useRouter } from 'expo-router';
import { validarCredenciales } from './src/validacion';
import { enviarCredencialesAlBackend } from './src/conexion_back/conexion';
import {BlackBox} from './utils/constantes'
import { saveTokens } from '@/storage/storage';


const blackbox = new BlackBox();

export default function HomeScreen() {
  const [usuario, setUsuario] = useState('');
  const [clave, setClave] = useState('');
  const [mensajeError, setMensajeError] = useState('');
  const [modoDemo, setModoDemo] = useState(false); 
  const router = useRouter();

  const iniciarSesion = async () => {
    blackbox.setUsuario(usuario);
    blackbox.setClave(clave);
  
    try {
      // Hacemos login y obtenemos el access_token
      const response = await enviarCredencialesAlBackend(usuario, clave);
      
      if (response && response.data && response.data.access_token && response.data.refresh_token) {
        // Guardamos el access_token en AsyncStorage
        await saveTokens(response.data.access_token, response.data.refresh_token);
        
        // Redirigimos a la pantalla principal
        router.push('/layout');
      } else {
        setMensajeError("Error al obtener los tokens.");
      }
    } catch (error: unknown) {
      // Verificamos que el error sea del tipo 'Error' y luego mostramos el mensaje
      if (error instanceof Error) {
        setMensajeError(error.message);
        alert(error.message); // Esta es la alerta con el mensaje de error
        
      } else {
        setMensajeError("Error inesperado al iniciar sesión");
        alert("Error inesperado al iniciar sesión");
      }
    }
  };
  

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#8B4000' }}>
      <Text style={{ fontSize: 50, fontWeight: 'bold', color: 'white', marginBottom: 20 }}>
        {modoDemo ? 'UCN BUDDY demo' : 'UCN BUDDY'}
      </Text>

      <TextInput
        placeholder="Usuario"
        value={usuario}
        onChangeText={setUsuario}
        style={{ width: 200, height: 40, borderBottomWidth: 1, marginBottom: 10, backgroundColor: 'white' }}
      />
      <TextInput
        placeholder="Clave"
        value={clave}
        onChangeText={setClave}
        secureTextEntry
        style={{ width: 200, height: 40, borderBottomWidth: 1, marginBottom: 10, backgroundColor: 'white' }}
      />
      {mensajeError !== '' && <Text style={{ color: 'red', marginBottom: 10 }}>{mensajeError}</Text>}
      <Button title="Iniciar Sesión" onPress={iniciarSesion} />
    </View>
  );
}