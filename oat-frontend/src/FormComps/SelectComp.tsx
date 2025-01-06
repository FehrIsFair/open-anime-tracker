import { Select, SelectChangeEvent, MenuItem } from '@mui/material'
import React from 'react';

interface SelectProps {
  id: string
  label_id: string
  value: any
  setValue: any
  menu_options: Array<any>
}

const SelectComponent = (props: SelectProps): JSX.Element => {

  const onChange = (event: SelectChangeEvent) => {
    props.setValue(event.target.value)
  }

  return (
    <>
      <Select
       id={props.id}
       label={props.label_id}
       value={props.value}
       onChange={onChange}
         >
          {props.menu_options.map((option) => {
            return (
              <MenuItem value={option.value}>{option.label}</MenuItem>
            )
          })}
      </Select>
    </>
  )
}
export default SelectComponent
