import React, { useState } from 'react'
import FileUpload from './components/FileUpload'
import ResultDisplay from './components/ResultDisplay'
import Header from './components/Header'
import './App.css'

function App() {
    const [result, setResult] = useState(null)
    const [isLoading, setIsLoading] = useState(false)
    const [error, setError] = useState(null)

    const handleUpload = async (file) => {
        setIsLoading(true)
        setError(null)
        setResult(null)

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
            } else {
                // Handle error responses from backend
                setError(data.detail || data.message || 'An error occurred while processing your file.')
            }
        } catch (err) {
            setError('Failed to connect to the server. Please ensure the backend is running.')
            console.error('Error:', err)
        } finally {
            setIsLoading(false)
        }
    }

    const handleReset = () => {
        setResult(null)
        setError(null)
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
