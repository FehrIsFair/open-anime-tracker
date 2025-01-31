import axios from 'axios'
import User, { to_json, Login } from '../Models/user'


export const userCreate = async (user: User) => {
  const payload: JSON = to_json(user)
  axios({
    method: 'POST',
    url: 'http://localhost:5000/user/create',
    data: payload,
  }).then((res) => {
    return res
  }).catch((err) => {
    console.log(err)
  })
}

export const login = async (login: Login) => {
  const payload: JSON = to_json(login)
  axios({
    method: 'POST',
    url: 'http://localhost:5000/auth/login',
    data: payload,
  }).then((res) => {
    return res.data
  }).catch((err) => {
    console.log(err)
  })
}
