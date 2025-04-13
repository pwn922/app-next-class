import React from 'react';
import { Linking } from 'react-native';
import { View, Text, Button } from 'react-native';
import Icon from 'react-native-vector-icons/FontAwesome';

const App = () => {

  const handleLogin = async () => {
    const loginUrl = 'https://89fd-179-8-31-61.ngrok-free.app/api/v1/login';
  
    try {
      console.log("Redirigiendo a:", loginUrl);
      await Linking.openURL(loginUrl);
    } catch (err) {
      console.error('Error al redirigir:', err);
      alert('No se pudo abrir el navegador');
    }
  };

  return (
    <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center', backgroundColor: '#8B4000' }}>
      <Text style={{ fontSize: 50, fontWeight: 'bold', color: 'white', marginBottom: 20 }}>
        UCN BUDDY
      </Text>

      {/* Botón de inicio de sesión con Google */}
      <Button
        title="Iniciar sesión con Google"
        onPress={handleLogin}
        color="#4285F4"  // Color de Google
      />

      
    </View>
  );
};

export default App;
