import { request } from "./client"

export const register = (email, password) => 
    request("/auth/register", {method: "POST", body: {email, password}, auth: false});

export const login = (email, password) => 
    request("/auth/login", {method: "POST", body: {email, password}, auth: false});

export const getMe = () => request("/auth/me");