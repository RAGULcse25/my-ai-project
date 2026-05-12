import { useState, useEffect, useRef } from "react";
import { CATS } from "../config/categories";

const STAGES = [
  { name:"Researching", icon:"🔍", sub:"Deep Search",    desc:"Perplexity Sonar · Best Practices", color:"#93c5fd", duration:60,  progressRange:[0,20]  },
  { name:"Planning",    icon:"🧠", sub:"Architecture",   desc:"DeepSeek-R1 · Multi-Agent Logic",  color:"#c4b5fd", duration:60,  progressRange:[20,45] },
  { name:"Coding",      icon:"💻", sub:"2X Token Power", desc:"Claude 4.6 · 8K tokens/agent",    color:"#a5b4fc", duration:180, progressRange:[45,90] },
  { name:"Preview",     icon:"⚡", sub:"Lovable Engine", desc:"Rendering · Sandboxed iframe",     color:"#86efac", duration:20,  progressRange:[90,100]},
];

const LOG_MSGS = [
  "Initializing S.E.A.D.S. v14 pipeline...",
  "Perplexity Sonar: querying best practices...",
  "Research complete — 14 patterns found",
  "DeepSeek-R1: decomposing task into subtasks...",
  "Planning agent: defining component hierarchy...",
  "Coding Agent: writing primary components...",
  "Verify Agent: auditing for IIT-level quality...",
  "Patching edge cases...",
  "Lovable Preview Engine: compiling iframe...",
  "Preview ready — Loading workspace...",
];

function CircleTimer({ elapsed, total, color, size = 80 }) {
  const r = (size - 8) / 2;
  const circumference = 2 * Math.PI * r;
  const pct = Math.min(elapsed / total, 1);
  const offset = circumference * (1 - pct);
  const remaining = Math.max(0, total - elapsed);
  const mm = String(Math.floor(remaining / 60)).padStart(2, "0");
  const ss = String(remaining % 60).padStart(2, "0");
  return (
    <svg width={size} height={size} style={{ transform:"rotate(-90deg)" }}>
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke="rgba(255,255,255,0.05)" strokeWidth={4} />
      <circle cx={size/2} cy={size/2} r={r} fill="none" stroke={color} strokeWidth={4}
        strokeDasharray={circumference} strokeDashoffset={offset} strokeLinecap="round"
        style={{ transition:"stroke-dashoffset 0.8s ease", filter:`drop-shadow(0 0 6px ${color}80)` }} />
      <text x="50%" y="50%" dominantBaseline="middle" textAnchor="middle"
        fill={color} fontSize="13" fontFamily="monospace" fontWeight="700"
        style={{ transform:"rotate(90deg)", transformOrigin:"50% 50%" }}>
        {mm}:{ss}
      </text>
    </svg>
  );
}

