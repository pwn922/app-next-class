import React from 'react';
import { View, Button } from 'react-native';

type Pantalla = 'horario' | 'mapa';

type SelectorPantallaProps = {
  pantalla: Pantalla;
  setPantalla: React.Dispatch<React.SetStateAction<Pantalla>>;
};

export default function SelectorPantalla({ pantalla, setPantalla }: SelectorPantallaProps) {
  return (
    <View style={{ flexDirection: 'row', marginTop: 10 }}>
      {pantalla !== 'horario' && (
        <Button title="Ver Horario" onPress={() => setPantalla('horario')} color="#FF3B30" />
      )}
      {pantalla !== 'mapa' && (
        <>
          {pantalla !== 'horario' && <View style={{ width: 10 }} />}
          <Button title="Ver Mapa" onPress={() => setPantalla('mapa')} color="#FF3B30" />
        </>
      )}
    </View>
  );
}
