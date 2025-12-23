import React, { useState, useCallback } from 'react'
import { motion, AnimatePresence } from 'framer-motion'
import {
    WhatsappShareButton,
    FacebookShareButton,
    TwitterShareButton,
    LinkedinShareButton,
    TelegramShareButton,
    WhatsappIcon,
    FacebookIcon,
    TwitterIcon,
    LinkedinIcon,
    TelegramIcon
} from 'react-share'
import { generatePDF, downloadPDF } from '../utils/pdfGenerator'
import { trackEvent } from '../utils/analytics'

export default React.memo(function DownloadSharePanel({ result, language }) {
    const [isGenerating, setIsGenerating] = useState(false)
    const [shareUrl, setShareUrl] = useState('')
    const [showShareMenu, setShowShareMenu] = useState(false)

    const handleDownloadPDF = useCallback(async (selectedLanguage) => {
        setIsGenerating(true)
        trackEvent('pdf_download_initiated', { language: selectedLanguage })

        try {
            // Use translated content if Hindi is selected and available
            const content = selectedLanguage === 'hi' && result.translatedSummary
                ? result.translatedSummary
                : result.summary

            // Generate PDF asynchronously (optimized with caching)
            const { blob, filename } = await generatePDF(
                content,
                result.filename || 'document',
                selectedLanguage
            )

            downloadPDF(blob, filename)

            trackEvent('pdf_download_success', {
                language: selectedLanguage,
                filename
            })
        } catch (error) {
            console.error('PDF generation error:', error)
            trackEvent('pdf_download_error', {
                language: selectedLanguage,
                error: error.message
            })
            alert('Failed to generate PDF. Please try again.')
        } finally {
            setIsGenerating(false)
        }
    }, [result])

    const handleShare = useCallback(() => {
        setShowShareMenu(!showShareMenu)
        if (!shareUrl) {
            // Generate shareable URL (current page)
            setShareUrl(window.location.href)
        }
        trackEvent('share_button_clicked')
    }, [showShareMenu, shareUrl])

    const shareTitle = `Check out this insurance document summary from Sacha Advisor`
    const shareText = `I just analyzed my insurance document with Sacha Advisor - AI-powered insurance explainer! 🎯`

    return (
        <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="mt-8"
        >
            {/* Download and Share Actions */}
            <div className="bg-gradient-to-br from-primary-light to-white rounded-lg p-6 shadow-md border border-primary/20">
                <h3 className="text-lg font-semibold text-gray-800 mb-4 flex items-center gap-2">
                    📥 Download & Share
                </h3>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    {/* Download Button */}
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={() => handleDownloadPDF(language)}
                        disabled={isGenerating || (language === 'hi' && !result.translatedSummary)}
                        className={`flex items-center justify-center gap-3 py-4 px-6 rounded-lg font-semibold transition-all duration-200 ${isGenerating || (language === 'hi' && !result.translatedSummary)
                            ? 'bg-gray-300 text-gray-500 cursor-not-allowed'
                            : 'bg-primary text-white hover:bg-primary-dark shadow-lg hover:shadow-xl'
                            }`}
                    >
                        {isGenerating ? (
                            <>
                                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-white"></div>
                                Generating PDF...
                            </>
                        ) : (
                            <>
                                <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 10v6m0 0l-3-3m3 3l3-3m2 8H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
                                </svg>
                                Download PDF {language === 'hi' ? '(हिंदी)' : '(English)'}
                            </>
                        )}
                    </motion.button>

                    {/* Share Button */}
                    <motion.button
                        whileHover={{ scale: 1.02 }}
                        whileTap={{ scale: 0.98 }}
                        onClick={handleShare}
                        className="flex items-center justify-center gap-3 py-4 px-6 bg-white text-primary border-2 border-primary rounded-lg font-semibold hover:bg-primary hover:text-white transition-all duration-200 shadow-md hover:shadow-lg"
                    >
                        <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                        </svg>
                        Share Summary
                    </motion.button>
                </div>

                {/* Social Share Menu */}
                <AnimatePresence>
                    {showShareMenu && (
                        <motion.div
                            initial={{ opacity: 0, height: 0 }}
                            animate={{ opacity: 1, height: 'auto' }}
                            exit={{ opacity: 0, height: 0 }}
                            className="mt-4 p-4 bg-white rounded-lg border border-gray-200"
                        >
                            <p className="text-sm text-gray-600 mb-3">Share via:</p>
                            <div className="flex flex-wrap gap-3 justify-center">
                                <WhatsappShareButton
                                    url={shareUrl}
                                    title={shareText}
                                    separator=" - "
                                    onClick={() => trackEvent('share_whatsapp')}
                                >
                                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                                        <WhatsappIcon size={48} round />
                                    </motion.div>
                                </WhatsappShareButton>

                                <FacebookShareButton
                                    url={shareUrl}
                                    quote={shareText}
                                    onClick={() => trackEvent('share_facebook')}
                                >
                                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                                        <FacebookIcon size={48} round />
                                    </motion.div>
                                </FacebookShareButton>

                                <TwitterShareButton
                                    url={shareUrl}
                                    title={shareText}
                                    onClick={() => trackEvent('share_twitter')}
                                >
                                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                                        <TwitterIcon size={48} round />
                                    </motion.div>
                                </TwitterShareButton>

                                <LinkedinShareButton
                                    url={shareUrl}
                                    title={shareTitle}
                                    summary={shareText}
                                    onClick={() => trackEvent('share_linkedin')}
                                >
                                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                                        <LinkedinIcon size={48} round />
                                    </motion.div>
                                </LinkedinShareButton>

                                <TelegramShareButton
                                    url={shareUrl}
                                    title={shareText}
                                    onClick={() => trackEvent('share_telegram')}
                                >
                                    <motion.div whileHover={{ scale: 1.1 }} whileTap={{ scale: 0.9 }}>
                                        <TelegramIcon size={48} round />
                                    </motion.div>
                                </TelegramShareButton>
                            </div>
                        </motion.div>
                    )}
                </AnimatePresence>

                {/* Info Note */}
                <div className="mt-4 p-3 bg-yellow-50 border border-yellow-200 rounded-lg">
                    <p className="text-xs text-yellow-800 flex items-start gap-2">
                        <span className="text-lg">💡</span>
                        <span>
                            <strong>Note:</strong> The downloaded PDF includes a watermark and disclaimer.
                            It's compressed for easy sharing ({language === 'hi' ? 'हिंदी में उपलब्ध' : 'available in English and Hindi'}).
                        </span>
                    </p>
                </div>
            </div>
        </motion.div>
    )
})
