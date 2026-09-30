import React from "react";
import { Checkbox, FormControlLabel } from "@mui/material";

interface CheckBoxProps {
  id?: string;
  value: boolean;
  onChange: (value: boolean) => void;
  label: string;
  error?: string;
  testId?: string;
}

const CheckBoxComponent = (props: CheckBoxProps): JSX.Element => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(event.target.checked);
  };
  const testId = props.testId || `qa-${(props.id || props.label || 'checkbox').replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()}-toggle`;

  return (
    <>
      <FormControlLabel
        control={
          <Checkbox
            data-testid={testId}
            inputProps={{ 'data-testid': testId } as React.InputHTMLAttributes<HTMLInputElement>}
            id={props.id}
            checked={props.value}
            onChange={handleChange}
          />
        }
        label={props.label}
      />
      {props.error && (
        <span style={{ color: "red", fontSize: "0.75rem" }}>{props.error}</span>
      )}
    </>
  );
};
export default CheckBoxComponent;
