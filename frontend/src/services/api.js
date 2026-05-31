import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
});

export const downloadPdf = (summaryId, token) => {
  return api.get(
    `/summary/${summaryId}/pdf`,
    {
      responseType: "blob",
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  );
};

export default api;