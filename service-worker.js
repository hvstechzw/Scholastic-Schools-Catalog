// Service Worker for Scholastic Forum
const CACHE_NAME = 'scholastic-forum-v1';
const urlsToCache = [
    '/',
    '/index.html',
    '/assets/style.css',
    '/assets/main.js',
    '/assets/images/logo_light.png',
    '/schools/all.html'
];

self.addEventListener('install', event => {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(cache => cache.addAll(urlsToCache))
    );
});

self.addEventListener('fetch', event => {
    event.respondWith(
        caches.match(event.request)
            .then(response => response || fetch(event.request))
    );
});