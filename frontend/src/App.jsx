/**
 * Resume Analyzer - Main Application Component
 * Project Group 20 - Cloud Computing
 * 
 * Team Members:
 * - Keyur Nareshkumar Modi (Backend & NLP)
 * - Naveen John (Cloud Architecture & Deployment)
 * - Vindhya Sadanand Hegde (Frontend & UI/UX)
 * 
 * This React application provides an intuitive interface for resume analysis
 * using our custom NLP engine deployed on Azure serverless infrastructure.
 */

import { useState } from 'react'
import UploadForm from './components/UploadForm'
import ResultsDisplay from './components/ResultsDisplay'
import History from './components/History'
import './App.css'

function App() {
  const [activeTab, setActiveTab] = useState('analyze')
  const [analysisResult, setAnalysisResult] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalysisComplete = (result) => {
    setAnalysisResult(result)
  }

  return (
    <div className="min-h-screen py-8 px-4">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <header className="text-center mb-12">
          <h1 className="text-5xl font-bold text-white mb-4">
            📄 Resume Analyzer
          </h1>
          <p className="text-xl text-purple-100">
            Smart Job Matching with NLP-Powered Analysis
          </p>
          <p className="text-sm text-purple-200 mt-2">
            Project Group 20 | Cloud Computing Project
          </p>
        </header>

        {/* Tab Navigation */}
        <div className="flex justify-center mb-8">
          <div className="bg-white/10 backdrop-blur-lg rounded-lg p-1 inline-flex">
            <button
              onClick={() => setActiveTab('analyze')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'analyze'
                  ? 'bg-white text-purple-600 shadow-lg'
                  : 'text-white hover:bg-white/20'
              }`}
            >
              🎯 Analyze Resume
            </button>
            <button
              onClick={() => setActiveTab('history')}
              className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                activeTab === 'history'
                  ? 'bg-white text-purple-600 shadow-lg'
                  : 'text-white hover:bg-white/20'
              }`}
            >
              📊 History
            </button>
          </div>
        </div>

        {/* Main Content */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {activeTab === 'analyze' && (
            <>
              <div>
                <UploadForm
                  onAnalysisComplete={handleAnalysisComplete}
                  setLoading={setLoading}
                />
              </div>
              <div>
                <ResultsDisplay result={analysisResult} loading={loading} />
              </div>
            </>
          )}
          
          {activeTab === 'history' && (
            <div className="lg:col-span-2">
              <History />
            </div>
          )}
        </div>

        {/* Footer */}
        <footer className="mt-16 text-center text-purple-100">
          <p className="text-sm">
            Built with React, Flask, scikit-learn • Team: Keyur Modi, Naveen John, Vindhya Hegde
          </p>
        </footer>
      </div>
    </div>
  )
}

export default App






