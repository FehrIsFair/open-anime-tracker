import React from "react";
import {
  FormHelperText,
  InputLabel,
  MenuItem,
  Select,
  SelectChangeEvent,
} from "@mui/material";

interface SelectOption {
  label: string;
  value: string;
}

interface SelectProps {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  options: SelectOption[];
  error?: string;
}

const SelectComponent = (props: SelectProps): JSX.Element => {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };

  return (
    <>
      <InputLabel id={props.id}>{props.label}</InputLabel>
      <Select
        labelId={props.id}
        id={props.id}
        label={props.label}
        value={props.value}
        onChange={handleChange}
        error={!!props.error}
        fullWidth
      >
        {props.options.map((option) => (
          <MenuItem key={option.value} value={option.value}>
            {option.label}
          </MenuItem>
        ))}
      </Select>
      {props.error && <FormHelperText error={!!props.error}>{props.error}</FormHelperText>}
    </>
  );
};
export default SelectComponent;
