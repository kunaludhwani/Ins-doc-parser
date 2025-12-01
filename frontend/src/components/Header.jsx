import React from 'react'
import { motion } from 'framer-motion'

export default function Header() {
    return (
        <header className="bg-white shadow-sm border-b-4 border-primary">
            <div className="container mx-auto px-4 py-8 max-w-4xl">
                <motion.div
                    initial={{ opacity: 0, y: -20 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ duration: 0.5 }}
                >
                    <h1 className="text-4xl font-bold text-primary">
                        📘 Sacha Advisor
                    </h1>
                    <p className="text-gray-600 mt-2 text-lg">
                        AI-Powered Financial Document Explainer
                    </p>
                    <p className="text-gray-500 mt-1 text-sm">
                        Upload your financial documents and get a clear, human-friendly explanation
                    </p>
                </motion.div>
            </div>
        </header>
    )
}
