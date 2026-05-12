// App.jsx — S.E.A.D.S. v13
// Each category = its own page
// Questions = dynamic based on what user types
// ============================================================
import { useState, useRef, useEffect } from "react";
const API = "http://localhost:8000";

// ══════════════════════════════════════════════════════════════
// DYNAMIC QUESTION ENGINE
// Questions change based on what user actually typed
// ══════════════════════════════════════════════════════════════
function getQuestions(category, idea) {
  const u = (idea || "").toLowerCase();

  // ── WEBSITE ──────────────────────────────────────────────
  if (category === "website") {
    if (u.includes("portfolio"))
      return [
        { id:"q1", text:"Your profession?", type:"choice",
          options:["Software Developer","Data Scientist","UI/UX Designer","Photographer","Freelancer","Writer","Marketing Professional","Student"] },
        { id:"q2", text:"Sections to show?", type:"multi",
          options:["About me","Projects showcase","Skills & tools","Work experience","Education","Blog","Contact form","Resume download","GitHub stats"] },
        { id:"q3", text:"Visual style?", type:"choice",
          options:["Dark minimal (like GitHub)","Light & clean","Neon dark (developer)","Glassmorphism","Retro terminal","Colorful & creative"] },
        { id:"q4", text:"Special effects?", type:"multi",
          options:["Typing animation on hero","Scroll reveal animations","Project filter tabs","Dark/light toggle","Particle background","Smooth scroll"] },
      ];

    if (u.includes("restaurant") || u.includes("cafe") || u.includes("food"))
      return [
        { id:"q1", text:"Restaurant type?", type:"choice",
          options:["Fine dining","Casual restaurant","Fast food chain","Cafe/Coffee shop","Indian restaurant","Pizza place","Bakery","Cloud kitchen"] },
        { id:"q2", text:"Sections?", type:"multi",
          options:["Full menu with prices","Table reservation form","Food gallery","About & story","Chef profile","Customer reviews","Home delivery info","Map & location"] },
        { id:"q3", text:"Vibe?", type:"choice",
          options:["Elegant & luxury (dark)","Warm & cozy","Fresh & minimal","Bold & colorful","Traditional/vintage"] },
        { id:"q4", text:"Extras?", type:"multi",
          options:["Menu filter (veg/non-veg)","Zomato/Swiggy link buttons","Special offers section","WhatsApp order button","Chef's specials highlight"] },
      ];

    if (u.includes("startup") || u.includes("saas") || u.includes("landing") || u.includes("product"))
      return [
        { id:"q1", text:"Product type?", type:"choice",
          options:["SaaS web app","Mobile app","AI/ML tool","Developer tool","E-learning platform","Healthcare product","Fintech app","Other startup"] },
        { id:"q2", text:"Landing page sections?", type:"multi",
          options:["Hero with CTA","Features showcase","How it works (3 steps)","Pricing table","Testimonials","FAQ","Newsletter signup","Demo video embed"] },
        { id:"q3", text:"Design style?", type:"choice",
          options:["Dark SaaS (like Vercel/Linear)","Light & minimal","Gradient tech (purple/blue)","Bold & colorful","Clean white (Apple-like)","Glassmorphism"] },
        { id:"q4", text:"Main CTA goal?", type:"choice",
          options:["Get early access","Start free trial","Book a demo","Download the app","Sign up free","Contact sales team"] },
      ];

    if (u.includes("blog") || u.includes("news") || u.includes("article") || u.includes("magazine"))
      return [
        { id:"q1", text:"Blog focus?", type:"choice",
          options:["Technology & coding","Personal journal","Business & finance","Health & wellness","Travel adventures","Fashion & lifestyle","Food & recipes","News & current affairs"] },
        { id:"q2", text:"Blog features?", type:"multi",
          options:["Article card grid","Category filter","Search bar","Newsletter popup","Author bio","Comment section","Related articles","Social share buttons","Reading time estimate"] },
        { id:"q3", text:"Layout style?", type:"choice",
          options:["Medium-like (clean readable)","Dark editorial","Minimal typography","Magazine grid","Personal journal style"] },
        { id:"q4", text:"Advanced features?", type:"multi",
          options:["Dark/light toggle","Reading progress bar","Featured post hero","Tag cloud","Table of contents in articles"] },
      ];

    if (u.includes("corporate") || u.includes("company") || u.includes("business") || u.includes("firm"))
      return [
        { id:"q1", text:"Company industry?", type:"choice",
          options:["IT & Software","Management Consulting","Manufacturing","Finance & Banking","Healthcare","Legal services","Real Estate","Education & Training"] },
        { id:"q2", text:"Pages/Sections?", type:"multi",
          options:["Company about","Services list","Our team","Client logos","Case studies","Blog/News","Careers page","Contact & offices","Awards & certifications"] },
        { id:"q3", text:"Corporate theme?", type:"choice",
          options:["Professional blue (classic)","Dark & sophisticated","Clean white (modern)","Bold & contemporary","Traditional & formal"] },
        { id:"q4", text:"Features?", type:"multi",
          options:["Animated stats counter","Client testimonials","Service icon cards","Team member profiles","Download company brochure","WhatsApp chat button"] },
      ];

    if (u.includes("agency") || u.includes("creative") || u.includes("studio"))
      return [
        { id:"q1", text:"Agency specialization?", type:"choice",
          options:["UI/UX Design","Digital Marketing","Web Development","Branding & Identity","Video Production","Advertising","SEO & Content"] },
        { id:"q2", text:"Portfolio display?", type:"choice",
          options:["Grid gallery","Full-screen case studies","Card list with filters","Masonry layout","Horizontal scroll carousel"] },
        { id:"q3", text:"Agency vibe?", type:"choice",
          options:["Dark & bold (award-winning)","Minimal & clean","Colorful & playful","Black & white editorial","Gradient & vibrant"] },
        { id:"q4", text:"Must-have sections?", type:"multi",
          options:["Work portfolio","Our process (steps)","Client brands list","Team introduction","Awards & recognition","Video showreel","Get a quote form"] },
      ];

    // Default website questions
    return [
      { id:"q1", text:"What type of website?", type:"choice",
        options:["Landing page","Portfolio","Corporate / Company","Blog / Magazine","Restaurant","Creative Agency","NGO / Nonprofit","Product showcase"] },
      { id:"q2", text:"Key sections to include?", type:"multi",
        options:["Hero / Banner","About section","Features / Services","Gallery / Portfolio","Testimonials","Pricing","FAQ","Contact form","Team members"] },
      { id:"q3", text:"Visual theme?", type:"choice",
        options:["Modern dark","Clean white","Bold & colorful","Minimal & clean","Corporate blue","Glassmorphism","Retro / vintage"] },
      { id:"q4", text:"Special requirements?", type:"multi",
        options:["Mobile-first responsive","Contact form with email","Newsletter signup","Dark mode toggle","Scroll animations","Social media links","Fast loading"] },
    ];
  }

  // ── MOBILE APP ───────────────────────────────────────────
  if (category === "mobile") {
    if (u.includes("calculator") || u.includes("calc"))
      return [
        { id:"q1", text:"Calculator type?", type:"choice",
          options:["Basic (+ - × ÷)","Scientific (sin, cos, log, √)","Financial (EMI, interest, tax)","Unit converter","Tip calculator","Age / Date calculator"] },
        { id:"q2", text:"Framework?", type:"choice",
          options:["Flask (simplest — 1 file)","FastAPI (fast & modern)","Django (full features)"] },
        { id:"q3", text:"Extra features?", type:"multi",
          options:["Calculation history (SQLite)","Copy result button","Keyboard support","Dark/light toggle","Scientific keyboard switch","Share result"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark minimal","iPhone-style light","Android Material","Neon dark","Clean white","Colorful"] },
      ];

    if (u.includes("game") || u.includes("guessing") || u.includes("quiz") || u.includes("puzzle"))
      return [
        { id:"q1", text:"Game type?", type:"choice",
          options:["Number guessing game","Word guessing (Wordle-like)","Math quiz","Trivia/quiz game","Memory card game","Snake (Python + display)","Hangman"] },
        { id:"q2", text:"Framework?", type:"choice",
          options:["Flask (web browser game)","FastAPI (REST + frontend)","Django (full game portal)"] },
        { id:"q3", text:"Game features?", type:"multi",
          options:["Score tracking (SQLite)","Leaderboard","Multiple difficulty levels","Timer/countdown","Sound effects (beep)","User accounts","Achievements"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark gaming","Colorful & fun","Pixel/retro","Minimal clean","Neon arcade"] },
      ];

    if (u.includes("student") || u.includes("grade") || u.includes("school") || u.includes("education"))
      return [
        { id:"q1", text:"App purpose?", type:"choice",
          options:["Grade & CGPA calculator","Attendance tracker","Study planner / timetable","Exam countdown","Assignment tracker","Fee calculator","Student marks management"] },
        { id:"q2", text:"Framework?", type:"choice",
          options:["Flask","Django","FastAPI"] },
        { id:"q3", text:"Database features?", type:"multi",
          options:["Save student records (SQLite)","Login/register per student","Subject-wise grades","Export to CSV","Class-wise reports","Teacher dashboard"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Light & friendly","Dark minimal","Colorful educational","Material Design"] },
      ];

    if (u.includes("expense") || u.includes("budget") || u.includes("finance") || u.includes("money") || u.includes("track"))
      return [
        { id:"q1", text:"Finance app type?", type:"choice",
          options:["Personal expense tracker","Monthly budget planner","Income vs expense","Bill splitter","Savings goal tracker","Investment tracker","EMI calculator"] },
        { id:"q2", text:"Framework?", type:"choice",
          options:["Flask","FastAPI","Django"] },
        { id:"q3", text:"Features?", type:"multi",
          options:["Add/edit/delete transactions (SQLite)","Category-wise chart (pie chart)","Monthly summary","Export to CSV","Budget limit alerts","Recurring expenses","Multiple accounts"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark minimal","Light clean","Green (money theme)","Material Design"] },
      ];

    if (u.includes("todo") || u.includes("task") || u.includes("note") || u.includes("reminder"))
      return [
        { id:"q1", text:"App type?", type:"choice",
          options:["Simple to-do list","Kanban board (Todo/Doing/Done)","Notes app (like Google Keep)","Daily planner","Project task manager","Reminder with due dates"] },
        { id:"q2", text:"Framework?", type:"choice",
          options:["Flask","FastAPI","Django"] },
        { id:"q3", text:"Features?", type:"multi",
          options:["Save tasks (SQLite)","Priority (High/Med/Low)","Due date & reminder","Category/tags","Mark complete","Search tasks","User login","Import/export"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark minimal","Light Notion-like","Colorful playful","Material Design"] },
      ];

    // Default mobile questions
    return [
      { id:"q1", text:"Framework?", type:"choice",
        options:["Flask (simplest)","FastAPI (fast & modern)","Django (full-featured)"] },
      { id:"q2", text:"App category?", type:"choice",
        options:["Calculator / Tool","Game (Python logic)","Student / Education","Finance / Budget","Health & Fitness","Notes / Tasks","Social / Community","Other utility"] },
      { id:"q3", text:"Database?", type:"choice",
        options:["SQLite (saves data)","In-memory (no save)","PostgreSQL (production)"] },
      { id:"q4", text:"Features?", type:"multi",
        options:["User login/register","Mobile-responsive UI","REST API endpoints","Admin dashboard","CSV export","Charts/graphs","Dark mode","Search & filter"] },
    ];
  }

  // ── DESIGN TOOL ──────────────────────────────────────────
  if (category === "design") {
    if (u.includes("background") || u.includes("bg remove") || u.includes("remove bg"))
      return [
        { id:"q1", text:"Primary function?", type:"choice",
          options:["Background remover only","Background remover + replace","Background remover + editor","Full photo editor with bg removal"] },
        { id:"q2", text:"Extra tools?", type:"multi",
          options:["Add new background (colors/images)","Blur background","Photo filters","Brightness/contrast sliders","Text overlay","Stickers","Download PNG (transparent)","Before/after preview"] },
        { id:"q3", text:"API for bg removal?", type:"choice",
          options:["Remove.bg API (best quality)","Canvas threshold (no API needed)","PhotoRoom API","ClipDrop API","Simulate (demo mode)"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark (like Remove.bg)","Light clean","Minimal white"] },
      ];

    if (u.includes("photo editor") || u.includes("image editor") || u.includes("filter"))
      return [
        { id:"q1", text:"Editor features?", type:"multi",
          options:["Upload image from device","Instagram-style filters (15+)","Manual adjustments (brightness/contrast/saturation)","Crop & resize","Rotate & flip","Text overlay","Stickers & emoji","Background blur"] },
        { id:"q2", text:"Canvas filters to include?", type:"multi",
          options:["Grayscale","Sepia","Vintage","Vivid","Cold/Blue","Warm/Orange","High contrast","Soft/Fade","HDR","Noir"] },
        { id:"q3", text:"Export options?", type:"multi",
          options:["Download PNG","Download JPG (quality slider)","Download WebP","Copy to clipboard","Share on social","Save to browser"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark (like Lightroom)","Light (like Snapseed)","Minimal dark","Clean white"] },
      ];

    if (u.includes("banner") || u.includes("poster") || u.includes("thumbnail") || u.includes("social"))
      return [
        { id:"q1", text:"Design type?", type:"choice",
          options:["Social media post (1080×1080)","YouTube thumbnail (1280×720)","Instagram story (1080×1920)","Facebook cover (820×312)","Twitter/X header","LinkedIn banner","Event poster","Business card"] },
        { id:"q2", text:"Design tools?", type:"multi",
          options:["Pre-made templates (10+)","Background colors & gradients","Upload own image","Text with fonts (20+ fonts)","Shapes & icons","Stickers & emoji","Filter effects","Brand colors preset"] },
        { id:"q3", text:"Text features?", type:"multi",
          options:["Multiple font choices","Bold/italic/underline","Text shadow effects","Curved text","Outline text","Multiple text layers","Font size & color"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark (like Canva pro)","Light (like Canva free)","Minimal clean"] },
      ];

    if (u.includes("logo") || u.includes("brand"))
      return [
        { id:"q1", text:"Logo type?", type:"choice",
          options:["Text logo (wordmark)","Icon + text","Icon only (symbol)","Badge/emblem style","Monogram (initials)","Minimal geometric"] },
        { id:"q2", text:"Logo tools?", type:"multi",
          options:["Shape library (100+ shapes)","Icon library (200+ icons)","Color palette picker","Font combinations (50+)","Gradient fills","Symmetry tool","Undo/redo (50 steps)","Export SVG + PNG"] },
        { id:"q3", text:"Style presets?", type:"multi",
          options:["Tech/Startup","Fashion/Luxury","Food & Beverage","Healthcare","Education","Sports","Creative/Art","Professional/Corporate"] },
        { id:"q4", text:"Theme?", type:"choice",
          options:["Dark Figma-like","Light Canva-like","Minimal white"] },
      ];

    // Default design questions
    return [
      { id:"q1", text:"Main tool features?", type:"multi",
        options:["Background remover","Photo filters (15+)","Text overlay","Shapes & stickers","Crop & resize","Draw/paint","Undo/redo","Download PNG/JPG","Templates library"] },
      { id:"q2", text:"Primary purpose?", type:"choice",
        options:["Photo editing","Banner/poster creation","Logo design","Social media graphics","YouTube thumbnail","Business card"] },
      { id:"q3", text:"Editor theme?", type:"choice",
        options:["Dark (professional)","Light (like Canva)","Minimal white"] },
      { id:"q4", text:"Canvas preset?", type:"choice",
        options:["800×600 (default)","1080×1080 (Instagram square)","1280×720 (YouTube / HD)","1920×1080 (Full HD poster)","1080×1920 (Story/Reel)"] },
    ];
  }

  // ── PPT ──────────────────────────────────────────────────
  if (category === "ppt") {
    if (u.includes("ai") || u.includes("artificial intelligence") || u.includes("machine learning") || u.includes("data science"))
      return [
        { id:"q1", text:"AI topic focus?", type:"choice",
          options:["Introduction to AI/ML","Deep learning & neural networks","Generative AI & ChatGPT","AI in business/industry","Future of AI","AI ethics & risks","Computer vision","NLP & language models"] },
        { id:"q2", text:"Number of slides?", type:"choice",
          options:["8 slides","10 slides","12 slides","15 slides","20 slides"] },
        { id:"q3", text:"Presentation style?", type:"choice",
          options:["Dark professional (tech)","Gradient tech (purple/blue)","Minimal white","Colorful modern","Futuristic neon"] },
        { id:"q4", text:"Include?", type:"multi",
          options:["AI history timeline","Real-world examples","Statistics & data charts","Pros & cons comparison","Future predictions","Case studies","Technical diagrams","Q&A slide"] },
      ];

    if (u.includes("startup") || u.includes("pitch") || u.includes("investor") || u.includes("business plan"))
      return [
        { id:"q1", text:"Startup stage?", type:"choice",
          options:["Idea/concept stage","Pre-seed startup","Seed round pitch","Series A pitch","Product launch","Investor update"] },
        { id:"q2", text:"Number of slides?", type:"choice",
          options:["8 slides (quick pitch)","10 slides (standard)","12 slides (detailed)","15 slides (comprehensive)"] },
        { id:"q3", text:"Pitch deck style?", type:"choice",
          options:["Dark professional (bold)","Clean white (Apple-like)","Gradient modern","Minimal typographic","Bold & colorful"] },
        { id:"q4", text:"Essential slides?", type:"multi",
          options:["Problem & solution","Market size (TAM/SAM/SOM)","Product demo","Business model","Traction & metrics","Competition matrix","Team bios","Funding ask","Financial projections","Roadmap"] },
      ];

    if (u.includes("product") || u.includes("demo") || u.includes("feature") || u.includes("app"))
      return [
        { id:"q1", text:"Product type?", type:"choice",
          options:["Mobile app","Web app / SaaS","Physical product","API / Dev tool","AI product","E-commerce platform","Enterprise software"] },
        { id:"q2", text:"Demo structure?", type:"choice",
          options:["5 slides (quick overview)","8 slides (standard demo)","10 slides (detailed walkthrough)","12 slides (full demo)"] },
        { id:"q3", text:"Style?", type:"choice",
          options:["Dark & sleek (tech)","Light & clean","Colorful & vibrant","Minimal & elegant","Brand colors focused"] },
        { id:"q4", text:"Include?", type:"multi",
          options:["Problem being solved","Feature screenshots/mockups","How it works (steps)","Key metrics & results","Customer testimonials","Pricing plans","Call to action","Comparison with competitors"] },
      ];

    if (u.includes("education") || u.includes("course") || u.includes("teaching") || u.includes("student") || u.includes("lesson"))
      return [
        { id:"q1", text:"Subject/topic?", type:"choice",
          options:["Computer Science / Programming","Mathematics","Science (Physics/Chemistry/Biology)","History / Social Studies","Business / Economics","Language / Literature","General knowledge","Other"] },
        { id:"q2", text:"Audience level?", type:"choice",
          options:["School students (6-10th)","High school (11-12th)","College / University","Corporate training","Professional workshop","General public"] },
        { id:"q3", text:"Slides needed?", type:"choice",
          options:["5 slides","8 slides","10 slides","15 slides","20 slides"] },
        { id:"q4", text:"Include?", type:"multi",
          options:["Learning objectives","Concept diagrams","Examples & case studies","Quiz/question slides","Summary & key points","Activity / exercise","References / resources","Assignments"] },
      ];

    if (u.includes("research") || u.includes("paper") || u.includes("thesis") || u.includes("report") || u.includes("analysis"))
      return [
        { id:"q1", text:"Research type?", type:"choice",
          options:["Academic research paper","Market research report","Data analysis findings","Case study presentation","Project report","Survey results","Literature review","Feasibility study"] },
        { id:"q2", text:"Slides count?", type:"choice",
          options:["8 slides","10 slides","12 slides","15 slides","20 slides"] },
        { id:"q3", text:"Style?", type:"choice",
          options:["Academic minimal white","Dark professional","Corporate blue","Colorful modern"] },
        { id:"q4", text:"Include?", type:"multi",
          options:["Abstract / overview","Research methodology","Data tables & charts","Key findings","Statistical analysis","Conclusions","Recommendations","References/citations","Appendix"] },
      ];

    // Default PPT questions
    return [
      { id:"q1", text:"Presentation purpose?", type:"choice",
        options:["Business pitch / investor deck","Educational / teaching","Product demo","Research / report","Company overview","Project proposal","Creative portfolio","Conference talk"] },
      { id:"q2", text:"How many slides?", type:"choice",
        options:["5 slides (quick)","8 slides","10 slides (standard)","15 slides","20 slides (detailed)"] },
      { id:"q3", text:"Visual design?", type:"choice",
        options:["Dark professional (bold)","Minimal white (clean)","Colorful modern","Gradient tech","Corporate blue","Creative gradient","Nature/organic"] },
      { id:"q4", text:"Features to include?", type:"multi",
        options:["Animated slide transitions","Charts & graphs","Speaker notes","Table of contents","Progress bar top","Auto-play mode","Fullscreen button","PDF export hint","Swipe/touch support"] },
    ];
  }

  // ── GAME ─────────────────────────────────────────────────
  if (category === "game") {
    if (u.includes("chess"))
      return [
        { id:"q1", text:"Game mode?", type:"choice",
          options:["Player vs Computer (AI)","Player vs Player (Local)","AI vs AI"] },
        { id:"q2", text:"AI Difficulty?", type:"choice",
          options:["Easy (random/depth 1)","Medium (depth 2)","Hard (depth 3)","Expert (depth 4)"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Classic wood","Dark neon","Minimalist b/w","Glassmorphism"] },
        { id:"q4", text:"Game features?", type:"multi",
          options:["Highlight legal moves","Undo move button","Move history list","Captured pieces list","Timer / clock","Sound effects"] },
      ];

    if (u.includes("ludo"))
      return [
        { id:"q1", text:"Game mode?", type:"choice",
          options:["Player vs 3 AI","2 Players vs 2 AI","All 4 Humans (Local)","Watch AI play"] },
        { id:"q2", text:"Game speed?", type:"choice",
          options:["Normal","Fast animations","Turbo speed"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Classic colors","Neon dark mode","Pastel minimal","Retro 8-bit"] },
        { id:"q4", text:"House rules?", type:"multi",
          options:["Must roll 6 to start","Safe squares marked","Three 6s act as penalty","Fast win mode"] },
      ];

    if (u.includes("snake") || u.includes("arcade") || u.includes("retro"))
      return [
        { id:"q1", text:"Game type?", type:"choice",
          options:["Classic Snake","Tetris clone","Pong","Space Invaders","Asteroids","Pacman style","Flappy bird"] },
        { id:"q2", text:"Controls?", type:"multi",
          options:["Arrow keys (Desktop)","WASD keys (Desktop)","On-screen buttons (Mobile)","Swipe controls (Mobile)"] },
        { id:"q3", text:"Visual style?", type:"choice",
          options:["Retro 8-bit","Neon synthwave","Minimal flat design","Glassmorphism UI"] },
        { id:"q4", text:"Features?", type:"multi",
          options:["High score tracking","Pause menu","Difficulty progression","Sound effects","Multiple levels"] },
      ];

    // Default game questions
    return [
      { id:"q1", text:"Game type?", type:"choice",
        options:["2D Arcade (Snake, Pong)","Puzzle (Tetris, 2048)","Board Game (Chess, Ludo)","Platformer","Endless runner","Shooter","Card Game","Strategy"] },
      { id:"q2", text:"Game mechanics?", type:"multi",
        options:["Score tracking","Timer/Countdown","Levels/Stages","AI Opponent","Lives/Health system","Power-ups","Local multiplayer"] },
      { id:"q3", text:"Visual theme?", type:"choice",
        options:["Retro pixel art","Neon / Cyberpunk","Minimal clean","Colorful cartoon","Dark premium"] },
      { id:"q4", text:"Engine approach?", type:"choice",
        options:["HTML5 Canvas API (best for 2D)","DOM elements (best for board games)","Phaser.js (complex 2D)","Vanilla JS + HTML/CSS"] },
    ];
  }

  // ── ML PROJECT ───────────────────────────────────────────
  if (category === "ml") {
    if (u.includes("house") || u.includes("price") || u.includes("property") || u.includes("real estate") || u.includes("land"))
      return [
        { id:"q1", text:"Prediction target?", type:"choice",
          options:["House/flat price prediction","Land price estimation","Rental price prediction","Property valuation","Construction cost estimate"] },
        { id:"q2", text:"Input features to use?", type:"multi",
          options:["Location / area","Square footage / BHK","Number of bedrooms & bathrooms","Age of property","Floor number","Amenities (parking, gym, etc.)","Nearby schools/hospitals distance","Crime rate index"] },
        { id:"q3", text:"Algorithm?", type:"choice",
          options:["Random Forest (best for tabular)","XGBoost (high accuracy)","Linear Regression (simple & explainable)","Gradient Boosting","Decision Tree","Ridge/Lasso Regression"] },
        { id:"q4", text:"Output & extras?", type:"multi",
          options:["HTML prediction form UI","Feature importance chart","Price range confidence interval","Similar properties shown","Model accuracy metrics","Training data visualizations","Save model (joblib)","Jupyter notebook"] },
      ];

    if (u.includes("movie") || u.includes("film") || u.includes("recommend") || u.includes("suggestion") || u.includes("content"))
      return [
        { id:"q1", text:"Recommendation type?", type:"choice",
          options:["Movie recommendation","Music recommendation","Product recommendation","Book recommendation","News/article recommendation","Restaurant recommendation","Course recommendation"] },
        { id:"q2", text:"Approach?", type:"choice",
          options:["Content-based filtering (item similarity)","Collaborative filtering (user behavior)","Hybrid (content + collaborative)","Popularity-based (trending)","Matrix factorization (SVD)"] },
        { id:"q3", text:"Features to use?", type:"multi",
          options:["Genre/category","User ratings","Cast & director","Release year","Plot/description (NLP)","User viewing history","Similar users behavior","Popularity score"] },
        { id:"q4", text:"Output UI?", type:"multi",
          options:["HTML search & recommendation page","Movie cards with posters (picsum)","Rating input slider","Genre filter","'Because you liked...' explanation","Confidence score shown","Top 10 trending sidebar","Save favorites (localStorage)"] },
      ];

    if (u.includes("spam") || u.includes("email") || u.includes("sms") || u.includes("fraud") || u.includes("fake"))
      return [
        { id:"q1", text:"Classification target?", type:"choice",
          options:["Email spam detection","SMS spam filter","Fraud transaction detection","Fake news detection","Toxic comment classifier","Review spam filter","Phishing URL detector"] },
        { id:"q2", text:"Text features?", type:"multi",
          options:["Word frequency (TF-IDF)","Bag of words","Word length statistics","Special character count","URL presence","Capital letters ratio","Sentiment score"] },
        { id:"q3", text:"Algorithm?", type:"choice",
          options:["Naive Bayes (best for text)","Logistic Regression","Random Forest","SVM (text classification)","LSTM Neural Network","XGBoost"] },
        { id:"q4", text:"Output?", type:"multi",
          options:["HTML input form (paste text → classify)","Probability score (spam %)","Confidence visualization","Top spam words shown","Batch CSV classification","Confusion matrix","ROC curve","Word cloud of spam words"] },
      ];

    if (u.includes("churn") || u.includes("customer") || u.includes("retain") || u.includes("attrition"))
      return [
        { id:"q1", text:"Business domain?", type:"choice",
          options:["Telecom customer churn","Bank customer attrition","SaaS/subscription churn","E-commerce churn","Insurance policy lapse","Streaming service cancellation"] },
        { id:"q2", text:"Features to predict?", type:"multi",
          options:["Monthly charges","Contract type","Tenure (months)","Payment method","Internet service type","Customer service calls","Number of products","Account activity"] },
        { id:"q3", text:"Algorithm?", type:"choice",
          options:["Random Forest","XGBoost (best accuracy)","Logistic Regression (explainable)","Decision Tree","Gradient Boosting","Neural Network"] },
        { id:"q4", text:"Extras?", type:"multi",
          options:["Customer risk score UI","Churn probability bar","SHAP feature explanations","High-risk customer list","Retention recommendations","Confusion matrix","ROC-AUC curve","Model comparison table"] },
      ];

    if (u.includes("sentiment") || u.includes("review") || u.includes("opinion") || u.includes("emotion") || u.includes("nlp"))
      return [
        { id:"q1", text:"Sentiment source?", type:"choice",
          options:["Product reviews (Amazon/Flipkart)","Twitter/X posts","Restaurant reviews","App store ratings","Customer feedback forms","News article sentiment","Social media comments","Movie/book reviews"] },
        { id:"q2", text:"Classification type?", type:"choice",
          options:["Binary: Positive / Negative","3-way: Positive / Neutral / Negative","5-star rating prediction","Emotion detection (happy/sad/angry/fear/surprise)","Aspect-based sentiment"] },
        { id:"q3", text:"Model type?", type:"choice",
          options:["VADER (rule-based, no training)","TF-IDF + Logistic Regression","TF-IDF + Naive Bayes","BERT/DistilBERT (deep learning)","TextBlob (simple)","LSTM (sequence model)"] },
        { id:"q4", text:"Output UI?", type:"multi",
          options:["Type text → get sentiment","Emoji indicator (😊😐😠)","Confidence % shown","Word cloud (positive/negative)","Batch CSV analysis","Chart of sentiment distribution","Sample reviews pre-loaded","Live API endpoint"] },
      ];

    // Default ML questions
    return [
      { id:"q1", text:"ML project type?", type:"choice",
        options:["Price / Value prediction","Movie or product recommendation","Spam / Fraud detection","Customer churn prediction","Sentiment analysis","Customer segmentation","Image classification","Demand forecasting"] },
      { id:"q2", text:"Best algorithm?", type:"choice",
        options:["Random Forest (best all-rounder)","XGBoost (best accuracy)","Linear/Logistic Regression (simple)","Decision Tree (explainable)","K-Means (clustering)","Neural Network MLP","SVM (classification)"] },
      { id:"q3", text:"User interface?", type:"choice",
        options:["HTML form (predict from inputs)","Streamlit web app","FastAPI + HTML frontend","Jupyter notebook only"] },
      { id:"q4", text:"Deliverables?", type:"multi",
        options:["Trained model (joblib)","Python main.py script","Jupyter notebook (.ipynb)","Prediction UI (HTML)","requirements.txt","README with setup","Feature importance chart","Model evaluation report"] },
    ];
  }

  // ── ECOMMERCE ────────────────────────────────────────────
  if (category === "ecommerce") {
    if (u.includes("flipkart") || u.includes("indian") || u.includes("india"))
      return [
        { id:"q1", text:"Indian store type?", type:"choice",
          options:["Flipkart-style (multi-category)","Meesho-style (budget fashion)","BigBasket-style (grocery)","Nykaa-style (beauty)","Boat/electronics store","Bata-style (footwear)","Fabindia-style (ethnic)"] },
        { id:"q2", text:"Must-have features?", type:"multi",
          options:["Product grid with ₹ prices","Discount badges (% off)","Search with filters","Cart + quantity control","Wishlist (heart icon)","Flipkart-style payment (UPI/Card/EMI/COD)","Order tracking","Login/Register"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Flipkart blue & orange","Clean white Indian style","Dark premium","Colorful modern"] },
        { id:"q4", text:"Product categories?", type:"multi",
          options:["Electronics (mobiles, laptops)","Fashion (clothing, shoes)","Home & Kitchen","Beauty & Personal care","Books & Stationery","Sports & Fitness","Grocery & Food","Toys & Baby"] },
      ];

    if (u.includes("amazon") || u.includes("international") || u.includes("global"))
      return [
        { id:"q1", text:"Store style?", type:"choice",
          options:["Amazon-style (everything)","Specialized category","Subscription box","Marketplace (multi-seller)","Flash sale site (daily deals)","Wholesale/B2B"] },
        { id:"q2", text:"Features?", type:"multi",
          options:["Prime/membership badge","Product comparison","'Also bought' recommendations","Review system (stars)","One-click checkout","Multiple delivery options","Seller dashboard view","Return/refund policy page"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Amazon orange & dark navy","Clean white (minimal)","Dark mode store","Modern colorful"] },
        { id:"q4", text:"Categories?", type:"multi",
          options:["Electronics","Books","Fashion","Home & Garden","Sports","Toys","Automotive","Health & Beauty","Food & Grocery"] },
      ];

    if (u.includes("fashion") || u.includes("clothing") || u.includes("apparel") || u.includes("dress") || u.includes("boutique"))
      return [
        { id:"q1", text:"Fashion store type?", type:"choice",
          options:["Women's fashion","Men's fashion","Kids' clothing","Ethnic & traditional wear","Sports & activewear","Luxury / premium fashion","Fast fashion","Vintage / thrift store"] },
        { id:"q2", text:"Shopping features?", type:"multi",
          options:["Size selector (XS-XXL)","Color picker per product","Style filter (casual/formal/ethnic)","Outfit combinations ('complete the look')","Size guide popup","Virtual try-on hint","Wishlist","Instagram-style product gallery"] },
        { id:"q3", text:"Fashion theme?", type:"choice",
          options:["Dark luxury (like Zara)","Clean white (like H&M)","Bold & colorful","Minimal editorial","Warm & earthy tones"] },
        { id:"q4", text:"Extras?", type:"multi",
          options:["New arrivals section","Trending now","Price range filter","Brand filter","Customer photos section","Sale / discount section","Free shipping badge","Express delivery option"] },
      ];

    if (u.includes("electronics") || u.includes("gadget") || u.includes("tech") || u.includes("mobile phone") || u.includes("laptop"))
      return [
        { id:"q1", text:"Electronics focus?", type:"choice",
          options:["All electronics","Smartphones & tablets","Laptops & computers","Audio (earphones, speakers)","Smart home & IoT","Cameras & photography","Gaming equipment","Accessories & cables"] },
        { id:"q2", text:"Product features?", type:"multi",
          options:["Spec comparison table","Brand filter (Samsung/Apple/etc)","Price range slider","Rating & review filter","EMI / easy pay option","Exchange/trade-in option","Warranty info","Expert review badge"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Dark tech (like Croma)","Clean white (like Apple)","Blue (like Flipkart electronics)","Bold modern"] },
        { id:"q4", text:"Categories?", type:"multi",
          options:["Smartphones","Laptops","Headphones & Earbuds","Smart Watches","Tablets","Cameras","Gaming","Smart Home","Accessories"] },
      ];

    // Default ecommerce questions
    return [
      { id:"q1", text:"Store inspiration?", type:"choice",
        options:["Flipkart (Indian, multi-category)","Amazon (international, everything)","Fashion boutique","Electronics only","Grocery delivery","Beauty & cosmetics","Sports & fitness","Multi-category general"] },
      { id:"q2", text:"Shopping features?", type:"multi",
        options:["Search + smart filter","Cart + checkout flow","Wishlist (heart toggle)","Product reviews & ratings","Payment (UPI/Card/EMI/COD)","Order tracking","Promo codes / coupons","Size & color selector","Product comparison"] },
      { id:"q3", text:"Store theme?", type:"choice",
        options:["Flipkart blue & orange","Amazon dark orange","Dark minimal premium","Clean white modern","Bold & colorful"] },
      { id:"q4", text:"Product categories?", type:"multi",
        options:["Electronics","Fashion & Clothing","Home & Kitchen","Books","Beauty & Skincare","Sports","Grocery & Food","Toys","Shoes","Jewellery"] },
    ];
  }

  // ── MORE ─────────────────────────────────────────────────
  if (category === "more") {
    if (u.includes("weather"))
      return [
        { id:"q1", text:"Weather app features?", type:"multi",
          options:["Current temperature & feels like","7-day forecast","Hourly forecast (24hr chart)","Weather map","UV index & air quality","Humidity & wind speed","Sunrise & sunset times","Rain probability"] },
        { id:"q2", text:"API to use?", type:"choice",
          options:["OpenWeatherMap (free, add WEATHER_API_KEY)","WeatherAPI (free)","Simulated/mock data (no API key)"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Dark with weather animations","Light & clean (like iOS weather)","Glassmorphism","Gradient sky (changes with weather)"] },
        { id:"q4", text:"Extras?", type:"multi",
          options:["Search any city","Auto-detect location","Temperature unit toggle (°C/°F)","Weather alerts","Clothing recommendation","Save favorite cities","Background changes with weather"] },
      ];

    if (u.includes("quiz") || u.includes("trivia") || u.includes("test"))
      return [
        { id:"q1", text:"Quiz type?", type:"choice",
          options:["General knowledge","Technology & coding","Science","History","Sports","Bollywood / entertainment","Geography","Mathematics","Custom topic"] },
        { id:"q2", text:"Quiz features?", type:"multi",
          options:["Multiple choice (4 options)","True/False questions","Timer per question (30s)","Score tracking","Leaderboard (localStorage)","Difficulty levels","Category selection","Explanation after answer","Share score"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Dark gaming style","Colorful & fun","Clean minimal","Kahoot-like bright"] },
        { id:"q4", text:"Questions source?", type:"choice",
          options:["Hardcoded 20 questions","Open Trivia DB API (free)","Custom questions (fill in form)","Mix of categories"] },
      ];

    if (u.includes("chat") || u.includes("message") || u.includes("whatsapp") || u.includes("messenger"))
      return [
        { id:"q1", text:"Chat type?", type:"choice",
          options:["WhatsApp-style (contacts + chat)","Discord-style (channels + DM)","Simple 2-person chat","Group chat room","AI chatbot (auto-reply)","Customer support chat widget"] },
        { id:"q2", text:"Features?", type:"multi",
          options:["Message bubbles (send/received style)","Typing indicator (...)","Read receipts (✓✓)","Emoji picker","File/image share","Online/offline status","Message search","Message reactions (emoji)","Reply to message","Dark mode"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["WhatsApp green dark","WhatsApp light","Discord dark","iMessage blue","Telegram style","Custom dark","Material Design"] },
        { id:"q4", text:"Demo behavior?", type:"choice",
          options:["Auto-reply bot (simulated)","Pre-loaded conversation","Both sides manually","AI responses (using API)"] },
      ];

    if (u.includes("todo") || u.includes("task") || u.includes("kanban") || u.includes("planner") || u.includes("productivity"))
      return [
        { id:"q1", text:"Task app type?", type:"choice",
          options:["Kanban board (Trello-like)","Simple list (Google Tasks-like)","Calendar + tasks","Project manager (Asana-like)","Notion-like blocks","Daily planner","Habit tracker","Pomodoro + tasks"] },
        { id:"q2", text:"Features?", type:"multi",
          options:["Drag & drop cards","Priority labels (High/Med/Low)","Due date picker","Subtasks / checklist","Tags & categories","Progress % per task","Recurring tasks","Completed task archive","Search & filter","Export tasks"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Dark minimal (like Linear)","Light Notion-like","Colorful Trello-like","Glassmorphism","Material Design"] },
        { id:"q4", text:"Storage?", type:"choice",
          options:["localStorage (browser, no backend)","JSON file save","Cloud sync (simulated)"] },
      ];

    if (u.includes("portfolio") || u.includes("resume") || u.includes("cv") || u.includes("profile"))
      return [
        { id:"q1", text:"Portfolio for whom?", type:"choice",
          options:["Software/Web developer","Data Scientist / ML engineer","UI/UX Designer","Photographer","Writer / Content creator","Video editor","General professional"] },
        { id:"q2", text:"Sections?", type:"multi",
          options:["Hero with name + title","About me paragraph","Skills with icons","Work experience timeline","Projects showcase","Education","Certifications","Blog posts","Contact form","Resume PDF link"] },
        { id:"q3", text:"Theme?", type:"choice",
          options:["Dark developer (like GitHub)","Light clean","Neon terminal style","Glassmorphism","Minimal typography","Colorful creative"] },
        { id:"q4", text:"Special effects?", type:"multi",
          options:["Typing animation","Scroll reveal animations","Project filter by tech","Dark/light toggle","Particle/star background","GitHub contribution graph style","Skill progress bars","Smooth scroll + active nav"] },
      ];

    // Default more questions
    return [
      { id:"q1", text:"What to build?", type:"choice",
        options:["Weather app","Quiz / trivia game","Scientific calculator","Chat messenger","Kanban to-do","Blog / news site","Developer portfolio","Unit converter","Pomodoro timer","Dictionary app","Flashcard study app","Habit tracker"] },
      { id:"q2", text:"Key features?", type:"multi",
        options:["LocalStorage (save data)","Dark mode toggle","Search functionality","Charts & graphs","API integration","Mobile responsive","Smooth animations","User accounts","Export/import","Keyboard shortcuts"] },
      { id:"q3", text:"Visual theme?", type:"choice",
        options:["Dark minimal","Light & clean","Colorful & vibrant","Glassmorphism","Material Design","Neon dark","Pastel soft"] },
      { id:"q4", text:"Design style?", type:"choice",
        options:["Minimal & elegant","Feature-rich dashboard","Mobile-first","Desktop app feel","Playful & fun","Professional & clean"] },
    ];
  }

  return [];
}

// ══════════════════════════════════════════════════════════════
// CATEGORY PAGE COMPONENT — reused for all 8 categories
// ══════════════════════════════════════════════════════════════
function CategoryPage({ category, config, onBuild, onBack }) {
  const [step, setStep]       = useState("input"); // input | questions | building
  const [input, setInput]     = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const inputRef = useRef(null);

  useEffect(() => {
    setTimeout(() => inputRef.current?.focus(), 100);
  }, []);

  const handleInput = (val) => {
    setInput(val);
  };

  const goToQuestions = (prompt) => {
    const finalPrompt = prompt || input;
    if (!finalPrompt.trim()) return;
    setInput(finalPrompt);
    const qs = getQuestions(category, finalPrompt);
    setQuestions(qs);
    setAnswers({});
    setStep("questions");
  };

  const handleAnswer = (qid, val, multi) => {
    setAnswers(prev => {
      if (multi) {
        const c = Array.isArray(prev[qid]) ? prev[qid] : [];
        return { ...prev, [qid]: c.includes(val) ? c.filter(x=>x!==val) : [...c,val] };
      }
      return { ...prev, [qid]: val };
    });
  };

  const handleBuild = () => {
    const fa = {};
    questions.forEach(q => {
      const a = answers[q.id];
      fa[q.id] = Array.isArray(a) ? a.join(", ") : (a || "");
    });
    onBuild(input, fa, category);
  };

  const C = config.color;

  // ── INPUT STEP ─────────────────────────────────────────
  if (step === "input") return (
    <div style={{...PS.root, background: `radial-gradient(ellipse at 20% 20%, ${C}08 0%, #0d1017 60%)`}}>
      {/* Header */}
      <div style={PS.header}>
        <button style={PS.backBtn} onClick={onBack}>← Back</button>
        <div style={{display:"flex",alignItems:"center",gap:10}}>
          <div style={{...PS.catIcon, background:`${C}22`, border:`1px solid ${C}44`}}>{config.icon}</div>
          <div>
            <div style={{fontSize:18,fontWeight:800,color:"#f9fafb",fontFamily:"'Syne',sans-serif"}}>{config.label}</div>
            <div style={{fontSize:11,color:C,fontFamily:"monospace"}}>{config.desc}</div>
          </div>
        </div>
        <div style={{marginLeft:"auto",fontSize:10,color:"#374151",fontFamily:"monospace"}}>⚡ 100+ agents ready</div>
      </div>

      <div style={PS.content}>
        {/* Prompt examples */}
        <div style={PS.examplesGrid}>
          {config.examples.map((ex,i) => (
            <button key={i} onClick={() => goToQuestions(ex.text)}
              style={{...PS.exampleCard, borderColor:`${C}33`}}>
              <div style={{fontSize:28,marginBottom:8}}>{ex.emoji}</div>
              <div style={{fontSize:11,fontWeight:700,color:"#e2e8f0",marginBottom:4,fontFamily:"'Syne',sans-serif"}}>{ex.label}</div>
              <div style={{fontSize:10,color:"#6b7280",lineHeight:1.4,fontFamily:"monospace"}}>{ex.text}</div>
              <div style={{marginTop:8,fontSize:9,color:C,fontFamily:"monospace"}}>Click to build →</div>
            </button>
          ))}
        </div>

        {/* Or type your own */}
        <div style={PS.divider}>
          <div style={PS.dividerLine}/>
          <span style={PS.dividerText}>OR TYPE YOUR OWN</span>
          <div style={PS.dividerLine}/>
        </div>

        <div style={PS.inputWrap}>
          <div style={{...PS.searchBox, borderColor: input.trim() ? `${C}66` : "#1e2530"}}>
            <span style={{fontSize:18,marginRight:8,opacity:.5}}>{config.icon}</span>
            <input
              ref={inputRef}
              style={PS.searchInput}
              placeholder={`Describe your ${config.label.toLowerCase()}...`}
              value={input}
              onChange={e => handleInput(e.target.value)}
              onKeyDown={e => e.key==="Enter" && input.trim() && goToQuestions()}
            />
            <button
              style={{...PS.sendBtn, background: input.trim() ? C : "#1e2530", color: input.trim() ? "#fff":"#4b5563"}}
              onClick={() => goToQuestions()}
              disabled={!input.trim()}
            >→</button>
          </div>
          {input.trim().length > 5 && (
            <div style={{fontSize:10,color:"#4b5563",marginTop:6,fontFamily:"monospace",textAlign:"center"}}>
              ⚡ Smart questions will appear based on: "<span style={{color:C}}>{input.slice(0,40)}</span>"
            </div>
          )}
        </div>
      </div>
    </div>
  );

  // ── QUESTIONS STEP ──────────────────────────────────────
  if (step === "questions") return (
    <div style={{...PS.root, background:`radial-gradient(ellipse at 80% 10%, ${C}06 0%, #0d1017 50%)`}}>
      <div style={PS.header}>
        <button style={PS.backBtn} onClick={() => setStep("input")}>← Edit idea</button>
        <div style={{display:"flex",alignItems:"center",gap:8}}>
          <div style={{...PS.catIcon,width:28,height:28,fontSize:14,background:`${C}22`,border:`1px solid ${C}44`}}>{config.icon}</div>
          <div style={{fontSize:12,fontWeight:700,color:"#e2e8f0",fontFamily:"'Syne',sans-serif"}}>{config.label}</div>
        </div>
        <div style={{marginLeft:"auto"}}>
          <div style={{fontSize:10,color:"#4b5563",background:"#131920",border:"1px solid #1e2530",borderRadius:8,padding:"4px 10px",fontFamily:"monospace"}}>
            "{input.slice(0,35)}{input.length>35?"...":""}"
          </div>
        </div>
      </div>

      <div style={{...PS.content, maxWidth:640}}>
        {/* Title */}
        <div style={{textAlign:"center",marginBottom:24}}>
          <div style={{fontSize:22,fontWeight:800,color:"#f9fafb",fontFamily:"'Syne',sans-serif",marginBottom:6}}>
            A few quick questions
          </div>
          <div style={{fontSize:12,color:"#6b7280",fontFamily:"monospace"}}>
            These are tailored for: <span style={{color:C}}>"{input.slice(0,50)}"</span>
          </div>
        </div>

        {/* Questions */}
        <div style={{display:"flex",flexDirection:"column",gap:20}}>
          {questions.map((q, qi) => (
            <div key={q.id} style={{background:"#0d1117",border:"1px solid #1e2530",borderRadius:12,padding:16}}>
              <div style={{fontSize:12,fontWeight:600,color:"#e2e8f0",marginBottom:10,fontFamily:"'Syne',sans-serif",display:"flex",gap:8,alignItems:"center"}}>
                <span style={{width:20,height:20,borderRadius:"50%",background:`${C}22`,border:`1px solid ${C}44`,display:"flex",alignItems:"center",justifyContent:"center",fontSize:10,color:C,flexShrink:0}}>{qi+1}</span>
                {q.text}
                {q.type==="multi"&&<span style={{fontSize:9,color:"#4b5563",fontFamily:"monospace",marginLeft:"auto"}}>select multiple</span>}
              </div>
              <div style={{display:"flex",flexWrap:"wrap",gap:6}}>
                {q.options.map(opt => {
                  const sel = q.type==="multi"
                    ? (Array.isArray(answers[q.id])&&answers[q.id].includes(opt))
                    : answers[q.id]===opt;
                  return (
                    <button key={opt}
                      onClick={() => handleAnswer(q.id, opt, q.type==="multi")}
                      style={{padding:"7px 14px",borderRadius:8,border:`1px solid ${sel?C+"66":"#1e2530"}`,
                        background: sel?`${C}15`:"#131920",
                        color: sel?C:"#9ca3af",
                        cursor:"pointer",fontSize:11,fontFamily:"monospace",
                        transition:"all .15s",display:"flex",alignItems:"center",gap:5}}>
                      {q.type==="multi"&&<span style={{fontSize:10,color:sel?C:"#374151"}}>{sel?"✓":"○"}</span>}
                      {opt}
                    </button>
                  );
                })}
              </div>
            </div>
          ))}
        </div>

        {/* Build buttons */}
        <div style={{display:"flex",gap:10,marginTop:20}}>
          <button
            onClick={() => onBuild(input, {}, category)}
            style={{flex:1,padding:"12px",borderRadius:10,background:"#131920",border:"1px solid #1e2530",color:"#6b7280",cursor:"pointer",fontSize:12,fontFamily:"monospace"}}>
            Skip → Build Now
          </button>
          <button
            onClick={handleBuild}
            style={{flex:2,padding:"12px",borderRadius:10,background:C,border:"none",color:"#fff",cursor:"pointer",fontSize:13,fontWeight:700,fontFamily:"'Syne',sans-serif"}}>
            ⚡ Build {config.label}
          </button>
        </div>
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
// CATEGORY CONFIGS — each has icon, color, desc, examples
// ══════════════════════════════════════════════════════════════
const CATS = {
  website: {
    icon:"🌐", label:"Website", color:"#3b82f6",
    desc:"Landing pages, portfolios, blogs, corporate sites",
    examples:[
      {emoji:"👤",label:"Portfolio",          text:"create portfolio website for data scientist"},
      {emoji:"🚀",label:"Startup Landing",    text:"create startup landing page for AI SaaS company"},
      {emoji:"🍕",label:"Restaurant",         text:"create restaurant website with menu and online booking"},
      {emoji:"📰",label:"Blog",               text:"create tech blog website with dark theme"},
      {emoji:"🏢",label:"Corporate",          text:"create corporate website for IT company"},
      {emoji:"🎨",label:"Creative Agency",    text:"create creative design agency website"},
      {emoji:"💚",label:"NGO",                text:"create NGO website for education charity organization"},
      {emoji:"🛍️",label:"Product Page",       text:"create product landing page for mobile app"},
    ],
  },
  mobile: {
    icon:"📱", label:"Mobile App", color:"#8b5cf6",
    desc:"Python apps: Flask / Django / FastAPI + SQLite",
    examples:[
      {emoji:"🔢",label:"Calculator",         text:"create scientific calculator app with history using Flask"},
      {emoji:"🎯",label:"Number Guessing",    text:"create number guessing game with score tracking"},
      {emoji:"📚",label:"Grade Tracker",      text:"create student grade and CGPA calculator app"},
      {emoji:"💰",label:"Expense Tracker",    text:"create personal expense tracker with charts using Flask"},
      {emoji:"📝",label:"Todo App",           text:"create kanban todo app with SQLite using Flask"},
      {emoji:"🏃",label:"Health Tracker",     text:"create BMI and health tracker app with FastAPI"},
      {emoji:"🎓",label:"Quiz App",           text:"create Python quiz game with leaderboard using Django"},
      {emoji:"📅",label:"Study Planner",      text:"create student study planner with timetable using Flask"},
    ],
  },
  design: {
    icon:"🎨", label:"Design Tool", color:"#ec4899",
    desc:"Photo editors, background remover, Canva-like tools",
    examples:[
      {emoji:"🖼️",label:"Photo Editor",       text:"create photo editor with Instagram-style filters"},
      {emoji:"✂️",label:"BG Remover",         text:"create background remover tool with Replace background"},
      {emoji:"📢",label:"Banner Maker",       text:"create social media banner maker with templates"},
      {emoji:"🎯",label:"Logo Maker",         text:"create logo maker tool with shapes and fonts"},
      {emoji:"📸",label:"Thumbnail Maker",    text:"create YouTube thumbnail maker with text overlay"},
      {emoji:"🎨",label:"Color Palette",      text:"create color palette generator and picker tool"},
      {emoji:"✍️",label:"Text Effects",       text:"create text effect designer with shadows and gradients"},
      {emoji:"📐",label:"Canva Clone",        text:"create Canva-like design tool with drag and drop"},
    ],
  },
  ppt: {
    icon:"📊", label:"Slides / PPT", color:"#f59e0b",
    desc:"Auto-generate beautiful presentations instantly",
    examples:[
      {emoji:"🤖",label:"AI Presentation",    text:"create ppt presentation about artificial intelligence"},
      {emoji:"💼",label:"Startup Pitch",      text:"create startup pitch deck for investor meeting"},
      {emoji:"📱",label:"Product Demo",       text:"create product demo presentation for mobile app"},
      {emoji:"🎓",label:"Educational",        text:"create educational slides about machine learning basics"},
      {emoji:"📊",label:"Sales Report",       text:"create quarterly sales report presentation with charts"},
      {emoji:"🔬",label:"Research Paper",     text:"create research paper presentation about climate change"},
      {emoji:"🏢",label:"Company Overview",   text:"create company overview presentation for new employees"},
      {emoji:"🚀",label:"Project Proposal",   text:"create project proposal presentation for client approval"},
    ],
  },
  game: {
    icon:"🎮", label:"Game", color:"#10b981",
    desc:"Browser games: Rules, UI, Logic, Input",
    examples:[
      {emoji:"♟️",label:"Chess Game",    text:"create fully functional chess game with strict rules"},
      {emoji:"🎲",label:"Ludo Board",    text:"create 4-player ludo board game with dice roll"},
      {emoji:"🐍",label:"Snake Game",   text:"create retro snake game with score tracking"},
      {emoji:"🧩",label:"Sudoku",  text:"create sudoku puzzle game with difficulty levels"},
      {emoji:"🏓",label:"Pong",   text:"create classic pong game vs AI"},
      {emoji:"🃏",label:"Solitaire",       text:"create klondike solitaire card game"},
      {emoji:"🏎️",label:"Racing",    text:"create 2d top down car racing game"},
      {emoji:"⚔️",label:"RPG",     text:"create simple turn based RPG battle game"},
    ],
  },
  ml: {
    icon:"🤖", label:"ML Project", color:"#6366f1",
    desc:"Full ML projects: data → model → prediction UI",
    examples:[
      {emoji:"🏠",label:"House Price",        text:"create house price prediction ML project with sklearn"},
      {emoji:"🎬",label:"Movie Recommender",  text:"create movie recommendation system using collaborative filtering"},
      {emoji:"📧",label:"Spam Detector",      text:"create email spam classifier using Naive Bayes"},
      {emoji:"📉",label:"Churn Prediction",   text:"create customer churn prediction for telecom company"},
      {emoji:"💭",label:"Sentiment Analysis", text:"create sentiment analysis for product reviews using NLP"},
      {emoji:"💳",label:"Fraud Detection",    text:"create credit card fraud detection using Random Forest"},
      {emoji:"🩺",label:"Disease Prediction", text:"create diabetes prediction ML project using SVM"},
      {emoji:"👥",label:"Customer Segments",  text:"create customer segmentation using K-means clustering"},
    ],
  },
  ecommerce: {
    icon:"🛒", label:"E-Commerce", color:"#f97316",
    desc:"Shopping sites only: catalog, cart, checkout, payment",
    examples:[
      {emoji:"🛍️",label:"Flipkart Clone",     text:"create flipkart-like ecommerce website for Indian market"},
      {emoji:"📦",label:"Amazon Clone",       text:"create amazon-style multi-category shopping website"},
      {emoji:"👗",label:"Fashion Store",      text:"create women fashion boutique with size selector"},
      {emoji:"💻",label:"Electronics Shop",   text:"create electronics store for mobiles and laptops"},
      {emoji:"🌿",label:"Grocery Store",      text:"create online grocery delivery store like BigBasket"},
      {emoji:"💄",label:"Beauty Store",       text:"create beauty and cosmetics store like Nykaa"},
      {emoji:"📚",label:"Books Store",        text:"create online bookstore with genre filter"},
      {emoji:"👟",label:"Shoes Store",        text:"create footwear store with size and brand filter"},
    ],
  },
  more: {
    icon:"⋯", label:"More Apps", color:"#64748b",
    desc:"Weather, quiz, chat, todo, portfolio & more",
    examples:[
      {emoji:"🌤️",label:"Weather App",        text:"create weather app with 7-day forecast and maps"},
      {emoji:"❓",label:"Quiz App",           text:"create general knowledge quiz app with timer and leaderboard"},
      {emoji:"💬",label:"Chat Messenger",     text:"create WhatsApp-style chat messenger app"},
      {emoji:"✅",label:"Kanban Todo",        text:"create Kanban board todo app with drag and drop"},
      {emoji:"👨‍💻",label:"Dev Portfolio",     text:"create developer portfolio with projects and GitHub"},
      {emoji:"🍅",label:"Pomodoro Timer",     text:"create Pomodoro productivity timer with task list"},
      {emoji:"📖",label:"Blog Site",         text:"create blog website with article cards and search"},
      {emoji:"🔄",label:"Unit Converter",    text:"create unit converter app with all measurement types"},
    ],
  },
};

// ══════════════════════════════════════════════════════════════
// HOME PAGE
// ══════════════════════════════════════════════════════════════
function HomePage({ onSelectCategory, projects }) {
  return (
    <div style={H.root}>
      <aside style={H.sidebar}>
        <div style={H.brand}>
          <div style={H.brandIcon}>⚡</div>
          <div>
            <div style={H.brandName}>S.E.A.D.S.</div>
            <div style={H.brandSub}>v13 · 100+ agents</div>
          </div>
        </div>
        <div style={H.sectionLabel}>RECENT</div>
        <div style={{flex:1,overflowY:"auto",padding:"0 8px"}}>
          {projects.slice(0,12).map((p,i) => (
            <div key={i} style={{display:"flex",alignItems:"center",gap:6,padding:"5px 7px",borderRadius:5,color:"#4b5563",fontSize:10,fontFamily:"monospace",overflow:"hidden"}}>
              <span style={{fontSize:11,flexShrink:0}}>{p.type==="fullstack"?"🏗️":"📄"}</span>
              <span style={{overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{p.name}</span>
            </div>
          ))}
          {!projects.length && <div style={{padding:"10px",fontSize:10,color:"#1e2530",textAlign:"center"}}>No projects yet</div>}
        </div>
        <div style={{padding:"10px 12px",borderTop:"1px solid #1e2530"}}>
          <div style={{fontSize:9,color:"#4ade80",fontFamily:"monospace",marginBottom:3}}>● Backend LIVE</div>
          <div style={{fontSize:9,color:"#374151",fontFamily:"monospace"}}>💎 10K tokens / agent</div>
        </div>
      </aside>

      <main style={H.main}>
        <div style={H.center}>
          <div style={H.workspaceBadge}>
            <div style={H.avatar}>R</div>
            <span style={{fontSize:13,color:"#9ca3af",fontFamily:"'Syne',sans-serif"}}>Ragul's Workspace</span>
            <span style={{color:"#374151"}}>▾</span>
          </div>
          <h1 style={H.headline}>Hi Ragul, what do you want to make?</h1>
          <p style={{fontSize:13,color:"#4b5563",fontFamily:"monospace",marginBottom:8}}>Choose a category below to get started ↓</p>

          {/* Category grid */}
          <div style={H.catGrid}>
            {Object.entries(CATS).map(([id, cat]) => (
              <button key={id} onClick={() => onSelectCategory(id, cat)}
                style={{...H.catCard, "--c": cat.color}}>
                <div style={{...H.catCardIcon, background:`${cat.color}18`, border:`1px solid ${cat.color}33`}}>
                  {cat.icon}
                </div>
                <div style={H.catCardLabel}>{cat.label}</div>
                <div style={H.catCardDesc}>{cat.desc}</div>
                <div style={{display:"flex",gap:4,flexWrap:"wrap",marginTop:8}}>
                  {cat.examples.slice(0,3).map(e=>(
                    <span key={e.label} style={{fontSize:9,padding:"2px 6px",borderRadius:8,background:`${cat.color}11`,border:`1px solid ${cat.color}22`,color:cat.color,fontFamily:"monospace"}}>{e.label}</span>
                  ))}
                  <span style={{fontSize:9,padding:"2px 6px",borderRadius:8,background:"#131920",border:"1px solid #1e2530",color:"#374151",fontFamily:"monospace"}}>+{cat.examples.length-3} more</span>
                </div>
                <div style={{marginTop:10,padding:"6px 0",borderTop:`1px solid ${cat.color}22`,fontSize:10,color:cat.color,fontFamily:"monospace",display:"flex",alignItems:"center",gap:4}}>
                  Open {cat.label} →
                </div>
              </button>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
// BUILDING / PREVIEW (same as before, simplified)
// ══════════════════════════════════════════════════════════════
function BuildingPage({ idea, category }) {
  const C = (CATS[category]||CATS.website).color;
  const phases = ["Planning","Running Agents","Quality Check","Live Preview"];
  const [phase, setPhase] = useState(0);
  useEffect(()=>{
    const t = setInterval(()=>setPhase(p=>p<3?p+1:p),2000);
    return ()=>clearInterval(t);
  },[]);
  return (
    <div style={{display:"flex",alignItems:"center",justifyContent:"center",height:"100vh",background:"#0d1017",flexDirection:"column",gap:20,fontFamily:"monospace"}}>
      <div style={{width:48,height:48,borderRadius:"50%",border:`3px solid #1e2530`,borderTopColor:C,animation:"spin 1s linear infinite"}}/>
      <div style={{fontSize:16,fontWeight:700,color:"#e2e8f0",fontFamily:"'Syne',sans-serif"}}>Building {idea.slice(0,40)}...</div>
      <div style={{display:"flex",gap:8}}>
        {phases.map((p,i)=>(
          <div key={p} style={{fontSize:10,padding:"4px 10px",borderRadius:6,background:i<=phase?`${C}22`:"#131920",border:`1px solid ${i<=phase?C+"44":"#1e2530"}`,color:i<=phase?C:"#374151"}}>{i<=phase?"✓ ":""}{p}</div>
        ))}
      </div>
      <style>{`@keyframes spin{to{transform:rotate(360deg)}}`}</style>
    </div>
  );
}

function PreviewPage({ idea, previewHtml, files, buildLogs, agentsUsed, onHome, onEdit, category }) {
  const [tab, setTab] = useState("canvas");
  const [fileIdx, setFileIdx] = useState(0);
  const [ikey, setIkey] = useState(0);
  const C = (CATS[category]||CATS.website).color;

  const download = (i) => {
    const f = files[i];
    if (!f) return;
    const b=new Blob([f.content],{type:"text/plain"});
    const u=URL.createObjectURL(b); const a=document.createElement("a");
    a.href=u; a.download=f.name; a.click(); URL.revokeObjectURL(u);
  };

  return (
    <div style={{display:"flex",width:"100vw",height:"100vh",background:"#0d1017",fontFamily:"monospace",overflow:"hidden"}}>
      {/* Log sidebar */}
      <div style={{width:272,flexShrink:0,background:"#080c10",borderRight:"1px solid #1e2530",display:"flex",flexDirection:"column",overflow:"hidden"}}>
        {/* Header */}
        <div style={{padding:"10px 14px",borderBottom:"1px solid #1e2530",display:"flex",alignItems:"center",gap:8}}>
          <button onClick={onHome} style={{background:"none",border:"1px solid #1e2530",borderRadius:6,color:"#6b7280",cursor:"pointer",padding:"4px 8px",fontSize:10}}>← Home</button>
          <span style={{fontSize:9,padding:"2px 7px",borderRadius:10,background:"rgba(74,222,128,.1)",border:"1px solid rgba(74,222,128,.3)",color:"#4ade80"}}>● LIVE</span>
        </div>
        {/* Build idea */}
        <div style={{padding:"10px 14px",borderBottom:"1px solid #1e2530"}}>
          <div style={{fontSize:9,color:"#374151",marginBottom:3}}>BUILT:</div>
          <div style={{fontSize:10,color:"#e2e8f0",lineHeight:1.4,wordBreak:"break-word"}}>"{idea}"</div>
          <div style={{marginTop:4,fontSize:9,color:C}}>{(CATS[category]||CATS.website).icon} {(CATS[category]||CATS.website).label} Pipeline</div>
        </div>
        {/* Logs */}
        <div style={{flex:1,overflowY:"auto",padding:12,display:"flex",flexDirection:"column",gap:8}}>
          {/* Phases */}
          {["Planning","Agents Running","Quality Check","Live Preview"].map((ph,i)=>(
            <div key={ph} style={{display:"flex",alignItems:"center",gap:6,fontSize:9,color:"#4ade80"}}>
              <div style={{width:5,height:5,borderRadius:"50%",background:"#4ade80",flexShrink:0}}/>✓ {ph}
            </div>
          ))}
          {/* Plan logs */}
          {buildLogs.plan?.length>0&&(
            <div>
              <div style={{fontSize:8,color:"#6366f1",letterSpacing:1.5,textTransform:"uppercase",marginBottom:3}}>PHASE 1 — PLANNING</div>
              {buildLogs.plan.map((l,i)=><div key={i} style={{fontSize:9,color:"#6b7280",lineHeight:1.5,display:"flex",gap:4}}><span style={{color:"#4ade80",flexShrink:0}}>●</span>{l}</div>)}
            </div>
          )}
          {/* Agents */}
          <div>
            <div style={{fontSize:8,color:"#6366f1",letterSpacing:1.5,textTransform:"uppercase",marginBottom:3}}>PHASE 2 — {agentsUsed.length} AGENTS</div>
            <div style={{display:"flex",flexWrap:"wrap",gap:2}}>
              {agentsUsed.map((a,i)=><span key={i} style={{fontSize:8,color:"#6366f1",background:"rgba(99,102,241,.08)",border:"1px solid rgba(99,102,241,.15)",borderRadius:2,padding:"1px 4px"}}>[{a}]</span>)}
            </div>
          </div>
          {/* Code/Test */}
          {buildLogs.code?.map((l,i)=><div key={i} style={{fontSize:9,color:"#6b7280",display:"flex",gap:4}}><span style={{color:"#4ade80",flexShrink:0}}>●</span>{l}</div>)}
          {buildLogs.test?.map((l,i)=><div key={i} style={{fontSize:9,color:"#6b7280",display:"flex",gap:4}}><span style={{color:"#4ade80",flexShrink:0}}>●</span>{l}</div>)}
          <div style={{fontSize:10,color:"#4ade80",fontWeight:600}}>✅ {idea.slice(0,30)} is LIVE! 🎉</div>
        </div>
        {/* Edit input */}
        <div style={{flexShrink:0,padding:"8px 10px",borderTop:"1px solid #1e2530",display:"flex",gap:5}}>
          <input id="edi" placeholder="Edit or improve..."
            style={{flex:1,background:"#131920",border:"1px solid #1e2530",borderRadius:7,padding:"6px 8px",fontSize:9,color:"#e2e8f0",outline:"none",fontFamily:"monospace"}}
            onKeyDown={e=>{if(e.key==="Enter"&&e.target.value.trim()){onEdit(e.target.value.trim());e.target.value="";}}}
          />
          <button style={{width:26,height:26,borderRadius:6,background:C,border:"none",color:"#fff",cursor:"pointer",fontSize:12}}
            onClick={()=>{const i=document.getElementById("edi");if(i.value.trim()){onEdit(i.value.trim());i.value="";}}}>↑</button>
        </div>
      </div>

      {/* Preview area */}
      <div style={{flex:1,display:"flex",flexDirection:"column",overflow:"hidden"}}>
        {/* Tabs */}
        <div style={{display:"flex",alignItems:"center",borderBottom:"1px solid #1e2530",background:"#0d1017",flexShrink:0,height:40}}>
          {["canvas","files","code"].map(t=>(
            <button key={t} onClick={()=>setTab(t)}
              style={{padding:"0 16px",height:"100%",background:"none",border:"none",borderBottom:`2px solid ${tab===t?C:"transparent"}`,color:tab===t?"#e2e8f0":"#4b5563",cursor:"pointer",fontSize:10,textTransform:"uppercase",letterSpacing:1}}>
              {t==="canvas"?"◉ Canvas":t==="files"?`📁 Files (${files.length})`:"📄 Code"}
            </button>
          ))}
          <div style={{marginLeft:"auto",display:"flex",gap:6,paddingRight:12,alignItems:"center"}}>
            <span style={{fontSize:9,padding:"2px 8px",borderRadius:10,background:`${C}18`,border:`1px solid ${C}33`,color:C}}>⚡ {agentsUsed.length} agents</span>
            {[["↺","Refresh",()=>setIkey(k=>k+1)],["⬇","Download",()=>download(fileIdx)],["⤢","New tab",()=>{const w=window.open();w.document.write(previewHtml);}],["⎘","Copy",()=>navigator.clipboard.writeText(previewHtml)]].map(([i,t,f])=>(
              <button key={i} title={t} onClick={f} style={{width:24,height:24,borderRadius:5,background:"#131920",border:"1px solid #1e2530",color:"#6b7280",cursor:"pointer",fontSize:11}}>{i}</button>
            ))}
          </div>
        </div>

        {/* Canvas */}
        {tab==="canvas"&&<iframe key={ikey} srcDoc={previewHtml} sandbox="allow-scripts allow-same-origin allow-modals" style={{flex:1,border:"none",display:"block"}} title="preview"/>}

        {/* Files */}
        {tab==="files"&&(
          <div style={{flex:1,padding:20,overflowY:"auto"}}>
            <div style={{marginBottom:12,fontSize:10,color:"#4b5563"}}>📁 Saved to: E:\seads\online_app\{idea.replace(/ /g,"-").toLowerCase().slice(0,25)}\</div>
            <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(160px,1fr))",gap:10}}>
              {files.map((f,i)=>(
                <div key={i} onClick={()=>{setFileIdx(i);setTab("code");}}
                  style={{background:"#0d1117",border:`1px solid ${fileIdx===i?C+"44":"#1e2530"}`,borderRadius:10,padding:"12px 14px",cursor:"pointer"}}>
                  <div style={{fontSize:22,marginBottom:6}}>
                    {f.name.endsWith(".html")?"🌐":f.name.endsWith(".css")?"🎨":f.name.endsWith(".js")?"⚡":f.name.endsWith(".py")?"🐍":f.name.endsWith(".md")?"📝":"📄"}
                  </div>
                  <div style={{fontSize:11,color:"#e2e8f0",fontWeight:600,marginBottom:2}}>{f.name}</div>
                  <div style={{fontSize:9,color:"#374151",marginBottom:8}}>{(f.size/1024).toFixed(1)} KB</div>
                  <button onClick={e=>{e.stopPropagation();download(i);}} style={{fontSize:9,padding:"3px 8px",background:"#1e2530",border:"none",borderRadius:4,color:"#9ca3af",cursor:"pointer"}}>⬇ Save</button>
                </div>
              ))}
            </div>
            {files.length>1&&<button onClick={()=>files.forEach((_,i)=>setTimeout(()=>download(i),i*300))} style={{marginTop:12,padding:"9px 20px",background:C,border:"none",borderRadius:8,color:"#fff",cursor:"pointer",fontSize:11,fontFamily:"monospace"}}>⬇ Download All {files.length} Files</button>}
          </div>
        )}

        {/* Code */}
        {tab==="code"&&(
          <div style={{flex:1,display:"flex",flexDirection:"column",overflow:"hidden"}}>
            {files.length>1&&(
              <div style={{display:"flex",borderBottom:"1px solid #1e2530",flexShrink:0,overflowX:"auto"}}>
                {files.map((f,i)=>(
                  <button key={i} onClick={()=>setFileIdx(i)}
                    style={{padding:"6px 14px",background:"none",border:"none",borderBottom:`2px solid ${fileIdx===i?C:"transparent"}`,color:fileIdx===i?"#e2e8f0":"#4b5563",cursor:"pointer",fontSize:10,fontFamily:"monospace",whiteSpace:"nowrap"}}>
                    {f.name}
                  </button>
                ))}
              </div>
            )}
            <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",padding:"6px 12px",borderBottom:"1px solid #1e2530",flexShrink:0}}>
              <span style={{fontSize:10,color:"#9ca3af"}}>{files[fileIdx]?.name}</span>
              <div style={{display:"flex",gap:6}}>
                <button onClick={()=>{navigator.clipboard.writeText(files[fileIdx]?.content||"");}} style={{padding:"3px 10px",borderRadius:5,background:"#1e2530",border:"none",color:"#9ca3af",cursor:"pointer",fontSize:9}}>Copy</button>
                <button onClick={()=>download(fileIdx)} style={{padding:"3px 10px",borderRadius:5,background:C,border:"none",color:"#fff",cursor:"pointer",fontSize:9}}>⬇ Save</button>
              </div>
            </div>
            <pre style={{flex:1,overflow:"auto",padding:12,fontSize:9,lineHeight:1.6,color:"#9ca3af",whiteSpace:"pre-wrap",wordBreak:"break-all",margin:0}}>
              <code>{files[fileIdx]?.content||""}</code>
            </pre>
          </div>
        )}
      </div>
    </div>
  );
}

// ══════════════════════════════════════════════════════════════
// MAIN APP — routes between pages
// ══════════════════════════════════════════════════════════════
export default function App() {
  const [page, setPage]       = useState("home");   // home | category | building | preview
  const [activeCat, setActiveCat] = useState(null); // {id, config}
  const [idea, setIdea]       = useState("");
  const [previewHtml, setPreviewHtml] = useState("");
  const [files, setFiles]     = useState([]);
  const [buildLogs, setBuildLogs] = useState({plan:[],code:[],test:[]});
  const [agentsUsed, setAgentsUsed] = useState([]);
  const [projects, setProjects] = useState([]);
  const [toast, setToast]     = useState("");

  useEffect(()=>{
    fetch(`${API}/api/projects`).then(r=>r.json()).then(d=>setProjects(d.projects||[])).catch(()=>{});
  },[page]);

  const showToast = (msg) => { setToast(msg); setTimeout(()=>setToast(""),3000); };

  // Called when user selects a category chip on home
  const handleSelectCategory = (id, config) => {
    setActiveCat({ id, config });
    setPage("category");
  };

  // Called when user submits from category page
  const handleBuild = async (finalIdea, finalAnswers, categoryId) => {
    setIdea(finalIdea);
    setPage("building");
    try {
      const res = await fetch(`${API}/api/run`, {
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body: JSON.stringify({ idea:finalIdea, answers:finalAnswers, category:categoryId }),
      });
      const data = await res.json();
      setBuildLogs({ plan:data.plan_logs||[], code:data.code_logs||[], test:data.test_logs||[] });
      setAgentsUsed(data.agents_used||[]);
      setFiles(data.files||[]);
      if (data.preview_html) {
        setPreviewHtml(data.preview_html);
        setPage("preview");
      } else { setPage("home"); showToast("❌ Generation failed"); }
    } catch(e) {
      setPage("home");
      showToast("❌ Backend not running — start backend first!");
    }
  };

  const handleEdit = async (editIdea) => {
    await handleBuild(editIdea, {}, activeCat?.id || "more");
  };

  if (page==="home") return (
    <>
      <HomePage onSelectCategory={handleSelectCategory} projects={projects}/>
      {toast&&<div style={TOAST}>{toast}</div>}
      <GlobalStyles/>
    </>
  );

  if (page==="category") return (
    <>
      <CategoryPage
        category={activeCat.id}
        config={activeCat.config}
        onBuild={handleBuild}
        onBack={()=>setPage("home")}
      />
      <GlobalStyles/>
    </>
  );

  if (page==="building") return (
    <>
      <BuildingPage idea={idea} category={activeCat?.id||"more"}/>
      <GlobalStyles/>
    </>
  );

  if (page==="preview") return (
    <>
      <PreviewPage
        idea={idea}
        category={activeCat?.id||"more"}
        previewHtml={previewHtml}
        files={files}
        buildLogs={buildLogs}
        agentsUsed={agentsUsed}
        onHome={()=>setPage("home")}
        onEdit={handleEdit}
      />
      {toast&&<div style={TOAST}>{toast}</div>}
      <GlobalStyles/>
    </>
  );
}

// ── Page-level styles ─────────────────────────────────────────
const PS = {
  root:       {display:"flex",flexDirection:"column",height:"100vh",background:"#0d1017",color:"#e2e8f0",fontFamily:"monospace",overflow:"hidden"},
  header:     {display:"flex",alignItems:"center",gap:14,padding:"16px 24px",borderBottom:"1px solid #1e2530",flexShrink:0,background:"rgba(13,16,23,.95)",backdropFilter:"blur(12px)"},
  backBtn:    {background:"none",border:"1px solid #1e2530",borderRadius:7,color:"#6b7280",cursor:"pointer",padding:"6px 12px",fontSize:11,fontFamily:"monospace"},
  catIcon:    {width:44,height:44,borderRadius:12,display:"flex",alignItems:"center",justifyContent:"center",fontSize:22,flexShrink:0},
  content:    {flex:1,overflowY:"auto",padding:"24px",display:"flex",flexDirection:"column",gap:20,alignItems:"center",maxWidth:960,margin:"0 auto",width:"100%"},
  examplesGrid:{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(170px,1fr))",gap:12,width:"100%"},
  exampleCard:{background:"#0d1117",border:"1px solid",borderRadius:12,padding:"16px 14px",cursor:"pointer",textAlign:"left",transition:"all .2s",fontFamily:"monospace"},
  divider:    {display:"flex",alignItems:"center",gap:12,width:"100%",maxWidth:600},
  dividerLine:{flex:1,height:1,background:"#1e2530"},
  dividerText:{fontSize:10,color:"#374151",letterSpacing:2,textTransform:"uppercase",whiteSpace:"nowrap"},
  inputWrap:  {width:"100%",maxWidth:600},
  searchBox:  {display:"flex",alignItems:"center",background:"#0d1117",border:"2px solid",borderRadius:14,padding:"8px 8px 8px 14px",transition:"border-color .2s"},
  searchInput:{flex:1,background:"none",border:"none",outline:"none",fontSize:14,color:"#e2e8f0",fontFamily:"'Syne',sans-serif",padding:"6px 4px"},
  sendBtn:    {width:40,height:40,borderRadius:10,border:"none",cursor:"pointer",fontSize:18,fontWeight:700,transition:"all .2s",flexShrink:0},
};

const H = {
  root:      {display:"flex",width:"100vw",height:"100vh",background:"#0d1017",color:"#e2e8f0",overflow:"hidden"},
  sidebar:   {width:210,flexShrink:0,background:"#080c10",borderRight:"1px solid #1e2530",display:"flex",flexDirection:"column",overflow:"hidden"},
  brand:     {display:"flex",alignItems:"center",gap:10,padding:"16px",borderBottom:"1px solid #1e2530"},
  brandIcon: {width:34,height:34,borderRadius:8,background:"linear-gradient(135deg,#6366f1,#8b5cf6)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:17},
  brandName: {fontSize:14,fontWeight:700,color:"#fff",fontFamily:"'Syne',sans-serif"},
  brandSub:  {fontSize:9,color:"#374151",fontFamily:"monospace"},
  sectionLabel:{padding:"8px 14px",fontSize:9,color:"#374151",letterSpacing:"2px",textTransform:"uppercase",fontFamily:"monospace"},
  main:      {flex:1,overflowY:"auto",padding:"32px 24px",display:"flex",justifyContent:"center"},
  center:    {width:"100%",maxWidth:900,display:"flex",flexDirection:"column",alignItems:"center",gap:24},
  workspaceBadge:{display:"flex",alignItems:"center",gap:8,background:"#131920",border:"1px solid #1e2530",borderRadius:20,padding:"6px 16px 6px 8px",cursor:"pointer"},
  avatar:    {width:24,height:24,borderRadius:"50%",background:"linear-gradient(135deg,#6366f1,#8b5cf6)",display:"flex",alignItems:"center",justifyContent:"center",fontSize:11,fontWeight:700,color:"#fff"},
  headline:  {fontSize:"clamp(20px,3.5vw,36px)",fontWeight:800,color:"#f9fafb",textAlign:"center",fontFamily:"'Syne',sans-serif",lineHeight:1.15},
  catGrid:   {display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(200px,1fr))",gap:14,width:"100%"},
  catCard:   {background:"#0d1117",border:"1px solid #1e2530",borderRadius:14,padding:18,cursor:"pointer",textAlign:"left",transition:"all .2s"},
  catCardIcon:{width:48,height:48,borderRadius:12,display:"flex",alignItems:"center",justifyContent:"center",fontSize:24,marginBottom:10},
  catCardLabel:{fontSize:15,fontWeight:700,color:"#e2e8f0",fontFamily:"'Syne',sans-serif",marginBottom:4},
  catCardDesc:{fontSize:10,color:"#6b7280",fontFamily:"monospace",lineHeight:1.4},
};

const TOAST = {position:"fixed",bottom:24,right:24,background:"#1e2530",border:"1px solid #374151",borderRadius:10,padding:"10px 18px",fontSize:12,color:"#e2e8f0",zIndex:999,fontFamily:"monospace"};

function GlobalStyles(){return(
  <style>{`
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=JetBrains+Mono:wght@300;400;500&display=swap');
    *{box-sizing:border-box;margin:0;padding:0}
    html,body{height:100%;overflow:hidden}
    ::-webkit-scrollbar{width:3px;height:3px}
    ::-webkit-scrollbar-thumb{background:#1e2530;border-radius:2px}
    input::placeholder{color:#374151!important}
    @keyframes spin{to{transform:rotate(360deg)}}
  `}</style>
);}
