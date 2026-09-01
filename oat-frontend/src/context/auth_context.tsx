import React, { createContext, useState, useCallback, useEffect } from "react";
import { Navigate, useLocation } from 'react-router-dom';

import User from '../Models/user'
import { validateSession } from '../BackendRequests/user'


export interface Auth {
  user: User | null
  setUser: React.Dispatch<React.SetStateAction<User | null>>
  setLogin: (user: User) => void
  logout: () => void
  loading: boolean
}

export const AuthContext = createContext<Auth>({
  user: null,
  setUser: () => {},
  setLogin: () => {},
  logout: () => {},
  loading: true,
});


// Protected route wrapper: redirects if user is not authenticated
export const AuthRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { user, loading } = React.useContext(AuthContext);
  const location = useLocation();

  if (loading) return null; // Wait for session check

  if (!user) {
    return <Navigate to="/signin" replace state={{ from: location }} />;
  }

  return <>{children}</>;
};


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  // Restore session from server cookie on mount
  useEffect(() => {
    validateSession()
      .then((data) => {
        setUser({ username: data.username, email: data.email || '', password: null })
      })
      .catch(() => {
        setUser(null)
      })
      .finally(() => {
        setLoading(false)
      })
  }, [])

  const setLogin = useCallback((user: User) => {
    setUser(user)
  }, [])

  const logout = useCallback(() => {
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{user, setUser, setLogin, logout, loading}}>
      {children}
    </AuthContext.Provider>
  )
}
