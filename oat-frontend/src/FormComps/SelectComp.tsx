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
  testId?: string;
}

const SelectComponent = (props: SelectProps): JSX.Element => {
  const handleChange = (event: SelectChangeEvent) => {
    props.onChange(event.target.value);
  };
  const testId = props.testId || `qa-${props.id.replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()}-select`;

  return (
    <>
      <InputLabel id={props.id}>{props.label}</InputLabel>
      <Select
        data-testid={testId}
        labelId={props.id}
        id={props.id}
        label={props.label}
        value={props.value}
        onChange={handleChange}
        error={!!props.error}
        fullWidth
      >
        {props.options.map((option) => (
          <MenuItem
            key={option.value}
            value={option.value}
            data-testid={`${testId}_option_${String(option.value).toLowerCase().replace(/[^a-zA-Z0-9]+/g, '_')}-select`}
          >
            {option.label}
          </MenuItem>
        ))}
      </Select>
      {props.error && <FormHelperText error={!!props.error}>{props.error}</FormHelperText>}
    </>
  );
};
export default SelectComponent;
