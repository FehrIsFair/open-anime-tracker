import User, { to_json, Login } from '../Models/user'
import engine from './base'


export const userCreate = async (user: User) => {
  const payload = to_json(user)
  try {
    const res = await engine.post('/user/create', payload)
    return res.data
  } catch (err: any) {
    console.error('userCreate error:', err.response?.data || err.message)
    throw err
  }
}

export const login = async (login: Login): Promise<any> => {
  const payload = to_json(login)
  try {
    const res = await engine.post('/auth/login', payload)
    return res.data
  } catch (err: any) {
    console.error('login error:', err.response?.data || err.message)
    throw err
  }
}

export const logout = async (): Promise<any> => {
  try {
    const res = await engine.post('/auth/logout')
    return res.data
  } catch (err: any) {
    console.error('logout error:', err.response?.data || err.message)
    throw err
  }
}
