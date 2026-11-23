import { useCallback, useEffect, useState } from "react";
import * as authApi from "../api/auth";
import { setUnauthorizedHandler, tokenStore } from "../api/client";
import { AuthContext } from "./AuthContext";

export function AuthProvider({children}) {
    const [user, setUser] = useState(null);
    const [loading, setLoading] = useState(() => Boolean(tokenStore.get()));

    const logout = useCallback(() => {
        tokenStore.clear();
        setUser(null);
    }, []);

    useEffect(() => {
        setUnauthorizedHandler(logout);
    }, [logout]);

    // Restore the session on page load
    useEffect(() => {
        if(!tokenStore.get()) return;
        authApi
            .getMe()
            .then(setUser)
            .catch(() => tokenStore.clear())
            .finally(() => setLoading(false));
    }, []);

    const login = async (email, password) => {
        const {access_token} = await authApi.login(email, password);
        tokenStore.set(access_token);
        setUser(await authApi.getMe());
    };

    const register = async (email, password) => {
        await authApi.register(email, password);
        await login(email, password);
    };

    return (
        <AuthContext.Provider value={{user, loading, login, register, logout}}>
            {children}
        </AuthContext.Provider>
    );
}