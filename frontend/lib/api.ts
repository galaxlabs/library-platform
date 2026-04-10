import axios from 'axios';

function resolveApiBaseUrl() {
  const configured = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8001/api/v1';

  if (typeof window === 'undefined') {
    return configured;
  }

  if (configured.startsWith('/')) {
    const { hostname, protocol } = window.location;
    if (hostname === 'localhost' || hostname === '127.0.0.1') {
      return `http://127.0.0.1:8001${configured}`;
    }
    return `${protocol}//${window.location.host}${configured}`;
  }

  return configured;
}

const api = axios.create({
  baseURL: resolveApiBaseUrl(),
});

let refreshPromise: Promise<string | null> | null = null;

api.interceptors.request.use((config) => {
  if (typeof window === 'undefined') {
    return config;
  }

  const token = window.localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (typeof window === 'undefined') {
      return Promise.reject(error);
    }

    const originalRequest = error.config;
    const status = error?.response?.status;
    const refreshToken = window.localStorage.getItem('refresh_token');

    if (status !== 401 || !refreshToken || originalRequest?._retry) {
      return Promise.reject(error);
    }

    originalRequest._retry = true;
    if (!refreshPromise) {
      refreshPromise = api
        .post('/auth/token/refresh/', { refresh: refreshToken })
        .then((response) => {
          const nextToken = response.data?.access ?? null;
          if (nextToken) {
            window.localStorage.setItem('access_token', nextToken);
          }
          return nextToken;
        })
        .catch(() => {
          window.localStorage.removeItem('access_token');
          window.localStorage.removeItem('refresh_token');
          window.localStorage.removeItem('user');
          return null;
        })
        .finally(() => {
          refreshPromise = null;
        });
    }

    const nextToken = await refreshPromise;
    if (!nextToken) {
      return Promise.reject(error);
    }

    originalRequest.headers = originalRequest.headers ?? {};
    originalRequest.headers.Authorization = `Bearer ${nextToken}`;
    return api(originalRequest);
  }
);

export function extractResults<T>(payload: T[] | { results?: T[] }): T[] {
  if (Array.isArray(payload)) {
    return payload;
  }
  return payload?.results ?? [];
}

export default api;
