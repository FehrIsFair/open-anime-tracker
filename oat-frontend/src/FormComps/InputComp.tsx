import { FormControl, TextField } from "@mui/material";
import React from "react";

interface InputProps {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
}

const InputComponent = (props: InputProps): JSX.Element => {
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(event.target.value);
  };

  return (
    <FormControl fullWidth>
      <TextField
        data-testid={props.id}
        id={props.id}
        label={props.label}
        variant="outlined"
        value={props.value}
        onChange={onChange}
        type="text"
      />
    </FormControl>
  );
};
export default InputComponent;
