// School page specific JavaScript - Optimized

class SchoolPage {
    constructor() {
        this.galleryImages = [];
        this.currentImageIndex = 0;
        this.lightbox = null;
        this.init();
    }
    
    init() {
        this.initGallery();
        this.initLazyLoading();
        this.initInteractiveElements();
        this.initPerformanceMonitoring();
    }
    
    initGallery() {
        const galleryItems = document.querySelectorAll('.gallery-item');
        this.galleryImages = Array.from(galleryItems).map((item, index) => ({
            element: item,
            src: item.querySelector('img').src,
            filename: item.getAttribute('data-filename'),
            date: item.getAttribute('data-date'),
            size: item.getAttribute('data-size')
        }));
        
        // Add click handlers
        galleryItems.forEach((item, index) => {
            item.addEventListener('click', () => this.openLightbox(index));
        });
        
        // Initialize lightbox
        this.initLightbox();
    }
    
    initLightbox() {
        this.lightbox = document.getElementById('lightbox');
        if (!this.lightbox) return;
        
        // Create lightbox elements
        const lightboxContent = document.createElement('div');
        lightboxContent.className = 'lightbox-content';
        lightboxContent.innerHTML = `
            <div class="lightbox-close" id="lightboxClose">
                <i class="fas fa-times"></i>
            </div>
            <div class="lightbox-nav lightbox-prev" id="lightboxPrev">
                <i class="fas fa-chevron-left"></i>
            </div>
            <img class="lightbox-image" id="lightboxImage" src="" alt="">
            <div class="lightbox-caption" id="lightboxCaption"></div>
            <div class="lightbox-nav lightbox-next" id="lightboxNext">
                <i class="fas fa-chevron-right"></i>
            </div>
        `;
        
        this.lightbox.appendChild(lightboxContent);
        
        // Add event listeners
        document.getElementById('lightboxClose').addEventListener('click', () => this.closeLightbox());
        document.getElementById('lightboxPrev').addEventListener('click', () => this.showPrevImage());
        document.getElementById('lightboxNext').addEventListener('click', () => this.showNextImage());
        
        // Keyboard navigation
        document.addEventListener('keydown', (e) => {
            if (!this.lightbox.classList.contains('active')) return;
            
            switch(e.key) {
                case 'Escape':
                    this.closeLightbox();
                    break;
                case 'ArrowRight':
                    this.showNextImage();
                    break;
                case 'ArrowLeft':
                    this.showPrevImage();
                    break;
            }
        });
        
        // Close on background click
        this.lightbox.addEventListener('click', (e) => {
            if (e.target === this.lightbox) {
                this.closeLightbox();
            }
        });
    }
    
    openLightbox(index) {
        if (this.galleryImages.length === 0) return;
        
        this.currentImageIndex = index;
        this.updateLightbox();
        this.lightbox.classList.add('active');
        document.body.style.overflow = 'hidden';
    }
    
    updateLightbox() {
        const image = this.galleryImages[this.currentImageIndex];
        const lightboxImage = document.getElementById('lightboxImage');
        const lightboxCaption = document.getElementById('lightboxCaption');
        
        lightboxImage.src = image.src;
        lightboxCaption.textContent = `${image.filename} • ${image.date} • ${image.size}`;
        
        // Preload next and previous images
        this.preloadAdjacentImages();
    }
    
    preloadAdjacentImages() {
        const nextIndex = (this.currentImageIndex + 1) % this.galleryImages.length;
        const prevIndex = (this.currentImageIndex - 1 + this.galleryImages.length) % this.galleryImages.length;
        
        this.preloadImage(this.galleryImages[nextIndex].src);
        this.preloadImage(this.galleryImages[prevIndex].src);
    }
    
    preloadImage(src) {
        const img = new Image();
        img.src = src;
    }
    
    showNextImage() {
        if (this.galleryImages.length === 0) return;
        this.currentImageIndex = (this.currentImageIndex + 1) % this.galleryImages.length;
        this.updateLightbox();
    }
    
    showPrevImage() {
        if (this.galleryImages.length === 0) return;
        this.currentImageIndex = (this.currentImageIndex - 1 + this.galleryImages.length) % this.galleryImages.length;
        this.updateLightbox();
    }
    
    closeLightbox() {
        this.lightbox.classList.remove('active');
        document.body.style.overflow = '';
    }
    
    initLazyLoading() {
        const lazyImages = document.querySelectorAll('.lazy-image');
        
        if ('IntersectionObserver' in window) {
            const imageObserver = new IntersectionObserver((entries, observer) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        const img = entry.target;
                        img.classList.add('loaded');
                        observer.unobserve(img);
                    }
                });
            }, {
                rootMargin: '100px 0px'
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        } else {
            // Fallback
            lazyImages.forEach(img => img.classList.add('loaded'));
        }
    }
    
    initInteractiveElements() {
        // Animate rating bars
        const bars = document.querySelectorAll('.bar-fill');
        bars.forEach((bar, index) => {
            const width = bar.style.width;
            bar.style.width = '0';
            setTimeout(() => {
                bar.style.width = width;
            }, 300 + index * 200);
        });
        
        // Add hover effects
        document.querySelectorAll('.interactive-stat, .amenity, .contact-method, .social-link').forEach(el => {
            el.addEventListener('mouseenter', () => {
                el.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            });
            
            el.addEventListener('mouseleave', () => {
                el.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
            });
        });
    }
    
    initPerformanceMonitoring() {
        // Track gallery interactions
        const galleryGrid = document.getElementById('galleryGrid');
        if (galleryGrid) {
            galleryGrid.addEventListener('click', () => {
                if (typeof gtag !== 'undefined') {
                    gtag('event', 'gallery_interaction', {
                        event_category: 'Engagement',
                        event_label: 'Gallery Click'
                    });
                }
            });
        }
        
        // Log page load performance
        if ('performance' in window) {
            window.addEventListener('load', () => {
                const timing = performance.timing;
                const loadTime = timing.loadEventEnd - timing.navigationStart;
                console.log(`School page loaded in ${loadTime}ms`);
            });
        }
    }
}

// Initialize school page
document.addEventListener('DOMContentLoaded', () => {
    window.schoolPage = new SchoolPage();
});
