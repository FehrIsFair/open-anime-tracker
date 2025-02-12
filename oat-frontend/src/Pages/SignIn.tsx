import React from "react";
import { Box } from "@mui/material";

import EmailComponent from "../FormComps/EmailComponent";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import PasswordComponent from "../FormComps/PasswordComp";
import { Login } from "../Models/user";
import { cookie_handler } from "../extentsions/helper_funcs"
import engine from "../BackendRequests/base";

const SignIn = () => {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");

  const submitForm = async () => {
    const request_json: Login = {
      email: email,
      password: password
    }
    let res = await engine.post('/auth/login', request_json)
    cookie_handler.set('oat', res.data)
  }
 
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
export default SignIn;
