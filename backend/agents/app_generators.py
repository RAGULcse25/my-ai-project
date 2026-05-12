# agents/app_generators.py — All specialized app generators
# ============================================================

import os, json
from dotenv import load_dotenv
load_dotenv()

def llm_call(prompt: str, tokens: int = 10000) -> str:
    """Import at runtime to avoid circular"""
    from core.llm_config import get_llm_response
    return get_llm_response(
        prompt=prompt, max_tokens=tokens, temperature=0.1,
        system=(
            "You are an expert React developer. Return ONLY complete raw HTML using React/CDN. "
            "Use Tailwind CSS + Shadcn UI patterns + Lucide Icons. "
            "Use Babel standalone for JSX. "
            "ZERO alert()/confirm()/prompt(). "
            "Production quality. Fully working React app. "
            "MANDATORY: Make the navbar sticky (e.g., sticky top-0 z-50). "
            "MANDATORY: Create a highly COLORFUL and VIBRANT design. "
            "MANDATORY: Every process and interaction MUST be animated (hover, loading, page transitions)."
        ),
        task_type="code",
    )


# ════════════════════════════════════════════════════════════
#  SPOTIFY CLONE — Music Streaming App
# ════════════════════════════════════════════════════════════
def generate_spotify(answers: dict) -> str:
    theme    = answers.get("q3", "Dark")
    features = answers.get("q1", "")

    return llm_call(f"""Create a COMPLETE, PREMIUM React Spotify-clone music streaming app.
Theme:{theme} Features:{features}
STRICT: Use React 18, Tailwind, Lucide, Framer Motion.
Patterns: Shadcn UI Card, Sidebar, Toast.

LAYOUT (3-panel like Spotify):
LEFT SIDEBAR (240px):
  - Logo (green Spotify-style)
  - Your Library: Liked Songs, Playlists
  - 5 sample playlists with cover art (picsum)
  - Install App button (PWA hint)

CENTER PANEL (flex):
  - Genre chips: All, Pop, Rock, Hip-Hop, Electronic, Classical, Bollywood, Indie
  - Featured playlist hero card (big cover art)
  - Recently Played: horizontal scroll row
  - Popular tracks: list with #, title, artist, album, duration

RIGHT PANEL (300px, collapses on mobile):
  - Now Playing card (big cover, song info)
  - Queue: next 3 songs

BOTTOM PLAYER (fixed, 90px):
  - Album art (60x60), song name, artist, heart icon
  - prev, play/pause, next, shuffle, repeat buttons
  - Progress bar (interactive seek)
  - Volume slider
  - Full screen toggle

SAMPLE DATA (30 tracks):
const TRACKS = [
  {{id:1,title:"Blinding Lights",artist:"The Weeknd",album:"After Hours",duration:"3:20",genre:"Pop",cover:"https://picsum.photos/seed/track1/300/300",color:"#e91e63"}},
  {{id:2,title:"Levitating",artist:"Dua Lipa",album:"Future Nostalgia",duration:"3:23",genre:"Pop",cover:"https://picsum.photos/seed/track2/300/300",color:"#9c27b0"}},
  {{id:3,title:"Tum Hi Ho",artist:"Arijit Singh",album:"Aashiqui 2",duration:"4:22",genre:"Bollywood",cover:"https://picsum.photos/seed/track3/300/300",color:"#f44336"}},
  {{id:4,title:"Kesariya",artist:"Arijit Singh",album:"Brahmastra",duration:"4:34",genre:"Bollywood",cover:"https://picsum.photos/seed/track4/300/300",color:"#ff9800"}},
];

WEB AUDIO API (simulate playback):
- Create AudioContext on user interaction
- Play sine wave tone when "playing" (simulate music)
- Progress bar auto-advances while playing
- Keyboard: Space=play/pause, right=next, left=prev

FEATURES:
- Like/unlike songs (heart icon, saved to localStorage)
- Search: real-time filter tracks
- Create playlist (modal + add songs)
- Shuffle mode, repeat mode
- Toast: "Added to Liked Songs"

MOBILE RESPONSIVE: bottom nav, collapsible panels
PWA: meta name="theme-color", viewport meta

Return ONLY complete <!DOCTYPE html>:""", tokens=8000)


