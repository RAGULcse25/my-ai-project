import { useState, useEffect, useRef } from "react";
import { CATS } from "../config/categories";

// ─── Animated Counter ─────────────────────────────────────────
function useCounter(end, duration = 2000) {
  const [val, setVal] = useState(0);
  useEffect(() => {
    let start = 0;
    const step = end / (duration / 16);
    const timer = setInterval(() => {
      start += step;
      if (start >= end) { setVal(end); clearInterval(timer); }
      else setVal(Math.floor(start));
    }, 16);
    return () => clearInterval(timer);
  }, [end, duration]);
  return val;
}

// ─── Stat Badge ───────────────────────────────────────────────
function StatBadge({ label, value, suffix = "", color }) {
  const count = useCounter(value);
  return (
    <div style={{
      display: "flex", flexDirection: "column", alignItems: "center",
      padding: "12px 22px", borderRadius: 14,
      background: "rgba(255,255,255,0.03)",
      border: `1px solid ${color}25`,
      backdropFilter: "blur(16px)",
      boxShadow: `0 0 24px ${color}10`,
      transition: "all 0.3s ease",
    }}
      onMouseEnter={e => { e.currentTarget.style.boxShadow=`0 0 32px ${color}25`; e.currentTarget.style.transform="translateY(-2px)"; }}
      onMouseLeave={e => { e.currentTarget.style.boxShadow=`0 0 24px ${color}10`; e.currentTarget.style.transform="translateY(0)"; }}
    >
      <span style={{ fontSize: 22, fontWeight: 900, color, fontFamily: "'Syne', sans-serif" }}>
        {count}{suffix}
      </span>
      <span style={{ fontSize: 9, color: "#4b5563", fontFamily: "monospace", letterSpacing: "1.5px", textTransform: "uppercase", marginTop: 3 }}>
        {label}
      </span>
    </div>
  );
}

// ─── Category Card ────────────────────────────────────────────
function CatCard({ id, cat, onClick, idx }) {
  const [hovered, setHovered] = useState(false);
  const [entered, setEntered] = useState(false);
  useEffect(() => { const t = setTimeout(() => setEntered(true), idx * 80); return () => clearTimeout(t); }, [idx]);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        position: "relative", textAlign: "left", overflow: "hidden",
        background: hovered
          ? `linear-gradient(145deg, rgba(255,255,255,0.04), ${cat.color}12)`
          : "rgba(255,255,255,0.02)",
        border: `1px solid ${hovered ? cat.color + "55" : "rgba(255,255,255,0.07)"}`,
        borderRadius: 22, padding: "22px 20px", cursor: "pointer",
        backdropFilter: "blur(16px)",
        transition: "all 0.4s cubic-bezier(0.2,0.8,0.2,1)",
        transform: hovered ? "translateY(-6px) scale(1.02)" : entered ? "translateY(0) scale(1)" : "translateY(25px) scale(0.95)",
        opacity: entered ? 1 : 0,
        boxShadow: hovered
          ? `0 20px 50px ${cat.color}18, 0 0 0 1px ${cat.color}15, inset 0 1px 0 rgba(255,255,255,0.08)`
          : "0 4px 20px rgba(0,0,0,0.25)",
      }}
    >
      {/* Glow orb on hover */}
      {hovered && (
        <div style={{
          position: "absolute", top: -50, right: -50, width: 150, height: 150,
          borderRadius: "50%", pointerEvents: "none",
          background: `radial-gradient(circle, ${cat.color}28, transparent 70%)`,
        }} />
      )}
      {/* Shimmer line on hover */}
      {hovered && (
        <div style={{
          position: "absolute", inset: 0, pointerEvents: "none",
          background: `linear-gradient(90deg, transparent, ${cat.color}08, transparent)`,
          animation: "shimmerPass 1.8s ease infinite",
        }} />
      )}

      {/* Icon */}
      <div style={{
        width: 52, height: 52, borderRadius: 16, marginBottom: 12,
        display: "flex", alignItems: "center", justifyContent: "center",
        fontSize: 24, background: `${cat.color}15`,
        border: `1px solid ${cat.color}30`,
        boxShadow: hovered ? `0 0 24px ${cat.color}35` : "none",
        transition: "all 0.35s ease",
        transform: hovered ? "scale(1.1) rotate(5deg)" : "scale(1) rotate(0deg)",
      }}>{cat.icon}</div>

      {/* Label */}
      <div style={{ fontSize: 15, fontWeight: 800, color: "#f0f4ff", fontFamily: "'Syne', sans-serif", marginBottom: 5 }}>
        {cat.label}
      </div>

      {/* Desc */}
      <div style={{ fontSize: 10, color: "#4b5563", fontFamily: "monospace", lineHeight: 1.6, marginBottom: 10 }}>
        {cat.desc}
      </div>

      {/* Example chips */}
      <div style={{ display: "flex", gap: 4, flexWrap: "wrap", marginBottom: 10 }}>
        {cat.examples.slice(0, 3).map(e => (
          <span key={e.label} style={{
            fontSize: 9, padding: "3px 9px", borderRadius: 20,
            background: `${cat.color}12`, border: `1px solid ${cat.color}28`,
            color: cat.color, fontFamily: "monospace", fontWeight: 600,
          }}>{e.label}</span>
        ))}
        <span style={{
          fontSize: 9, padding: "3px 9px", borderRadius: 20,
          background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.07)",
          color: "#374151", fontFamily: "monospace",
        }}>+{cat.examples.length - 3} more</span>
      </div>

      {/* CTA */}
      <div style={{
        paddingTop: 10, borderTop: `1px solid ${cat.color}18`,
        display: "flex", alignItems: "center", justifyContent: "space-between",
        fontSize: 10, color: hovered ? cat.color : "#374151",
        fontFamily: "monospace", fontWeight: 700, transition: "color 0.2s ease",
      }}>
        <span>Open {cat.label}</span>
        <span style={{ transform: hovered ? "translateX(5px)" : "translateX(0)", transition: "transform 0.2s ease" }}>→</span>
      </div>
    </button>
  );
}

