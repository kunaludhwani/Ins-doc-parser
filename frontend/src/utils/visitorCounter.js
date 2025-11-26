// Visitor counter utility for tracking document uploads
// Uses localStorage for persistent counter across sessions

const COUNTER_KEY = 'sacha_advisor_visitor_count';
const INITIAL_COUNT = 1250; // Starting count based on historical visits

/**
 * Initialize counter if not exists
 * @returns {number} Current counter value
 */
export const initializeCounter = () => {
    const stored = localStorage.getItem(COUNTER_KEY);
    if (!stored) {
        localStorage.setItem(COUNTER_KEY, INITIAL_COUNT.toString());
        return INITIAL_COUNT;
    }
    return parseInt(stored, 10);
};

/**
 * Get current visitor count
 * @returns {number} Current counter value
 */
export const getVisitorCount = () => {
    const count = localStorage.getItem(COUNTER_KEY);
    return count ? parseInt(count, 10) : initializeCounter();
};

/**
 * Increment visitor counter when document is uploaded
 * @returns {number} New counter value
 */
export const incrementVisitorCount = () => {
    const currentCount = getVisitorCount();
    const newCount = currentCount + 1;
    localStorage.setItem(COUNTER_KEY, newCount.toString());
    return newCount;
};

/**
 * Format counter for display (adds commas)
 * @param {number} count - Counter value
 * @returns {string} Formatted string (e.g., "1,250")
 */
export const formatCount = (count) => {
    return count.toLocaleString('en-US');
};
