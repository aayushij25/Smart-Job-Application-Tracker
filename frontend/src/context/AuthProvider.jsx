import { useCallback, useEffect, useState } from "react";
import * as authApi from "../api/auth";
import { setUnauthorizedHandler, tokenStore } from "../api/client";
import { AuthContext } from "./AuthContext";

// Read the "exp" claim (seconds) from the JWT payload and return it in ms.
function getTokenExpiry(token) {
    try {
        const base64 = token.split(".")[1].replace(/-/g, "+").replace(/_/g, "/");
        const { exp } = JSON.parse(atob(base64));
        return exp ? exp * 1000 : null;
    } catch {
        return null;
    }
}

function isTokenExpired(token) {
    const exp = getTokenExpiry(token);
    return exp !== null && exp <= Date.now();
}

export function AuthProvider({children}) {
    const [user, setUser] = useState(null);

    // Only "loading" if there is a still-valid token to check with the server
    const [loading, setLoading] = useState(() => {
        const token = tokenStore.get();
        return Boolean(token) && !isTokenExpired(token);
    });

    // True when a token is already expired at page load, or we log out because it ran out
    const [sessionExpired, setSessionExpired] = useState(() => {
        const token = tokenStore.get();
        return Boolean(token) && isTokenExpired(token);
    });

    // expired === true only when the session ran out (logout button passes a click event)
    const logout = useCallback((expired = false) => {
        tokenStore.clear();
        setUser(null);
        setSessionExpired(expired === true);
    }, []);

    // Any 401 from the API means the session is over
    useEffect(() => {
        setUnauthorizedHandler(() => logout(true));
    }, [logout]);

    // Restore the session on page load
    useEffect(() => {
        const token = tokenStore.get();
        if (!token) return;

        if (isTokenExpired(token)) {
            tokenStore.clear();  // sessionExpired and loading were already set in the initial state
            return;
        }

        authApi
            .getMe()
            .then(setUser)
            .catch(() => tokenStore.clear())
            .finally(() => setLoading(false));
    }, []);

    // Auto logout while the page is open
    useEffect(() => {
        if (!user) return;
        const token = tokenStore.get();
        const exp = token ? getTokenExpiry(token) : null;
        if (!exp) return;

        const timer = setTimeout(() => logout(true), Math.max(exp - Date.now(), 0));
        return () => clearTimeout(timer);
    }, [user, logout]);

    const login = async (email, password) => {
        const {access_token} = await authApi.login(email, password);
        tokenStore.set(access_token);
        setSessionExpired(false);
        setUser(await authApi.getMe());
    };

    const register = async (email, password) => {
        await authApi.register(email, password);
        await login(email, password);
    };

    return (
        <AuthContext.Provider value={{user, loading, login, register, logout, sessionExpired}}>
            {children}
        </AuthContext.Provider>
    );
}