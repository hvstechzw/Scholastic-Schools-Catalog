// Optimized Main JavaScript
document.documentElement.setAttribute('data-theme','light');
document.documentElement.style.colorScheme='light';
document.body.style.colorScheme='light';

// Mobile Menu
const mobileMenuBtn=document.getElementById('mobileMenuBtn');
const navLinks=document.getElementById('navLinks');
if(mobileMenuBtn&&navLinks){
    mobileMenuBtn.addEventListener('click',function(e){
        e.preventDefault();e.stopPropagation();
        navLinks.classList.toggle('active');
        this.innerHTML=navLinks.classList.contains('active')?'<i class="fas fa-times"></i>':'<i class="fas fa-bars"></i>';
    });
    document.addEventListener('click',function(e){
        if(!navLinks.contains(e.target)&&!mobileMenuBtn.contains(e.target)){
            navLinks.classList.remove('active');
            mobileMenuBtn.innerHTML='<i class="fas fa-bars"></i>';
        }
    });
}

// Search and Filter
function initSearchFilter(){
    const searchInput=document.getElementById('searchInput');
    const schoolCards=document.querySelectorAll('.featured-card');
    const schoolsCount=document.getElementById('schoolsCount');
    
    if(!searchInput||!schoolCards.length)return;
    
    let searchTimeout;
    searchInput.addEventListener('input',function(){
        clearTimeout(searchTimeout);
        searchTimeout=setTimeout(filterSchools,300);
    });
    
    function filterSchools(){
        const searchTerm=searchInput.value.toLowerCase().trim();
        let visibleCount=0;
        
        schoolCards.forEach(card=>{
            const searchData=card.getAttribute('data-search');
            const matchesSearch=searchTerm===''||searchData.includes(searchTerm);
            
            if(matchesSearch){
                card.style.display='block';
                visibleCount++;
            }else{
                card.style.display='none';
            }
        });
        
        if(schoolsCount){
            schoolsCount.textContent=`Showing ${visibleCount} schools`;
        }
    }
}

// Smooth Scroll
document.querySelectorAll('a[href^="#"]').forEach(anchor=>{
    anchor.addEventListener('click',function(e){
        if(this.getAttribute('href')==='#')return;
        e.preventDefault();
        const target=document.querySelector(this.getAttribute('href'));
        if(target){
            target.scrollIntoView({behavior:'smooth',block:'start'});
        }
    });
});

// Initialize on DOM ready
document.addEventListener('DOMContentLoaded',function(){
    initSearchFilter();
    // Theme lock
    setInterval(()=>{
        if(document.documentElement.getAttribute('data-theme')!=='light'){
            document.documentElement.setAttribute('data-theme','light');
        }
    },1000);
});
