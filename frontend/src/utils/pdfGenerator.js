// PDF Generation Utility with watermark and compression
import jsPDF from 'jspdf';

/**
 * Generate compressed PDF with watermark
 * @param {string} content - Markdown content to convert to PDF
 * @param {string} fileName - Original file name
 * @param {string} language - Language code ('en' or 'hi')
 * @returns {Blob} PDF blob
 */
export const generatePDF = (content, fileName, language = 'en') => {
    const doc = new jsPDF({
        orientation: 'portrait',
        unit: 'mm',
        format: 'a4',
        compress: true // Enable compression
    });

    // Extract clean filename without extension
    const cleanFileName = fileName.replace(/\.[^/.]+$/, '');
    const pdfFileName = `Summary for ${cleanFileName}`;

    // Page dimensions
    const pageWidth = doc.internal.pageSize.getWidth();
    const pageHeight = doc.internal.pageSize.getHeight();
    const margin = 15;
    const maxWidth = pageWidth - (2 * margin);

    // Add watermark to all pages
    const addWatermark = (pageNum) => {
        doc.setFontSize(50);
        doc.setTextColor(240, 240, 240); // Very light gray
        doc.setFont('helvetica', 'bold');

        // Calculate center position with rotation
        const text = 'Sacha Advisor';
        const textWidth = doc.getTextWidth(text);

        // Save current state
        doc.saveGraphicsState();

        // Rotate and place watermark diagonally
        doc.setGState(new doc.GState({ opacity: 0.1 }));
        doc.text(text, pageWidth / 2, pageHeight / 2, {
            align: 'center',
            angle: 45
        });

        // Restore state
        doc.restoreGraphicsState();
    };

    // Add header
    doc.setFontSize(20);
    doc.setTextColor(230, 57, 70); // Primary red color
    doc.setFont('helvetica', 'bold');
    doc.text('Sacha Advisor', margin, 20);

    doc.setFontSize(12);
    doc.setTextColor(100, 100, 100);
    doc.setFont('helvetica', 'normal');
    doc.text('AI-Powered Insurance Document Summary', margin, 28);

    // Add document name
    doc.setFontSize(14);
    doc.setTextColor(0, 0, 0);
    doc.setFont('helvetica', 'bold');
    const wrappedTitle = doc.splitTextToSize(`Document: ${cleanFileName}`, maxWidth);
    doc.text(wrappedTitle, margin, 38);

    // Add date
    doc.setFontSize(10);
    doc.setTextColor(120, 120, 120);
    doc.setFont('helvetica', 'normal');
    const date = new Date().toLocaleDateString(language === 'hi' ? 'hi-IN' : 'en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric'
    });
    doc.text(`Generated: ${date}`, margin, 45);

    // Add separator line
    doc.setDrawColor(230, 57, 70);
    doc.setLineWidth(0.5);
    doc.line(margin, 48, pageWidth - margin, 48);

    // Process content - convert markdown to plain text with formatting
    let yPosition = 55;
    const lineHeight = 6;

    const processContent = (text) => {
        // Split by sections (markdown headers)
        const sections = text.split(/(\*\*[^*]+\*\*)/g);

        sections.forEach(section => {
            if (!section.trim()) return;

            // Check if we need a new page
            if (yPosition > pageHeight - 30) {
                doc.addPage();
                addWatermark(doc.internal.getNumberOfPages());
                yPosition = 20;
            }

            // Handle bold headers (markdown **)
            if (section.startsWith('**') && section.endsWith('**')) {
                const headerText = section.replace(/\*\*/g, '');
                doc.setFont('helvetica', 'bold');
                doc.setFontSize(12);
                doc.setTextColor(230, 57, 70);

                yPosition += 3;
                doc.text(headerText, margin, yPosition);
                yPosition += lineHeight + 1;
            } else {
                // Regular content
                doc.setFont('helvetica', 'normal');
                doc.setFontSize(10);
                doc.setTextColor(60, 60, 60);

                // Split into bullet points or paragraphs
                const lines = section.split('\n').filter(line => line.trim());

                lines.forEach(line => {
                    if (yPosition > pageHeight - 30) {
                        doc.addPage();
                        addWatermark(doc.internal.getNumberOfPages());
                        yPosition = 20;
                    }

                    const trimmedLine = line.trim();
                    if (trimmedLine.startsWith('- ')) {
                        // Bullet point
                        const bulletText = trimmedLine.substring(2);
                        const wrappedText = doc.splitTextToSize(bulletText, maxWidth - 5);
                        doc.text('•', margin, yPosition);
                        doc.text(wrappedText, margin + 5, yPosition);
                        yPosition += wrappedText.length * lineHeight;
                    } else if (trimmedLine.length > 0) {
                        // Regular paragraph
                        const wrappedText = doc.splitTextToSize(trimmedLine, maxWidth);
                        doc.text(wrappedText, margin, yPosition);
                        yPosition += wrappedText.length * lineHeight;
                    }
                });

                yPosition += 2; // Extra spacing between sections
            }
        });
    };

    // Add watermark to first page
    addWatermark(1);

    // Process main content
    processContent(content);

    // Add disclaimer on last page
    if (yPosition > pageHeight - 50) {
        doc.addPage();
        addWatermark(doc.internal.getNumberOfPages());
        yPosition = 20;
    }

    yPosition += 10;
    doc.setDrawColor(200, 200, 200);
    doc.setLineWidth(0.3);
    doc.line(margin, yPosition, pageWidth - margin, yPosition);
    yPosition += 8;

    doc.setFontSize(9);
    doc.setFont('helvetica', 'bold');
    doc.setTextColor(200, 50, 50);
    doc.text('⚠️ IMPORTANT DISCLAIMER', margin, yPosition);

    yPosition += 6;
    doc.setFont('helvetica', 'normal');
    doc.setFontSize(8);
    doc.setTextColor(100, 100, 100);

    const disclaimerText = language === 'hi'
        ? 'यह दस्तावेज़ AI द्वारा उत्पन्न किया गया है और इसमें त्रुटियां हो सकती हैं। कृपया कोई भी वित्तीय निर्णय लेने से पहले तथ्यों की पुष्टि करें। यह सूचना केवल सामान्य मार्गदर्शन के लिए है और पेशेवर वित्तीय या कानूनी सलाह का विकल्प नहीं है।'
        : 'This document is AI-generated and may contain errors. Please verify all facts before making any financial decisions. This information is for general guidance only and is not a substitute for professional financial or legal advice.';

    const wrappedDisclaimer = doc.splitTextToSize(disclaimerText, maxWidth);
    doc.text(wrappedDisclaimer, margin, yPosition);

    // Add footer with page numbers
    const pageCount = doc.internal.getNumberOfPages();
    for (let i = 1; i <= pageCount; i++) {
        doc.setPage(i);
        doc.setFontSize(8);
        doc.setTextColor(150, 150, 150);
        doc.text(
            `Page ${i} of ${pageCount} | © ${new Date().getFullYear()} Sacha Advisor`,
            pageWidth / 2,
            pageHeight - 10,
            { align: 'center' }
        );
    }

    return {
        blob: doc.output('blob'),
        filename: `${pdfFileName}.pdf`
    };
};

/**
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