# ════════════════════════════════════════════════════════════
#  JIO TV CLONE — Live TV Streaming App
# ════════════════════════════════════════════════════════════
def generate_jiotv(answers: dict) -> str:
    return llm_call(f"""Create COMPLETE JioTV-style live TV streaming app as single HTML.
Theme: Dark with Jio blue accents. Mobile-first.
RULE: ZERO alert() — toast notifications only.

LAYOUT:
HEADER: JioTV logo, search, profile icon, notification bell
TABS: Live TV | Movies | TV Shows | Kids | Music | News

CHANNEL GRID:
Display 20 channels in responsive grid (4 cols desktop, 2 mobile):
const CHANNELS = [
  {{id:1,name:"Star Sports 1",category:"Sports",logo:"https://picsum.photos/seed/sports1/100/60",isLive:true,viewers:"1.2M",color:"#1565c0",currentShow:"IPL Match Live"}},
  {{id:2,name:"Sony Entertainment",category:"Entertainment",logo:"https://picsum.photos/seed/sony/100/60",isLive:true,viewers:"856K",color:"#c62828",currentShow:"KBC Season 14"}},
  {{id:3,name:"Colors TV",category:"Entertainment",logo:"https://picsum.photos/seed/colors/100/60",isLive:true,viewers:"743K",color:"#e65100",currentShow:"Bigg Boss 17"}},
  {{id:4,name:"Star Plus",category:"Entertainment",logo:"https://picsum.photos/seed/starplus/100/60",isLive:true,viewers:"623K",color:"#6a1b9a",currentShow:"Anupamaa"}},
  {{id:5,name:"Zee TV",category:"Entertainment",logo:"https://picsum.photos/seed/zeetv/100/60",isLive:true,viewers:"512K",color:"#1b5e20",currentShow:"Kumkum Bhagya"}},
  {{id:6,name:"BBC News",category:"News",logo:"https://picsum.photos/seed/bbc/100/60",isLive:true,viewers:"234K",color:"#b71c1c",currentShow:"World News"}},
  {{id:7,name:"Aaj Tak",category:"News",logo:"https://picsum.photos/seed/aajtaknews/100/60",isLive:true,viewers:"445K",color:"#e53935",currentShow:"Breaking News"}},
  {{id:8,name:"MTV India",category:"Music",logo:"https://picsum.photos/seed/mtv/100/60",isLive:true,viewers:"312K",color:"#f57f17",currentShow:"MTV Unplugged"}},
  {{id:9,name:"Cartoon Network",category:"Kids",logo:"https://picsum.photos/seed/cartoonnet/100/60",isLive:true,viewers:"678K",color:"#0277bd",currentShow:"Tom and Jerry"}},
  {{id:10,name:"Discovery",category:"Infotainment",logo:"https://picsum.photos/seed/discovery/100/60",isLive:true,viewers:"189K",color:"#00695c",currentShow:"Planet Earth"}},
];

CHANNEL CARD:
- Channel logo (image)
- Channel name + category badge
- LIVE dot + viewer count
- Current show name
- Watch Now button

PLAYER MODAL (when channel clicked):
- Large video player area (16:9 ratio, dark bg with channel branding)
- Channel name, current show, LIVE badge
- Episode guide (3 upcoming shows)
- Quality selector (Auto/HD/SD)
- Share button, + My List, Cast button
- Channel description

CATEGORIES: filter by Sports/Entertainment/News/Kids/Music
SEARCH: filter channels by name/show
MY LIST: add/remove channels (localStorage)
EPG (Electronic Program Guide): shows schedule for selected channel

MOBILE: bottom nav (Home/Live/Movies/My List/Profile)
Return ONLY complete <!DOCTYPE html>:""", tokens=6000)


