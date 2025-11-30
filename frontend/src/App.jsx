import React, { useState, useEffect } from 'react'
import FileUpload from './components/FileUpload'
import ResultDisplay from './components/ResultDisplay'
import DownloadSharePanel from './components/DownloadSharePanel'
import Header from './components/Header'
import { trackFileUpload, trackAnalysisComplete, trackError, trackUserAction, trackPageView } from './utils/analytics'
import './App.css'

function App() {
    const [result, setResult] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)
    const [uploadStartTime, setUploadStartTime] = useState(null)
    const [language, setLanguage] = useState('en')
    const [isTranslating, setIsTranslating] = useState(false)

    // Track initial page view
    useEffect(() => {
        trackPageView('/')
    }, [])

    const handleUpload = async (file, selectedLanguage, sessionId) => {
        const startTime = Date.now()
        setUploadStartTime(startTime)
        setIsLoading(true)
        setError(null)
        setResult(null)
        setLanguage(selectedLanguage)

        // Track file upload event
        const fileExtension = file.name.split('.').pop().toLowerCase()
        trackFileUpload(`.${fileExtension}`, file.size)

        const formData = new FormData()
        formData.append('file', file)

        const apiUrl = import.meta.env.VITE_API_URL || ''

        try {
            const response = await fetch(`${apiUrl}/api/upload`, {
                method: 'POST',
                headers: {
                    'X-Session-ID': sessionId,
                    'X-Language': selectedLanguage === 'hi' ? 'hindi' : 'english'
                },
                body: formData,
            })

            const data = await response.json()

            if (response.ok && data.status === 'success') {
                // If Hindi selected, translate immediately
                if (selectedLanguage === 'hi') {
                    setIsTranslating(true)
                    try {
                        const translateResponse = await fetch(`${apiUrl}/api/translate`, {
                            method: 'POST',
                            headers: {
                                'Content-Type': 'application/json'
                            },
                            body: JSON.stringify({
                                text: data.summary,
                                target_language: 'hi'
                            })
                        })
                        const translateData = await translateResponse.json()
                        if (translateResponse.ok) {
                            data.translatedSummary = translateData.translated_text
                        }
                    } catch (translateErr) {
                        console.error('Translation error:', translateErr)
                    } finally {
                        setIsTranslating(false)
                    }
                }

                setResult(data)

                // Track successful analysis
                const processingTime = Date.now() - startTime
                trackAnalysisComplete(data.is_insurance, processingTime)

                // Send acknowledgment that user saw the result
                try {
                    await fetch(`${apiUrl}/api/acknowledge`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-Session-ID': sessionId
                        },
                        body: JSON.stringify({
                            session_id: sessionId,
                            result_viewed: true
                        })
                    })
                } catch (ackErr) {
                    console.error('Acknowledgment error:', ackErr)
                    // Don't show error to user - this is background logging
                }
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
                        <ResultDisplay
                            result={result}
                            language={language}
                            isTranslating={isTranslating}
                        />

                        <DownloadSharePanel
                            result={result}
                            language={language}
                        />

                        <div className="mt-8 text-center">
                            <button
                                onClick={handleReset}
                                className="px-8 py-3 bg-primary text-white rounded-lg font-semibold hover:bg-primary-dark transition-colors duration-200 shadow-lg hover:shadow-xl"
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
