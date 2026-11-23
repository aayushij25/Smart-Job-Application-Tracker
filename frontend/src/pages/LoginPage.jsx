import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
    const {user, login, register} = useAuth();
    const [mode, setMode] = useState("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    if (user) return <Navigate to="/" replace />;

    const isLogin = mode === "login";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        setSubmitting(true);
        try {
            if (isLogin) await login(email, password);
            else await register(email, password);
        } catch (err) {
            setError(err.message);
        } finally {
            setSubmitting(false);
        }
    };

    const toggleMode = () => {
        setMode (isLogin ? "register": "login");
        setError("");
    };

    return (
        <div className="auth-wrap">
            <form className="auth-card" onSubmit={handleSubmit}>
                <h1>{isLogin ? "Log in": "Create account"}</h1>
                {error && <div className="error">{error}</div>}
                <input
                    type="email"
                    placeholder="Email"
                    autoComplete="email"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
                <input 
                type="password"
                placeholder="Password (8+ characters)"
                autoComplete={isLogin ? "current-password": "new-password"}
                minLength={isLogin ? undefined : 8}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                />
                <button className="primary" type="submit" disabled={submitting}>
                    {submitting ? "Please wait...": isLogin ? "Log in": "Register"}
                </button>
                <button type="button" className="link-btn" onClick={toggleMode}>
                    {isLogin ? "No account? Register": "Have an account? Log in"}
                </button>
            </form>
        </div>
    )
}