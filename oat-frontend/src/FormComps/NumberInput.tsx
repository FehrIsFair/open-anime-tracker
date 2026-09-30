import React from "react";
import { FormControl, TextField } from "@mui/material";

interface NumberInputProps {
  id: string;
  label: string;
  value: number;
  onChange: (value: number) => void;
  testId?: string;
}

const NumberInputComponent = (props: NumberInputProps): JSX.Element => {
  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const parsed = Number(event.target.value);
    props.onChange(isNaN(parsed) ? 0 : parsed);
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
        type="number"
      />
    </FormControl>
  );
};
export default NumberInputComponent;
