import React, { createContext, useState, useCallback } from "react";

import User from '../Models/user'


export interface Auth {
  user: User | null
  setUser: React.Dispatch<React.SetStateAction<User | null>>
  setLogin: (user: User) => void
  logout: () => void
}

export const AuthContext = createContext<Auth>({
  user: null,
  setUser: () => {},
  setLogin: () => {},
  logout: () => {},
});


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)

  const setLogin = useCallback((user: User) => {
    setUser(user)
  }, [])

  const logout = useCallback(() => {
    setUser(null)
  }, [])

  return (
    <AuthContext.Provider value={{user, setUser, setLogin, logout}}>
      {children}
    </AuthContext.Provider>
  )
}