# ════════════════════════════════════════════════════════════
#  BOOKING APP — Hotel/Doctor/Restaurant
# ════════════════════════════════════════════════════════════
def generate_booking_app(idea: str, answers: dict) -> str:
    booking_type = answers.get("q1", "Hotel")
    theme        = answers.get("q3", "Clean white")

    types_config = {
        "Hotel":      {"items":"hotels",      "fields":["Check-in","Check-out","Guests","Rooms"],       "icon":"Hotel"},
        "Doctor":     {"items":"doctors",     "fields":["Date","Time","Specialty","Symptoms"],           "icon":"Doctor"},
        "Restaurant": {"items":"restaurants", "fields":["Date","Time","Guests","Preferences"],           "icon":"Food"},
        "Flight":     {"items":"flights",     "fields":["From","To","Date","Passengers"],                "icon":"Flight"},
        "Movie":      {"items":"movies",      "fields":["Date","Theater","Show Time","Seats"],           "icon":"Movie"},
    }
    cfg = types_config.get(booking_type, types_config["Hotel"])

    return llm_call(f"""Create COMPLETE {booking_type} booking app as single HTML.
Theme:{theme} RULE: ZERO alert() — toast notifications only.

TYPE: {booking_type} booking platform
FIELDS NEEDED: {cfg['fields']}
ICON: {cfg['icon']}

LAYOUT:
HEADER: Logo ({cfg['icon']} BookNow), search bar, login button, language selector
HERO: Big search form with fields: {', '.join(cfg['fields'])}
     + Search button (prominent CTA)

LISTINGS GRID (12 items):
- Include 12 realistic {cfg['items']} with name, location, rating(4.0-5.0), reviews, price, image(picsum),
  amenities/features (3-5 tags), availability

ITEM CARD:
- Image (400x250, picsum)
- Name + location
- Star rating + review count
- Key features (badge chips)
- Price (prominent)
- Book Now + Wishlist buttons

BOOKING MODAL (when Book Now clicked):
- Item summary
- Calendar date picker (HTML calendar)
- Time slots (if applicable): 9AM, 10AM, 11AM, 2PM, 3PM, 4PM
- Guest/quantity selector
- Price breakdown (base + taxes + fees)
- Promo code input
- PAY NOW button → shows success screen with booking ID

BOOKING SUCCESS:
- Confetti animation (CSS keyframes)
- Booking reference number
- Download ticket (shows in modal)
- Add to calendar button

FILTERS: Price range, Rating, Location, Availability
SORT: Price low-high, Rating, Popularity
MY BOOKINGS: localStorage history of past bookings

MOBILE RESPONSIVE: bottom nav, full-screen modal
Return ONLY complete <!DOCTYPE html>:""", tokens=6000)


# ════════════════════════════════════════════════════════════
#  CANVA-LIKE DESIGN TOOL
# ════════════════════════════════════════════════════════════
def generate_design_tool(answers: dict) -> str:
    theme    = answers.get("q3", "Dark (like Figma)")
    features = answers.get("q1", "Background remover, Photo filters, Text overlay")
    canvas_size = answers.get("q4", "800x600 (default)")

    return llm_call(f"""Create a COMPLETE React-based Professional Photo Editor like Canva.
Theme: {theme}
Features: {features}
Canvas size: {canvas_size}
STRICT: Use React 18, Tailwind, Canvas API, Lucide Icons via CDN.
ZERO alert()/confirm()/prompt() — use toast notifications.

LAYOUT (4-panel Canva/Figma layout):
LEFT PANEL (tools): Select, Text, Shape, Image, Pen, Eraser, Crop, Icon library
CENTER: Canvas area with zoom controls + rulers
RIGHT PANEL: Layer manager, properties panel (color, font, opacity, shadow)
TOP TOOLBAR: File, Edit, View, + template picker + download button

CANVAS FEATURES:
- Drag & drop elements
- Resize handles on selected elements
- Text editing (double-click)
- Color picker (full spectrum)
- Font selector (10+ fonts via Google Fonts)
- Image upload (local file)
- Background color/gradient picker
- Undo/Redo (Ctrl+Z / Ctrl+Y)
- Grid/Snap-to-grid toggle
- Download PNG/JPG/SVG

TEMPLATES (6 presets): Social Post, Banner, Poster, Thumbnail, Card, Logo

Return ONLY complete <!DOCTYPE html>:""", tokens=10000)


