import Anime, { to_json } from '../Models/anime'
import engine from './base'

export const animePost = async (anime: Anime) => {
  const payload = to_json(anime)
  try {
    const res = await engine.post('/anime/create', payload)
    return res.data
  } catch (err: any) {
    console.error('animePost error:', err.response?.data || err.message)
    throw err
  }
}

export const animeGet = async () => {
  const res = await engine.get('/anime')
  return res.data
}
