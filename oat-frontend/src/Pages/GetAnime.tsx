import React from 'react';
import { Box, AppBar, Toolbar, Typography, Button, FormControl, Card } from '@mui/material'

import {h1} from '../TextFormating/text_config'
import InputComponent from '../FormComps/InputComp';
import { AnimeTypeEnum, StatusEnum, ContentRating } from '../Enums/AnimeType';
import SelectComponent from '../FormComps/SelectComp';
import SubmitBtn from '../FormComps/Buttons/SubmitBtn';
import Anime from '../Models/anime';
import _ from 'lodash';
import { animeGet } from '../BackendRequests/anime';
import NumberInputComponent from '../FormComps/NumberInput';
import TextAreaComponent from '../FormComps/TextAreaComp';
import CheckBoxComponent from '../FormComps/CheckBoxComp';
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