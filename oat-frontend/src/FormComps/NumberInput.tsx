import { TextField } from '@mui/material'

interface InputProps {
  id: string
  label: string
  value: number
  set_field: any
}

const NumberInputComponent = (props: InputProps): JSX.Element => {

  const onChange = (event: any) => {
    props.set_field(event.target.value as number)
  }

  return (
    <>
      <TextField id={props.id} 
        label={props.label}
        variant='outlined' 
        value={props.value}
        onChange={onChange} 
      />
    </>
  )
}
export default NumberInputComponent