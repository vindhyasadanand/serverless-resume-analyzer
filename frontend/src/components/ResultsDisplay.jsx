import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'

function ResultsDisplay({ result, loading }) {
  if (loading) {
    return (
      <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8 flex items-center justify-center min-h-[500px]">
        <div className="text-center">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-purple-500 border-t-transparent mx-auto mb-4"></div>
          <p className="text-xl text-gray-600 font-semibold">Analyzing Resume...</p>
          <p className="text-sm text-gray-500 mt-2">Parsing skills, calculating compatibility</p>
        </div>
      </div>
    )
  }

  if (!result) {
    return (
      <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8 flex items-center justify-center min-h-[500px]">
        <div className="text-center text-gray-400">
          <div className="text-6xl mb-4">📊</div>
          <p className="text-xl font-semibold">No Results Yet</p>
          <p className="text-sm mt-2">Upload a resume to see the analysis</p>
        </div>
      </div>
    )
  }

  const score = result.score
  const breakdown = result.breakdown
  const matchedSkills = result.matched_skills
  const missingSkills = result.missing_skills
  const recommendations = result.recommendations

  // Score color based on value
  const getScoreColor = (score) => {
    if (score >= 70) return 'text-green-600'
    if (score >= 50) return 'text-yellow-600'
    return 'text-red-600'
  }

  const getScoreBg = (score) => {
    if (score >= 70) return 'bg-green-100 border-green-300'
    if (score >= 50) return 'bg-yellow-100 border-yellow-300'
    return 'bg-red-100 border-red-300'
  }

  // Prepare data for pie chart
  const chartData = [
    { name: 'Skills', value: breakdown.skills, color: '#8b5cf6' },
    { name: 'Experience', value: breakdown.experience, color: '#ec4899' },
    { name: 'Education', value: breakdown.education, color: '#f59e0b' },
    { name: 'Format', value: breakdown.format, color: '#10b981' },
  ]

  return (
    <div className="bg-white/95 backdrop-blur-lg rounded-2xl shadow-2xl p-8 fade-in">
      <h2 className="text-3xl font-bold text-gray-800 mb-6">Analysis Results</h2>

      {/* Overall Score */}
      <div className={`${getScoreBg(score)} border-2 rounded-xl p-6 mb-6`}>
        <div className="text-center">
          <p className="text-lg font-semibold text-gray-700 mb-2">Overall Compatibility</p>
          <div className={`text-6xl font-bold ${getScoreColor(score)}`}>
            {score}%
          </div>
          <p className="text-sm text-gray-600 mt-2">
            {score >= 70 ? '🎉 Excellent Match!' : score >= 50 ? '👍 Good Match' : '⚠️ Needs Improvement'}
          </p>
        </div>
      </div>

      {/* Breakdown Chart */}
      <div className="mb-6">
        <h3 className="text-xl font-bold text-gray-800 mb-4">Score Breakdown</h3>
        <div className="h-64">
          <ResponsiveContainer width="100%" height="100%">
            <PieChart>
              <Pie
                data={chartData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}%`}
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {chartData.map((entry, index) => (
                  <Cell key={`cell-${index}`} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Matched Skills */}
      {matchedSkills && matchedSkills.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-3">✅ Matched Skills</h3>
          <div className="flex flex-wrap gap-2">
            {matchedSkills.map((skill, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-green-100 text-green-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Missing Skills */}
      {missingSkills && missingSkills.length > 0 && (
        <div className="mb-6">
          <h3 className="text-lg font-bold text-gray-800 mb-3">❌ Missing Skills</h3>
          <div className="flex flex-wrap gap-2">
            {missingSkills.map((skill, idx) => (
              <span
                key={idx}
                className="px-3 py-1 bg-red-100 text-red-800 rounded-full text-sm font-medium"
              >
                {skill}
              </span>
            ))}
          </div>
        </div>
      )}

      {/* Recommendations */}
      {recommendations && recommendations.length > 0 && (
        <div className="bg-gradient-to-r from-purple-50 to-indigo-50 rounded-xl p-6 border-2 border-purple-200">
          <h3 className="text-lg font-bold text-gray-800 mb-3">💡 Recommendations</h3>
          <ul className="space-y-2">
            {recommendations.map((rec, idx) => (
              <li key={idx} className="text-sm text-gray-700 flex items-start">
                <span className="text-purple-600 mr-2">•</span>
                <span>{rec}</span>
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  )
}

export default ResultsDisplay






