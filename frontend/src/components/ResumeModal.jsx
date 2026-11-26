import { useEffect, useState } from "react";
import { getResume, saveResume } from "../api/resume";

export default function ResumeModal({ onClose }) {
  const [text, setText] = useState("");
  const [savedAt, setSavedAt] = useState(null);
  const [loaded, setLoaded] = useState(false);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);

  useEffect(() => {
    let cancelled = false;
    getResume()
      .then((resume) => {
        if (cancelled || !resume) return;
        setText(resume.text);
        setSavedAt(resume.updated_at);
      })
      .catch((err) => !cancelled && setError(err.message))
      .finally(() => !cancelled && setLoaded(true));
    return () => {
      cancelled = true;
    };
  }, []);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setBusy(true);
    try {
      await saveResume(text);
      onClose();
    } catch (err) {
      setError(err.message);
      setBusy(false);
    }
  };

  return (
    <div className="modal-backdrop" onMouseDown={(e) => e.target === e.currentTarget && onClose()}>
      <form className="modal wide" onSubmit={handleSubmit}>
        <h2>Your resume</h2>
        <p className="hint">
          Paste it as plain text. {savedAt && `Last saved ${new Date(savedAt).toLocaleDateString()}.`}{" "}
          The first save can take a few seconds.
        </p>
        {error && <div className="error">{error}</div>}
        <textarea
          rows={16}
          value={text}
          onChange={(e) => setText(e.target.value)}
          maxLength={20000}
          placeholder={loaded ? "Paste your resume text here" : "Loading…"}
          disabled={!loaded}
          required
        />
        <div className="modal-actions">
          <span className="spacer" />
          <button type="button" onClick={onClose}>Cancel</button>
          <button type="submit" className="primary" disabled={busy || !loaded}>
            {busy ? "Saving…" : "Save"}
          </button>
        </div>
      </form>
    </div>
  );
}