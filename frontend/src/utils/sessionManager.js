/**
 * Session Manager
 * Generates and manages unique session IDs for analytics tracking
 */

import { v4 as uuidv4 } from 'uuid';

const SESSION_KEY = 'sacha_session_id';
const SESSION_TIMEOUT = 30 * 60 * 1000; // 30 minutes
const LAST_ACTIVITY_KEY = 'sacha_last_activity';

/**
 * Get or create session ID
 * Sessions expire after 30 minutes of inactivity
 */
export const getSessionId = () => {
    const now = Date.now();
    const lastActivity = parseInt(localStorage.getItem(LAST_ACTIVITY_KEY) || '0');

    // Check if session expired
    if (now - lastActivity > SESSION_TIMEOUT) {
        // Create new session
        const newSessionId = uuidv4();
        localStorage.setItem(SESSION_KEY, newSessionId);
        localStorage.setItem(LAST_ACTIVITY_KEY, now.toString());
        return newSessionId;
    }

    // Get or create session
    let sessionId = localStorage.getItem(SESSION_KEY);
    if (!sessionId) {
        sessionId = uuidv4();
        localStorage.setItem(SESSION_KEY, sessionId);
    }

    // Update last activity
    localStorage.setItem(LAST_ACTIVITY_KEY, now.toString());

    return sessionId;
};

/**
 * Track page view time
 */
export const startTimeTracking = () => {
    const startTime = Date.now();
    return () => {
        const endTime = Date.now();
        return Math.round((endTime - startTime) / 1000); // Return seconds
    };
};

/**
 * Track scroll depth
 */
export const trackScrollDepth = () => {
    const getScrollPercentage = () => {
        const scrollTop = window.scrollY;
        const docHeight = document.documentElement.scrollHeight - window.innerHeight;
        return Math.round((scrollTop / docHeight) * 100);
    };

    let maxScroll = 0;

    const handleScroll = () => {
        const current = getScrollPercentage();
        if (current > maxScroll) {
            maxScroll = current;
        }
    };

    window.addEventListener('scroll', handleScroll);

    return () => {
        window.removeEventListener('scroll', handleScroll);
        return Math.min(maxScroll, 100); // Cap at 100%
    };
};

/**
 * Get language preference
 */
export const getLanguagePreference = () => {
    return localStorage.getItem('language_preference') || 'english';
};

/**
 * Set language preference
 */
export const setLanguagePreference = (language) => {
    localStorage.setItem('language_preference', language);
};
