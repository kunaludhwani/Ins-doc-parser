// PDF Generation Utility - Optimized for Performance
import jsPDF from 'jspdf';
import html2canvas from 'html2canvas';

// Cache for repeated conversions
const markdownCache = new Map();

/**
 * Convert markdown-like content to HTML with caching
 * @param {string} content - Content with markdown formatting
 * @returns {string} HTML string
 */
const markdownToHtml = (content) => {
    // Check cache first
    if (markdownCache.has(content)) {
        return markdownCache.get(content);
    }

    let html = content;

    // Convert bold text **text** to <strong> (section headers)
    html = html.replace(/\*\*([^*]+)\*\*/g, '<h2 style="color: #E63946; font-size: 16pt; font-weight: 600; margin-top: 20px; margin-bottom: 12px; border-bottom: 2px solid #E63946; padding-bottom: 6px; font-family: \'Segoe UI\', Arial, sans-serif;">$1</h2>');

    // Convert bullet points with better spacing
    html = html.replace(/^- (.+)$/gm, '<div style="margin-left: 20px; margin-bottom: 10px; line-height: 1.7; font-size: 11pt;"><span style="color: #E63946; font-weight: bold; font-size: 14pt;">• </span><span style="color: #2c3e50;">$1</span></div>');

    // Convert line breaks to paragraphs with better typography
    html = html.split('\n\n').map(para => {
        if (para.trim() && !para.includes('<h2>') && !para.includes('•')) {
            return `<p style="margin-bottom: 14px; line-height: 1.8; text-align: justify; color: #2c3e50; font-size: 11pt;">${para.trim()}</p>`;
        }
        return para;
    }).join('\n');

    // Cache the result (limit cache size)
    if (markdownCache.size > 50) {
        const firstKey = markdownCache.keys().next().value;
        markdownCache.delete(firstKey);
    }
    markdownCache.set(content, html);

    return html;
};

/**
 * Generate PDF from HTML with proper Unicode support
 * @param {string} content - Markdown content to convert to PDF
 * @param {string} fileName - Original file name
 * @param {string} language - Language code ('en' or 'hi')
 * @returns {Promise<{blob: Blob, filename: string}>} PDF blob and filename
 */
