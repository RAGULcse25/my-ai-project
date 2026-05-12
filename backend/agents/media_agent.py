# agents/media_agent.py — INDIA EDITION
# ============================================================
# APIs that WORK in India (no VPN needed):
#
#  OMDb API       → omdbapi.com         FREE 1000/day
#  RapidAPI IMDb  → rapidapi.com        FREE 500/month  
#  Unsplash       → unsplash.com        FREE 50/hr
#  YouTube v3     → console.cloud.google FREE 10K/day
#  JioSaavn       → saavn.com API       FREE (music)
#  News API       → newsapi.org         FREE 100/day
# ============================================================

import os
from dotenv import load_dotenv
load_dotenv()

OMDB_KEY     = os.getenv("OMDB_API_KEY","")
YOUTUBE_KEY  = os.getenv("YOUTUBE_API_KEY","")
UNSPLASH_KEY = os.getenv("UNSPLASH_API_KEY","")
NEWS_KEY     = os.getenv("NEWS_API_KEY","")


# ─────────────────────────────────────────────────────────────
# MOVIE APP — OMDb API (India-friendly, FREE)
# Get key: omdbapi.com → $0 plan → 1000 requests/day FREE
# ─────────────────────────────────────────────────────────────
def generate_movie_app(answers: dict) -> str:
    theme    = answers.get("q3","Dark")
    features = answers.get("q1","")

    if OMDB_KEY:
        api_js = f"""
// OMDb API — Works perfectly in India!
// Free: 1000 requests/day at omdbapi.com
const OMDB_KEY  = '{OMDB_KEY}';
const OMDB_BASE = 'https://www.omdbapi.com/';

async function searchMovies(query) {{
  const r = await fetch(`${{OMDB_BASE}}?s=${{encodeURIComponent(query)}}&type=movie&apikey=${{OMDB_KEY}}`);
  const d = await r.json();
  return d.Search || [];
}}

async function getMovieDetails(imdbId) {{
  const r = await fetch(`${{OMDB_BASE}}?i=${{imdbId}}&plot=full&apikey=${{OMDB_KEY}}`);
  return r.json();
}}

async function getTrending() {{
  // OMDb doesn't have a trending endpoint, so we search popular titles
  const POPULAR = ['Avengers','Spider-Man','Batman','Fast Furious','Mission Impossible',
                   'Interstellar','Inception','RRR','KGF','Pathaan'];
  const query = POPULAR[Math.floor(Math.random()*POPULAR.length)];
  return searchMovies(query);
}}

async function searchByYear(year) {{
  return searchMovies(`popular ${{year}}`);
}}

function posterUrl(item) {{
  if(item.Poster && item.Poster !== 'N/A') return item.Poster;
  return `https://picsum.photos/seed/${{item.imdbID||Math.random()}}/300/450`;
}}
"""
        load_section = """
async function loadHome() {
  showLoader();
  // Load multiple categories in parallel
  const [action, bollywood, recent] = await Promise.all([
    searchMovies('action 2023'),
    searchMovies('India 2023'),
    searchMovies('adventure 2024'),
  ]);
  renderSection('trendingRow',  action.slice(0,10));
  renderSection('bollywoodRow', bollywood.slice(0,10));
  renderSection('recentRow',    recent.slice(0,10));
  hideLoader();
}
"""
    else:
        api_js = """
// OMDb Demo Mode — get FREE key at omdbapi.com (works in India!)
// Sign up → Email verification → Get API key instantly
const MOCK_MOVIES = [
  {Title:'RRR',Year:'2022',imdbRating:'7.9',Genre:'Action,Drama',Poster:'https://picsum.photos/seed/rrr/300/450',imdbID:'tt8178634',Plot:'A fictional story about two legendary revolutionaries.'},
  {Title:'KGF: Chapter 2',Year:'2022',imdbRating:'8.2',Genre:'Action,Drama',Poster:'https://picsum.photos/seed/kgf2/300/450',imdbID:'tt10698556',Plot:'Rocky faces the might of Adheera.'},
  {Title:'Pathaan',Year:'2023',imdbRating:'5.8',Genre:'Action,Thriller',Poster:'https://picsum.photos/seed/pathaan/300/450',imdbID:'tt14708912',Plot:'An Indian spy takes on the leader of a rogue mercenary organization.'},
  {Title:'Jawan',Year:'2023',imdbRating:'6.9',Genre:'Action,Crime',Poster:'https://picsum.photos/seed/jawan/300/450',imdbID:'tt15724962',Plot:'A man is compelled to fight injustice.'},
  {Title:'Animal',Year:'2023',imdbRating:'7.0',Genre:'Action,Crime',Poster:'https://picsum.photos/seed/animal/300/450',imdbID:'tt13751694',Plot:'The hardened son of a business tycoon sets out to settle scores.'},
  {Title:'Leo',Year:'2023',imdbRating:'7.1',Genre:'Action,Thriller',Poster:'https://picsum.photos/seed/leo2023/300/450',imdbID:'tt14697586',Plot:'A mild-mannered man is forced out of his peaceful existence.'},
  {Title:'Oppenheimer',Year:'2023',imdbRating:'8.4',Genre:'Biography,Drama',Poster:'https://picsum.photos/seed/opp23/300/450',imdbID:'tt15398776',Plot:'The story of American scientist J. Robert Oppenheimer.'},
  {Title:'Spider-Man: Across the Spider-Verse',Year:'2023',imdbRating:'8.6',Genre:'Animation,Action',Poster:'https://picsum.photos/seed/spidey23/300/450',imdbID:'tt9362722',Plot:'Miles Morales catapults across the Multiverse.'},
  {Title:'Dune: Part Two',Year:'2024',imdbRating:'8.5',Genre:'Action,Adventure,Drama',Poster:'https://picsum.photos/seed/dune2/300/450',imdbID:'tt15239678',Plot:'Paul Atreides unites with the Fremen.'},
  {Title:'Interstellar',Year:'2014',imdbRating:'8.7',Genre:'Adventure,Drama,Sci-Fi',Poster:'https://picsum.photos/seed/inter/300/450',imdbID:'tt0816692',Plot:'Explorers travel through a wormhole in space.'},
  {Title:'Inception',Year:'2010',imdbRating:'8.8',Genre:'Action,Adventure,Sci-Fi',Poster:'https://picsum.photos/seed/incep/300/450',imdbID:'tt1375666',Plot:'A thief who steals corporate secrets through dreams.'},
  {Title:'3 Idiots',Year:'2009',imdbRating:'8.4',Genre:'Comedy,Drama',Poster:'https://picsum.photos/seed/3idiots/300/450',imdbID:'tt1187043',Plot:'Two friends search for their missing companion.'},
];

function posterUrl(item) {{
  return (item.Poster && item.Poster!=='N/A') ? item.Poster
    : `https://picsum.photos/seed/${{item.imdbID||'m'}}/300/450`;
}}
async function searchMovies(q) {{
  return MOCK_MOVIES.filter(m =>
    m.Title.toLowerCase().includes(q.toLowerCase()) ||
    m.Genre.toLowerCase().includes(q.toLowerCase())
  );
}}
async function getMovieDetails(id) {{
  return MOCK_MOVIES.find(m=>m.imdbID===id) || MOCK_MOVIES[0];
}}
async function getTrending() {{ return MOCK_MOVIES; }}
"""
        load_section = """
async function loadHome() {
  showLoader();
  await new Promise(r=>setTimeout(r,400));
  const all = MOCK_MOVIES;
  const bollywood = all.filter(m=>['RRR','KGF: Chapter 2','Pathaan','Jawan','Animal','Leo','3 Idiots'].includes(m.Title));
  const hollywood = all.filter(m=>['Oppenheimer','Dune: Part Two','Interstellar','Inception','Spider-Man: Across the Spider-Verse'].includes(m.Title));
  renderSection('trendingRow',  all.slice(0,8));
  renderSection('bollywoodRow', bollywood);
  renderSection('recentRow',    hollywood);
  hideLoader();
}
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>MovieHub India</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;900&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
:root{{
  --bg:#0f0f0f;--surface:#1a1a1a;--card:#252525;
  --text:#fff;--sub:#aaa;--accent:#e50914;
  --gold:#ffd700;--border:#333;
}}
html,body{{height:100%;background:var(--bg);color:var(--text);font-family:Inter,sans-serif;overflow-x:hidden}}
::-webkit-scrollbar{{width:5px;height:5px}}
::-webkit-scrollbar-thumb{{background:#444;border-radius:3px}}

/* NAV */
nav{{position:sticky;top:0;z-index:100;background:rgba(15,15,15,0.95);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--border);
  padding:0 28px;height:60px;display:flex;align-items:center;gap:20px}}
.logo{{font-size:22px;font-weight:900;color:var(--accent);letter-spacing:-1px;cursor:pointer;
  display:flex;align-items:center;gap:6px}}
.logo span{{color:#fff}}
.nav-links{{display:flex;gap:20px;margin-left:16px}}
.nav-links a{{color:#ccc;font-size:13px;cursor:pointer;transition:color .2s;text-decoration:none}}
.nav-links a:hover{{color:#fff}}
.search-row{{margin-left:auto;display:flex;gap:8px;align-items:center}}
.search-row input{{padding:8px 16px;background:rgba(255,255,255,0.08);border:1px solid var(--border);
  border-radius:22px;color:#fff;font-size:13px;outline:none;width:200px;transition:width .3s}}
.search-row input:focus{{width:280px;background:rgba(255,255,255,0.12)}}
.search-row input::placeholder{{color:#666}}
.nav-icons{{display:flex;gap:14px;align-items:center;margin-left:16px}}
.nav-icons span{{cursor:pointer;font-size:18px;transition:transform .2s}}
.nav-icons span:hover{{transform:scale(1.15)}}
.avatar{{width:32px;height:32px;border-radius:50%;
  background:linear-gradient(135deg,#6366f1,#8b5cf6);
  display:flex;align-items:center;justify-content:center;
  font-size:12px;font-weight:700;cursor:pointer}}

/* HERO */
.hero{{height:440px;position:relative;overflow:hidden;margin-bottom:24px}}
.hero-bg{{position:absolute;inset:0;
  background:linear-gradient(135deg,#1a0a2e 0%,#0d1117 40%,#1a1a0a 100%)}}
.hero-particles{{position:absolute;inset:0;overflow:hidden}}
.hero-overlay{{position:absolute;inset:0;
  background:linear-gradient(to right,rgba(0,0,0,0.9) 35%,transparent 80%)}}
.hero-content{{position:absolute;bottom:0;left:0;right:0;padding:48px}}
.hero-badge{{display:inline-flex;align-items:center;gap:6px;
  background:var(--accent);padding:4px 12px;border-radius:20px;
  font-size:10px;font-weight:700;letter-spacing:2px;margin-bottom:14px}}
.hero-title{{font-size:44px;font-weight:900;line-height:1.05;margin-bottom:10px;
  max-width:500px;text-shadow:0 2px 20px rgba(0,0,0,0.8)}}
.hero-meta{{display:flex;gap:12px;align-items:center;margin-bottom:14px;font-size:13px;flex-wrap:wrap}}
.rating-badge{{background:var(--gold);color:#000;padding:2px 8px;
  border-radius:4px;font-weight:700;font-size:12px}}
.quality-badge{{background:#1a6fff;padding:2px 8px;border-radius:3px;
  font-size:10px;font-weight:600;letter-spacing:1px}}
.hero-desc{{font-size:13px;color:#ccc;line-height:1.7;margin-bottom:22px;
  max-width:480px;display:-webkit-box;-webkit-line-clamp:3;
  -webkit-box-orient:vertical;overflow:hidden}}
.hero-btns{{display:flex;gap:12px;flex-wrap:wrap}}
.btn-play{{padding:13px 30px;background:var(--accent);border:none;border-radius:6px;
  color:#fff;font-size:14px;font-weight:600;cursor:pointer;
  display:flex;align-items:center;gap:8px;transition:all .2s}}
.btn-play:hover{{background:#b20710;transform:translateY(-1px)}}
.btn-add{{padding:13px 30px;background:rgba(255,255,255,0.15);border:none;
  border-radius:6px;color:#fff;font-size:14px;cursor:pointer;
  backdrop-filter:blur(4px);transition:all .2s;border:1px solid rgba(255,255,255,0.2)}}
.btn-add:hover{{background:rgba(255,255,255,0.25)}}

/* CATEGORIES */
.categories{{display:flex;gap:8px;padding:0 28px 20px;overflow-x:auto}}
.categories::-webkit-scrollbar{{height:0}}
.cat-btn{{padding:7px 18px;border-radius:20px;border:1px solid var(--border);
  background:transparent;color:#ccc;font-size:12px;cursor:pointer;
  white-space:nowrap;transition:all .2s}}
.cat-btn:hover,.cat-btn.active{{background:#fff;color:#000;border-color:#fff}}

/* SECTIONS */
.section{{padding:0 28px 28px}}
.section-header{{display:flex;align-items:center;justify-content:space-between;margin-bottom:14px}}
.section-header h2{{font-size:17px;font-weight:600}}
.see-all{{font-size:12px;color:var(--accent);cursor:pointer}}
.row{{display:flex;gap:12px;overflow-x:auto;padding-bottom:6px}}
.row::-webkit-scrollbar{{height:3px}}

/* MOVIE CARD */
.card{{flex:0 0 155px;cursor:pointer;transition:transform .2s}}
.card:hover{{transform:translateY(-4px)}}
.card-img{{position:relative;width:155px;height:232px;border-radius:8px;overflow:hidden;background:var(--card)}}
.card-img img{{width:100%;height:100%;object-fit:cover;transition:transform .3s}}
.card:hover .card-img img{{transform:scale(1.06)}}
.card-overlay{{position:absolute;inset:0;background:linear-gradient(to top,rgba(0,0,0,0.9) 0%,transparent 60%);
  opacity:0;transition:opacity .2s}}
.card:hover .card-overlay{{opacity:1}}
.card-actions{{position:absolute;bottom:8px;left:8px;right:8px;display:flex;gap:6px;
  opacity:0;transform:translateY(4px);transition:all .2s}}
.card:hover .card-actions{{opacity:1;transform:translateY(0)}}
.card-btn{{flex:1;padding:5px;background:rgba(255,255,255,0.9);border:none;
  border-radius:4px;color:#000;font-size:10px;font-weight:600;cursor:pointer}}
.card-btn.outline{{background:transparent;border:1px solid #fff;color:#fff}}
.card-rating{{position:absolute;top:6px;right:6px;background:rgba(0,0,0,0.8);
  padding:2px 6px;border-radius:4px;font-size:10px;font-weight:600;color:var(--gold)}}
.card-info{{padding:6px 0}}
.card-info h4{{font-size:12px;font-weight:500;overflow:hidden;
  text-overflow:ellipsis;white-space:nowrap;margin-bottom:2px}}
.card-info p{{font-size:10px;color:var(--sub)}}

/* MODAL */
.modal{{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.88);
  z-index:200;align-items:center;justify-content:center;padding:20px}}
.modal.open{{display:flex}}
.modal-box{{background:#181818;border-radius:14px;max-width:720px;width:100%;
  max-height:90vh;overflow-y:auto;box-shadow:0 24px 80px rgba(0,0,0,0.7)}}
.modal-hero{{position:relative;height:280px;border-radius:14px 14px 0 0;overflow:hidden}}
.modal-hero img{{width:100%;height:100%;object-fit:cover}}
.modal-hero-overlay{{position:absolute;inset:0;background:linear-gradient(to bottom,transparent 30%,#181818 100%)}}
.modal-close{{position:absolute;top:14px;right:14px;width:36px;height:36px;
  background:rgba(0,0,0,0.7);border:none;border-radius:50%;color:#fff;
  font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center}}
.modal-body{{padding:0 24px 28px}}
.modal-title{{font-size:26px;font-weight:800;margin-bottom:10px;margin-top:-24px;position:relative}}
.modal-tags{{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:14px}}
.tag{{padding:3px 10px;border:1px solid #444;border-radius:12px;font-size:11px;color:#ccc}}
.modal-plot{{font-size:14px;line-height:1.7;color:#ccc;margin-bottom:20px}}
.modal-actions{{display:flex;gap:10px;flex-wrap:wrap}}

/* LOADER */
.loader{{display:none;justify-content:center;padding:48px}}
.loader.show{{display:flex}}
.dots{{display:flex;gap:8px}}
.dot{{width:10px;height:10px;background:var(--accent);border-radius:50%;animation:bounce .8s infinite}}
.dot:nth-child(2){{animation-delay:.2s}}
.dot:nth-child(3){{animation-delay:.4s}}
@keyframes bounce{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-10px)}}}}

/* TOAST */
.toast{{position:fixed;bottom:24px;right:24px;padding:12px 20px;
  border-radius:10px;font-size:13px;opacity:0;transition:opacity .3s;
  z-index:300;pointer-events:none;max-width:320px;
  background:#212121;border-left:4px solid #4caf50}}
.toast.show{{opacity:1}}

/* WATCHLIST BADGE */
.wl-badge{{position:absolute;top:-6px;right:-6px;width:16px;height:16px;
  background:var(--accent);border-radius:50%;font-size:9px;
  display:flex;align-items:center;justify-content:center;font-weight:700}}
</style>
</head>
<body>

<nav>
  <div class="logo" onclick="loadHome()">🎬 Movie<span>Hub</span></div>
  <div class="nav-links">
    <a onclick="loadHome()">Home</a>
    <a onclick="searchCategory('action')">Movies</a>
    <a onclick="searchCategory('series drama')">Series</a>
    <a onclick="searchCategory('india bollywood')">Bollywood</a>
    <a onclick="showWatchlist()">My List</a>
  </div>
  <div class="search-row">
    <input id="searchInput" placeholder="Search movies..." autocomplete="off"/>
    <button onclick="handleSearch()" style="background:none;border:none;color:#fff;cursor:pointer;font-size:18px;padding:4px">🔍</button>
  </div>
  <div class="nav-icons">
    <span title="Notifications">🔔</span>
    <div style="position:relative">
      <span onclick="showWatchlist()" title="My List" style="font-size:20px;cursor:pointer">📋</span>
      <div class="wl-badge" id="wlBadge">0</div>
    </div>
    <div class="avatar">R</div>
  </div>
</nav>

<!-- Hero -->
<div class="hero" id="hero">
  <div class="hero-bg"></div>
  <div class="hero-overlay"></div>
  <div class="hero-content">
    <div class="hero-badge">🔥 FEATURED TONIGHT</div>
    <div class="hero-title" id="heroTitle">RRR</div>
    <div class="hero-meta">
      <span class="rating-badge">⭐ 7.9</span>
      <span>2022</span>
      <span>Action • Drama</span>
      <span class="quality-badge">4K HDR</span>
      <span class="quality-badge" style="background:#1db954">DOLBY</span>
    </div>
    <div class="hero-desc" id="heroDesc">
      A fictional story about two legendary revolutionaries and their journey far away from home.
    </div>
    <div class="hero-btns">
      <button class="btn-play" onclick="showToast('Starting RRR...','success')">▶ Play Now</button>
      <button class="btn-add" onclick="addToWatchlist('RRR','tt8178634')">+ My List</button>
      <button class="btn-add" onclick="openModal({{Title:'RRR',Year:'2022',imdbRating:'7.9',Genre:'Action,Drama',Poster:'https://picsum.photos/seed/rrr/300/450',imdbID:'tt8178634',Plot:'A fictional story about two legendary revolutionaries.'}})">ℹ Info</button>
    </div>
  </div>
</div>

<!-- Categories -->
<div class="categories">
  <button class="cat-btn active" onclick="setCategory(this,'')">All</button>
  <button class="cat-btn" onclick="setCategory(this,'action')">Action</button>
  <button class="cat-btn" onclick="setCategory(this,'comedy')">Comedy</button>
  <button class="cat-btn" onclick="setCategory(this,'drama')">Drama</button>
  <button class="cat-btn" onclick="setCategory(this,'thriller')">Thriller</button>
  <button class="cat-btn" onclick="setCategory(this,'horror')">Horror</button>
  <button class="cat-btn" onclick="setCategory(this,'sci-fi')">Sci-Fi</button>
  <button class="cat-btn" onclick="setCategory(this,'animation')">Animation</button>
  <button class="cat-btn" onclick="setCategory(this,'india bollywood')">Bollywood</button>
  <button class="cat-btn" onclick="setCategory(this,'marvel superhero')">Superhero</button>
</div>

<div class="loader" id="loader"><div class="dots"><div class="dot"></div><div class="dot"></div><div class="dot"></div></div></div>

<div id="content">
  <div class="section">
    <div class="section-header"><h2>🔥 Trending Now</h2><span class="see-all" onclick="searchCategory('popular 2024')">See all →</span></div>
    <div class="row" id="trendingRow"></div>
  </div>
  <div class="section">
    <div class="section-header"><h2>🇮🇳 Bollywood Hits</h2><span class="see-all" onclick="searchCategory('india bollywood')">See all →</span></div>
    <div class="row" id="bollywoodRow"></div>
  </div>
  <div class="section">
    <div class="section-header"><h2>🌍 Hollywood Blockbusters</h2><span class="see-all" onclick="searchCategory('hollywood blockbuster')">See all →</span></div>
    <div class="row" id="recentRow"></div>
  </div>
</div>

<!-- Modal -->
<div class="modal" id="modal" onclick="if(event.target.id==='modal')closeModal()">
  <div class="modal-box">
    <div class="modal-hero">
      <img id="modalImg" src="" alt=""/>
      <div class="modal-hero-overlay"></div>
      <button class="modal-close" onclick="closeModal()">✕</button>
    </div>
    <div class="modal-body">
      <div class="modal-title" id="modalTitle"></div>
      <div class="modal-tags" id="modalTags"></div>
      <div class="modal-plot" id="modalPlot"></div>
      <div class="modal-actions">
        <button class="btn-play" onclick="showToast('Starting movie...','success')">▶ Play</button>
        <button class="btn-add" id="modalAddBtn">+ My List</button>
        <button class="btn-add" onclick="showToast('Downloaded!','success')">⬇ Download</button>
        <button class="btn-add" onclick="showToast('Shared!','info')">↗ Share</button>
      </div>
    </div>
  </div>
</div>

<div class="toast" id="toast"></div>

<script>
{api_js}

{load_section}

let watchlist = JSON.parse(localStorage.getItem('movieWL_india')||'[]');

function cardHTML(m, idx) {{
  const img   = posterUrl(m);
  const title = m.Title || m.title || 'Unknown';
  const year  = m.Year  || m.year  || '';
  const rating= m.imdbRating || m.vote_average || '';
  const id    = m.imdbID || m.id || idx;
  const safeM = encodeURIComponent(JSON.stringify(m));
  const inWL  = watchlist.some(w=>w.id===id);

  return `
    <div class="card">
      <div class="card-img">
        <img src="${{img}}" alt="${{escH(title)}}" loading="lazy"
          onerror="this.src='https://picsum.photos/seed/${{id}}/300/450'"/>
        ${{rating?`<div class="card-rating">⭐ ${{String(rating).slice(0,3)}}</div>`:''}}
        <div class="card-overlay"></div>
        <div class="card-actions">
          <button class="card-btn" onclick="event.stopPropagation();showToast('Playing ${{escH(title)}}...','success')">▶ Play</button>
          <button class="card-btn outline" onclick="event.stopPropagation();addToWatchlist('${{escH(title)}}','${{id}}')" 
            style="${{inWL?'border-color:#4caf50;color:#4caf50':''}}">
            ${{inWL?'✓':'+'}}
          </button>
        </div>
      </div>
      <div class="card-info" onclick="openModalById('${{id}}',decodeURIComponent('${{safeM}}'))">
        <h4>${{escH(title)}}</h4>
        <p>${{year}} ${{m.Genre?'• '+m.Genre.split(',')[0]:''}}</p>
      </div>
    </div>`;
}}

function renderSection(id, movies) {{
  const el = document.getElementById(id);
  if(!el) return;
  el.innerHTML = movies.length
    ? movies.map(cardHTML).join('')
    : '<p style="color:#555;padding:20px">No movies found</p>';
}}

async function handleSearch() {{
  const q = document.getElementById('searchInput').value.trim();
  if(!q) return;
  showLoader();
  const results = await searchMovies(q);
  hideLoader();
  document.getElementById('content').innerHTML = `
    <div class="section">
      <div class="section-header">
        <h2>🔍 "${{escH(q)}}" — ${{results.length}} result${{results.length!==1?'s':''}}</h2>
        <span class="see-all" onclick="loadHome()">← Back</span>
      </div>
      <div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(155px,1fr));gap:14px">
        ${{results.length?results.map(cardHTML).join(''):'<p style=\\"color:#555;grid-column:1/-1;text-align:center;padding:40px\\">No results found</p>'}}
      </div>
    </div>`;
}}

async function searchCategory(q) {{
  document.getElementById('searchInput').value = q;
  await handleSearch();
}}

function setCategory(el, q) {{
  document.querySelectorAll('.cat-btn').forEach(b=>b.classList.remove('active'));
  el.classList.add('active');
  if(!q) loadHome(); else searchCategory(q);
}}

function openModal(movie) {{
  const img = posterUrl(movie);
  document.getElementById('modalImg').src    = img;
  document.getElementById('modalImg').onerror= function(){{this.src='https://picsum.photos/seed/movie/700/400'}};
  document.getElementById('modalTitle').textContent = movie.Title||movie.title||'';
  document.getElementById('modalTags').innerHTML = [
    movie.Year||'', movie.Genre||'',
    movie.imdbRating?`⭐ ${{movie.imdbRating}} IMDb`:'',
    movie.Runtime||'', movie.Language||''
  ].filter(Boolean).map(t=>`<span class="tag">${{escH(String(t))}}</span>`).join('');
  document.getElementById('modalPlot').textContent = movie.Plot||movie.overview||'';
  document.getElementById('modalAddBtn').textContent =
    watchlist.some(w=>w.id===movie.imdbID) ? '✓ In My List' : '+ My List';
  document.getElementById('modalAddBtn').onclick = ()=>addToWatchlist(movie.Title,movie.imdbID);
  document.getElementById('modal').classList.add('open');
}}

async function openModalById(id, jsonStr) {{
  try {{
    const movie = JSON.parse(jsonStr);
    openModal(movie);
  }} catch {{
    const movie = await getMovieDetails(id);
    openModal(movie);
  }}
}}

function closeModal() {{
  document.getElementById('modal').classList.remove('open');
}}

function addToWatchlist(title, id) {{
  if(!watchlist.some(w=>w.id===id)) {{
    watchlist.push({{title, id}});
    localStorage.setItem('movieWL_india', JSON.stringify(watchlist));
    updateWLBadge();
    showToast(`"${{title}}" added to My List ✓`,'success');
  }} else {{
    showToast(`Already in My List`,'info');
  }}
}}

function showWatchlist() {{
  document.getElementById('content').innerHTML = `
    <div class="section">
      <div class="section-header">
        <h2>📋 My List (${{watchlist.length}})</h2>
        <span class="see-all" onclick="loadHome()">← Home</span>
      </div>
      ${{watchlist.length===0
        ? '<p style="color:#555;padding:20px">Your list is empty. Add movies by clicking + My List.</p>'
        : `<div style="display:flex;flex-direction:column;gap:10px">
            ${{watchlist.map(w=>`
              <div style="display:flex;justify-content:space-between;align-items:center;
                padding:14px 18px;background:#1a1a1a;border-radius:10px;border:1px solid #333">
                <span style="display:flex;align-items:center;gap:10px">
                  <span style="font-size:20px">🎬</span>
                  <span style="font-weight:500">${{escH(w.title)}}</span>
                </span>
                <div style="display:flex;gap:8px">
                  <button onclick="showToast('Playing...','success')"
                    class="btn-play" style="padding:7px 16px;font-size:12px">▶ Play</button>
                  <button onclick="removeWL('${{w.id}}',this)"
                    style="padding:7px 14px;background:none;border:1px solid #555;
                    border-radius:6px;color:#aaa;cursor:pointer;font-size:12px">✕ Remove</button>
                </div>
              </div>`).join('')}}
           </div>`
      }}
    </div>`;
}}

function removeWL(id, btn) {{
  watchlist = watchlist.filter(w=>w.id!==id);
  localStorage.setItem('movieWL_india',JSON.stringify(watchlist));
  updateWLBadge();
  btn.closest('div[style*="background:#1a1a1a"]')?.remove();
  showToast('Removed from My List','info');
}}

function updateWLBadge() {{
  const b = document.getElementById('wlBadge');
  b.textContent = watchlist.length;
  b.style.display = watchlist.length>0?'flex':'none';
}}

function showToast(msg, type='success') {{
  const el = document.getElementById('toast');
  const colors = {{success:'#4caf50', error:'#f44336', info:'#2196f3', warn:'#ff9800'}};
  el.style.borderLeftColor = colors[type]||colors.info;
  el.textContent = msg;
  el.classList.add('show');
  clearTimeout(el._t);
  el._t = setTimeout(()=>el.classList.remove('show'), 3000);
}}

function showLoader() {{ document.getElementById('loader').classList.add('show'); }}
function hideLoader() {{ document.getElementById('loader').classList.remove('show'); }}
function escH(s) {{ return String(s||'').replace(/[&<>"']/g,c=>({{
  '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]); }}

document.getElementById('searchInput').addEventListener('keydown',e=>{{
  if(e.key==='Enter') handleSearch();
}});

updateWLBadge();
loadHome();
</script>
</body>
</html>"""


