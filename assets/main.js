// Main JavaScript for Scholastic Forum - Optimized with caching and lazy loading

// Performance monitoring
const performance = {
    startTime: performance.now(),
    metrics: {
        domInteractive: 0,
        domContentLoaded: 0,
        windowLoaded: 0,
        firstPaint: 0
    }
};

// Cache DOM elements for better performance
const cache = {
    elements: {},
    get: function(id) {
        if (!this.elements[id]) {
            this.elements[id] = document.getElementById(id);
        }
        return this.elements[id];
    }
};

// Lazy loading manager
class LazyLoader {
    constructor() {
        this.observer = null;
        this.images = [];
        this.init();
    }
    
    init() {
        if ('IntersectionObserver' in window) {
            this.observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        this.loadImage(entry.target);
                        this.observer.unobserve(entry.target);
                    }
                });
            }, {
                rootMargin: '50px 0px',
                threshold: 0.1
            });
        }
        
        this.images = document.querySelectorAll('.lazy-image');
        this.images.forEach(img => {
            if (this.observer) {
                this.observer.observe(img);
            } else {
                // Fallback: load all images immediately
                this.loadImage(img);
            }
        });
    }
    
    loadImage(img) {
        if (img.dataset.src) {
            img.src = img.dataset.src;
        }
        img.classList.add('loaded');
        
        // Remove placeholder if exists
        const placeholder = img.parentNode.querySelector('.image-placeholder');
        if (placeholder) {
            placeholder.style.display = 'none';
        }
    }
    
    addImage(img) {
        if (this.observer) {
            this.observer.observe(img);
        } else {
            this.loadImage(img);
        }
    }
}

// Theme manager with caching
class ThemeManager {
    constructor() {
        this.theme = 'light';
        this.init();
    }
    
    init() {
        // Force light theme permanently
        this.setTheme('light');
        
        // Prevent any theme changes
        this.lockTheme();
        
        // Store in cache
        localStorage.setItem('theme', 'light');
        localStorage.setItem('theme-locked', 'true');
    }
    
    setTheme(theme) {
        this.theme = theme;
        document.documentElement.setAttribute('data-theme', theme);
        document.documentElement.style.colorScheme = theme;
        document.body.style.colorScheme = theme;
        
        // Cache the theme
        sessionStorage.setItem('current-theme', theme);
    }
    
    lockTheme() {
        // Mutation observer to prevent theme changes
        const observer = new MutationObserver((mutations) => {
            mutations.forEach((mutation) => {
                if (mutation.attributeName === 'data-theme' || 
                    mutation.attributeName === 'style') {
                    this.setTheme('light');
                }
            });
        });
        
        observer.observe(document.documentElement, {
            attributes: true,
            attributeFilter: ['data-theme', 'style']
        });
        
        observer.observe(document.body, {
            attributes: true,
            attributeFilter: ['style']
        });
        
        // Prevent dark mode media query changes
        const darkModeMediaQuery = window.matchMedia('(prefers-color-scheme: dark)');
        darkModeMediaQuery.addListener(() => {
            this.setTheme('light');
        });
    }
}

// Search and filter manager with debouncing
class SearchManager {
    constructor() {
        this.searchInput = cache.get('searchInput');
        this.schoolCards = document.querySelectorAll('.featured-card, .school-card');
        this.timeout = null;
        this.init();
    }
    
    init() {
        if (this.searchInput) {
            this.searchInput.addEventListener('input', this.debounce(this.filterSchools.bind(this), 300));
        }
        
        // Initialize filters
        this.initializeFilters();
    }
    
