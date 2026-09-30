import React from "react";
import { FormHelperText, TextareaAutosize, Typography } from "@mui/material";

interface TextAreaProps {
  id: string;
  label?: string;
  value: string;
  onChange: (value: string) => void;
  placeholder?: string;
  error?: string;
  testId?: string;
}

const TextAreaComponent = (props: TextAreaProps): JSX.Element => {
  const onChange = (event: React.ChangeEvent<HTMLTextAreaElement>) => {
    props.onChange(event.target.value);
  };
  const testId = props.testId || `qa-${props.id.replace(/[^a-zA-Z0-9]+/g, '_').toLowerCase()}-input`;

  return (
    <>
      {props.label && (
        <Typography variant="subtitle2" sx={{ mt: 1 }}>{props.label}</Typography>
      )}
      <TextareaAutosize
        data-testid={testId}
        id={props.id}
        placeholder={props.placeholder}
        value={props.value}
        onChange={onChange}
        minRows={3}
        style={{
          width: "100%",
          padding: "8px",
          boxSizing: "border-box",
          border: "1px solid",
          borderColor: props.error ? "error.main" : "divider",
          borderRadius: 4,
          fontSize: "1rem",
        }}
      />
      {props.error && <FormHelperText error={!!props.error}>{props.error}</FormHelperText>}
    </>
  );
};
export default TextAreaComponent;
