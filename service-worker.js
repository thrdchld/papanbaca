const CACHE_NAME = 'papanbaca-v1';
const ASSETS = [
  './',
  './index.html',
  './manifest.json',
  './main.js',
  './package.json',
  './README.md'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then(cache => cache.addAll(ASSETS))
  );
});

self.addEventListener('fetch', (e) => {
  // Cache-first for navigation and local assets, network fallback
  e.respondWith(
    caches.match(e.request).then(cached => {
      if (cached) return cached;
      return fetch(e.request).then(resp => {
        // Put a copy in cache for future offline use
        if (e.request.method === 'GET' && resp && resp.status === 200 && resp.type !== 'opaque') {
          const respClone = resp.clone();
          caches.open(CACHE_NAME).then(cache => cache.put(e.request, respClone));
        }
        return resp;
      }).catch(()=>{
        // fallback to index.html for navigation requests
        if (e.request.mode === 'navigate') return caches.match('./index.html');
      });
    })
  );
});

self.addEventListener('activate', (e) => {
  e.waitUntil(
    caches.keys().then(keys => Promise.all(
      keys.map(k => { if (k !== CACHE_NAME) return caches.delete(k); })
    ))
  );
  self.clients.claim();
});
