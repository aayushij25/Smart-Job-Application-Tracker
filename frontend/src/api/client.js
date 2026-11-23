const API_URL = import.meta.env.VITE_API_URL;
const TOKEN_KEY = "jt_token";

export const tokenStore = {
    get: () => localStorage.getItem(TOKEN_KEY),
    set: (token) => localStorage.setItem(TOKEN_KEY, token),
    clear: () => localStorage.removeItem(TOKEN_KEY) 
};

export class ApiError extends Error {
    constructor(status, message) {
        super(message);
        this.status = status;
    }
}

let onUnauthorized = () => {};
export function setUnauthorizedHandler(fn) {
    onUnauthorized = fn;
}

function formatDetail(detail) {
    if (typeof detail === "string") return detail;
    if (Array.isArray(detail)) return detail.map((d) => d.msg).join(",");
    return null;
}

export async function request(path, {method = "GET", body, auth = true} = {}) {
    const headers = {};
    if (body !== undefined) headers["Content-Type"] = "application/json";
    const token = tokenStore.get();
    if (auth && token) headers.Authorization = `Bearer ${token}`;    

    let res;
    try {
        res = await fetch(`${API_URL}${path}`, {
            method,
            headers,
            body: body !== undefined ? JSON.stringify(body) : undefined,
        });
    } catch {
        throw new ApiError(0, "Cannot reach the server. Is the backend running?");
    }

    if (res.status == 204) return null;

    const data = await res.json().catch(() => null);

    if (!res.ok) {
        if (res.status == 401 && auth) onUnauthorized();
        throw new ApiError(res.status, formatDetail(data?.detail) ?? "Something went wrong");
    }
    return data;
}