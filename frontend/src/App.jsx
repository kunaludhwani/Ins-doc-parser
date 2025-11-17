import React, { useState, useEffect } from 'react'
import FileUpload from './components/FileUpload'
import ResultDisplay from './components/ResultDisplay'
import Header from './components/Header'
import { trackFileUpload, trackAnalysisComplete, trackError, trackUserAction, trackPageView } from './utils/analytics'
import './App.css'

function App() {
    const [result, setResult] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)
    const [uploadStartTime, setUploadStartTime] = useState(null)

    // Track initial page view
    useEffect(() => {
        trackPageView('/')
    }, [])

    const handleUpload = async (file) => {
        const startTime = Date.now()
        setUploadStartTime(startTime)
        setIsLoading(true)
        setError(null)
        setResult(null)

        // Track file upload event
        const fileExtension = file.name.split('.').pop().toLowerCase()
        trackFileUpload(`.${fileExtension}`, file.size)

        const formData = new FormData()
        formData.append('file', file)

        const apiUrl = import.meta.env.VITE_API_URL || ''

        try {
            const response = await fetch(`${apiUrl}/api/upload`, {
                method: 'POST',
                body: formData,
            })

            const data = await response.json()

            if (response.ok && data.status === 'success') {
                setResult(data)

                // Track successful analysis
                const processingTime = Date.now() - startTime
                trackAnalysisComplete(data.is_insurance, processingTime)
            } else {
                // Handle error responses from backend
                const errorMessage = data.detail || data.message || 'An error occurred while processing your file.'
                setError(errorMessage)

                // Track error
                trackError('api_error', errorMessage)
            }
        } catch (err) {
            const errorMessage = 'Failed to connect to the server. Please ensure the backend is running.'
            setError(errorMessage)
            console.error('Error:', err)

            // Track connection error
            trackError('connection_error', err.message)
        } finally {
            setIsLoading(false)
        }
    }

    const handleReset = () => {
        setResult(null)
        setError(null)

        // Track reset action
        trackUserAction('analyze_another_document')
        trackPageView('/')
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-primary-light via-white to-primary-light">
            <Header />

            <main className="container mx-auto px-4 py-12 max-w-4xl">
                {!result ? (
                    <FileUpload onUpload={handleUpload} isLoading={isLoading} error={error} />
                ) : (
                    <>
                        <ResultDisplay result={result} />
                        <div className="mt-8 text-center">
                            <button
                                onClick={handleReset}
                                className="px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary-dark transition-colors duration-200"
                            >
                                Analyze Another Document
                            </button>
                        </div>
                    </>
                )}
            </main>

            <footer className="bg-gray-900 text-white text-center py-6 mt-16">
                <p className="text-sm">
                    Sacha Advisor v1.1 | Simplifying Insurance Documents with AI
                </p>
            </footer>
        </div>
    )
}

export default App
