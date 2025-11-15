import React from 'react'
import { motion } from 'framer-motion'

export default function LoadingSpinner() {
    return (
        <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center justify-center py-12"
        >
            <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
                className="w-16 h-16 border-4 border-gray-300 border-t-primary rounded-full"
            />

            <p className="mt-6 text-gray-700 font-semibold text-lg">
                Analyzing your document...
            </p>

            <motion.div
                animate={{ y: [0, 10, 0] }}
                transition={{ duration: 1.5, repeat: Infinity }}
                className="mt-2 text-4xl"
            >
                🔍
            </motion.div>

            <p className="mt-4 text-gray-500 text-sm text-center max-w-md">
                We're extracting the text and using AI to simplify the insurance language for you.
                <br />
                This usually takes 5-10 seconds.
            </p>
        </motion.div>
    )
}
