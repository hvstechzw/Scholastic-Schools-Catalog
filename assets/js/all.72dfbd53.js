// All Schools Page JavaScript
document.documentElement.setAttribute('data-theme','light');
document.documentElement.style.colorScheme='light';
document.body.style.colorScheme='light';

// Filter and Search
let currentPage=1;
let filteredSchools=[];
const schoolsPerPage=12;

function initAllSchoolsFilter(){
    const allSchoolCards=Array.from(document.querySelectorAll('#allSchoolsGrid .school-card'));
    const allSearchInput=document.getElementById('allSearchInput');
    const locationFilter=document.getElementById('locationFilter');
    const levelFilter=document.getElementById('levelFilter');
    const typeFilter=document.getElementById('typeFilter');
    const ratingFilter=document.getElementById('ratingFilter');
    const sortSelect=document.getElementById('sortSelect');
    const resetFilters=document.getElementById('resetFilters');
    
    if(!allSchoolCards.length)return;
    
    filteredSchools=allSchoolCards;
    
    let filterTimeout;
    function scheduleFilter(){
        clearTimeout(filterTimeout);
        filterTimeout=setTimeout(filterAndSortSchools,300);
    }
    
    function filterAndSortSchools(){
        const searchTerm=allSearchInput.value.toLowerCase().trim();
        const locationValue=locationFilter.value.toLowerCase();
        const levelValue=levelFilter.value.toLowerCase();
        const typeValue=typeFilter.value.toLowerCase();
        const minRating=parseFloat(ratingFilter.value);
        const sortBy=sortSelect.value;
        
        filteredSchools=allSchoolCards.filter(card=>{
            const location=card.getAttribute('data-location');
            const level=card.getAttribute('data-level');
            const type=card.getAttribute('data-type');
            const rating=parseFloat(card.getAttribute('data-rating'));
            const searchData=card.getAttribute('data-search');
            
            const matchesSearch=searchTerm===''||searchData.includes(searchTerm);
            const matchesLocation=locationValue==='all'||location.includes(locationValue);
            const matchesLevel=levelValue==='all'||level===levelValue;
            const matchesType=typeValue==='all'||type===typeValue;
            const matchesRating=minRating===0||rating>=minRating;
            
            return matchesSearch&&matchesLocation&&matchesLevel&&matchesType&&matchesRating;
        });
        
        // Sort
        filteredSchools.sort((a,b)=>{
            switch(sortBy){
                case'name':return a.getAttribute('data-name').localeCompare(b.getAttribute('data-name'));
                case'name-desc':return b.getAttribute('data-name').localeCompare(a.getAttribute('data-name'));
                case'rating':return parseFloat(b.getAttribute('data-rating'))-parseFloat(a.getAttribute('data-rating'));
                default:return 0;
            }
        });
        
        updateDisplay();
        updatePagination();
    }
    
    function updateDisplay(){
        const startIndex=(currentPage-1)*schoolsPerPage;
        const endIndex=startIndex+schoolsPerPage;
        const schoolsToShow=filteredSchools.slice(startIndex,endIndex);
        
        allSchoolCards.forEach(card=>card.style.display='none');
        schoolsToShow.forEach(card=>card.style.display='block');
        
        const gridTitle=document.querySelector('.grid-title');
        if(gridTitle)gridTitle.textContent=`Educational Institutions (${filteredSchools.length} Found)`;
        
        const noResults=document.getElementById('noResults');
        if(filteredSchools.length===0){
            if(!noResults){
                const noResultsDiv=document.createElement('div');
                noResultsDiv.id='noResults';
                noResultsDiv.className='no-results';
                noResultsDiv.innerHTML=`
                    <div class="no-results-icon"><i class="fas fa-search"></i></div>
                    <h3>No Schools Found</h3>
                    <p>Try adjusting your search or filter criteria.</p>
                    <button class="reset-btn" onclick="resetAllFilters()"><i class="fas fa-redo"></i> Reset All Filters</button>
                `;
                document.querySelector('.schools-grid-container').appendChild(noResultsDiv);
            }
        }else if(noResults){
            noResults.remove();
        }
    }
    
    function updatePagination(){
        const totalPages=Math.ceil(filteredSchools.length/schoolsPerPage);
        const pagination=document.getElementById('pagination');
        
        if(totalPages<=1){
            pagination.innerHTML='';
            return;
        }
        
        let paginationHTML='';
        paginationHTML+=`<a href="#" class="page-btn ${currentPage===1?'disabled':''}" onclick="changePage(${currentPage-1});return false;"><i class="fas fa-chevron-left"></i></a>`;
        
        for(let i=1;i<=totalPages&&i<=5;i++){
            paginationHTML+=`<a href="#" class="page-btn ${i===currentPage?'active':''}" onclick="changePage(${i});return false;">${i}</a>`;
        }
        
        paginationHTML+=`<a href="#" class="page-btn ${currentPage===totalPages?'disabled':''}" onclick="changePage(${currentPage+1});return false;"><i class="fas fa-chevron-right"></i></a>`;
        pagination.innerHTML=paginationHTML;
    }
    
    function changePage(page){
        if(page<1||page>Math.ceil(filteredSchools.length/schoolsPerPage))return;
        currentPage=page;
        updateDisplay();
        window.scrollTo({top:document.querySelector('.schools-grid').offsetTop-100,behavior:'smooth'});
    }
    
    function resetAllFilters(){
        allSearchInput.value='';
        locationFilter.value='all';
        levelFilter.value='all';
        typeFilter.value='all';
        ratingFilter.value='0';
        sortSelect.value='name';
        currentPage=1;
        filterAndSortSchools();
    }
    
    // Event listeners
    allSearchInput.addEventListener('input',scheduleFilter);
    locationFilter.addEventListener('change',scheduleFilter);
    levelFilter.addEventListener('change',scheduleFilter);
    typeFilter.addEventListener('change',scheduleFilter);
    ratingFilter.addEventListener('change',scheduleFilter);
    sortSelect.addEventListener('change',scheduleFilter);
    resetFilters.addEventListener('click',resetAllFilters);
    
    // Expose functions
    window.changePage=changePage;
    window.resetAllFilters=resetAllFilters;
    
    // Initial filter
    filterAndSortSchools();
}

// Initialize
document.addEventListener('DOMContentLoaded',function(){
    initAllSchoolsFilter();
    // Theme lock
    setInterval(()=>{
        if(document.documentElement.getAttribute('data-theme')!=='light'){
            document.documentElement.setAttribute('data-theme','light');
        }
    },1000);
});