// ─── Sidebar Project Item ─────────────────────────────────────
function ProjectItem({ project, idx }) {
  const [hovered, setHovered] = useState(false);
  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        display: "flex", alignItems: "center", gap: 7,
        padding: "6px 8px", borderRadius: 8, cursor: "pointer",
        background: hovered ? "rgba(196,181,253,0.07)" : "transparent",
        border: `1px solid ${hovered ? "rgba(196,181,253,0.2)" : "transparent"}`,
        transition: "all 0.2s ease",
        animation: `slideInLeft 0.3s ease ${idx * 50}ms both`,
      }}
    >
      <span style={{ fontSize: 12, flexShrink: 0 }}>
        {project.type === "fullstack" ? "🏗️" : "📄"}
      </span>
      <span style={{
        fontSize: 9.5, fontFamily: "monospace",
        color: hovered ? "#c4b5fd" : "#4b5563",
        overflow: "hidden", textOverflow: "ellipsis", whiteSpace: "nowrap",
        transition: "color 0.2s",
      }}>{project.name}</span>
    </div>
  );
}

// ─── Main HomePage ────────────────────────────────────────────
export default function HomePage({ onSelectCategory, projects }) {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchFocused, setSearchFocused] = useState(false);
  const [time, setTime] = useState(new Date());
  const canvasRef = useRef(null);

  useEffect(() => { const t = setInterval(() => setTime(new Date()), 1000); return () => clearInterval(t); }, []);

  // Pastel animated mesh background
  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext("2d");
    let animId;

    const resize = () => { canvas.width = window.innerWidth; canvas.height = window.innerHeight; };
    resize();
    window.addEventListener("resize", resize);

    // Pastel anime node colors
    const nodeColors = ["rgba(196,181,253,", "rgba(147,197,253,", "rgba(249,168,212,", "rgba(134,239,172,"];

    const nodes = Array.from({ length: 45 }, (_, i) => ({
      x: Math.random() * window.innerWidth,
      y: Math.random() * window.innerHeight,
      vx: (Math.random() - 0.5) * 0.35,
      vy: (Math.random() - 0.5) * 0.35,
      r: Math.random() * 1.8 + 0.5,
      colorIdx: i % nodeColors.length,
    }));

    const draw = () => {
      ctx.clearRect(0, 0, canvas.width, canvas.height);
      nodes.forEach(n => {
        n.x += n.vx; n.y += n.vy;
        if (n.x < 0 || n.x > canvas.width)  n.vx *= -1;
        if (n.y < 0 || n.y > canvas.height) n.vy *= -1;
      });
      // Connections
      for (let i = 0; i < nodes.length; i++) {
        for (let j = i + 1; j < nodes.length; j++) {
          const dx = nodes[i].x - nodes[j].x;
          const dy = nodes[i].y - nodes[j].y;
          const dist = Math.sqrt(dx * dx + dy * dy);
          if (dist < 130) {
            ctx.beginPath();
            ctx.strokeStyle = `rgba(196,181,253,${0.06 * (1 - dist / 130)})`;
            ctx.lineWidth = 0.5;
            ctx.moveTo(nodes[i].x, nodes[i].y);
            ctx.lineTo(nodes[j].x, nodes[j].y);
            ctx.stroke();
          }
        }
      }
      // Nodes
      nodes.forEach(n => {
        ctx.beginPath();
        ctx.arc(n.x, n.y, n.r, 0, Math.PI * 2);
        ctx.fillStyle = nodeColors[n.colorIdx] + "0.45)";
        ctx.fill();
      });
      animId = requestAnimationFrame(draw);
    };
    draw();
    return () => { cancelAnimationFrame(animId); window.removeEventListener("resize", resize); };
  }, []);

  const hour = time.getHours();
  const greeting = hour < 12 ? "Good Morning" : hour < 17 ? "Good Afternoon" : "Good Evening";
  const dayName = time.toLocaleDateString("en-US", { weekday: "long" });

  const filteredCats = searchQuery
    ? Object.entries(CATS).filter(([id, cat]) =>
        cat.label.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cat.desc.toLowerCase().includes(searchQuery.toLowerCase()) ||
        cat.examples.some(e => e.label.toLowerCase().includes(searchQuery.toLowerCase()))
      )
    : Object.entries(CATS);

  return (
    <div style={{ display:"flex", width:"100vw", height:"100vh", overflow:"hidden", position:"relative", background:"#070b14" }}>

      {/* Canvas mesh */}
      <canvas ref={canvasRef} style={{ position:"absolute", inset:0, pointerEvents:"none", zIndex:0 }} />

      {/* Ambient glow blobs */}
      <div style={{ position:"absolute", top:"15%", left:"35%", width:600, height:600, borderRadius:"50%", background:"radial-gradient(circle, rgba(196,181,253,0.05) 0%, transparent 70%)", pointerEvents:"none", zIndex:0 }} />
      <div style={{ position:"absolute", bottom:"10%", right:"10%", width:400, height:400, borderRadius:"50%", background:"radial-gradient(circle, rgba(249,168,212,0.04) 0%, transparent 70%)", pointerEvents:"none", zIndex:0 }} />

      {/* ── SIDEBAR ─────────────────────────────────────────── */}
      <aside style={{
        width:220, flexShrink:0, zIndex:10,
        background:"rgba(7,11,20,0.95)",
        borderRight:"1px solid rgba(255,255,255,0.06)",
        display:"flex", flexDirection:"column", overflow:"hidden",
        backdropFilter:"blur(24px)",
      }}>
        {/* Brand */}
        <div style={{ padding:"18px 16px", borderBottom:"1px solid rgba(255,255,255,0.06)", display:"flex", alignItems:"center", gap:10 }}>
          <div style={{
            width:38, height:38, borderRadius:12, flexShrink:0,
            background:"linear-gradient(135deg, #c4b5fd, #93c5fd, #f9a8d4)",
            display:"flex", alignItems:"center", justifyContent:"center",
            fontSize:18, animation:"animeGlow 3s ease-in-out infinite",
            boxShadow:"0 0 20px rgba(196,181,253,0.4)",
          }}>⚡</div>
          <div>
            <div style={{ fontSize:15, fontWeight:900, color:"#fff", fontFamily:"'Syne', sans-serif", letterSpacing:"0.5px" }}>
              S.E.A.D.S.
            </div>
            <div style={{ fontSize:8.5, color:"#374151", fontFamily:"monospace" }}>
              v14 · 100+ agents · Claude 4.6
            </div>
          </div>
        </div>

        {/* Live Clock */}
        <div style={{ padding:"10px 16px", borderBottom:"1px solid rgba(255,255,255,0.05)" }}>
          <div style={{
            fontSize:18, fontWeight:800, fontFamily:"'Syne', sans-serif",
            background:"linear-gradient(135deg, #c4b5fd, #93c5fd)",
            WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent",
          }}>
            {time.toLocaleTimeString("en-US", { hour:"2-digit", minute:"2-digit", second:"2-digit" })}
          </div>
          <div style={{ fontSize:9, color:"#374151", fontFamily:"monospace" }}>
            {dayName}, {time.toLocaleDateString("en-US", { month:"short", day:"numeric", year:"numeric" })}
          </div>
        </div>

        {/* Status pills */}
        <div style={{ padding:"10px 12px", borderBottom:"1px solid rgba(255,255,255,0.05)", display:"flex", gap:6 }}>
          <div style={{ flex:1, background:"rgba(134,239,172,0.07)", border:"1px solid rgba(134,239,172,0.2)", borderRadius:8, padding:"6px 8px", textAlign:"center" }}>
            <div style={{ fontSize:8, color:"#86efac", fontFamily:"monospace" }}>● BACKEND LIVE</div>
          </div>
          <div style={{ flex:1, background:"rgba(196,181,253,0.07)", border:"1px solid rgba(196,181,253,0.2)", borderRadius:8, padding:"6px 8px", textAlign:"center" }}>
            <div style={{ fontSize:8, color:"#c4b5fd", fontFamily:"monospace" }}>💎 8K tokens</div>
          </div>
        </div>

        {/* Recent projects */}
        <div style={{ padding:"8px 12px", fontSize:8, color:"#374151", letterSpacing:"2px", fontFamily:"monospace", textTransform:"uppercase" }}>
          Recent Projects
        </div>
        <div style={{ flex:1, overflowY:"auto", padding:"0 8px", scrollbarWidth:"none" }}>
          {projects.slice(0, 14).map((p, i) => <ProjectItem key={i} project={p} idx={i} />)}
          {!projects.length && (
            <div style={{ padding:"20px 8px", textAlign:"center", fontSize:9, color:"#1e2530", fontFamily:"monospace" }}>
              No projects yet.<br/>Start building below ↓
            </div>
          )}
        </div>

        {/* Footer */}
        <div style={{ padding:"10px 14px", borderTop:"1px solid rgba(255,255,255,0.06)" }}>
          <div style={{ fontSize:8, color:"#374151", fontFamily:"monospace", textAlign:"center" }}>AI Project Generator</div>
          <div style={{ fontSize:8, color:"#1e2530", fontFamily:"monospace", textAlign:"center", marginTop:2 }}>S.E.A.D.S. © 2026</div>
        </div>
      </aside>

      {/* ── MAIN CONTENT ────────────────────────────────────── */}
      <main style={{
        flex:1, overflowY:"auto", display:"flex", flexDirection:"column",
        alignItems:"center", padding:"32px 28px 60px",
        zIndex:1, scrollbarWidth:"thin", scrollbarColor:"rgba(196,181,253,0.15) transparent",
      }}>
        <div style={{ width:"100%", maxWidth:900, display:"flex", flexDirection:"column", alignItems:"center", gap:22 }}>

          {/* Workspace greeting badge */}
          <div style={{
            display:"flex", alignItems:"center", gap:8,
            background:"rgba(255,255,255,0.03)", border:"1px solid rgba(255,255,255,0.07)",
            borderRadius:30, padding:"6px 18px 6px 8px", backdropFilter:"blur(16px)",
          }}>
            <div style={{
              width:28, height:28, borderRadius:"50%",
              background:"linear-gradient(135deg, #c4b5fd, #f9a8d4)",
              display:"flex", alignItems:"center", justifyContent:"center",
              fontSize:12, fontWeight:700, color:"#fff",
              boxShadow:"0 0 12px rgba(196,181,253,0.4)",
            }}>S</div>
            <span style={{ fontSize:12, color:"#9ca3af", fontFamily:"'Syne', sans-serif" }}>{greeting} 👋</span>
            <span style={{ fontSize:10, color:"#374151", fontFamily:"monospace" }}>— {dayName}'s Workspace</span>
          </div>

          {/* Headline */}
          <div style={{ textAlign:"center" }}>
            <h1 style={{
              fontSize:"clamp(28px,4vw,48px)", fontWeight:900,
              fontFamily:"'Syne', sans-serif", lineHeight:1.1, marginBottom:10,
              background:"linear-gradient(135deg, #f0f4ff 0%, #c4b5fd 50%, #93c5fd 100%)",
              WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent",
            }}>
              What do you want to build today?
            </h1>
            <p style={{ fontSize:13, color:"#4b5563", fontFamily:"monospace", lineHeight:1.7 }}>
              🔍 Research 1 min → 🧠 Plan 1 min → 💻 Code 3 min → ⚡ Live Preview → 🚀 Deploy
            </p>
          </div>

          {/* Stats row */}
          <div style={{ display:"flex", gap:12, flexWrap:"wrap", justifyContent:"center" }}>
            <StatBadge label="Agents"       value={100} suffix="+" color="#c4b5fd" />
            <StatBadge label="Project Types" value={14}             color="#93c5fd" />
            <StatBadge label="Token Budget"  value={8}  suffix="K/call" color="#f9a8d4" />
            <StatBadge label="Avg Build Time" value={5} suffix=" min"   color="#86efac" />
          </div>

          {/* Search */}
          <div style={{ width:"100%", maxWidth:700 }}>
            <div style={{
              display:"flex", alignItems:"center",
              background: searchFocused ? "rgba(13,17,28,0.97)" : "rgba(13,17,28,0.7)",
              border: `2px solid ${searchFocused ? "#c4b5fd" : "rgba(255,255,255,0.08)"}`,
              borderRadius:18, padding:"10px 12px 10px 18px",
              transition:"all 0.3s ease", backdropFilter:"blur(16px)",
              boxShadow: searchFocused ? "0 0 30px rgba(196,181,253,0.18)" : "none",
            }}>
              <span style={{ fontSize:16, marginRight:10, opacity:0.5 }}>🔍</span>
              <input
                value={searchQuery}
                onChange={e => setSearchQuery(e.target.value)}
                onFocus={() => setSearchFocused(true)}
                onBlur={() => setSearchFocused(false)}
                placeholder="Search a category: website, ML project, game, dashboard..."
                style={{
                  flex:1, background:"none", border:"none", outline:"none",
                  fontSize:14, color:"#f0f4ff", fontFamily:"'Syne', sans-serif", padding:"4px 0",
                }}
              />
              {searchQuery && (
                <button onClick={() => setSearchQuery("")} style={{
                  background:"rgba(255,255,255,0.05)", border:"1px solid rgba(255,255,255,0.08)",
                  borderRadius:6, color:"#4b5563", cursor:"pointer", padding:"4px 10px",
                  fontSize:10, fontFamily:"monospace", transition:"all 0.2s",
                }}>✕ Clear</button>
              )}
            </div>
          </div>

          {/* Divider */}
          <div style={{ display:"flex", alignItems:"center", gap:12, width:"100%", maxWidth:700 }}>
            <div style={{ flex:1, height:1, background:"linear-gradient(90deg, transparent, rgba(255,255,255,0.07))" }} />
            <span style={{ fontSize:9, color:"#374151", letterSpacing:"2px", textTransform:"uppercase", fontFamily:"monospace", whiteSpace:"nowrap" }}>
              Choose a category to start
            </span>
            <div style={{ flex:1, height:1, background:"linear-gradient(90deg, rgba(255,255,255,0.07), transparent)" }} />
          </div>

          {/* Category grid */}
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill, minmax(210px, 1fr))", gap:14, width:"100%" }}>
            {filteredCats.map(([id, cat], idx) => (
              <CatCard key={id} id={id} cat={cat} idx={idx} onClick={() => onSelectCategory(id, cat)} />
            ))}
            {filteredCats.length === 0 && (
              <div style={{ gridColumn:"1 / -1", textAlign:"center", padding:"40px", color:"#374151", fontFamily:"monospace", fontSize:12 }}>
                No category matching "{searchQuery}" — try "website", "ML", "game"
              </div>
            )}
          </div>

          {/* Bottom badge */}
          <div style={{
            marginTop:8, padding:"10px 24px", borderRadius:30,
            background:"linear-gradient(135deg, rgba(196,181,253,0.08), rgba(147,197,253,0.08))",
            border:"1px solid rgba(196,181,253,0.18)",
            fontSize:10, fontFamily:"monospace", letterSpacing:"1px", textAlign:"center",
            color:"#c4b5fd",
          }}>
            ⚡ S.E.A.D.S. v14 · Self-Evolving Autonomous Developer Swarm · Claude 4.6
          </div>
        </div>
      </main>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800;900&family=JetBrains+Mono:wght@400;600&display=swap');
        @keyframes animeGlow { 0%,100%{box-shadow:0 0 20px rgba(196,181,253,0.4)} 50%{box-shadow:0 0 35px rgba(249,168,212,0.6)} }
        @keyframes slideInLeft { from{opacity:0;transform:translateX(-12px)} to{opacity:1;transform:translateX(0)} }
        @keyframes shimmerPass { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }
        ::-webkit-scrollbar { width:4px; } ::-webkit-scrollbar-track { background:transparent; }
        ::-webkit-scrollbar-thumb { background:rgba(196,181,253,0.2); border-radius:4px; }
      `}</style>
    </div>
  );
}
