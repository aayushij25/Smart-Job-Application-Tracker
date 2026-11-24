import { useEffect, useMemo, useState } from "react";
import ApplicationFormModal from "../components/ApplicationFormModal";
import KanbanBoard from "../components/KanbanBoard";
import { COLUMNS } from "../constants";
import { useApplications } from "../hooks/useApplications";
import { useAuth } from "../hooks/useAuth";

export default function BoardPage() {
    const {user, logout} = useAuth();
    const {
        applications, 
        loading, 
        error, 
        reload,
        addApplication,
        editApplication,
        removeApplication,
        moveApplication,
    } = useApplications();
    console.log(applications.map((a) => [a.id, a.status]));

    const [modal, setModal] = useState(null); //null = closed, {} = create, {application} = edit
    const [toast, setToast] = useState("");

    useEffect(() => {
        if (!toast) return;
        const timer = setTimeout(() => setToast(""), 4000);
        return () => clearTimeout(timer);
    }, [toast]);

    // Group by status in one pass using a hash map: O(n)
    const byStatus = useMemo(() => {
        const groups = Object.fromEntries(COLUMNS.map((c) => [c.id, []]));
        for (const app of applications) groups[app.status]?.push(app);
        return groups;
    }, [applications]);

    const handleMove = async (id, from, to) => {
        try {
            await moveApplication(id, from, to);
        } catch (err) {
            setToast(err.message);
        }
    };

    const handleSave = async (data) => {
        if (modal.application) await editApplication(modal.application.id, data);
        else await addApplication(data);
        setModal(null);
    };

    const handleDelete = async () => {
        await removeApplication(modal.application.id);
        setModal(null);
    };

    return (
        <div className="page">
            <header className="topbar">
                <h1>Job Tracker</h1>
                <div>
                    <button className="primary" onClick={() => setModal({})}>
                        + Add application
                    </button>
                    <span>{user.email}</span>
                    <button onClick={logout}>Log out</button>
                </div>
            </header>

            {error && (
                <div className="error">
                    {error} <button onClick={reload}>Retry</button>
                </div>
            )}
            {loading ? (
                <p>Loading...</p>
            ) : (
                <KanbanBoard 
                    byStatus={byStatus} 
                    onMove={handleMove}
                    onOpen={(application) => setModal({application})}
                />
            )}

            {modal && (
                <ApplicationFormModal 
                    key={modal.application?.id ?? "new"}
                    application={modal.application}
                    onSubmit={handleSave}
                    onDelete={handleDelete}
                    onClose={() => setModal(null)}
                />
            )}

            {toast && (
                <div className="toast" role="alert">
                    {toast}
                </div>
            )}
        </div>
    );
}