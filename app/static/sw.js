
self.addEventListener('install', function(e) {
 e.waitUntil(
   caches.open('catpage').then(function(cache) {
     return cache.addAll([
       '/',
       '/static/funny-pictures-cat-sound-studio.jpg'
     ]);
   })
 );
});

self.addEventListener('fetch', function(e) {
  console.log(e.request.url);
  e.respondWith(
    caches.match(e.request).then(function(response) {
      return response || fetch(e.request);
    })
  );
});
