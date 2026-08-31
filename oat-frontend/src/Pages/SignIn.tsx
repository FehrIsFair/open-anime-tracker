import React, { useContext } from "react";
import { Box, Typography } from "@mui/material";
import { useNavigate } from "react-router-dom";

import EmailComponent from "../FormComps/EmailComponent";
import SubmitBtn from "../FormComps/Buttons/SubmitBtn";
import PasswordComponent from "../FormComps/PasswordComp";
import { login } from "../BackendRequests/user";
import { AuthContext } from "../context/auth_context";

const SignIn = () => {
  const [email, setEmail] = React.useState("");
  const [password, setPassword] = React.useState("");
  const [error, setError] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const { setLogin } = useContext(AuthContext);
  const navigate = useNavigate();

  const submitForm = async () => {
    setError("");
    setLoading(true);
    try {
      const data = await login({ email, password });
      setLogin({ username: data[0]?.username || data[0], email: data[0]?.email || data[1], password: null });
      navigate("/add-anime", { replace: true });
    } catch (err: any) {
      setError(err.response?.data?.message || "Login failed. Please check your credentials.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ maxWidth: 400, mx: "auto", mt: 4, p: 2 }}>
      <Typography variant="h5" sx={{ mb: 2, textAlign: "center" }}>
        Sign In
      </Typography>
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
      {error && <Typography color="error" sx={{ mt: 1, fontSize: "0.875rem" }}>{error}</Typography>}
      <SubmitBtn variant="contained" onSubmit={submitForm} disabled={loading} sx={{ mt: 2 }}>
        {loading ? "Signing in..." : "Submit"}
      </SubmitBtn>
    </Box>
  );
};
export default SignIn;
