// School Page JavaScript
document.documentElement.setAttribute('data-theme','light');
document.documentElement.style.colorScheme='light';
document.body.style.colorScheme='light';

// Gallery Lightbox
let currentImageIndex=0;
const galleryImages=[];
const lightbox=document.getElementById('lightbox');
const lightboxImage=document.getElementById('lightboxImage');
const lightboxClose=document.getElementById('lightboxClose');
const lightboxPrev=document.getElementById('lightboxPrev');
const lightboxNext=document.getElementById('lightboxNext');

function initGallery(){
    const galleryItems=document.querySelectorAll('.gallery-item');
    galleryItems.forEach((item,index)=>{
        const img=item.querySelector('img');
        if(img){
            galleryImages.push({
                src:img.src,
                filename:item.getAttribute('data-filename'),
                date:item.getAttribute('data-date'),
                size:item.getAttribute('data-size')
            });
            item.addEventListener('click',()=>openLightbox(index));
        }
    });
}

function openLightbox(index){
    if(galleryImages.length===0)return;
    currentImageIndex=index;
    updateLightbox();
    lightbox.classList.add('active');
    document.body.style.overflow='hidden';
}

function updateLightbox(){
    const image=galleryImages[currentImageIndex];
    lightboxImage.src=image.src;
}

function closeLightbox(){
    lightbox.classList.remove('active');
    document.body.style.overflow='';
}

function showNextImage(){
    if(galleryImages.length===0)return;
    currentImageIndex=(currentImageIndex+1)%galleryImages.length;
    updateLightbox();
}

function showPrevImage(){
    if(galleryImages.length===0)return;
    currentImageIndex=(currentImageIndex-1+galleryImages.length)%galleryImages.length;
    updateLightbox();
}

// Event listeners
if(lightboxClose)lightboxClose.addEventListener('click',closeLightbox);
if(lightboxNext)lightboxNext.addEventListener('click',showNextImage);
if(lightboxPrev)lightboxPrev.addEventListener('click',showPrevImage);

document.addEventListener('keydown',function(e){
    if(!lightbox||!lightbox.classList.contains('active'))return;
    switch(e.key){
        case'Escape':closeLightbox();break;
        case'ArrowRight':showNextImage();break;
        case'ArrowLeft':showPrevImage();break;
    }
});

if(lightbox)lightbox.addEventListener('click',function(e){
    if(e.target===lightbox)closeLightbox();
});

// Initialize
document.addEventListener('DOMContentLoaded',function(){
    initGallery();
    // Theme lock
    setInterval(()=>{
        if(document.documentElement.getAttribute('data-theme')!=='light'){
            document.documentElement.setAttribute('data-theme','light');
        }
    },1000);
});
