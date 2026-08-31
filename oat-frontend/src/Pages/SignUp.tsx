import React, { useContext } from "react";
import { Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import InputComponent from "../FormComps/InputComp";
import EmailComponent from "../FormComps/EmailComponent";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import PasswordComponent from "../FormComps/PasswordComp";
import { userCreate } from "../BackendRequests/user";
import { AuthContext } from "../context/auth_context";

const SignUp = () => {
  const [username, setUsername] = React.useState("");
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [confirmPass, setConfirmPass] = React.useState("");
  const [error, setError] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const { setLogin } = useContext(AuthContext);
  const navigate = useNavigate();

  const submitForm = async () => {
    setError("");

    if (password !== confirmPass) {
      setError("Passwords do not match.");
      return;
    }

    setLoading(true);
    try {
      await userCreate({ username, email, password });
      setLogin({ username, email, password: null });
      navigate("/add-anime", { replace: true });
    } catch (err: any) {
      setError(err.response?.data?.message || "Signup failed. Please try again.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h5" sx={{ mb: 2, textAlign: "center" }}>
        Sign Up
      </Typography>
      <InputComponent
        id="username"
        label="Username"
        value={username}
        onChange={setUsername}
      />
      <EmailComponent
        id="email"
        label="Email"
        value={email}
        onChange={setEmail}
      />
      <PasswordComponent
        id="password"
        label="Password"
        value={password}
        onChange={setPassword}
      />
      <PasswordComponent
        id="confirm_password"
        label="Confirm Password"
        value={confirmPass}
        onChange={setConfirmPass}
      />
      {error && <Typography color="error" sx={{ mt: 1, fontSize: "0.875rem" }}>{error}</Typography>}
      <SubmitBtn variant="contained" onSubmit={submitForm} disabled={loading} sx={{ mt: 2 }}>
        {loading ? "Creating account..." : "Submit"}
      </SubmitBtn>
    </Box>
  );
};
export default SignUp;
