import React, { createContext, useEffect } from "react";

import User from '../Models/user'
import { cookie_handler } from "../extentsions/helper_funcs"
import engine from "../BackendRequests/base";


export const AuthContext = createContext<User>({
    username: null,
    email: null,
    password: null
});


export const AuthProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
    const [currentUser, setCurrentUser] = React.useState<User>({username: null, email: null, password: null})
    useEffect(() => {
        const get_auth = async () => {
            return await engine.post('/auth/auth_check', {cookie: cookie_value})
        }

        let cookie_value: any = cookie_handler.get('oat')
        if (cookie_value) {
            let res = get_auth()
            let data = res.data
            if (data.user) {
                setCurrentUser(data.user)
            } else {
                setCurrentUser({
                    username: null,
                    email: null,
                    password: null
                })
            }
        }
    }, [currentUser, setCurrentUser])
    return (
        <AuthContext.Provider value={currentUser}>
            {children}
        </AuthContext.Provider>
    )
}
