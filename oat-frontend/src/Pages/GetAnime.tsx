import React from 'react';
import { Box, Typography, Card } from '@mui/material'

import {h1} from '../TextFormating/text_config'
import Anime from '../Models/anime';
import engine from '../BackendRequests/base';



const GetAnime = () => {
  const [anime, setAnime] = React.useState(Array<Anime>)
  const [loaded, setLoaded] = React.useState(false)

  React.useEffect(() => {
    if (!loaded && anime) {
      setLoaded(true)
    }

    async function getAnime() {
      const {data} = await engine.get('/anime', {headers: {"Content-Type": 'application/json'}})
      setAnime(data.data)
    }

    if (anime.length === 0) {
      getAnime()
    }
  }, [anime, setAnime, loaded])


  return (
    <Box>
      <Typography
        variant="h1"
        sx={h1}
      >Anime be here</Typography>
      {anime?.map((item) => {
        return (
          <Card>
            <Typography variant='h4'>{item.title}</Typography>
            <Typography>{item.desc}</Typography>
            <Typography>{item.content_rating}</Typography>
            <Typography>{item.jp_title}</Typography>
            <Typography>{item._type}</Typography>
            <Typography>{item.rating}</Typography>
          </Card>
        )
      })}
    </Box>
  )
}
export default GetAnime