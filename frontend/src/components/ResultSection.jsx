import React from 'react'
import { motion } from 'framer-motion'

export default function ResultSection({ title, content, delay = 0 }) {
    return (
        <motion.div
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay, duration: 0.5 }}
            className="bg-white rounded-lg shadow p-6 border-l-4 border-primary"
        >
            <h3 className="text-lg font-bold text-primary mb-3">
                {title}
            </h3>
            <p className="text-gray-700 whitespace-pre-wrap leading-relaxed">
                {content}
            </p>
        </motion.div>
    )
}
