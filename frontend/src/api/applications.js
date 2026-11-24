import { request } from "./client"

export function listApplications({status, limit = 100, offset = 0} = {}) {
    const params = new URLSearchParams({limit, offset});
    if (status) params.set("status", status);
    return request('/applications?{params}');
}

export const createApplication = (data) => 
    request("/applications", {method: "POST", body: data });

export const updateApplication = (id, changes) => 
    request(`/applications/${id}`, {method: "PATCH", body: changes});

export const changeStatus = (id, status) => 
    request(`/applications/${id}/status`, {method: "PATCH", body: {status}});

export const deleteApplication = (id) => 
    request(`/applications/${id}`, {method: "DELETE"});