# ════════════════════════════════════════════════════════════
#  MOBILE SHOPPING APP (Flipkart/Amazon style)
# ════════════════════════════════════════════════════════════
def generate_mobile_shop(answers: dict) -> str:
    store = answers.get("q1", "Flipkart-like")
    theme = answers.get("q3", "Flipkart blue")

    palettes = {
        "flipkart blue":  {"primary":"#2874f0","accent":"#fb641b","bg":"#f1f3f6","nav":"#2874f0"},
        "amazon orange":  {"primary":"#ff9900","accent":"#febd69","bg":"#eaeded","nav":"#131921"},
        "dark minimal":   {"primary":"#6366f1","accent":"#a78bfa","bg":"#0f0f0f","nav":"#111"},
        "clean white":    {"primary":"#2563eb","accent":"#60a5fa","bg":"#f8fafc","nav":"#fff"},
    }
    p = palettes.get(theme.lower(), palettes["flipkart blue"])

    return llm_call(f"""Create COMPLETE mobile shopping React app (mobile-first).
Type:{store} Theme:{theme} Primary:{p['primary']} Accent:{p['accent']}
STRICT: Use React 18, Tailwind, Lucide, Framer Motion via CDN.
ZERO alert()/confirm()/prompt().

SCREENS:
1. HOME: Header (logo, search, cart badge), Category carousel, Flash Sale banner,
   Featured products grid, Bottom nav (Home/Search/Cart/Profile)
2. PRODUCT DETAIL: Image gallery, name, price, rating, "Add to Cart" / "Buy Now"
3. CART: Item list, quantity controls, price summary, "Place Order"
4. CHECKOUT: Address form, payment options (COD, UPI, Card), Order confirmation

SAMPLE PRODUCTS (20 items with realistic data):
- Electronics: phones, laptops, headphones
- Fashion: shirts, shoes, watches
- Home: furniture, kitchen items

FEATURES:
- Real search with filter (price, rating, category)
- Wishlist (heart icon, localStorage)
- Cart with quantity (localStorage)
- Toast: "Added to cart!", "Removed from wishlist"
- Shimmer loading skeletons
- Infinite scroll simulation

Return ONLY complete <!DOCTYPE html>:""", tokens=10000)


# ════════════════════════════════════════════════════════════
#  ADVANCED ECOMMERCE (Full Desktop Flipkart)
# ════════════════════════════════════════════════════════════
def generate_advanced_ecommerce(answers: dict) -> str:
    store    = answers.get("q1", "Flipkart-like")
    features = answers.get("q2", "Cart,Search,Filter")
    theme    = answers.get("q3", "Flipkart blue")
    cats     = answers.get("q4", "Electronics,Fashion,Home")

    return llm_call(f"""Create COMPLETE PREMIUM E-commerce React Store like {store}.
Features:{features} Theme:{theme} Categories:{cats}
STRICT: Use React 18, Tailwind, Lucide, Framer Motion, Shadcn patterns via CDN.
ZERO alert()/confirm()/prompt().

FULL DESKTOP LAYOUT:
- Sticky header: Logo, mega-menu, search bar, cart, user menu
- Category sidebar with expandable tree
- Product grid (4-col desktop, 2 mobile) with sort + filter
- Product cards: image, name, price, original price, discount %, rating, "Add to Cart"
- Detailed filter panel: brand, price range slider, rating, availability
- Pagination / infinite scroll
- Footer: links, newsletter, social, payment logos

PRODUCT DETAIL PAGE (single page SPA):
- Image zoom gallery (main + thumbnails)
- Size/color selector
- Stock indicator
- Quantity + Add to Cart + Buy Now
- EMI calculator
- Reviews section (5 sample reviews)
- Related products row

CHECKOUT FLOW (3 steps):
1. Address: form with validation
2. Payment: UPI, NetBanking, COD, Card (UI only)
3. Confirmation: order ID, estimated delivery

SAMPLE DATA: 50 products across categories with realistic prices (INR)

Return ONLY complete <!DOCTYPE html>:""", tokens=10000)


# ════════════════════════════════════════════════════════════
#  YOUTUBE CLONE — Video Platform
# ════════════════════════════════════════════════════════════
def generate_youtube(answers: dict) -> str:
    theme    = answers.get("q3", "Dark")
    features = answers.get("q1", "Video feed, Search, Subscriptions")

    return llm_call(f"""Create COMPLETE YouTube-clone video platform as single HTML.
Theme: {theme} Features: {features}
ZERO alert()/confirm()/prompt(). Use React 18, Tailwind, Lucide via CDN.

LAYOUT (3-panel YouTube layout):
LEFT SIDEBAR (collapsed on mobile):
  - Home, Explore, Shorts, Subscriptions, Library, History, Watch Later
  - Subscribed channels (10 with avatar)

CENTER FEED:
  - Search bar at top with voice icon
  - Category filter chips: All, Music, Gaming, News, Live, Shorts, Tech
  - Video grid (responsive, 3-4 cols): thumbnail (picsum), duration badge,
    channel avatar, title, views, upload time
  - Shorts row: vertical video cards

VIDEO PLAYER (when video clicked, SPA navigation):
  - 16:9 video area (YouTube-like dark player with play controls)
  - Video title, views, like/dislike, share, save buttons
  - Channel info + Subscribe button
  - Comments section (10 sample comments)
  - Related videos sidebar

SAMPLE VIDEOS (20 videos):
- Tech, Gaming, Music, Vlogs, Education categories
- Realistic data: title, channel, views (1K-10M), upload time, duration

FEATURES:
- Dark/Light mode toggle
- Search: filter videos by title/channel
- Liked Videos (localStorage)
- Watch history (localStorage)
- Toast notifications ("Subscribed!", "Video saved")

MOBILE: bottom nav (Home/Shorts/Add/Subscriptions/Library)
Return ONLY complete <!DOCTYPE html>:""", tokens=8000)