    debounce(func, wait) {
        return (...args) => {
            clearTimeout(this.timeout);
            this.timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
    
    initializeFilters() {
        const filters = ['levelFilter', 'typeFilter', 'genderFilter', 'curriculumFilter'];
        filters.forEach(filterId => {
            const filter = cache.get(filterId);
            if (filter) {
                filter.addEventListener('change', this.filterSchools.bind(this));
            }
        });
    }
    
    filterSchools() {
        const searchTerm = this.searchInput ? this.searchInput.value.toLowerCase().trim() : '';
        
        this.schoolCards.forEach(card => {
            const searchData = card.getAttribute('data-search') || '';
            const matchesSearch = searchTerm === '' || searchData.includes(searchTerm);
            
            card.style.display = matchesSearch ? 'block' : 'none';
            
            if (matchesSearch) {
                card.style.animation = 'fadeInUp 0.4s ease-out forwards';
            }
        });
        
        this.updateCount();
    }
    
    updateCount() {
        const visibleCount = Array.from(this.schoolCards).filter(card => 
            card.style.display !== 'none'
        ).length;
        
        const countElement = cache.get('schoolsCount') || cache.get('gridTitle');
        if (countElement) {
            const total = this.schoolCards.length;
            countElement.textContent = `Showing ${visibleCount} of ${total} institutions`;
        }
    }
}

// Image optimization and caching
class ImageCache {
    constructor() {
        this.cache = new Map();
        this.maxSize = 50; // Maximum number of images to cache
    }
    
    async getImage(url) {
        if (this.cache.has(url)) {
            return this.cache.get(url);
        }
        
        try {
            const response = await fetch(url);
            const blob = await response.blob();
            const objectURL = URL.createObjectURL(blob);
            
            // Add to cache
            this.cache.set(url, objectURL);
            
            // Manage cache size
            if (this.cache.size > this.maxSize) {
                const firstKey = this.cache.keys().next().value;
                URL.revokeObjectURL(this.cache.get(firstKey));
                this.cache.delete(firstKey);
            }
            
            return objectURL;
        } catch (error) {
            console.error('Error loading image:', error);
            return url; // Fallback to original URL
        }
    }
    
    clear() {
        this.cache.forEach(url => URL.revokeObjectURL(url));
        this.cache.clear();
    }
}

// Scroll performance optimization
class ScrollManager {
    constructor() {
        this.lastScrollTop = 0;
        this.scrollThreshold = 100;
        this.init();
    }
    
    init() {
        // Throttle scroll events
        window.addEventListener('scroll', this.throttle(this.handleScroll.bind(this), 16));
        
        // Initialize scroll to top button
        this.initScrollToTop();
    }
    
    throttle(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    
    handleScroll() {
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Show/hide scroll to top button
        const scrollTopBtn = cache.get('scrollTop');
        if (scrollTopBtn) {
            if (scrollTop > 300) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        }
        
        // Parallax effect for hero banner
        const heroBanner = document.querySelector('.hero-banner');
        if (heroBanner) {
            heroBanner.style.transform = `translateY(${scrollTop * 0.5}px)`;
        }
        
        this.lastScrollTop = scrollTop;
    }
    
    initScrollToTop() {
        const scrollTopBtn = cache.get('scrollTop');
        if (scrollTopBtn) {
            scrollTopBtn.addEventListener('click', (e) => {
                e.preventDefault();
                window.scrollTo({
                    top: 0,
                    behavior: 'smooth'
                });
            });
        }
    }
}

// Mobile menu manager
class MobileMenu {
    constructor() {
        this.menuBtn = cache.get('mobileMenuBtn');
        this.navLinks = cache.get('navLinks');
        this.init();
    }
    
    init() {
        if (this.menuBtn && this.navLinks) {
            this.menuBtn.addEventListener('click', this.toggleMenu.bind(this));
            
            // Close menu when clicking outside
            document.addEventListener('click', this.handleClickOutside.bind(this));
            
            // Close menu when clicking a link
            this.navLinks.querySelectorAll('a').forEach(link => {
                link.addEventListener('click', this.closeMenu.bind(this));
            });
        }
    }
    
    toggleMenu(e) {
        e.preventDefault();
        e.stopPropagation();
        
        const isOpen = this.navLinks.classList.toggle('active');
        this.menuBtn.setAttribute('aria-expanded', isOpen);
        this.menuBtn.innerHTML = isOpen 
            ? '<i class="fas fa-times"></i>' 
            : '<i class="fas fa-bars"></i>';
        this.menuBtn.classList.toggle('active');
    }
    
    closeMenu() {
        this.navLinks.classList.remove('active');
        this.menuBtn.innerHTML = '<i class="fas fa-bars"></i>';
        this.menuBtn.setAttribute('aria-expanded', 'false');
        this.menuBtn.classList.remove('active');
    }
    
    handleClickOutside(e) {
        if (!this.navLinks.contains(e.target) && !this.menuBtn.contains(e.target)) {
            this.closeMenu();
        }
    }
}

// Performance metrics collection
class PerformanceMetrics {
    constructor() {
        this.metrics = {};
        this.init();
    }
    
    init() {
        // Collect navigation timing
        if ('performance' in window && 'timing' in performance) {
            const timing = performance.timing;
            
            this.metrics = {
                dns: timing.domainLookupEnd - timing.domainLookupStart,
                tcp: timing.connectEnd - timing.connectStart,
                ttfb: timing.responseStart - timing.requestStart,
                download: timing.responseEnd - timing.responseStart,
                domInteractive: timing.domInteractive - timing.navigationStart,
                domContentLoaded: timing.domContentLoadedEventEnd - timing.navigationStart,
                windowLoaded: timing.loadEventEnd - timing.navigationStart,
                total: timing.loadEventEnd - timing.navigationStart
            };
            
            // Log metrics
            console.log('Performance metrics:', this.metrics);
            
            // Send to analytics if available
            this.sendToAnalytics();
        }
    }
    
    sendToAnalytics() {
        // Example: Send to Google Analytics
        if (typeof gtag !== 'undefined') {
            gtag('event', 'performance_metrics', {
                event_category: 'Performance',
                event_label: 'Page Load',
                value: this.metrics.total,
                metrics: JSON.stringify(this.metrics)
            });
        }
    }
    
    getMetric(name) {
        return this.metrics[name] || 0;
    }
}

// Cache warming for frequently accessed pages
class CacheWarmer {
    constructor() {
        this.pagesToWarm = [
            'schools/all.html',
            'index.html'
        ];
        this.init();
    }
    
    init() {
        // Warm cache on idle time
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => this.warmCache());
        } else {
            setTimeout(() => this.warmCache(), 5000);
        }
    }
    
    async warmCache() {
        for (const page of this.pagesToWarm) {
            try {
                await fetch(page, {
                    method: 'HEAD',
                    cache: 'force-cache'
                });
                console.log(`Cache warmed for: ${page}`);
            } catch (error) {
                console.warn(`Failed to warm cache for ${page}:`, error);
            }
        }
    }
}

// Main initialization
class App {
    constructor() {
        this.lazyLoader = null;
        this.themeManager = null;
        this.searchManager = null;
        this.scrollManager = null;
        this.mobileMenu = null;
        this.performanceMetrics = null;
        this.imageCache = null;
        this.cacheWarmer = null;
        this.init();
    }
    
