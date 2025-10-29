import { useState, useEffect } from 'react'
import { getHistory, deleteAnalysis, getStats } from '../services/api'

function History() {
  const [history, setHistory] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchData()
  }, [])

  const fetchData = async () => {
    setLoading(true)
    try {
      const [historyData, statsData] = await Promise.all([
        getHistory(50),
        getStats()
      ])
      setHistory(historyData.analyses)
      setStats(statsData.stats)
    } catch (err) {
      setError('Failed to load history')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('Are you sure you want to delete this analysis?')) return
    
    try {
      await deleteAnalysis(id)
      setHistory(history.filter(item => item.id !== id))
    } catch (err) {
      alert('Failed to delete analysis')
    }
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString()
  }

  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600 bg-green-100'
    if (score >= 50) return 'text-yellow-600 bg-yellow-100'
    return 'text-red-600 bg-red-100'
  }

  if (loading) {
    return (
      <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-4 border-purple-500 border-t-transparent mx-auto mb-4"></div>
          <p className="text-gray-600">Loading history...</p>
        </div>
      </div>
    )
  }

  return (
    <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Analysis History</h2>

      {/* Statistics */}
      {stats && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="bg-gradient-to-br from-purple-500 to-purple-600 rounded-xl p-4 text-white">
            <p className="text-sm font-semibold opacity-90">Total Analyses</p>
            <p className="text-3xl font-bold">{stats.total_analyses}</p>
          </div>
          <div className="bg-gradient-to-br from-blue-500 to-blue-600 rounded-xl p-4 text-white">
            <p className="text-sm font-semibold opacity-90">Average Score</p>
            <p className="text-3xl font-bold">{stats.average_score}%</p>
          </div>
          <div className="bg-gradient-to-br from-green-500 to-green-600 rounded-xl p-4 text-white">
            <p className="text-sm font-semibold opacity-90">Highest Score</p>
            <p className="text-3xl font-bold">{stats.highest_score}%</p>
          </div>
          <div className="bg-gradient-to-br from-orange-500 to-orange-600 rounded-xl p-4 text-white">
            <p className="text-sm font-semibold opacity-90">Lowest Score</p>
            <p className="text-3xl font-bold">{stats.lowest_score}%</p>
          </div>
        </div>
      )}

      {/* Error */}
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded mb-6">
          <p className="text-red-700">{error}</p>
        </div>
      )}

      {/* History List */}
      {history && history.length > 0 ? (
        <div className="space-y-4">
          {history.map((item) => (
            <div
              key={item.id}
              className="border-2 border-gray-200 rounded-xl p-6 hover:shadow-lg transition-shadow"
            >
              <div className="flex items-start justify-between">
                <div className="flex-1">
                  <div className="flex items-center gap-4 mb-3">
                    <h3 className="text-lg font-bold text-gray-800">
                      📄 {item.filename}
                    </h3>
                    <span className={`px-4 py-1 rounded-full font-bold ${getScoreColor(item.overall_score)}`}>
                      {item.overall_score}%
                    </span>
                  </div>
                  
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-3">
                    <div className="text-sm">
                      <span className="text-gray-500">Skills:</span>
                      <span className="font-semibold ml-1">{item.breakdown.skills}%</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Experience:</span>
                      <span className="font-semibold ml-1">{item.breakdown.experience}%</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Education:</span>
                      <span className="font-semibold ml-1">{item.breakdown.education}%</span>
                    </div>
                    <div className="text-sm">
                      <span className="text-gray-500">Format:</span>
                      <span className="font-semibold ml-1">{item.breakdown.format}%</span>
                    </div>
                  </div>

                  {item.matched_skills && item.matched_skills.length > 0 && (
                    <div className="mb-2">
                      <p className="text-xs text-gray-500 mb-1">Matched Skills:</p>
                      <div className="flex flex-wrap gap-1">
                        {item.matched_skills.slice(0, 5).map((skill, idx) => (
                          <span
                            key={idx}
                            className="px-2 py-0.5 bg-green-100 text-green-700 rounded text-xs"
                          >
                            {skill}
                          </span>
                        ))}
                        {item.matched_skills.length > 5 && (
                          <span className="text-xs text-gray-500">
                            +{item.matched_skills.length - 5} more
                          </span>
                        )}
                      </div>
                    </div>
                  )}

                  <p className="text-xs text-gray-400 mt-2">
                    {formatDate(item.created_at)}
                  </p>
                </div>

                <button
                  onClick={() => handleDelete(item.id)}
                  className="ml-4 px-3 py-1 bg-red-100 text-red-600 rounded-lg hover:bg-red-200 transition-colors text-sm font-medium"
                >
                  Delete
                </button>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <div className="text-center py-12 text-gray-400">
          <div className="text-6xl mb-4">📭</div>
          <p className="text-xl font-semibold">No History Yet</p>
          <p className="text-sm mt-2">Analyze your first resume to see it here</p>
        </div>
      )}
    </div>
  )
}

export default History






