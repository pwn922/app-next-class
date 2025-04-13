export const bloquesHorario = {
  A: { inicio: '08:10', fin: '09:40' },
  B: { inicio: '09:55', fin: '11:25' },
  C: { inicio: '11:40', fin: '13:10' },
  C2: { inicio: '13:10', fin: '14:30' },
  D: { inicio: '14:30', fin: '16:00' },
  E: { inicio: '16:15', fin: '17:45' },
  F: { inicio: '18:00', fin: '19:30' }
};

export const bloques = ['A', 'B', 'C', 'C2', 'D', 'E', 'F'];
export const dias = ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado'];

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