    init() {
        // Initialize performance monitoring first
        this.performanceMetrics = new PerformanceMetrics();
        
        // Initialize managers
        this.themeManager = new ThemeManager();
        this.lazyLoader = new LazyLoader();
        this.searchManager = new SearchManager();
        this.scrollManager = new ScrollManager();
        this.mobileMenu = new MobileMenu();
        this.imageCache = new ImageCache();
        
        // Initialize cache warmer (low priority)
        this.cacheWarmer = new CacheWarmer();
        
        // Initialize other components
        this.initSchoolCards();
        this.initKeyboardShortcuts();
        this.initServiceWorker();
        this.initErrorHandling();
        
        // Mark page as loaded
        document.documentElement.classList.add('loaded');
        
        console.log('App initialized with performance optimizations');
    }
    
    initSchoolCards() {
        const schoolCards = document.querySelectorAll('.featured-card, .school-card');
        schoolCards.forEach(card => {
            // Make cards keyboard accessible
            card.setAttribute('tabindex', '0');
            card.setAttribute('role', 'button');
            
            // Add click handler
            card.addEventListener('click', (e) => {
                if (!e.target.classList.contains('view-btn') && 
                    !e.target.closest('.view-btn')) {
                    const schoolId = card.getAttribute('data-school-id');
                    if (schoolId) {
                        // Add click animation
                        card.style.transform = 'scale(0.95)';
                        setTimeout(() => {
                            card.style.transform = '';
                            window.location.href = `schools/${schoolId}.html`;
                        }, 150);
                    }
                }
            });
            
            // Add keyboard support
            card.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    const schoolId = card.getAttribute('data-school-id');
                    if (schoolId) {
                        window.location.href = `schools/${schoolId}.html`;
                    }
                }
            });
        });
    }
    
    initKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Focus search on Ctrl+K or /
            if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
                e.preventDefault();
                const searchInput = cache.get('searchInput') || cache.get('allSearchInput');
                if (searchInput) searchInput.focus();
            }
            
            if (e.key === '/' && document.activeElement.tagName !== 'INPUT') {
                e.preventDefault();
                const searchInput = cache.get('searchInput') || cache.get('allSearchInput');
                if (searchInput) searchInput.focus();
            }
            
            // Escape to clear search
            if (e.key === 'Escape' && document.activeElement.tagName === 'INPUT') {
                document.activeElement.value = '';
                this.searchManager.filterSchools();
            }
        });
    }
    
    initServiceWorker() {
        // Register service worker for offline support
        if ('serviceWorker' in navigator) {
            window.addEventListener('load', () => {
                navigator.serviceWorker.register('/service-worker.js')
                    .then(registration => {
                        console.log('ServiceWorker registered:', registration);
                    })
                    .catch(error => {
                        console.log('ServiceWorker registration failed:', error);
                    });
            });
        }
    }
    
    initErrorHandling() {
        // Global error handler
        window.addEventListener('error', (e) => {
            console.error('Global error:', e.error);
            
            // Send to error tracking service
            if (typeof gtag !== 'undefined') {
                gtag('event', 'exception', {
                    description: e.error.message,
                    fatal: false
                });
            }
        });
        
        // Unhandled promise rejection
        window.addEventListener('unhandledrejection', (e) => {
            console.error('Unhandled promise rejection:', e.reason);
        });
    }
}

// Initialize app when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.app = new App();
    });
} else {
    window.app = new App();
}

// Export for module usage if needed
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        App,
        LazyLoader,
        ThemeManager,
        SearchManager,
        ScrollManager,
        MobileMenu,
        PerformanceMetrics,
        ImageCache,
        CacheWarmer
    };
}
