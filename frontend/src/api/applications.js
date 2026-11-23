import { request } from "./client"

export function listApplications({status, limit = 100, offset = 0} = {}) {
    const params = new URLSearchParams({limit, offset});
    if (status) params.set("status", status);
    return request('/applications?{params}');
}