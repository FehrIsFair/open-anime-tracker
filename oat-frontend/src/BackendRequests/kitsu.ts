import engine from './base'

export const kitsuImport = async (kitsuId: number) => {
  try {
    const res = await engine.post('/anime/kitsu-import', { kitsuId })
    return res.data
  } catch (err: any) {
    console.error('kitsuImport error:', err.response?.data || err.message)
    throw err
  }
}

export interface Season {
  seasonNumber: number
  kitsuId: number
  typeSeason: string
  hasParts: boolean
  part: number | null
}

export const importSeasons = async (animeId: number, seasons: Season[]) => {
  try {
    const res = await engine.post('/anime/kitsu-import-seasons', { animeId, seasons })
    return res.data
  } catch (err: any) {
    console.error('importSeasons error:', err.response?.data || err.message)
    throw err
  }
}