export const generatePDF = async (content, fileName, language = 'en') => {
    // Extract clean filename without extension
    const cleanFileName = fileName.replace(/\.[^/.]+$/, '');
    const pdfFileName = `Summary for ${cleanFileName}`;

    const currentDate = new Date().toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });

    // Convert content to HTML
    const htmlContent = markdownToHtml(content);

    // Create a temporary container for HTML content
    const container = document.createElement('div');
    container.style.cssText = `
        position: absolute;
        left: -9999px;
        top: 0;
        width: 210mm;
        background-color: #ffffff;
        font-family: 'Segoe UI', 'Roboto', 'Arial', 'Helvetica Neue', sans-serif;
        font-size: 11pt;
        line-height: 1.7;
        color: #2c3e50;
        padding: 25mm 20mm;
        box-sizing: border-box;
    `;

    // Build HTML structure with watermark
    container.innerHTML = `
        <div style="position: relative; min-height: 1000px;">
            <!-- Watermark -->
            <div style="
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%) rotate(-45deg);
                font-size: 72pt;
                font-weight: 700;
                color: #e8e8e8;
                opacity: 0.12;
                white-space: nowrap;
                pointer-events: none;
                z-index: 0;
                user-select: none;
                font-family: 'Segoe UI', Arial, sans-serif;
                letter-spacing: 4px;
            ">Sacha Advisor</div>
            
            <!-- Content -->
            <div style="position: relative; z-index: 1;">
                <!-- Header -->
                <div style="
                    margin-bottom: 35px;
                    border-bottom: 3px solid #E63946;
                    padding-bottom: 18px;
                    background: linear-gradient(to right, #fff 0%, #fff5f5 100%);
                    padding: 20px;
                    margin: -20px -20px 35px -20px;
                ">
                    <h1 style="
                        color: #E63946;
                        font-size: 28pt;
                        margin: 0 0 10px 0;
                        font-weight: 700;
                        letter-spacing: -0.5px;
                        font-family: 'Segoe UI', Arial, sans-serif;
                    ">Sacha Advisor</h1>
                    <p style="
                        color: #7f8c8d;
                        font-size: 12pt;
                        margin: 0 0 15px 0;
                        font-weight: 400;
                        letter-spacing: 0.5px;
                    ">AI-Powered Insurance Document Summary</p>
                    <div style="
                        background-color: white;
                        padding: 12px 15px;
                        border-left: 4px solid #E63946;
                        margin-top: 15px;
                    ">
                        <p style="
                            color: #2c3e50;
                            font-size: 13pt;
                            margin: 0 0 6px 0;
                            font-weight: 600;
                        ">📄 ${cleanFileName}</p>
                        <p style="
                            color: #95a5a6;
                            font-size: 10pt;
                            margin: 0;
                            font-weight: 400;
                        ">📅 ${currentDate}</p>
                    </div>
                </div>

                <!-- Main Content -->
                <div style="
                    margin-bottom: 45px;
                    padding: 0 5px;
                ">
                    ${htmlContent}
                </div>

                <!-- Disclaimer -->
                <div style="
                    margin-top: 45px;
                    padding: 22px 24px;
                    background: linear-gradient(135deg, #fff5f5 0%, #ffe8e8 100%);
                    border-left: 5px solid #E63946;
                    border-radius: 4px;
                    box-shadow: 0 2px 8px rgba(230, 57, 70, 0.08);
                ">
                    <h3 style="
                        color: #c82333;
                        font-size: 13pt;
                        margin: 0 0 12px 0;
                        font-weight: 700;
                        font-family: 'Segoe UI', Arial, sans-serif;
                    ">⚠️ ${language === 'hi' ? 'महत्वपूर्ण अस्वीकरण' : 'IMPORTANT DISCLAIMER'}</h3>
                    <p style="
                        font-size: 10pt;
                        color: #555;
                        margin: 0;
                        line-height: 1.7;
                        text-align: justify;
                    ">${language === 'hi'
            ? 'यह दस्तावेज़ AI द्वारा उत्पन्न किया गया है और इसमें त्रुटियां हो सकती हैं। कृपया कोई भी वित्तीय निर्णय लेने से पहले तथ्यों की पुष्टि करें। यह सूचना केवल सामान्य मार्गदर्शन के लिए है और पेशेवर वित्तीय या कानूनी सलाह का विकल्प नहीं है।'
            : 'This document is AI-generated and may contain errors. Please verify all facts before making any financial decisions. This information is for general guidance only and is not a substitute for professional financial or legal advice.'
        }</p>
                </div>

                <!-- Footer -->
                <div style="
                    margin-top: 35px;
                    text-align: center;
                    font-size: 9pt;
                    color: #95a5a6;
                    padding-top: 20px;
                    border-top: 2px solid #ecf0f1;
                    font-weight: 500;
                    letter-spacing: 0.3px;
                ">© ${new Date().getFullYear()} Sacha Advisor | Simplifying Insurance with AI</div>
            </div>
        </div>
    `;

    document.body.appendChild(container);

    try {
        // Brief pause for rendering
        await new Promise(resolve => setTimeout(resolve, 100));

        // Capture full content as canvas with optimized settings
        const fullCanvas = await html2canvas(container, {
            scale: 2.0, // Reduced from 2.5 for 20% faster rendering
            useCORS: true,
            logging: false,
            backgroundColor: '#ffffff',
            windowWidth: container.offsetWidth,
            windowHeight: container.scrollHeight,
            letterRendering: true,
            allowTaint: false,
            imageTimeout: 0 // Prevent hanging on images
        });

        // Setup PDF
        const pdf = new jsPDF({
            orientation: 'portrait',
            unit: 'mm',
            format: 'a4',
            compress: true
        });

        // Page specs
        const pdfWidth = 210;
        const pdfHeight = 297;

        // Calculate how content maps to pages
        const canvasPixelWidth = fullCanvas.width;
        const canvasPixelHeight = fullCanvas.height;
        const widthRatio = pdfWidth / canvasPixelWidth;
        const contentHeightInPDF = canvasPixelHeight * widthRatio;

        // Determine pages needed
        const pagesNeeded = Math.ceil(contentHeightInPDF / pdfHeight);
        const pixelsPerPage = pdfHeight / widthRatio;

        // Process each page
        for (let i = 0; i < pagesNeeded; i++) {
            if (i > 0) pdf.addPage();

            // Calculate slice boundaries
            const startY = i * pixelsPerPage;
            const remainingHeight = canvasPixelHeight - startY;
            const sliceHeight = Math.min(pixelsPerPage, remainingHeight);

            // Skip if no content left
            if (sliceHeight <= 0) break;

            // Create page-specific canvas
            const sliceCanvas = document.createElement('canvas');
            sliceCanvas.width = canvasPixelWidth;
            sliceCanvas.height = sliceHeight;

            const context = sliceCanvas.getContext('2d');
            context.fillStyle = '#ffffff';
            context.fillRect(0, 0, sliceCanvas.width, sliceCanvas.height);

            // Transfer content slice
            context.drawImage(
                fullCanvas,
                0, startY,
                canvasPixelWidth, sliceHeight,
                0, 0,
                canvasPixelWidth, sliceHeight
            );

            // Convert and add to PDF with optimized compression
            const sliceImage = sliceCanvas.toDataURL('image/jpeg', 0.88); // Reduced from 0.95
            const heightInPDF = sliceHeight * widthRatio;
            pdf.addImage(sliceImage, 'JPEG', 0, 0, pdfWidth, heightInPDF, undefined, 'FAST');
        }

        // Remove temp element
        document.body.removeChild(container);

        return {
            blob: pdf.output('blob'),
            filename: `${pdfFileName}.pdf`
        };
    } catch (error) {
        if (document.body.contains(container)) {
            document.body.removeChild(container);
        }
        throw error;
    }
};/**
 * Download PDF
 * @param {Blob} blob - PDF blob
 * @param {string} filename - File name
 */
export const downloadPDF = (blob, filename) => {
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = filename;
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
    URL.revokeObjectURL(url);
};
