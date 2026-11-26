import { request } from "./client";

export const getResume = () => request("/resume");
export const saveResume = (text) => request("/resume", { method: "PUT", body: { text } });