import NavItem, { NavProps } from './link-items';


const UserNav = () => {
    const routes: Array<NavProps> = [
        {path: '/', text: 'Home'},
        {path: '/add-anime', text: 'Add Anime'},
        {path: '/get-anime', text: 'Get Anime'},
    ]
    return (
        <>
            {routes.map((route) => {
                return <NavItem path={route.path} text={route.text} />
            })}
        </>
    )
}
export default UserNav