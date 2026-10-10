# _src/src.html に FX・プリント画面を うめこんで index.html と sw.js を つくる
import io, os, hashlib
here = os.path.dirname(os.path.abspath(__file__))
rd = lambda n: io.open(os.path.join(here, n), encoding='utf-8').read()
src = rd('src.html')
for mark, f in [('/*FX_HERE*/', 'fx.js'), ('/*PRINTUI_JS*/', 'printui.js'), ('/*PRINTUI_CSS*/', 'printui.css')]:
    assert mark in src, mark
    src = src.replace(mark, rd(f).strip())
out = os.path.join(here, '..')
io.open(os.path.join(out, 'index.html'), 'w', encoding='utf-8', newline='\n').write(src)
ver = hashlib.md5(src.encode('utf-8')).hexdigest()[:10]
sw = """// オフラインでも つかえるように（しゃしんなどの データは この たんまつの IndexedDB に あり、ここでは あつかわない）
const CACHE = 'mitoshi-%s';
self.addEventListener('install', e => { e.waitUntil(caches.open(CACHE).then(c => c.addAll(['./', 'index.html'])).then(() => self.skipWaiting())); });
self.addEventListener('activate', e => { e.waitUntil(caches.keys().then(ks => Promise.all(ks.filter(k => k.startsWith('mitoshi-') && k !== CACHE).map(k => caches.delete(k)))).then(() => self.clients.claim())); });
self.addEventListener('fetch', e => { const r = e.request; if (r.method !== 'GET' || new URL(r.url).origin !== location.origin) return; e.respondWith(fetch(r).then(res => { const c = res.clone(); caches.open(CACHE).then(k => k.put(r, c)); return res; }).catch(() => caches.match(r, { ignoreSearch: true }).then(x => x || caches.match('index.html')))); });
""" % ver
io.open(os.path.join(out, 'sw.js'), 'w', encoding='utf-8', newline='\n').write(sw)
print('built', len(src), ver)
