import { TextareaAutosize } from '@mui/material'

interface InputProps {
  id: string
  value: string
  set_field: any
  placeholder: string
}

const TextAreaComponent = (props: InputProps): JSX.Element => {

  const onChange = (event: any) => {
    props.set_field(event.target.value as string)
  }

  return (
    <>
      <TextareaAutosize id={props.id} 
        placeholder={props.placeholder}
        value={props.value}
        onChange={onChange} 
      />
    </>
  )
}
export default TextAreaComponent