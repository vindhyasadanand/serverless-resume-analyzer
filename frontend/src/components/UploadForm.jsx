import { useState } from 'react'
import { analyzeResume } from '../services/api'

function UploadForm({ onAnalysisComplete, setLoading }) {
  const [file, setFile] = useState(null)
  const [jobDescription, setJobDescription] = useState('')
  const [error, setError] = useState('')
  const [fileName, setFileName] = useState('')

  const handleFileChange = (e) => {
    const selectedFile = e.target.files[0]
    if (selectedFile) {
      const validTypes = ['application/pdf', 'text/plain', 'application/vnd.openxmlformats-officedocument.wordprocessingml.document']
      if (!validTypes.includes(selectedFile.type)) {
        setError('Please upload a PDF, TXT, or DOCX file')
        return
      }
      if (selectedFile.size > 5 * 1024 * 1024) {
        setError('File size must be less than 5MB')
        return
      }
      setFile(selectedFile)
      setFileName(selectedFile.name)
      setError('')
    }
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')

    if (!file) {
      setError('Please select a resume file')
      return
    }
    if (!jobDescription.trim()) {
      setError('Please enter a job description')
      return
    }

    setLoading(true)
    try {
      const result = await analyzeResume(file, jobDescription)
      onAnalysisComplete(result)
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to analyze resume. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleReset = () => {
    setFile(null)
    setFileName('')
    setJobDescription('')
    setError('')
    onAnalysisComplete(null)
  }

  return (
    <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Upload Resume</h2>
      
      <form onSubmit={handleSubmit} className="space-y-6">
        {/* File Upload */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Resume File (PDF, TXT, DOCX)
          </label>
          <div className="relative">
            <input
              type="file"
              onChange={handleFileChange}
              accept=".pdf,.txt,.docx"
              className="file-input"
              id="file-upload"
            />
            <label
              htmlFor="file-upload"
              className="flex items-center justify-center w-full px-4 py-3 border-2 border-dashed border-purple-300 rounded-lg cursor-pointer hover:border-purple-500 transition-colors bg-purple-50 hover:bg-purple-100"
            >
              <span className="text-purple-600 font-medium">
                {fileName || '📎 Choose file or drag here'}
              </span>
            </label>
          </div>
          {fileName && (
            <p className="mt-2 text-sm text-green-600">✓ {fileName}</p>
          )}
        </div>

        {/* Job Description */}
        <div>
          <label className="block text-sm font-semibold text-gray-700 mb-2">
            Job Description
          </label>
          <textarea
            value={jobDescription}
            onChange={(e) => setJobDescription(e.target.value)}
            placeholder="Paste the job description here...

Example:
We are seeking a Python Developer with experience in:
- Python, Flask, Django
- AWS (Lambda, S3, DynamoDB)
- Machine Learning & NLP
- REST API development"
            className="w-full px-4 py-3 border-2 border-gray-300 rounded-lg focus:border-purple-500 focus:ring-2 focus:ring-purple-200 transition-all resize-none"
            rows="10"
          />
        </div>

        {/* Error Message */}
        {error && (
          <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
            <p className="text-red-700 font-medium">⚠️ {error}</p>
          </div>
        )}

        {/* Buttons */}
        <div className="flex gap-4">
          <button
            type="submit"
            className="flex-1 bg-gradient-to-r from-purple-600 to-indigo-600 text-white font-bold py-3 px-6 rounded-lg hover:from-purple-700 hover:to-indigo-700 transform hover:scale-105 transition-all shadow-lg"
          >
            🚀 Analyze Resume
          </button>
          <button
            type="button"
            onClick={handleReset}
            className="px-6 py-3 bg-gray-200 text-gray-700 font-semibold rounded-lg hover:bg-gray-300 transition-all"
          >
            Reset
          </button>
        </div>
      </form>

      {/* Info Box */}
      <div className="mt-6 p-4 bg-blue-50 rounded-lg border border-blue-200">
        <h3 className="font-semibold text-blue-900 mb-2">💡 How it works:</h3>
        <ul className="text-sm text-blue-800 space-y-1">
          <li>• Upload your resume (PDF, TXT, or DOCX)</li>
          <li>• Paste the job description</li>
          <li>• Get instant compatibility score with detailed analysis</li>
          <li>• View matched/missing skills and recommendations</li>
        </ul>
      </div>
    </div>
  )
}

export default UploadForm






