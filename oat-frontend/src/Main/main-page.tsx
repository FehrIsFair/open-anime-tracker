import React from 'react';
import {BrowserRouter, Route} from 'react-router-dom'
import { Box, AppBar, Toolbar, Typography, Button } from '@mui/material'

import {h1} from '../TextFormating/text_config'


const MainPage = (): JSX.Element => {
  return (
    <Box>
      <Typography 
      variant='h1' 
      sx={h1}>
        Hello World.
      </Typography>
    </Box>
  )
};
export default MainPage