import React from "react";
import { Box } from "@mui/material";

import EmailComponent from "../FormComps/EmailComponent";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import PasswordComponent from "../FormComps/PasswordComp";
import { login } from "../BackendRequests/user";
import { Login } from "../Models/user";
import { cookie_handler } from "../extentsions/helper_funcs"

const SignUp = () => {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");

  const submitForm = () => {
    const request_json: Login = {
      email: email,
      password: password
    }
    let res = login(request_json)
    debugger;
  };
 
  return (
    <Box>
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
      <SubmitBtn variant={2} submit_func={submitForm} />
    </Box>
  );
};
export default SignUp;
