const API_URL = (import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000').replace(/\/+$/, '');

export class ApiError extends Error {
  constructor(message, status) { super(message); this.status = status; }
}

export async function api(path, { token, method = 'GET', body, formData } = {}) {
  const headers = {};
  if (token) headers.Authorization = `Bearer ${token}`;
  if (body) headers['Content-Type'] = 'application/json';
  let response;
  try {
    response = await fetch(`${API_URL}${path}`, {
      method, headers, body: body ? JSON.stringify(body) : formData,
    });
  } catch {
    throw new ApiError('EduConnect server cannot be reached. Please try again shortly; the server may be starting up.', 0);
  }
  const data = await response.json().catch(() => ({}));
  if (!response.ok) throw new ApiError(data.detail || data.message || 'Something went wrong. Please try again.', response.status);
  return data;
}

export { API_URL };
