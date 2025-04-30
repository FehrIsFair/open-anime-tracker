import React, { useContext } from "react";
import { Box } from "@mui/material";

import EmailComponent from "../FormComps/EmailComponent";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import PasswordComponent from "../FormComps/PasswordComp";
import { Login } from "../Models/user";
import { cookie_handler } from "../extentsions/helper_funcs"
import engine from "../BackendRequests/base";
import { AuthContext } from "../context/auth_context";
import { redirect } from "react-router-dom";

const SignIn = () => {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const context = useContext(AuthContext)

  const submitForm = async () => {
    const request_json: Login = {
      email: email,
      password: password
    }
    let res = await engine.post('/auth/login', request_json)
    let uuid = res.data[0]
    let _email = res.data[1]
    let username = res.data[2]
    if (_email) {
      cookie_handler.set('oat', uuid)
      context.setLogin({username: username, password: null, email: email})
      redirect('/add-anime')
    } else {
      console.log("Didn't log user in.")
    }
    
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
