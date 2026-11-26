import { useState } from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function LoginPage() {
    const {user, login, register, sessionExpired} = useAuth();
    const [mode, setMode] = useState("login");
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [error, setError] = useState("");
    const [submitting, setSubmitting] = useState(false);

    // Starts from the context value; any interaction below hides it
    const [showExpired, setShowExpired] = useState(sessionExpired);
    const dismissExpired = () => setShowExpired(false);

    if (user) return <Navigate to="/" replace />;

    const isLogin = mode === "login";

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError("");
        dismissExpired();
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
        dismissExpired();
        setMode(isLogin ? "register" : "login");
        setEmail("");
        setPassword("");
        setError("");
    };

    return (
        <div className="auth-wrap">
            <form className="auth-card" onSubmit={handleSubmit}>
                <h1>{isLogin ? "Log in" : "Create account"}</h1>
                {showExpired && !error && (
                    <div className="error">Your session expired. Please log in again.</div>
                )}
                {error && <div className="error">{error}</div>}
                <input
                    type="email"
                    placeholder="Email"
                    autoComplete="email"
                    value={email}
                    onFocus={dismissExpired}
                    onChange={(e) => {
                        dismissExpired();
                        setEmail(e.target.value);
                    }}
                    required
                />
                <input
                    type="password"
                    placeholder="Password (8+ characters)"
                    autoComplete={isLogin ? "current-password" : "new-password"}
                    minLength={isLogin ? undefined : 8}
                    value={password}
                    onFocus={dismissExpired}
                    onChange={(e) => {
                        dismissExpired();
                        setPassword(e.target.value);
                    }}
                    required
                />
                <button className="primary" type="submit" disabled={submitting}>
                    {submitting ? "Please wait... the free server can take up to a minute to wake up" : isLogin ? "Log in" : "Register"}
                </button>
                <button type="button" className="link-btn" onClick={toggleMode}>
                    {isLogin ? "No account? Register" : "Have an account? Log in"}
                </button>
            </form>
        </div>
    );
}