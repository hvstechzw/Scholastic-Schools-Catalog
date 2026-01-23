// Directory page JavaScript - Optimized for filtering and pagination

class DirectoryPage {
    constructor() {
        this.schoolCards = [];
        this.filteredSchools = [];
        this.currentPage = 1;
        this.schoolsPerPage = 12;
        this.sortBy = 'name';
        this.filters = {
            search: '',
            location: 'all',
            level: 'all',
            type: 'all',
            rating: '0'
        };
        this.init();
    }
    
    init() {
        this.cacheElements();
        this.initSchools();
        this.initFilters();
        this.initSorting();
        this.initPagination();
        this.initLazyLoading();
        this.initPerformanceOptimizations();
    }
    
    cacheElements() {
        this.elements = {
            searchInput: document.getElementById('allSearchInput'),
            locationFilter: document.getElementById('locationFilter'),
            levelFilter: document.getElementById('levelFilter'),
            typeFilter: document.getElementById('typeFilter'),
            ratingFilter: document.getElementById('ratingFilter'),
            sortSelect: document.getElementById('sortSelect'),
            resetFilters: document.getElementById('resetFilters'),
            schoolsGrid: document.getElementById('allSchoolsGrid'),
            gridTitle: document.getElementById('gridTitle'),
            pagination: document.getElementById('pagination'),
            skeletonGrid: document.getElementById('skeletonGrid')
        };
    }
    
    initSchools() {
        this.schoolCards = Array.from(this.elements.schoolsGrid.querySelectorAll('.school-card'));
        
        // Hide skeleton and show grid
        setTimeout(() => {
            if (this.elements.skeletonGrid) {
                this.elements.skeletonGrid.style.display = 'none';
            }
            if (this.elements.schoolsGrid) {
                this.elements.schoolsGrid.style.display = 'grid';
            }
            this.filterAndSortSchools();
        }, 800);
    }
    
    initFilters() {
        // Search input with debouncing
        if (this.elements.searchInput) {
            this.elements.searchInput.addEventListener('input', this.debounce(() => {
                this.filters.search = this.elements.searchInput.value.toLowerCase().trim();
                this.filterAndSortSchools();
            }, 300));
        }
        
        // Filter selectors
        ['locationFilter', 'levelFilter', 'typeFilter', 'ratingFilter'].forEach(filterId => {
            const filter = this.elements[filterId];
            if (filter) {
                filter.addEventListener('change', () => {
                    this.filters[filterId.replace('Filter', '').toLowerCase()] = filter.value;
                    this.filterAndSortSchools();
                });
            }
        });
        
        // Reset filters
        if (this.elements.resetFilters) {
            this.elements.resetFilters.addEventListener('click', () => this.resetAllFilters());
        }
    }
    
    initSorting() {
        if (this.elements.sortSelect) {
            this.elements.sortSelect.addEventListener('change', () => {
                this.sortBy = this.elements.sortSelect.value;
                this.filterAndSortSchools();
            });
        }
    }
    
