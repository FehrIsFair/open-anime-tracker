import { useContext } from 'react';
import { useNavigate } from 'react-router-dom';
import { Box, Button } from '@mui/material';

import NavItem, { NavProps } from './link-items';
import { AuthContext } from '../context/auth_context';
import { logout as logoutApi } from '../BackendRequests/user';


const UserNav = () => {
    const { user, logout } = useContext(AuthContext);
    const navigate = useNavigate();

    const handleLogout = async () => {
        try {
            await logoutApi();
        } catch (err) {
            console.error('Logout failed:', err);
        } finally {
            logout();
            navigate('/sign-in', { replace: true });
        }
    }

    const routes: Array<NavProps> = [
        {path: '/', text: 'Home'},
        {path: '/add-anime', text: 'Add Anime'},
        {path: '/get-anime', text: 'Get Anime'},
    ]

    return (
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
            {routes.map((route) => (
                <NavItem key={route.path} path={route.path} text={route.text} />
            ))}
            <Button variant="outlined" color="error" onClick={handleLogout}>
                Sign Out
            </Button>
        </Box>
    )
}
export default UserNav