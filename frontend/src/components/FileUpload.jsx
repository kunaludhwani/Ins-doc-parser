import React, { useRef, useState } from 'react'
import { motion } from 'framer-motion'
import LoadingSpinner from './LoadingSpinner'

export default function FileUpload({ onUpload, isLoading, error }) {
    const fileInputRef = useRef(null)
    const [dragActive, setDragActive] = useState(false)
    const [selectedFile, setSelectedFile] = useState(null)
    const [selectedLanguage, setSelectedLanguage] = useState('')

    const handleDrag = (e) => {
        e.preventDefault()
        e.stopPropagation()
        if (e.type === 'dragenter' || e.type === 'dragover') {
            setDragActive(true)
        } else if (e.type === 'dragleave') {
            setDragActive(false)
        }
    }

    const handleDrop = (e) => {
        e.preventDefault()
        e.stopPropagation()
        setDragActive(false)

        if (e.dataTransfer.files && e.dataTransfer.files[0]) {
            const file = e.dataTransfer.files[0]
            setSelectedFile(file)
        }
    }

    const handleChange = (e) => {
        if (e.target.files && e.target.files[0]) {
            const file = e.target.files[0]
            setSelectedFile(file)
        }
    }

    const handleUpload = () => {
        if (!selectedLanguage) {
            alert('Please select a language before uploading')
            return
        }
        if (selectedFile) {
            onUpload(selectedFile, selectedLanguage)
        }
    }

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full"
        >
            {isLoading ? (
                <LoadingSpinner />
            ) : (
                <div
                    onDragEnter={handleDrag}
                    onDragLeave={handleDrag}
                    onDragOver={handleDrag}
                    onDrop={handleDrop}
                    className={`
            border-2 border-dashed rounded-lg p-12 text-center transition-all duration-300
            ${dragActive
                            ? 'border-primary bg-primary-light scale-105'
                            : 'border-gray-300 bg-white hover:border-primary hover:bg-primary-light'
                        }
          `}
                >
                    <input
                        ref={fileInputRef}
                        type="file"
                        onChange={handleChange}
                        className="hidden"
                        accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                        disabled={isLoading}
                    />

                    <motion.div
                        whileHover={{ scale: 1.1 }}
                        className="mb-4 inline-block text-6xl"
                    >
                        📄
                    </motion.div>

                    <h2 className="text-2xl font-bold text-gray-800 mb-2">
                        Upload Insurance Document
                    </h2>

                    <p className="text-gray-600 mb-4">
                        Drag and drop your file here, or click to browse
                    </p>

                    <p className="text-sm text-gray-500 mb-6">
                        Supported formats: PDF, DOC, DOCX, JPG, PNG
                        <br />
                        Max file size: 50 MB | Max pages: 100 (PDF)
                    </p>

                    {/* Language Selection */}
                    {!selectedFile && (
                        <div className="mb-6">
                            <label className="block text-gray-700 font-semibold mb-3">
                                Select Language for Explanation <span className="text-red-500">*</span>
                            </label>
                            <div className="flex gap-4 justify-center">
                                <button
                                    onClick={() => setSelectedLanguage('en')}
                                    className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                                        selectedLanguage === 'en'
                                            ? 'bg-primary text-white shadow-lg scale-105'
                                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                                >
                                    🇬🇧 English
                                </button>
                                <button
                                    onClick={() => setSelectedLanguage('hi')}
                                    className={`px-6 py-3 rounded-lg font-semibold transition-all ${
                                        selectedLanguage === 'hi'
                                            ? 'bg-primary text-white shadow-lg scale-105'
                                            : 'bg-gray-200 text-gray-700 hover:bg-gray-300'
                                    }`}
                                >
                                    🇮🇳 हिंदी
                                </button>
                            </div>
                        </div>
                    )}

                    <motion.button
                        whileHover={{ scale: 1.05 }}
                        whileTap={{ scale: 0.95 }}
                        onClick={() => fileInputRef.current?.click()}
                        disabled={isLoading || !selectedLanguage}
                        className="
              px-8 py-3 bg-primary text-white rounded-lg font-semibold
              hover:bg-primary-dark transition-colors duration-200
              disabled:opacity-50 disabled:cursor-not-allowed
            "
                    >
                        Choose File
                    </motion.button>

                    {selectedFile && !isLoading && (
                        <motion.div
                            initial={{ opacity: 0 }}
                            animate={{ opacity: 1 }}
                            className="mt-4"
                        >
                            <p className="text-gray-700 text-sm mb-3">
                                Selected: <span className="font-semibold">{selectedFile.name}</span>
                            </p>
                            <p className="text-gray-600 text-sm mb-3">
                                Language: <span className="font-semibold">{selectedLanguage === 'en' ? '🇬🇧 English' : '🇮🇳 हिंदी'}</span>
                            </p>
                            <button
                                onClick={handleUpload}
                                className="px-6 py-2 bg-green-600 text-white rounded-lg font-semibold hover:bg-green-700 transition-colors"
                            >
                                Upload & Analyze
                            </button>
                        </motion.div>
                    )}
                </div>
            )}

            {error && (
                <motion.div
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    className="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-lg"
                >
                    <p className="font-semibold">⚠️ Error</p>
                    <p className="mt-1">{error}</p>
                </motion.div>
            )}

            {/* Information box */}
            <motion.div
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
                className="mt-8 bg-blue-50 border-l-4 border-blue-500 p-4 rounded"
            >
                <p className="text-sm text-blue-900">
                    <span className="font-semibold">ℹ️ Privacy Note:</span> We don't store your uploaded files.
                    Only the explanation is logged for service improvement.
                </p>
            </motion.div>
        </motion.div>
    )
}