function StageCard({ stage, status, elapsed }) {
  const isActive  = status === "active";
  const isDone    = status === "done";
  const isPending = status === "pending";
  return (
    <div style={{
      display:"flex", flexDirection:"column", alignItems:"center", gap:10,
      padding:"20px 14px", borderRadius:20, minWidth:155,
      background: isActive
        ? `linear-gradient(135deg, ${stage.color}18, rgba(255,255,255,0.02))`
        : isDone ? "rgba(134,239,172,0.05)" : "rgba(255,255,255,0.02)",
      border:`1px solid ${isActive ? stage.color+"50" : isDone ? "rgba(134,239,172,0.25)" : "rgba(255,255,255,0.06)"}`,
      backdropFilter:"blur(16px)",
      transform: isActive ? "scale(1.06)" : "scale(1)",
      transition:"all 0.4s cubic-bezier(0.34,1.56,0.64,1)",
      boxShadow: isActive ? `0 0 30px ${stage.color}20, 0 8px 30px rgba(0,0,0,0.3)` : "0 4px 20px rgba(0,0,0,0.15)",
      opacity: isPending ? 0.4 : 1,
      position:"relative", overflow:"hidden",
    }}>
      {/* shimmer on active */}
      {isActive && (
        <div style={{
          position:"absolute", inset:0, pointerEvents:"none",
          background:`linear-gradient(90deg, transparent, ${stage.color}08, transparent)`,
          animation:"shimmerPass 2.5s ease infinite",
        }} />
      )}
      {isActive ? (
        <CircleTimer elapsed={elapsed} total={stage.duration} color={stage.color} />
      ) : (
        <div style={{
          width:80, height:80, borderRadius:"50%",
          display:"flex", alignItems:"center", justifyContent:"center",
          background: isDone ? "rgba(134,239,172,0.1)" : "rgba(255,255,255,0.03)",
          border:`3px solid ${isDone ? "rgba(134,239,172,0.4)" : "rgba(255,255,255,0.07)"}`,
          fontSize:32,
          boxShadow: isDone ? "0 0 20px rgba(134,239,172,0.2)" : "none",
        }}>
          {isDone ? "✅" : stage.icon}
        </div>
      )}
      <div style={{
        fontFamily:"'Syne', sans-serif", fontWeight:800, fontSize:12,
        textAlign:"center", textTransform:"uppercase", letterSpacing:"0.5px",
        color: isActive ? stage.color : isDone ? "#86efac" : "#374151",
      }}>
        {isDone ? "✓ " : isActive ? "⟳ " : ""}{stage.name}
      </div>
      <div style={{ fontSize:9, color:"#4b5563", fontFamily:"monospace", textAlign:"center", lineHeight:1.5 }}>
        <div style={{ color: isActive ? stage.color+"cc" : "#374151", fontWeight:600 }}>{stage.sub}</div>
        {stage.desc}
      </div>
      <div style={{
        fontSize:8, padding:"3px 10px", borderRadius:20, fontFamily:"monospace", fontWeight:600,
        background:`${isActive ? stage.color : "#1e2530"}18`,
        color: isActive ? stage.color : "#374151",
        border:`1px solid ${isActive ? stage.color+"30" : "rgba(255,255,255,0.06)"}`,
      }}>
        {stage.duration < 60 ? `${stage.duration}s` : `${stage.duration/60} min`} budget
      </div>
    </div>
  );
}

