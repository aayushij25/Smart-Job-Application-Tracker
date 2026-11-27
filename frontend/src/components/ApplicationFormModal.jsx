import { useEffect, useState } from "react";
import AnalysisPanel from "./AnalysisPanel";

const EMPTY = {
    company: "",
    role: "",
    applied_date: "",
    job_description: "",
    notes: "",
};

function toForm(application) {
    if(!application) return EMPTY;
    return {
        company: application.company,
        role: application.role,
        applied_date: application.applied_date ?? "",
        job_description: application.job_description ?? "",
        notes: application.notes ?? "",
    };
}

function toPayload(form) {
    return {
        company: form.company.trim(),
        role: form.role.trim(),
        applied_date: form.applied_date || null,
        job_description: form.job_description.trim() || null,
        notes: form.notes.trim() || null,
    };
}

export default function ApplicationFormModal({ application, onSubmit, onDelete, onAnalyze, onClose}) {
    const isEdit = Boolean(application);
    const [form, setForm] = useState(() => toForm(application));
    const [error, setError] = useState("");
    const [busy, setBusy] = useState(false);
    const [confirmingDelete, setConfirmingDelete] = useState(false);
    const [current, setCurrent] = useState(application);
    const [analyzing, setAnalyzing] = useState(false);

    const savedDescription = (application?.job_description ?? "").trim();
    const canAnalyze = isEdit && form.job_description.trim() !== ""&& form.job_description.trim() === savedDescription;

    useEffect(() => {
        const onKey = (e) => {
            if (e.key === "Escape") onClose();
        };
        window.addEventListener("keydown", onKey);
        return () => window.removeEventListener("keydown", onKey);
    }, [onClose]);

    const setField = (name) => (e) => 
        setForm((f) => ({...f, [name]: e.target.value}));

    const run = async (action) => {
        setError("");
        setBusy(true);
        try {
            await action();
        } catch (err) {
            setError(err.message);
            setBusy(false);
        }
    };

    const handleSubmit = (e) => {
        e.preventDefault();
        run(() => onSubmit(toPayload(form)));
    };

    const handleAnalyze = async() => {
        setError("");
        setAnalyzing(true);
        try {
            setCurrent(await onAnalyze(application.id));
        } catch(err) {
            setError(err.message);
        } finally {
            setAnalyzing(false);
        }
    };

    return (
        <div
            className="modal-backdrop"
            onMouseDown={(e) => e.target === e.currentTarget && onClose()}
        >
            <form className="modal" onSubmit={handleSubmit}>
                <h2>{isEdit ? "Edit application" :  "Add application"}</h2>
                {error && <div className="error">{error}</div>}

                <label>
                    Company 
                    <input value={form.company} onChange={setField("company")} maxLength={200} required autoFocus />
                </label>
                <label>
                    Role 
                    <input value={form.role} onChange={setField("role")} maxLength={200} required />
                </label>
                <label>
                    Applied date
                    <input type="date" value={form.applied_date} onChange={setField("applied_date")} />
                </label>
                <small className="hint">Setting a date moves a Saved application to Applied.</small>
                <label>
                    Job Description
                    <textarea rows={6} value={form.job_description} onChange={setField("job_description")} />
                </label>
                <label>
                    Notes
                    <textarea rows={3} value={form.notes} onChange={setField("notes")} />
                </label>

                {isEdit && (
                    <AnalysisPanel 
                        application={current}
                        canAnalyze={canAnalyze}
                        busy={analyzing}
                        onAnalyze={handleAnalyze}
                    />
                )}
                {confirmingDelete ? (
                    <div className="modal-actions">
                        <span>Delete this application?</span>
                        <span className="spacer" />
                        <button type="button" onClick={() => setConfirmingDelete(false)}>
                            Keep it
                        </button>
                        <button type="button" className="danger" disabled={busy} onClick={() => run(onDelete)}>
                            {busy ? "Deleting..." : "Yes, delete"}
                        </button>
                    </div>
                ) : (
                    <div className="modal-actions">
                        {isEdit && (
                            <button type="button" className="danger-outline" onClick={() => setConfirmingDelete(true)}>
                                Delete
                            </button>
                        )}
                        <span className="spacer" />
                        <button type="button" onClick={onClose}>Cancel</button>
                        <button type="submit" className="primary" disabled={busy}>
                            {busy ? "Saving..." : "Save"}
                        </button>
                    </div>
                )}
            </form>
        </div>
    );
}