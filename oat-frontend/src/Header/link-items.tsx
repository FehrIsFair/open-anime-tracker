import { Link } from 'react-router-dom'
import { Typography, Button } from '@mui/material'

import { p } from '../TextFormating/text_config'


export interface NavProps {
  path: string
  text: string
}


const NavItem = (props: NavProps): JSX.Element => {
  return (
    <Button data-testid={`qa-nav_${props.text.toLowerCase().replace(/[^a-z0-9]+/g, '_')}-click`}>
      <Link to={props.path}>
        <Typography
          noWrap
          sx={p}
        >
          {props.text}
        </Typography>
      </Link>
    </Button>
  )
}
export default NavItem