import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5001'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const analyzeResume = async (file, jobDescription) => {
  const formData = new FormData()
  formData.append('resume', file)
  formData.append('job_description', jobDescription)

  const response = await api.post('/api/analyze', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  return response.data
}

export const getHistory = async (limit = 50) => {
  const response = await api.get(`/api/history?limit=${limit}`)
  return response.data
}

export const getAnalysis = async (id) => {
  const response = await api.get(`/api/analysis/${id}`)
  return response.data
}

export const deleteAnalysis = async (id) => {
  const response = await api.delete(`/api/analysis/${id}`)
  return response.data
}

export const getStats = async () => {
  const response = await api.get('/api/stats')
  return response.data
}

export default api