# ─────────────────────────────────────────────────────────────
# YouTube App (unchanged, works in India)
# ─────────────────────────────────────────────────────────────
def generate_youtube_app(answers: dict) -> str:
    """(Keep existing implementation from previous media_agent.py)"""
    return _youtube_html(answers)


def _youtube_html(answers: dict) -> str:
    theme = answers.get("q3","Dark")
    youtube_key = os.getenv("YOUTUBE_API_KEY","")

    if youtube_key:
        api_js = f"""
const YT_KEY = '{youtube_key}';
async function fetchYT(endpoint) {{
  const r = await fetch('https://www.googleapis.com/youtube/v3/' + endpoint + '&key=' + YT_KEY);
  return r.json();
}}
async function getTrending() {{
  const d = await fetchYT('videos?part=snippet,statistics&chart=mostPopular&regionCode=IN&maxResults=16');
  return (d.items||[]).map(v=>({{
    id: v.id, title: v.snippet.title,
    channel: v.snippet.channelTitle,
    thumb: v.snippet.thumbnails?.medium?.url||'https://picsum.photos/seed/'+v.id+'/320/180',
    views: fmt(v.statistics?.viewCount||0), time: ago(v.snippet.publishedAt),
  }}));
}}
async function searchYT(q) {{
  const d = await fetchYT('search?part=snippet&q='+encodeURIComponent(q)+'&type=video&maxResults=16');
  return (d.items||[]).map(v=>({{
    id: v.id.videoId, title: v.snippet.title,
    channel: v.snippet.channelTitle,
    thumb: v.snippet.thumbnails?.medium?.url||'https://picsum.photos/seed/'+v.id.videoId+'/320/180',
    views: 'YouTube', time: ago(v.snippet.publishedAt),
  }}));
}}
function fmt(n){{return n>1e6?(n/1e6).toFixed(1)+'M views':n>1e3?(n/1e3).toFixed(0)+'K views':n+' views'}}
function ago(d){{
  const diff=(Date.now()-new Date(d))/1000;
  if(diff<3600) return Math.floor(diff/60)+' min ago';
  if(diff<86400) return Math.floor(diff/3600)+' hours ago';
  return Math.floor(diff/86400)+' days ago';
}}
"""
    else:
        api_js = """
// Add YOUTUBE_API_KEY to .env — Works in India (Google APIs not blocked)
// Get free at: console.cloud.google.com → YouTube Data API v3
const MOCK = [
  {id:'dQw4w9WgXcQ',title:'Learn Python in 60 Minutes - Complete Tutorial 2024',channel:'Programming with Mosh',views:'3.2M views',time:'2 days ago',thumb:'https://picsum.photos/seed/py1/320/180'},
  {id:'abc2',title:'Machine Learning Full Course - Beginner to Expert',channel:'freeCodeCamp.org',views:'2.1M views',time:'1 week ago',thumb:'https://picsum.photos/seed/ml2/320/180'},
  {id:'abc3',title:'React JS + FastAPI Full Stack Project 2024',channel:'Traversy Media',views:'845K views',time:'3 days ago',thumb:'https://picsum.photos/seed/react3/320/180'},
  {id:'abc4',title:'LangChain & LLMs - Build AI Agents from Scratch',channel:'AI Jason',views:'612K views',time:'5 days ago',thumb:'https://picsum.photos/seed/lang4/320/180'},
  {id:'abc5',title:'Data Science Roadmap 2024 - Complete Guide',channel:'Ken Jee',views:'498K views',time:'1 month ago',thumb:'https://picsum.photos/seed/ds5/320/180'},
  {id:'abc6',title:'System Design Interview - Top 10 Concepts',channel:'NeetCode',views:'1.4M views',time:'2 weeks ago',thumb:'https://picsum.photos/seed/sys6/320/180'},
  {id:'abc7',title:'Docker + Kubernetes for Developers - Full Course',channel:'TechWorld with Nana',views:'987K views',time:'1 month ago',thumb:'https://picsum.photos/seed/docker7/320/180'},
  {id:'abc8',title:'Build a Real-Time Chat App with Python & WebSockets',channel:'ArjanCodes',views:'234K views',time:'2 weeks ago',thumb:'https://picsum.photos/seed/chat8/320/180'},
];
async function getTrending() { return MOCK; }
async function searchYT(q) { return MOCK.filter(v=>v.title.toLowerCase().includes(q.toLowerCase())||v.channel.toLowerCase().includes(q.toLowerCase())); }
"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<title>YouTube</title>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap" rel="stylesheet"/>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
html,body{{height:100%;background:#0f0f0f;color:#fff;font-family:Roboto,sans-serif;overflow-x:hidden}}
::-webkit-scrollbar{{width:5px;height:5px}}::-webkit-scrollbar-thumb{{background:#444;border-radius:3px}}
header{{position:sticky;top:0;z-index:50;background:#0f0f0f;border-bottom:1px solid #272727;padding:0 20px;height:56px;display:flex;align-items:center;gap:16px}}
.logo{{font-size:20px;font-weight:700;color:#ff0000;letter-spacing:-1px;min-width:100px;cursor:pointer}}
.search{{flex:1;max-width:600px;display:flex;gap:0}}
.search input{{flex:1;padding:8px 14px;background:#121212;border:1px solid #303030;border-right:none;border-radius:40px 0 0 40px;color:#fff;font-size:14px;outline:none}}
.search input:focus{{border-color:#1a73e8}}
.search button{{padding:8px 16px;background:#272727;border:1px solid #303030;border-left:none;border-radius:0 40px 40px 0;color:#fff;cursor:pointer}}
.hdr-r{{margin-left:auto;display:flex;align-items:center;gap:14px}}
.av{{width:32px;height:32px;border-radius:50%;background:linear-gradient(135deg,#6366f1,#8b5cf6);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;cursor:pointer}}
.layout{{display:flex;height:calc(100vh - 56px)}}
nav{{width:230px;flex-shrink:0;overflow-y:auto;border-right:1px solid #272727;padding:8px}}
nav::-webkit-scrollbar{{width:0}}
.ni{{display:flex;align-items:center;gap:16px;padding:9px 14px;border-radius:10px;margin:1px 0;font-size:13px;cursor:pointer;transition:background .15s}}
.ni:hover,.ni.on{{background:#272727}}
.ni-ic{{font-size:17px;width:22px;text-align:center}}
.ns{{padding:6px 14px;font-size:10px;font-weight:600;color:#aaa;text-transform:uppercase;letter-spacing:1px;margin-top:6px}}
main{{flex:1;overflow-y:auto;padding:14px 20px}}
.chips{{display:flex;gap:7px;margin-bottom:18px;overflow-x:auto;padding-bottom:2px}}
.chips::-webkit-scrollbar{{height:0}}
.chip{{padding:6px 14px;background:#272727;border:none;border-radius:8px;color:#fff;font-size:12px;cursor:pointer;white-space:nowrap;transition:background .15s}}
.chip:hover,.chip.on{{background:#fff;color:#0f0f0f}}
.grid{{display:grid;grid-template-columns:repeat(auto-fill,minmax(270px,1fr));gap:14px}}
.vc{{cursor:pointer;border-radius:10px;overflow:hidden;transition:transform .15s}}
.vc:hover{{transform:translateY(-2px)}}
.tw{{position:relative;aspect-ratio:16/9;background:#272727;overflow:hidden;border-radius:10px}}
.tw img{{width:100%;height:100%;object-fit:cover;transition:transform .3s}}
.vc:hover .tw img{{transform:scale(1.04)}}
.dur{{position:absolute;bottom:6px;right:6px;background:rgba(0,0,0,0.85);padding:2px 5px;border-radius:3px;font-size:11px;font-weight:500}}
.vi{{display:flex;gap:10px;padding:9px 0}}
.ci{{width:34px;height:34px;border-radius:50%;background:linear-gradient(135deg,#667eea,#764ba2);display:flex;align-items:center;justify-content:center;font-size:12px;font-weight:700;flex-shrink:0}}
.vm h4{{font-size:13px;font-weight:500;line-height:1.4;margin-bottom:2px;display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}}
.vm p{{font-size:11px;color:#aaa}}
.overlay{{display:none;position:fixed;inset:0;background:rgba(0,0,0,0.92);z-index:100;align-items:center;justify-content:center}}
.overlay.open{{display:flex}}
.player{{background:#0f0f0f;border-radius:10px;overflow:hidden;max-width:860px;width:95%;box-shadow:0 20px 60px rgba(0,0,0,0.6)}}
.ph{{display:flex;justify-content:space-between;align-items:center;padding:10px 14px;border-bottom:1px solid #272727}}
.ph span{{font-size:13px;max-width:80%;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}}
.ph button{{background:none;border:none;color:#fff;font-size:20px;cursor:pointer;line-height:1}}
iframe.yp{{width:100%;aspect-ratio:16/9;border:none;display:block}}
.pi{{padding:14px}}
.pi h3{{font-size:14px;margin-bottom:4px}}
.pi p{{font-size:12px;color:#aaa}}
.loader{{display:none;justify-content:center;padding:40px}}
.loader.show{{display:flex}}
.spin{{width:36px;height:36px;border:3px solid #303030;border-top-color:#ff0000;border-radius:50%;animation:sp 1s linear infinite}}
@keyframes sp{{to{{transform:rotate(360deg)}}}}
.toast{{position:fixed;bottom:20px;right:20px;background:#303030;padding:11px 18px;border-radius:8px;font-size:12px;opacity:0;transition:opacity .3s;z-index:200;pointer-events:none}}
.toast.show{{opacity:1}}
</style>
</head>
<body>
<header>
  <div class="logo">▶ YouTube</div>
  <div class="search">
    <input id="si" placeholder="Search" autocomplete="off"/>
    <button onclick="doSearch()">🔍</button>
  </div>
  <div class="hdr-r">
    <span style="cursor:pointer;font-size:20px">🔔</span>
    <div class="av">R</div>
  </div>
</header>
<div class="layout">
  <nav>
    <div class="ni on" onclick="loadHome();hi(this)"><span class="ni-ic">🏠</span>Home</div>
    <div class="ni" onclick="loadHome();hi(this)"><span class="ni-ic">📱</span>Shorts</div>
    <div class="ni" onclick="t('Subscriptions coming soon!')"><span class="ni-ic">📺</span>Subscriptions</div>
    <div class="ni" onclick="t('Library coming soon!')"><span class="ni-ic">📚</span>Library</div>
    <div class="ns">Explore</div>
    <div class="ni" onclick="doSearchQ('trending india');hi(this)"><span class="ni-ic">🔥</span>Trending</div>
    <div class="ni" onclick="doSearchQ('music');hi(this)"><span class="ni-ic">🎵</span>Music</div>
    <div class="ni" onclick="doSearchQ('gaming');hi(this)"><span class="ni-ic">🎮</span>Gaming</div>
    <div class="ni" onclick="doSearchQ('technology');hi(this)"><span class="ni-ic">💻</span>Technology</div>
    <div class="ni" onclick="doSearchQ('education learning');hi(this)"><span class="ni-ic">📖</span>Learning</div>
    <div class="ni" onclick="doSearchQ('news');hi(this)"><span class="ni-ic">📰</span>News</div>
  </nav>
  <main>
    <div class="chips" id="chips">
      <button class="chip on" onclick="loadHome();sc(this)">All</button>
      <button class="chip" onclick="doSearchQ('python programming');sc(this)">Python</button>
      <button class="chip" onclick="doSearchQ('machine learning');sc(this)">ML/AI</button>
      <button class="chip" onclick="doSearchQ('web development');sc(this)">Web Dev</button>
      <button class="chip" onclick="doSearchQ('gaming');sc(this)">Gaming</button>
      <button class="chip" onclick="doSearchQ('music');sc(this)">Music</button>
      <button class="chip" onclick="doSearchQ('india bollywood');sc(this)">India</button>
      <button class="chip" onclick="doSearchQ('cooking recipe');sc(this)">Cooking</button>
    </div>
    <div class="loader" id="ld"><div class="spin"></div></div>
    <div class="grid" id="grid"></div>
  </main>
</div>

<div class="overlay" id="ol" onclick="if(event.target.id==='ol')close_()">
  <div class="player">
    <div class="ph">
      <span id="pt"></span>
      <button onclick="close_()">✕</button>
    </div>
    <iframe class="yp" id="yp" src="" allowfullscreen allow="autoplay;encrypted-media"></iframe>
    <div class="pi">
      <h3 id="ptt"></h3>
      <p id="pm"></p>
    </div>
  </div>
</div>
<div class="toast" id="toast"></div>

<script>
{api_js}

function card(v) {{
  const e = s => String(s||'').replace(/[&<>"']/g,c=>({{
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}})[c]);
  return `<div class="vc" onclick="open_('${{v.id}}','${{e(v.title)}}','${{e(v.channel)}}','${{e(v.views)}}','${{e(v.time)}}')">
    <div class="tw">
      <img src="${{v.thumb}}" loading="lazy" onerror="this.src='https://picsum.photos/seed/${{v.id}}/320/180'"/>
      <span class="dur">${{v.duration||'5:24'}}</span>
    </div>
    <div class="vi">
      <div class="ci">${{(v.channel||'Y')[0].toUpperCase()}}</div>
      <div class="vm">
        <h4>${{e(v.title)}}</h4>
        <p>${{e(v.channel)}} • ${{e(v.views)}} • ${{e(v.time)}}</p>
      </div>
    </div>
  </div>`;
}}

async function loadHome() {{
  sl(true);
  const vids = await getTrending();
  document.getElementById('grid').innerHTML = vids.map(card).join('');
  sl(false);
}}

async function doSearch() {{
  const q = document.getElementById('si').value.trim();
  if(!q) return;
  sl(true);
  const r = await searchYT(q);
  document.getElementById('grid').innerHTML = r.length
    ? r.map(card).join('')
    : '<p style="color:#aaa;grid-column:1/-1;text-align:center;padding:40px">No results</p>';
  sl(false);
}}

async function doSearchQ(q) {{
  document.getElementById('si').value = q;
  await doSearch();
}}

function open_(id,title,ch,views,time) {{
  document.getElementById('yp').src=`https://www.youtube.com/embed/${{id}}?autoplay=1&rel=0`;
  document.getElementById('pt').textContent=title;
  document.getElementById('ptt').textContent=title;
  document.getElementById('pm').textContent=ch+' • '+views+' • '+time;
  document.getElementById('ol').classList.add('open');
}}
function close_() {{
  document.getElementById('ol').classList.remove('open');
  document.getElementById('yp').src='';
}}

function hi(el) {{document.querySelectorAll('.ni').forEach(e=>e.classList.remove('on'));el.classList.add('on');}}
function sc(el) {{document.querySelectorAll('.chip').forEach(e=>e.classList.remove('on'));el.classList.add('on');}}
function sl(show) {{document.getElementById('ld').classList.toggle('show',show);}}
function t(msg) {{const el=document.getElementById('toast');el.textContent=msg;el.classList.add('show');setTimeout(()=>el.classList.remove('show'),2500);}}

document.getElementById('si').addEventListener('keydown',e=>{{if(e.key==='Enter')doSearch();}});
loadHome();
</script>
</body>
</html>"""
