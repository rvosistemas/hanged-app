/// <reference types="vite/client" />

const FLASK_API_BASE_URL = import.meta.env.FLASK_APP_API_BASE_URL || "http://localhost:8000";
const VUE_API_BASE_URL = import.meta.env.VUE_APP_API_BASE_URL || "http://localhost:5000";

export { FLASK_API_BASE_URL, VUE_API_BASE_URL };