# ════════════════════════════════════════════════════════════
#  NETFLIX/MOVIES CLONE — Movie Streaming App
# ════════════════════════════════════════════════════════════
def generate_movies(answers: dict) -> str:
    theme    = answers.get("q3", "Netflix dark")
    features = answers.get("q1", "Movie catalog, Search, My List")

    return llm_call(f"""Create COMPLETE Netflix-style movie streaming app as single HTML.
Theme: {theme} Features: {features}
ZERO alert()/confirm()/prompt(). Use React 18, Tailwind, Lucide via CDN.

LAYOUT:
HEADER: Netflix logo, nav links (Home/Series/Movies/New/My List), search, bell, profile avatar
HERO BANNER: Random featured movie with title, description, Play + More Info buttons

CONTENT ROWS (horizontal scroll with arrows):
- Trending Now (10 movies)
- Top 10 in India
- Continue Watching
- Action & Adventure
- Bollywood Hits
- English TV Series
- Anime
- Documentaries

MOVIE CARD:
- Poster image (picsum seed unique per movie)
- Hover: expand, show title, year, rating, Play/More Info/+ My List

MOVIE MODAL (More Info):
- Banner image, title, year, rating, duration, genre tags
- Description paragraph
- Cast: 5 actors with avatar
- Similar movies row
- Episode list (if series)

SAMPLE DATA (50 movies/shows):
- Bollywood, Hollywood, Web Series, Anime, Docs
- With realistic titles, years, IMDb ratings, descriptions

FEATURES:
- My List (localStorage — add/remove)
- Search with real-time filter
- Genre filter
- Profile selector (up to 5 profiles)
- Continue Watching progress bars
- Toast: "Added to My List"

MOBILE: bottom nav, swipeable carousels
Return ONLY complete <!DOCTYPE html>:""", tokens=8000)


# ════════════════════════════════════════════════════════════
#  APP DISPATCHER — picks right generator
# ════════════════════════════════════════════════════════════
def dispatch_app(idea: str, answers: dict) -> tuple:
    """
    Returns (html, source_name)
    """
    u = idea.lower()

    # Music streaming
    if any(w in u for w in ["spotify", "music streaming", "music player", "music app"]):
        return generate_spotify(answers), "music_agent"

    # TV streaming
    if any(w in u for w in ["jiotv", "jio tv", "live tv", "tv streaming", "hotstar", "disney+"]):
        return generate_jiotv(answers), "tv_agent"

    # YouTube
    if any(w in u for w in ["youtube", "video platform", "yt app", "video sharing"]):
        return generate_youtube(answers), "youtube_agent"

    # Netflix / Movies
    if any(w in u for w in ["netflix", "movie app", "hotstar", "prime video", "cinema app", "movie streaming"]):
        return generate_movies(answers), "movies_agent"

    # Design tool
    if any(w in u for w in ["canva", "design tool", "design editor", "graphic design", "photo editor"]):
        return generate_design_tool(answers), "canva_agent"

    # Mobile shopping
    if any(w in u for w in ["mobile app", "mobile shop", "android app", "ios app", "phone app"]):
        if any(w in u for w in ["shop", "buy", "store", "cart", "flipkart", "amazon"]):
            return generate_mobile_shop(answers), "mobile_ecommerce"

    # Booking apps
    if any(w in u for w in ["booking", "book", "reserve", "appointment", "hotel", "doctor", "restaurant", "flight"]):
        return generate_booking_app(idea, answers), "booking_agent"

    # Advanced ecommerce
    if any(w in u for w in ["ecommerce", "shop", "store", "flipkart", "amazon", "buy", "cart"]):
        return generate_advanced_ecommerce(answers), "ecommerce_agents"

    return None, None
