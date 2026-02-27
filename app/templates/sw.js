
self.addEventListener('install', function(e) {
 e.waitUntil(
   caches.open('catpage').then(function(cache) {
     return cache.addAll([
       '/',
       '/static/funny-pictures-cat-sound-studio.jpg',
       '/static/fjalla-one-latin-400.woff2',
       '/static/background.svg',
       '/static/icon.svg',
       '/static/icon-192.png',
       '/static/icon-512.png',
       '/static/apple-touch-icon.png',
       '/static/favicon.png',
     ]);
   })
 );
});

self.addEventListener('fetch', function(e) {
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});
