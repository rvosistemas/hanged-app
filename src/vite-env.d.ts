/// <reference types="vite/client" />

interface ImportMetaEnv {
    readonly VITE_FLASK_APP_API_BASE_URL: string
    readonly VITE_VUE_APP_API_BASE_URL: string
}

interface ImportMeta {
    readonly env: ImportMetaEnv
}