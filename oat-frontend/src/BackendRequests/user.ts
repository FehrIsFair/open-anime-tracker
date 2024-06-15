import axios from 'axios'
import User, { to_json } from '../Models/user'
import engine from './base'


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