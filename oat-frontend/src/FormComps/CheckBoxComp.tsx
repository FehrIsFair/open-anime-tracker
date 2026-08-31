import React from "react";
import { Checkbox, FormControlLabel } from "@mui/material";

interface CheckBoxProps {
  id?: string;
  value: boolean;
  onChange: (value: boolean) => void;
  label: string;
  error?: string;
}

const CheckBoxComponent = (props: CheckBoxProps): JSX.Element => {
  const handleChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(event.target.checked);
  };

  return (
    <>
      <FormControlLabel
        control={
          <Checkbox
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
