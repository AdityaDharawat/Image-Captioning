// Professional Image Caption Generator - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Initialize application
    initApplication();
    
    // Setup event listeners
    setupEventHandlers();
    
    // Initialize analytics
    initAnalytics();
});

/**
 * Initialize the application
 */
function initApplication() {
    // Check for preferred color scheme
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    if (prefersDark) {
        document.documentElement.classList.add('dark-mode');
    }
    
    // Initialize tooltips
    initTooltips();
    
    // Initialize clipboard functionality
    initClipboard();
}

/**
 * Setup event handlers for interactive elements
 */
function setupEventHandlers() {
    // File upload interactions
    const fileUploader = document.querySelector('.stFileUploader');
    if (fileUploader) {
        fileUploader.addEventListener('dragover', (e) => {
            e.preventDefault();
            fileUploader.classList.add('dragover');
        });
        
        fileUploader.addEventListener('dragleave', () => {
            fileUploader.classList.remove('dragover');
        });
        
        fileUploader.addEventListener('drop', (e) => {
            e.preventDefault();
            fileUploader.classList.remove('dragover');
        });
    }
    
    // Navigation scroll behavior
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 100,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Window resize handler
    window.addEventListener('resize', debounce(handleResize, 200));
}

/**
 * Initialize tooltips for UI elements
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        const tooltipText = element.getAttribute('data-tooltip');
        const tooltip = document.createElement('div');
        tooltip.className = 'tooltip';
        tooltip.textContent = tooltipText;
        element.appendChild(tooltip);
        
        element.addEventListener('mouseenter', () => {
            tooltip.classList.add('visible');
        });
        
        element.addEventListener('mouseleave', () => {
            tooltip.classList.remove('visible');
        });
    });
}

/**
 * Initialize clipboard functionality
 */
function initClipboard() {
    const copyButtons = document.querySelectorAll('[data-copy]');
    
    copyButtons.forEach(button => {
        button.addEventListener('click', () => {
            const textToCopy = button.getAttribute('data-copy');
            navigator.clipboard.writeText(textToCopy).then(() => {
                // Show success feedback
                const originalText = button.innerHTML;
                button.innerHTML = 'Copied!';
                
                setTimeout(() => {
                    button.innerHTML = originalText;
                }, 2000);
            }).catch(err => {
                console.error('Failed to copy text: ', err);
            });
        });
    });
}

/**
 * Initialize analytics tracking
 */
function initAnalytics() {
    // Track page view
    trackEvent('page_view', {
        page_title: document.title,
        page_path: window.location.pathname
    });
    
    // Track file uploads
    const fileInput = document.querySelector('input[type="file"]');
    if (fileInput) {
        fileInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                trackEvent('file_upload', {
                    file_type: e.target.files[0].type,
                    file_size: e.target.files[0].size
                });
            }
        });
    }
    
    // Track button clicks
    document.querySelectorAll('button').forEach(button => {
        button.addEventListener('click', () => {
            trackEvent('button_click', {
                button_text: button.textContent.trim(),
                button_id: button.id || null
            });
        });
    });
}

/**
 * Track custom events
 * @param {string} eventName 
 * @param {object} eventData 
 */
function trackEvent(eventName, eventData = {}) {
    // In a production environment, this would connect to your analytics service
    console.log(`Tracking event: ${eventName}`, eventData);
}

/**
 * Debounce function for performance
 * @param {function} func 
 * @param {number} wait 
 * @returns 
 */
function debounce(func, wait) {
    let timeout;
    return function() {
        const context = this, args = arguments;
        clearTimeout(timeout);
        timeout = setTimeout(() => {
            func.apply(context, args);
        }, wait);
    };
}

/**
 * Handle window resize events
 */
function handleResize() {
    // Update any responsive elements
    console.log('Window resized');
}

/**
 * Show loading state
 */
window.showLoadingState = function() {
    const loadingElement = document.getElementById('loading-state');
    if (loadingElement) {
        loadingElement.style.display = 'block';
    }
};

/**
 * Hide loading state
 */
window.hideLoadingState = function() {
    const loadingElement = document.getElementById('loading-state');
    if (loadingElement) {
        loadingElement.style.display = 'none';
    }
};

/**
 * Export results functionality
 */
window.exportResults = function(format = 'text') {
    const caption = document.querySelector('.caption-result p').textContent;
    
    switch (format) {
        case 'text':
            downloadFile(caption, 'caption.txt', 'text/plain');
            break;
        case 'json':
            const jsonData = {
                caption: caption,
                generatedAt: new Date().toISOString(),
                modelVersion: '2.1.0'
            };
            downloadFile(JSON.stringify(jsonData, null, 2), 'caption.json', 'application/json');
            break;
        default:
            console.error('Unsupported export format');
    }
};

/**
 * Download file helper
 * @param {string} content 
 * @param {string} filename 
 * @param {string} type 
 */
function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type: type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}