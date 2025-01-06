import React from 'react';
import {Container, AppBar, Toolbar} from '@mui/material'

import NavItem from './link-items';


const NavHeader = (): JSX.Element => {
  return (
    <AppBar position='static'>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {/* Logo goes here */}
          <NavItem path='/' text='Home' />
          <NavItem path='/add-anime' text='Add Anime' />
          <NavItem path='/get-anime' text='Get Anime' />
          <NavItem path='/signup' text='Sign Up' />
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default NavHeader;