    initPagination() {
        this.updatePagination();
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
                rootMargin: '50px 0px'
            });
            
            lazyImages.forEach(img => imageObserver.observe(img));
        } else {
            lazyImages.forEach(img => img.classList.add('loaded'));
        }
    }
    
    initPerformanceOptimizations() {
        // Use requestIdleCallback for non-critical work
        if ('requestIdleCallback' in window) {
            requestIdleCallback(() => {
                this.preloadNextPage();
            });
        }
        
        // Cache filter results for better performance
        this.filterCache = new Map();
    }
    
    filterAndSortSchools() {
        const cacheKey = JSON.stringify({ ...this.filters, sortBy: this.sortBy });
        
        // Check cache first
        if (this.filterCache.has(cacheKey)) {
            this.filteredSchools = this.filterCache.get(cacheKey);
        } else {
            this.filteredSchools = this.schoolCards.filter(card => {
                const name = card.getAttribute('data-name');
                const location = card.getAttribute('data-location');
                const level = card.getAttribute('data-level');
                const type = card.getAttribute('data-type');
                const rating = parseFloat(card.getAttribute('data-rating'));
                const searchData = card.getAttribute('data-search');
                
                const matchesSearch = !this.filters.search || searchData.includes(this.filters.search);
                const matchesLocation = this.filters.location === 'all' || location.includes(this.filters.location);
                const matchesLevel = this.filters.level === 'all' || level === this.filters.level;
                const matchesType = this.filters.type === 'all' || type === this.filters.type;
                const matchesRating = this.filters.rating === '0' || rating >= parseFloat(this.filters.rating);
                
                return matchesSearch && matchesLocation && matchesLevel && matchesType && matchesRating;
            });
            
            // Sort schools
            this.sortSchools();
            
            // Cache results
            this.filterCache.set(cacheKey, [...this.filteredSchools]);
            
            // Limit cache size
            if (this.filterCache.size > 10) {
                const firstKey = this.filterCache.keys().next().value;
                this.filterCache.delete(firstKey);
            }
        }
        
        this.currentPage = 1;
        this.updateDisplay();
        this.updatePagination();
    }
    
    sortSchools() {
        this.filteredSchools.sort((a, b) => {
            switch(this.sortBy) {
                case 'name':
                    return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
                case 'name-desc':
                    return b.getAttribute('data-name').localeCompare(a.getAttribute('data-name'));
                case 'rating':
                    return parseFloat(b.getAttribute('data-rating')) - parseFloat(a.getAttribute('data-rating'));
                case 'students':
                    return parseInt(b.getAttribute('data-students')) - parseInt(a.getAttribute('data-students'));
                case 'established':
                    return parseInt(b.getAttribute('data-established')) - parseInt(a.getAttribute('data-established'));
                case 'established-desc':
                    return parseInt(a.getAttribute('data-established')) - parseInt(b.getAttribute('data-established'));
                default:
                    return 0;
            }
        });
    }
    
    updateDisplay() {
        const startIndex = (this.currentPage - 1) * this.schoolsPerPage;
        const endIndex = startIndex + this.schoolsPerPage;
        const schoolsToShow = this.filteredSchools.slice(startIndex, endIndex);
        
        // Hide all schools
        this.schoolCards.forEach(card => {
            card.style.display = 'none';
            card.classList.remove('fade-in-up');
        });
        
        // Show filtered schools with animation
        schoolsToShow.forEach((card, index) => {
            card.style.display = 'block';
            card.style.animationDelay = `${index * 0.05}s`;
            card.classList.add('fade-in-up');
        });
        
        // Update title
        if (this.elements.gridTitle) {
            this.elements.gridTitle.textContent = `Educational Institutions (${this.filteredSchools.length} Found)`;
        }
        
        // Show/hide no results message
        this.showNoResultsMessage();
    }
    
    showNoResultsMessage() {
        const noResults = document.getElementById('noResults');
        
        if (this.filteredSchools.length === 0) {
            if (!noResults) {
                const noResultsDiv = document.createElement('div');
                noResultsDiv.id = 'noResults';
                noResultsDiv.className = 'no-results';
                noResultsDiv.innerHTML = `
                    <div class="no-results-icon">
                        <i class="fas fa-search"></i>
                    </div>
                    <h3 style="margin-bottom: 1rem; color: var(--dark); font-weight: 700;">No Schools Found</h3>
                    <p style="color: var(--gray-dark); margin-bottom: 1.5rem; font-size: 1.1rem;">
                        Try adjusting your search or filter criteria to find what you're looking for.
                    </p>
                    <button class="reset-btn ripple" onclick="directoryPage.resetAllFilters()" style="margin-top: 1rem;">
                        <i class="fas fa-redo"></i> Reset All Filters
                    </button>
                `;
                this.elements.schoolsGrid.parentNode.appendChild(noResultsDiv);
            }
        } else if (noResults) {
            noResults.remove();
        }
    }
    
    updatePagination() {
        const totalPages = Math.ceil(this.filteredSchools.length / this.schoolsPerPage);
        
        if (totalPages <= 1) {
            this.elements.pagination.innerHTML = '';
            return;
        }
        
        let paginationHTML = '';
        
        // Previous button
        paginationHTML += `
            <a href="#" class="page-btn ${this.currentPage === 1 ? 'disabled' : ''}" 
               onclick="directoryPage.changePage(${this.currentPage - 1}); return false;">
                <i class="fas fa-chevron-left"></i>
            </a>
        `;
        
        // Page numbers
        const maxVisiblePages = 5;
        let startPage = Math.max(1, this.currentPage - Math.floor(maxVisiblePages / 2));
        let endPage = Math.min(totalPages, startPage + maxVisiblePages - 1);
        
        if (endPage - startPage + 1 < maxVisiblePages) {
            startPage = Math.max(1, endPage - maxVisiblePages + 1);
        }
        
        for (let i = startPage; i <= endPage; i++) {
            paginationHTML += `
                <a href="#" class="page-btn ${i === this.currentPage ? 'active' : ''}" 
                   onclick="directoryPage.changePage(${i}); return false;">
                    ${i}
                </a>
            `;
        }
        
        // Next button
        paginationHTML += `
            <a href="#" class="page-btn ${this.currentPage === totalPages ? 'disabled' : ''}" 
               onclick="directoryPage.changePage(${this.currentPage + 1}); return false;">
                <i class="fas fa-chevron-right"></i>
            </a>
        `;
        
        this.elements.pagination.innerHTML = paginationHTML;
    }
    
    changePage(page) {
        this.currentPage = page;
        this.updateDisplay();
        this.updatePagination();
        
        // Smooth scroll to grid
        if (this.elements.schoolsGrid) {
            this.elements.schoolsGrid.scrollIntoView({
                behavior: 'smooth',
                block: 'start'
            });
        }
    }
    
    resetAllFilters() {
        // Reset filter values
        this.filters = {
            search: '',
            location: 'all',
            level: 'all',
            type: 'all',
            rating: '0'
        };
        
        // Reset UI elements
        if (this.elements.searchInput) this.elements.searchInput.value = '';
        if (this.elements.locationFilter) this.elements.locationFilter.value = 'all';
        if (this.elements.levelFilter) this.elements.levelFilter.value = 'all';
        if (this.elements.typeFilter) this.elements.typeFilter.value = 'all';
        if (this.elements.ratingFilter) this.elements.ratingFilter.value = '0';
        if (this.elements.sortSelect) this.elements.sortSelect.value = 'name';
        
        this.sortBy = 'name';
        this.currentPage = 1;
        
        // Apply filters
        this.filterAndSortSchools();
        
        // Add reset animation
        if (this.elements.resetFilters) {
            this.elements.resetFilters.style.transform = 'scale(0.9)';
            setTimeout(() => {
                this.elements.resetFilters.style.transform = '';
            }, 300);
        }
    }
    
    preloadNextPage() {
        const nextPageStart = this.currentPage * this.schoolsPerPage;
        const nextPageEnd = nextPageStart + this.schoolsPerPage;
        const nextPageSchools = this.filteredSchools.slice(nextPageStart, nextPageEnd);
        
        // Preload images for next page
        nextPageSchools.forEach(card => {
            const img = card.querySelector('img');
            if (img && img.classList.contains('lazy-image')) {
                const tempImg = new Image();
                tempImg.src = img.src;
            }
        });
    }
    
    debounce(func, wait) {
        let timeout;
        return (...args) => {
            clearTimeout(timeout);
            timeout = setTimeout(() => func.apply(this, args), wait);
        };
    }
}

// Initialize directory page
document.addEventListener('DOMContentLoaded', () => {
    window.directoryPage = new DirectoryPage();
    
    // Add keyboard shortcuts
    document.addEventListener('keydown', (e) => {
        // Focus search on /
        if (e.key === '/' && e.target.tagName !== 'INPUT') {
            e.preventDefault();
            const searchInput = document.getElementById('allSearchInput');
            if (searchInput) searchInput.focus();
        }
        
        // Escape to clear search
        if (e.key === 'Escape' && document.activeElement.tagName === 'INPUT') {
            document.activeElement.value = '';
            window.directoryPage.filterAndSortSchools();
        }
    });
});

// Export for global access
window.changePage = (page) => {
    if (window.directoryPage) {
        window.directoryPage.changePage(page);
    }
};

window.resetAllFilters = () => {
    if (window.directoryPage) {
        window.directoryPage.resetAllFilters();
    }
};
