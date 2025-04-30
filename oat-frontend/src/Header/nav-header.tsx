import {Container, AppBar, Toolbar} from '@mui/material'

import { useContext } from 'react';
import { AuthContext } from '../context/auth_context';
import NoUserNav from './no-user-nav';
import UserNav from './user-nav';


const NavHeader = (): JSX.Element => {
  const context = useContext(AuthContext)

  return (
    <AppBar position='static'>
      <Container maxWidth="xl">
        <Toolbar disableGutters>
          {(context.user ?
            <UserNav />
            :
            <NoUserNav />
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
}

export default NavHeader;