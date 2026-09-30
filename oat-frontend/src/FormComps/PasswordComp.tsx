import React from "react";
import { FormControl, IconButton, InputAdornment, TextField } from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material";

interface PasswordProps {
  id: string;
  label: string;
  value: string;
  onChange: (value: string) => void;
  testId?: string;
}

const PasswordComponent = (props: PasswordProps): JSX.Element => {
  const [showPassword, setShowPassword] = React.useState(false);

  const onChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    props.onChange(event.target.value);
  };

  const handleTogglePassword = () => {
    setShowPassword((prev) => !prev);
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
        type={showPassword ? "text" : "password"}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aria-label="toggle password visibility"
                onClick={handleTogglePassword}
                edge="end"
                data-testid="qa-password_visibility-toggle"
              >
                {showPassword ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          ),
        }}
      />
    </FormControl>
  );
};
export default PasswordComponent;
