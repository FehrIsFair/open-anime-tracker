import React, { createContext } from "react";

import User, {Auth} from '../Models/user'


export const AuthContext = createContext<Auth | any>({
    user: null,
    setUser: null
});


export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
    const [user, setUser] = React.useState<User>()

    const setLogin = (user: User) => {
        debugger
        setUser(user)
    }

    return (
        <AuthContext.Provider value={{user, setUser, setLogin}}>
            {children}
        </AuthContext.Provider>
    )
}
