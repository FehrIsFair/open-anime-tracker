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
  

  return (
    <Box>
      <Typography variant='h1' sx={h1}> This is the home page.</Typography>
    </Box>
  )
};
export default MainPage