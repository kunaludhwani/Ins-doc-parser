import React, { useState, useEffect, useMemo, useRef } from 'react'
import { motion } from 'framer-motion'
import ResultSection from './ResultSection'

export default React.memo(function ResultDisplay({ result, language = 'en', isTranslating = false }) {
    const [displayedText, setDisplayedText] = useState('')
    const [isTyping, setIsTyping] = useState(true)
    const intervalRef = useRef(null)

    // Memoize content selection to prevent unnecessary recalculations
    const content = useMemo(() => {
        if (!result?.summary) return '';
        return language === 'hi' && result.translatedSummary
            ? result.translatedSummary
            : result.summary;
    }, [result?.summary, result?.translatedSummary, language]);

    useEffect(() => {
        if (!content) return;

        let index = 0;
        setIsTyping(true);
        setDisplayedText('');

        // Clear any existing interval
        if (intervalRef.current) {
            clearInterval(intervalRef.current);
        }

        intervalRef.current = setInterval(() => {
            if (index < content.length) {
                setDisplayedText(content.substring(0, index + 1));
                index++;
            } else {
                setIsTyping(false);
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        }, 5);

        return () => {
            if (intervalRef.current) {
                clearInterval(intervalRef.current);
                intervalRef.current = null;
            }
        };
    }, [content])

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="w-full"
        >
            {/* Success Message */}
            <motion.div
                initial={{ scale: 0.9 }}
                animate={{ scale: 1 }}
                className="mb-8 p-6 bg-green-50 border-2 border-green-400 rounded-lg"
            >
                <p className="text-green-800 font-semibold text-lg">
                    ✅ Document Verified as Insurance Policy
                </p>
                <p className="text-green-700 mt-2">
                    Your document has been successfully analyzed. Here's the simplified explanation:
                </p>
            </motion.div>

            {/* Main Result Container */}
            <div className="bg-white rounded-lg shadow-lg p-8 mb-8">
                {/* Translation Loading State */}
                {isTranslating && (
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        className="mb-4 p-4 bg-blue-50 border border-blue-300 rounded-lg flex items-center gap-3"
                    >
                        <div className="animate-spin h-5 w-5 border-2 border-blue-600 border-t-transparent rounded-full"></div>
                        <span className="text-blue-800 font-medium">
                            {language === 'hi' ? 'हिंदी में अनुवाद कर रहे हैं...' : 'Translating to Hindi...'}
                        </span>
                    </motion.div>
                )}

                {/* Explanation Content */}
                <div className="prose prose-sm max-w-none">
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        transition={{ delay: 0.3 }}
                        className="whitespace-pre-wrap text-gray-800 leading-relaxed font-serif"
                        key={`${language}-${result.translatedSummary ? 'translated' : 'original'}`}
                    >
                        {displayedText}
                        {isTyping && <span className="animate-pulse">▍</span>}
                    </motion.div>
                </div>
            </div>

            {/* Disclaimer Section Only */}
            <div className="space-y-6">
                <ResultSection
                    title="⚠️ Important Disclaimer"
                    content="This explanation is for informational purposes only. It's not a substitute for the official policy document. Always refer to your actual policy document and consult your insurance agent for specific questions about your coverage."
                    delay={0.5}
                />
            </div>
        </motion.div>
    )
})
