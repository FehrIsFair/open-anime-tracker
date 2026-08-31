import { FormControl, TextField } from "@mui/material";
import React from "react";

interface EmailProps {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
}

const EmailComponent = (props: EmailProps): JSX.Element => {
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(event.target.value);
  };

  return (
    <FormControl fullWidth>
      <TextField
        id={props.id}
        label={props.label}
        variant="outlined"
        value={props.value}
        onChange={onChange}
        type="email"
      />
    </FormControl>
  );
};
export default EmailComponent;
