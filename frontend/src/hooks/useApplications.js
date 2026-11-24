import { useCallback, useEffect, useState } from "react";
import * as api from "../api/applications";

const replaceById = (list, updated) => 
    list.map((a) => (a.id === updated.id ? updated : a));

export function useApplications() {
  const [applications, setApplications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [reloadKey, setReloadKey] = useState(0);

  useEffect(() => {
    let cancelled = false;

    api
        .listApplications({ limit: 100 })
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

  const addApplication = useCallback(async (data) => {
    const created = await api.createApplication(data);
    setApplications((cur) => [created, ...cur]);
    return created;
  }, []);

  const editApplication = useCallback(async (id, changes) => {
    const updated = await api.updateApplication(id, changes);
    setApplications((cur) => replaceById(cur, updated));
    return updated;
  }, []);

  const removeApplication = useCallback(async (id) => {
    await api.deleteApplication(id);
    setApplications((cur) => cur.filter((a) => a.id !== id));
  }, []);

  //Move first, ask the server second, rollback on failure
  const moveApplication = useCallback(async (id, fromStatus, toStatus) => {
    setApplications((cur) => 
        cur.map((a) => (a.id === id ? {...a, status: toStatus} : a))
    );
    try {
        const updated = await api.changeStatus(id, toStatus);
        setApplications((cur) => replaceById(cur, updated)); //picks up applied_date
    } catch (err) {
        setApplications((cur) => 
            cur.map((a) => (a.id === id ? {...a, status: fromStatus}: a))
        );
        throw err; // let the page show message
    }
  }, []);

  return {
        applications, 
        loading, 
        error, 
        reload,
        addApplication,
        editApplication,
        removeApplication,
        moveApplication
    };
}