export default function BuildingPage({ idea, category, progress, status }) {
  const C = (CATS[category] || CATS.website).color;
  const [elapsed, setElapsed] = useState(0);
  const [logLines, setLogLines] = useState([LOG_MSGS[0]]);
  const logRef = useRef(null);

  useEffect(() => { const t = setInterval(() => setElapsed(s => s + 1), 1000); return () => clearInterval(t); }, []);
  useEffect(() => {
    const idx = Math.min(Math.floor((progress / 100) * LOG_MSGS.length), LOG_MSGS.length - 1);
    setLogLines(prev => { const next = LOG_MSGS.slice(0, idx + 1); return next.length > prev.length ? next : prev; });
  }, [progress]);
  useEffect(() => { if (logRef.current) logRef.current.scrollTop = logRef.current.scrollHeight; }, [logLines]);

  const currentStage = STAGES.findIndex(s => progress >= s.progressRange[0] && progress < s.progressRange[1]);
  const activeStageIdx = currentStage === -1 ? (progress >= 100 ? 3 : 0) : currentStage;
  const stageElapsed = (() => {
    const s = STAGES[activeStageIdx];
    const sp = Math.max(0, Math.min(progress - s.progressRange[0], s.progressRange[1] - s.progressRange[0]));
    return Math.floor((sp / (s.progressRange[1] - s.progressRange[0])) * s.duration);
  })();
  const totalBudget = STAGES.reduce((acc, s) => acc + s.duration, 0);
  const mm = String(Math.floor(elapsed / 60)).padStart(2, "0");
  const ss = String(elapsed % 60).padStart(2, "0");
  const bm = String(Math.floor(totalBudget / 60)).padStart(2, "0");
  const bs = String(totalBudget % 60).padStart(2, "0");

  return (
    <div style={{
      display:"flex", flexDirection:"column", alignItems:"center", justifyContent:"center",
      minHeight:"100vh", padding:"32px 24px", gap:28, position:"relative", overflow:"hidden",
      background:"linear-gradient(135deg, #070b14 0%, #0a0d1a 50%, #070b14 100%)",
    }}>
      {/* Background blobs */}
      <div style={{ position:"absolute", top:"10%", left:"15%", width:350, height:350, borderRadius:"50%", background:`radial-gradient(circle, ${C}08 0%, transparent 70%)`, pointerEvents:"none", animation:"animeFloat 8s ease-in-out infinite" }} />
      <div style={{ position:"absolute", bottom:"10%", right:"15%", width:280, height:280, borderRadius:"50%", background:"radial-gradient(circle, rgba(196,181,253,0.07) 0%, transparent 70%)", pointerEvents:"none", animation:"animeFloat 10s ease-in-out infinite 3s" }} />
      <div style={{ position:"absolute", top:"50%", left:"50%", width:500, height:500, borderRadius:"50%", transform:"translate(-50%,-50%)", background:"radial-gradient(circle, rgba(147,197,253,0.03) 0%, transparent 70%)", pointerEvents:"none" }} />

      {/* Header */}
      <div style={{ textAlign:"center", zIndex:1 }}>
        <div style={{
          display:"inline-flex", alignItems:"center", gap:8, borderRadius:30,
          padding:"6px 18px", marginBottom:14, fontSize:10, fontFamily:"monospace", fontWeight:700,
          background:`${C}12`, border:`1px solid ${C}30`, color:C,
        }}>
          <span style={{ animation:"pulseDot 1.5s ease-in-out infinite" }}>●</span>
          BUILDING · S.E.A.D.S. v14 PIPELINE ACTIVE
        </div>
        <h2 style={{
          fontSize:"clamp(18px,3vw,30px)", fontWeight:900,
          fontFamily:"'Syne', sans-serif", marginBottom:8,
          background:"linear-gradient(135deg, #f0f4ff, #c4b5fd, #93c5fd)",
          WebkitBackgroundClip:"text", WebkitTextFillColor:"transparent",
        }}>
          Building Your Workspace
        </h2>
        <div style={{ fontSize:12, color:"#4b5563", fontFamily:"monospace", maxWidth:480, margin:"0 auto" }}>
          🎯 <span style={{ color:C }}>"{idea}"</span>
        </div>
      </div>

      {/* Stats row */}
      <div style={{ display:"flex", gap:20, zIndex:1 }}>
        {[
          { label:"ELAPSED",       value:`${mm}:${ss}`,   color:"#c4b5fd" },
          { label:"BUDGET (5 MIN)", value:`${bm}:${bs}`,  color:"#374151" },
          { label:"COMPLETE",       value:`${Math.round(progress)}%`, color:C },
        ].map(({ label, value, color }) => (
          <div key={label} style={{ textAlign:"center" }}>
            <div style={{ fontSize:22, fontWeight:900, color, fontFamily:"monospace" }}>{value}</div>
            <div style={{ fontSize:8, color:"#374151", fontFamily:"monospace", letterSpacing:"1px" }}>{label}</div>
          </div>
        ))}
      </div>

      {/* Progress bar */}
      <div style={{ width:"100%", maxWidth:800, zIndex:1 }}>
        <div style={{
          height:6, borderRadius:4, overflow:"hidden",
          background:"rgba(255,255,255,0.06)",
          boxShadow:"inset 0 1px 3px rgba(0,0,0,0.4)",
        }}>
          <div style={{
            height:"100%", width:`${progress}%`, borderRadius:4,
            background:`linear-gradient(90deg, #c4b5fd, ${C}, #93c5fd)`,
            boxShadow:`0 0 16px ${C}60`,
            transition:"width 0.6s ease",
            position:"relative", overflow:"hidden",
          }}>
            <div style={{
              position:"absolute", inset:0,
              background:"linear-gradient(90deg, transparent, rgba(255,255,255,0.25), transparent)",
              animation:"shimmerPass 1.8s ease infinite",
            }} />
          </div>
        </div>
        <div style={{ display:"flex", justifyContent:"space-between", marginTop:4 }}>
          <span style={{ fontSize:8, color:"#1e2530", fontFamily:"monospace" }}>0%</span>
          <span style={{ fontSize:8, color:C, fontFamily:"monospace" }}>{Math.round(progress)}%</span>
          <span style={{ fontSize:8, color:"#1e2530", fontFamily:"monospace" }}>100%</span>
        </div>
      </div>

      {/* Stage cards */}
      <div style={{ display:"flex", gap:12, flexWrap:"wrap", justifyContent:"center", width:"100%", maxWidth:800, zIndex:1 }}>
        {STAGES.map((stage, i) => (
          <StageCard key={i} stage={stage}
            status={i < activeStageIdx ? "done" : i === activeStageIdx ? "active" : "pending"}
            elapsed={i === activeStageIdx ? stageElapsed : 0} />
        ))}
      </div>

      {/* Log console */}
      <div style={{
        width:"100%", maxWidth:800, zIndex:1,
        background:"rgba(4,8,14,0.85)", borderRadius:16, overflow:"hidden",
        backdropFilter:"blur(16px)",
        border:"1px solid rgba(255,255,255,0.06)",
        boxShadow:"0 8px 40px rgba(0,0,0,0.3)",
      }}>
        <div style={{
          display:"flex", alignItems:"center", gap:8, padding:"10px 16px",
          borderBottom:"1px solid rgba(255,255,255,0.06)",
          background:"rgba(255,255,255,0.02)",
        }}>
          <div style={{ width:8, height:8, borderRadius:"50%", background:"#86efac", boxShadow:"0 0 8px rgba(134,239,172,0.7)", animation:"pulseDot 1.5s ease-in-out infinite" }} />
          <span style={{ fontSize:9, color:"#374151", fontFamily:"monospace", letterSpacing:"2px", textTransform:"uppercase" }}>Live Pipeline Console</span>
          <span style={{ marginLeft:"auto", fontSize:9, color:"#1e2530", fontFamily:"monospace" }}>{logLines.length} events</span>
        </div>
        <div ref={logRef} style={{
          height:130, overflowY:"auto", padding:"12px 16px",
          display:"flex", flexDirection:"column", gap:5, scrollbarWidth:"none",
        }}>
          {logLines.map((line, i) => (
            <div key={i} style={{
              fontSize:10, fontFamily:"monospace", lineHeight:1.6,
              color: i === logLines.length - 1 ? "#c4b5fd" : "#374151",
              animation: i === logLines.length - 1 ? "fadeSlideIn 0.4s ease" : "none",
              display:"flex", gap:8,
            }}>
              <span style={{ color:"rgba(255,255,255,0.1)" }}>[{String(i+1).padStart(2,"0")}]</span>
              <span style={{ color:"rgba(134,239,172,0.4)" }}>▶</span>
              {line}
            </div>
          ))}
        </div>
      </div>

      {/* Status badge */}
      <div style={{
        zIndex:1, padding:"10px 28px", borderRadius:30,
        background:`${C}10`, border:`1px solid ${C}30`,
        fontSize:11, color:C, fontFamily:"monospace", fontWeight:700,
        animation:"pulseDot 2s ease-in-out infinite",
        maxWidth:600, textAlign:"center",
        boxShadow:`0 0 24px ${C}15`,
      }}>
        {status || "SWARM INITIALIZING..."}
      </div>

      <style>{`
        @keyframes pulseDot { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes animeFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-12px)} }
        @keyframes shimmerPass { 0%{transform:translateX(-100%)} 100%{transform:translateX(100%)} }
        @keyframes fadeSlideIn { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
      `}</style>
    </div>
  );
}
