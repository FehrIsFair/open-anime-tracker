import React from 'react';
import { Box, Typography} from '@mui/material'

import {h1} from '../TextFormating/text_config'


const MainPage = (): JSX.Element => {
  

  return (
    <Box>
      <Typography variant='h1' sx={h1}> This is the home page.</Typography>
    </Box>
  )
};
export default MainPage