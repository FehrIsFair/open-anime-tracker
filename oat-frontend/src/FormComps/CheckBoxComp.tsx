import { Checkbox } from '@mui/material'
import React from 'react';

interface CheckBoxProps {
  value: boolean
  set_value: any
  label: string
}


const CheckBoxComponent = (props: CheckBoxProps) => {

  const onChange = (event: any) => {
    if (props.value) {
      props.set_value(false)
    } else {
      props.set_value(true)
    }
  }

  return (
    <>
      <Checkbox 
        checked={props.value}
        onChange={onChange}
      />
    </>
  )
}
export default CheckBoxComponent
