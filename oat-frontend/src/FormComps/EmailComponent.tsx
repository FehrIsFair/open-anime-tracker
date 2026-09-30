import { FormControl, TextField } from "@mui/material";
import React from "react";

interface EmailProps {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  testId?: string;
}

const EmailComponent = (props: EmailProps): JSX.Element => {
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(event.target.value);
  };
  const testId = props.testId || `qa-${props.id.replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()}-input`;

  return (
    <FormControl fullWidth>
      <TextField
        data-testid={testId}
        inputProps={{ 'data-testid': testId }}
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
