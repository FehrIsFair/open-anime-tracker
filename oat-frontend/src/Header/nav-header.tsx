import React, {useEffect, useContext} from 'react';
import {Link} from 'react-router-dom'
import {Box, Container, AppBar, Toolbar, Typography, Button} from '@mui/material'

import NavItem from './link-items';
import {p} from '../TextFormating/text_config'


const NavHeader = (): JSX.Element => {
  return (
    <AppBar position='static'>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Logo goes here */}
          <NavItem path='/' text='Home' />
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default NavHeader;