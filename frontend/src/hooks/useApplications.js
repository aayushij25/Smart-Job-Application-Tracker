import { useCallback, useEffect, useState } from "react";
import { listApplications } from "../api/applications";

export function useApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;

    listApplications({ limit: 100})
        .then((data) => {
            if(!cancelled) {
                setApplications(data.items);
                setError("");
            }
        })
        .catch((err) => {
            if(!cancelled) setError(err.message);
        })
        .finally(() => {
            if (!cancelled) setLoading(false);
        });

        return () => {
            cancelled = true;
        };
  }, [reloadKey]);

  const reload = useCallback(() => {
    setLoading(true);
    setReloadKey((key) => key + 1);
  }, []);

  return {applications, loading, error, reload};
}