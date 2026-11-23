import { useMemo } from "react";
import KanbanBoard from "../components/KanbanBoard";
import { COLUMNS } from "../constants";
import { useApplications } from "../hooks/useApplications";
import { useAuth } from "../hooks/useAuth";

export default function BoardPage() {
    const {user, logout} = useAuth();
    const {applications, loading, error, reload} = useApplications();

    // Group by status in one pass using a hash map: O(n)
    const byStatus = useMemo(() => {
        const groups = Object.fromEntries(COLUMNS.map((c) => [c.id, []]));
        for (const app of applications) groups[app.status]?.push(app);
        return groups;
    }, [applications]);

    return (
        <div className="page">
            <header className="topbar">
                <h1>Job Tracker</h1>
                <div>
                    <span>{user.email}</span>
                    <button onClick={logout}>Log out</button>
                </div>
            </header>

            {error && (
                <div className="error">
                    {error} <button onClick={reload}>Retry</button>
                </div>
            )}
            {loading ? <p>Loading...</p> : <KanbanBoard byStatus={byStatus} />}
        </div>
    );
}