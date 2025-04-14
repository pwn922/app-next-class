import { useState, useEffect } from 'react';
import { View, Text, TextInput, Button } from 'react-native';
import { useRouter } from 'expo-router';
import { validarCredenciales } from './src/validacion';
import { enviarCredencialesAlBackend } from './src/conexion_back/conexion';
import {BlackBox} from './utils/constantes'


const blackbox = new BlackBox();

export default function HomeScreen() {
  const [usuario, setUsuario] = useState('');
  const [clave, setClave] = useState('');
  const [mensajeError, setMensajeError] = useState('');
  const [modoDemo, setModoDemo] = useState(false); 
  const router = useRouter();

  useEffect(() => {//aqui se decide si se trabaja con el backend o el demo (es solo un cambio del nombre) 
    const testBackend = async () => {
      try {
        await enviarCredencialesAlBackend('ping', 'test');
        setModoDemo(false);
      } catch (err) {
        console.warn('Conexión con el backend fallida. Usando modo demo.');
        setModoDemo(true);
      }
    };

    testBackend();
  }, []);

  const iniciarSesion = async () => {
    blackbox.setUsuario(usuario);
    blackbox.setClave(clave);

    try {
      const resultado = await validarCredenciales(blackbox.getUsuario(), resultado );
      if (resultado === 2) {
        setMensajeError("Usuario incorrecto");
      } else if (resultado === 3) {
        setMensajeError("Contraseña incorrecta");
      }
      else {
        if (resultado === 1) {
          setMensajeError('');
          router.push({
            pathname: '/layout',
            params: { usuario: blackbox.getUsuario(), clave: resultado }
          });
        }
        else {
          setMensajeError('');
          router.push({
            pathname: '/layout',
            params: { usuario: blackbox.getUsuario(), clave: resultado }
          });
        }
      }
    } catch (error) {
      setMensajeError("Error inesperado al iniciar sesión");
      console.error("Error en la autenticación:", error);
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
