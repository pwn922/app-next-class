import { BACKEND_URL } from '@env';

export const API_V1 = "/api/v1"
export const LOGIN_V1 = BACKEND_URL + API_V1 + "/login"
export const HORARIO_POR_USUARIO_URL = BACKEND_URL + API_V1 + "/user/schedules/"
export const INFO_PAVILION_BY_NAME_URL = BACKEND_URL + API_V1 + "/pavilions/"
export const GET_ALL_PAVILIONS = BACKEND_URL + API_V1 + "/pavilions/"
export const POST_SCHEDULE = BACKEND_URL + API_V1 + "/user/schedules/"
export const DELETE_USER_SCHEDULE_BY_ID = BACKEND_URL + API_V1 +"/user/schedules"
export const GET_USER = BACKEND_URL + API_V1 + "/user"

