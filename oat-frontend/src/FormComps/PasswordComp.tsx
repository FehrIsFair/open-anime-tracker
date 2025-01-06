import React from "react"
import { FormControl, IconButton, InputAdornment, TextField } from "@mui/material";
import { Visibility, VisibilityOff } from "@mui/icons-material"

interface InputProps {
  id: string;
  label: string;
  value: string;
  set_field: any;
}

const PasswordComponent = (props: InputProps): JSX.Element => {
  const [showpass, setShowpass] = React.useState(false);

  const onChange = (event: any) => {
    props.set_field(event.target.value as string);
  };

  const handleShowPassword = () => {
    setShowpass(!showpass)
  }

  return (
    <>
      <TextField
        id={props.id}
        label={props.label}
        variant="outlined"
        value={props.value}
        onChange={onChange}
        type={showpass ? "text" : "password"}
        InputProps={{
          endAdornment: (
            <InputAdornment position="end">
              <IconButton
                aira-labbel="toggle password visibility"
                onClick={handleShowPassword}
                edge="end"
              >
                {showpass ? <VisibilityOff /> : <Visibility />}
              </IconButton>
            </InputAdornment>
          )
        }}
        fullWidth
      />
    </>
  );
};
export default PasswordComponent;
