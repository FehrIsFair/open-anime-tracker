import { TextField } from '@mui/material'

interface InputProps {
  id: string
  label: string
  anime_title: string
  set_field: any
}

const InputComponent = (props: InputProps): JSX.Element => {

  const onChange = (event: any) => {
    props.set_field(event.target.value as string)
  }

  return (
    <>
      <TextField id={props.id} 
        label={props.label}
        variant='outlined' 
        value={props.anime_title}
        onChange={onChange} 
      />
    </>
  )
}
export default InputComponent