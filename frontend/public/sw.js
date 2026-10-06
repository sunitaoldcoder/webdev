// Cache the public application shell only. Farmer records and /api are never cached.
const CACHE='agri-shell-v2';
self.addEventListener('install',e=>e.waitUntil((async()=>{
 const cache=await caches.open(CACHE);
 const response=await fetch('/');
 if(!response.ok)throw new Error('Cannot cache application shell');
 const html=await response.clone().text();
 await cache.put('/',response);
 const assets=[...html.matchAll(/(?:src|href)="(\/assets\/[^" ]+)"/g)].map(m=>m[1]);
 await cache.addAll(['/icon.svg','/icon-192.png','/icon-512.png','/manifest.webmanifest',...assets]);
})()));
self.addEventListener('activate',e=>e.waitUntil(caches.keys().then(keys=>Promise.all(keys.filter(k=>k!==CACHE).map(k=>caches.delete(k))))));
self.addEventListener('fetch',e=>{
 const url=new URL(e.request.url);
 if(e.request.method!=='GET'||url.origin!==self.location.origin||url.pathname.startsWith('/api')||url.pathname.startsWith('/admin'))return;
 e.respondWith(fetch(e.request).catch(async()=>{
  const response=await caches.match(e.request);
  return response||(e.request.mode==='navigate'?await caches.match('/'):Response.error());
 }));
});
