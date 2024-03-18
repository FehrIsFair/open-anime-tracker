import React from 'react';
import { Box, AppBar, Toolbar, Typography, Button, FormControl } from '@mui/material'

import {h1} from '../TextFormating/text_config'
import InputComponent from '../FormComps/InputComp';
import { AnimeTypeEnum } from '../Enums/AnimeType';
import SelectComponent from '../FormComps/SelectComp';
import SubmitBtn from '../FormComps/Buttons/SubmitBtn';
import Anime from '../Models/anime';
import _ from 'lodash';
import { animePost } from '../BackendRequests/anime';


const MainPage = (): JSX.Element => {
  const [animeType, setAnimeType] = React.useState('SHOW');
  const [animeTitle, setAnimeTitle] = React.useState('');

  const dummy_json: any = {};

  const submitForm = () => {
    const request_json: Anime = {
      title: animeTitle,
      jp_title: '',
      other_titles: _(dummy_json).toJSON(),
      rating: 0,
      type: animeType,
      seasons: 0,
      episodes: 0,
      desc: 'This is a test.',
      status: ''
    }
    animePost(request_json)
  }

  return (
    <Box>
      <Typography 
      variant='h1' 
      sx={h1}>
        Create an anime
      </Typography>
      <FormControl>
        <InputComponent 
          id="anime-title"
          label="Title"
          anime_title={animeTitle}
          set_field={setAnimeTitle}
        />
        <SelectComponent 
          id="AnimeTypeSelect"
          label_id="anime-type"
          anime_type={animeType}
          setValue={setAnimeType}
          menu_options={AnimeTypeEnum}
        />
        <SubmitBtn variant={2} submit_func={submitForm}></SubmitBtn>
      </FormControl>
    </Box>
  )
};
export default MainPage