import axios from 'axios'
import Anime, { to_json } from '../Models/anime'
import engine from './base'

export const animePost = async (anime: Anime) => {
  const payload: JSON = to_json(anime)
  axios({
    method: 'POST',
    url: 'http://localhost:5000/anime/create',
    data: payload,
  }).then((res) => {
    return res
  }).catch((err): any => {
    console.log(err)
  })
}

export const animeGet = async () => {
  const {data} = await engine.get('/anime')
  return data
}
