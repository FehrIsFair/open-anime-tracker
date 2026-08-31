import React from "react";
import { FormControl, TextField } from "@mui/material";

interface NumberInputProps {
  id: string;
  label: string;
  value: number;
  onChange: (value: number) => void;
}

const NumberInputComponent = (props: NumberInputProps): JSX.Element => {
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const parsed = Number(event.target.value);
    props.onChange(isNaN(parsed) ? 0 : parsed);
  };

  return (
    <FormControl fullWidth>
      <TextField
        id={props.id}
        label={props.label}
        variant="outlined"
        value={props.value}
        onChange={onChange}
        type="number"
      />
    </FormControl>
  );
};
export default NumberInputComponent;
