// Definir el tipo de los bloques permitidos
export type Bloque = 'A' | 'B' | 'C' | 'C2' | 'D' | 'E' | 'F';

// Usar ese tipo en el array
export const bloques: Bloque[] = ['A', 'B', 'C', 'C2', 'D', 'E', 'F'];

// Tipar el objeto bloquesHorario correctamente
export const bloquesHorario: Record<Bloque, { inicio: string; fin: string }> = {
  A: { inicio: '08:10', fin: '09:40' },
  B: { inicio: '09:55', fin: '11:25' },
  C: { inicio: '11:40', fin: '13:10' },
  C2: { inicio: '13:10', fin: '14:30' },
  D: { inicio: '14:30', fin: '16:00' },
  E: { inicio: '16:15', fin: '17:45' },
  F: { inicio: '18:00', fin: '19:30' }
};
export type Dia = 'lunes' | 'martes' | 'miércoles' | 'jueves' | 'viernes' | 'sábado';
export type TablaHorario = {
  [bloque in Bloque]?: {
    [dia in Dia]?: string;
  };
};

export type Clase = {
  
  bloque: Bloque;
  dia: Dia;
  asignatura: string;
  sala: number;
  departamento: string;
};

export type ClaseConCoordenadas = {
  bloque: Bloque;
  dia: Dia;
  x: number;
  y: number;
  asignatura?: string;
};

export type ClaseConMinutos = ClaseConCoordenadas & { minutosInicio: number };

//export const bloques = ['A', 'B', 'C', 'C2', 'D', 'E', 'F'];
export const dias: Dia[] = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

export class BlackBox {
  private usuario: string;
  private clave: string;

  constructor() {
    this.usuario = '';
    this.clave = '';
  }

  setUsuario(usuario: string) {
    this.usuario = usuario;
  }

  setClave(clave: string) {
    this.clave = clave;
  }

  getUsuario(): string {
    return this.usuario;
  }

  getClave(): string {
    return this.clave;
  }
}