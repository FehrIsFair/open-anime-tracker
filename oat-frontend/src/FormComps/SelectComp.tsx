import { InputLabel, Select, SelectChangeEvent, MenuItem } from '@mui/material'
import React from 'react';

import { getVariableName } from '../extentsions/helper_funcs';

interface SelectProps {
  id: string
  label_id: string
  anime_type: any
  setValue: any
  menu_options: Array<any>
}

const SelectComponent = (props: SelectProps): JSX.Element => {

  const onChange = (event: SelectChangeEvent) => {
    props.setValue(event.target.value)
  }

  return (
    <>
      <InputLabel id={props.label_id}>Anime Type</InputLabel>
      <Select
       id={props.id}
       labelId={props.label_id}
       value={props.anime_type}
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