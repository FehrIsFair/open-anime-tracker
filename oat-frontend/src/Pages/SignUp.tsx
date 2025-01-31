import React from "react";
import { Box } from "@mui/material";

import InputComponent from "../FormComps/InputComp";
import EmailComponent from "../FormComps/EmailComponent";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import PasswordComponent from "../FormComps/PasswordComp";
import { userCreate } from "../BackendRequests/user";
import User from "../Models/user";

const SignUp = () => {
  const [username, setUsername] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPass, setConfirmPass] = React.useState("");
  const [error, setError] = React.useState("");
  

  const submitForm = () => {
    if (confirmPass === password) {
      const request_json: User = {
        username: username,
        email: email,
        password: password
      }
      userCreate(request_json)
    } else {
      setError("Passwords did not match.")
    }
  };
 
  return (
    <Box>
      <InputComponent
        id="username"
        label="Username"
        value={username}
        set_field={setUsername}
      />
      <EmailComponent
        id="email"
        label="Email"
        value={email}
        set_field={setEmail}
      />
      <PasswordComponent
        id="password"
        label="Password"
        value={password}
        set_field={setPassword}
      />
      <PasswordComponent
        id="confirm_password"
        label="Confirm Password"
        value={confirmPass}
        set_field={setConfirmPass}
      />
      <SubmitBtn variant={2} submit_func={submitForm} />
      ({error} ? <>Error Text</> : null)
    </Box>
  );
};
export default SignUp;
