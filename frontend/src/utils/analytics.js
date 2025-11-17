// Google Analytics utility functions for event tracking

/**
 * Send custom event to Google Analytics
 * @param {string} eventName - Name of the event
 * @param {object} eventParams - Additional parameters
 */
export const trackEvent = (eventName, eventParams = {}) => {
    if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('event', eventName, eventParams);
    }
};

/**
 * Track file upload events
 * @param {string} fileType - Type of file uploaded (.pdf, .docx, etc.)
 * @param {number} fileSize - Size of file in bytes
 */
export const trackFileUpload = (fileType, fileSize) => {
    trackEvent('file_upload', {
        event_category: 'engagement',
        event_label: fileType,
        value: Math.round(fileSize / 1024), // Convert to KB
        file_type: fileType,
        file_size_kb: Math.round(fileSize / 1024)
    });
};

/**
 * Track document analysis completion
 * @param {boolean} isInsurance - Whether document was classified as insurance
 * @param {number} processingTime - Time taken in milliseconds
 */
export const trackAnalysisComplete = (isInsurance, processingTime) => {
    trackEvent('analysis_complete', {
        event_category: 'conversion',
        event_label: isInsurance ? 'insurance_doc' : 'non_insurance',
        value: Math.round(processingTime / 1000), // Convert to seconds
        is_insurance: isInsurance,
        processing_time_sec: Math.round(processingTime / 1000)
    });
};

/**
 * Track errors
 * @param {string} errorType - Type of error
 * @param {string} errorMessage - Error message
 */
export const trackError = (errorType, errorMessage) => {
    trackEvent('error', {
        event_category: 'error',
        event_label: errorType,
        error_type: errorType,
        error_message: errorMessage.substring(0, 100) // Limit message length
    });
};

/**
 * Track user actions
 * @param {string} action - Action name (e.g., 'reset', 'retry')
 */
export const trackUserAction = (action) => {
    trackEvent('user_action', {
        event_category: 'engagement',
        event_label: action,
        action: action
    });
};

/**
 * Track page views (for SPAs)
 * @param {string} pagePath - Virtual page path
 */
export const trackPageView = (pagePath) => {
    if (typeof window !== 'undefined' && window.gtag) {
        window.gtag('config', 'G-9Z5GNNMRQ4', {
            page_path: pagePath
        });
    }
};
