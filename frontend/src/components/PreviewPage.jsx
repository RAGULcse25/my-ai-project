import LogPanel from "./LogPanel";
import OutputZone from "./OutputZone";
import AgentSidebar from "./AgentSidebar";
import { useState } from "react";
import { CATS } from "../config/categories";

export default function PreviewPage({ idea, previewHtml, files, buildLogs, agentsUsed, onHome, onEdit, category, intent, patchMode }) {
  const C = (CATS[category] || CATS.website).color;
  const cat = (CATS[category] || CATS.website);
  const [patchInput, setPatchInput] = useState("");
  const [patchFocused, setPatchFocused] = useState(false);

  const mergedLogs = [
    ...(buildLogs.plan || []).map(l => `[Planning] ${l}`),
    ...(buildLogs.code || []).map(l => `[Coding]  ${l}`),
    ...(buildLogs.test || []).map(l => `[Verify]  ${l}`),
  ];

  const handlePatch = (e) => {
    e.preventDefault();
    if (patchInput.trim()) {
      onEdit(patchInput.trim());
      setPatchInput("");
    }
  };

  return (
    <div style={{
      display:"flex", width:"100vw", height:"100vh",
      background:"linear-gradient(135deg, #070b14 0%, #0a0d18 100%)",
      overflow:"hidden",
    }}>

      {/* ── AGENT SIDEBAR ─────────────────────────────────── */}
      <div style={{
        width:180, flexShrink:0,
        borderRight:"1px solid rgba(255,255,255,0.06)",
        background:"rgba(7,11,20,0.96)",
        backdropFilter:"blur(20px)",
      }}>
        <AgentSidebar agents={agentsUsed} activeAgent={agentsUsed[agentsUsed.length - 1]} />
      </div>

      {/* ── LEFT CONTROL PANEL ────────────────────────────── */}
      <div style={{
        width:288, flexShrink:0,
        borderRight:"1px solid rgba(255,255,255,0.06)",
        display:"flex", flexDirection:"column",
        background:"rgba(9,12,20,0.95)",
        backdropFilter:"blur(20px)",
      }}>

        {/* Project identity */}
        <div style={{
          padding:"16px 16px 14px",
          borderBottom:"1px solid rgba(255,255,255,0.06)",
          background:"rgba(255,255,255,0.01)",
        }}>
          {/* HOME button */}
          <button
            onClick={onHome}
            style={{
              fontSize:9, background:"rgba(255,255,255,0.03)",
              border:"1px solid rgba(255,255,255,0.08)",
              borderRadius:8, color:"#4b5563", cursor:"pointer",
              padding:"6px 12px", marginBottom:14,
              fontFamily:"monospace", transition:"all 0.25s ease",
              letterSpacing:"1px",
            }}
            onMouseEnter={e => {
              e.target.style.borderColor = "rgba(196,181,253,0.35)";
              e.target.style.color = "#c4b5fd";
              e.target.style.background = "rgba(196,181,253,0.08)";
            }}
            onMouseLeave={e => {
              e.target.style.borderColor = "rgba(255,255,255,0.08)";
              e.target.style.color = "#4b5563";
              e.target.style.background = "rgba(255,255,255,0.03)";
            }}
          >
            ← HOME
          </button>

          {/* Category badge */}
          <div style={{ display:"flex", alignItems:"center", gap:10, marginBottom:12 }}>
            <div style={{
              width:34, height:34, borderRadius:10, flexShrink:0,
              background:`${C}18`, border:`1px solid ${C}40`,
              display:"flex", alignItems:"center", justifyContent:"center",
              fontSize:16, boxShadow:`0 0 16px ${C}20`,
              animation:"animeFloat 4s ease-in-out infinite",
            }}>
              {cat.icon}
            </div>
            <div>
              <div style={{
                fontSize:8, color:C, fontFamily:"monospace",
                fontWeight:700, letterSpacing:"1.5px", marginBottom:3,
              }}>
                {cat.label.toUpperCase()}
              </div>
              <div style={{
                fontSize:10, fontWeight:800, color:"#f0f4ff",
                fontFamily:"'Syne', sans-serif", lineHeight:1.2,
                overflow:"hidden", textOverflow:"ellipsis", whiteSpace:"nowrap",
                maxWidth:200,
              }}>
                {idea}
              </div>
            </div>
          </div>

          {/* Status pills */}
          <div style={{ display:"flex", gap:6 }}>
            <div style={{
              flex:1, padding:"5px 8px", borderRadius:8, textAlign:"center",
              background:"rgba(134,239,172,0.07)", border:"1px solid rgba(134,239,172,0.2)",
              fontSize:8, color:"#86efac", fontFamily:"monospace",
            }}>
              <span style={{ animation:"pulseDot 1.5s ease infinite", display:"inline-block" }}>●</span> LIVE
            </div>
            <div style={{
              flex:1, padding:"5px 8px", borderRadius:8, textAlign:"center",
              background:`${C}10`, border:`1px solid ${C}25`,
              fontSize:8, color:C, fontFamily:"monospace",
            }}>
              ⚡ READY
            </div>
            {patchMode && (
              <div style={{
                flex:1, padding:"5px 8px", borderRadius:8, textAlign:"center",
                background:"rgba(253,211,77,0.08)", border:"1px solid rgba(253,211,77,0.25)",
                fontSize:8, color:"#fcd34d", fontFamily:"monospace",
              }}>
                🩹 PATCH
              </div>
            )}
          </div>
        </div>

        {/* Build logs */}
        <div style={{ flex:1, overflow:"hidden" }}>
          <LogPanel logs={mergedLogs} agents={agentsUsed} status="LIVE PREVIEW ACTIVE" />
        </div>

        {/* Patch input */}
        <form
          onSubmit={handlePatch}
          style={{
            padding:"14px",
            borderTop:"1px solid rgba(255,255,255,0.06)",
            background:"rgba(7,11,20,0.85)",
          }}
        >
          <div style={{
            fontSize:8, color:"rgba(196,181,253,0.4)", fontFamily:"monospace",
            marginBottom:8, letterSpacing:"1.5px",
          }}>
            ✦ REFINE · PATCH · ENHANCE
          </div>
          <div style={{
            display:"flex", gap:7,
            background: patchFocused ? "rgba(13,17,28,0.98)" : "rgba(13,17,28,0.7)",
            border:`1px solid ${patchFocused ? C : "rgba(255,255,255,0.08)"}`,
            borderRadius:12, padding:"6px 6px 6px 12px",
            transition:"all 0.3s ease",
            boxShadow: patchFocused ? `0 0 20px ${C}20` : "none",
          }}>
            <input
              value={patchInput}
              onChange={e => setPatchInput(e.target.value)}
              onFocus={() => setPatchFocused(true)}
              onBlur={() => setPatchFocused(false)}
              placeholder="Make the navbar sticky..."
              style={{
                flex:1, background:"none", border:"none", outline:"none",
                fontSize:11, color:"#e2e8f0", fontFamily:"monospace", padding:"4px 0",
              }}
            />
            <button
              type="submit"
              style={{
                width:32, height:32,
                background: patchInput.trim()
                  ? `linear-gradient(135deg, ${C}, ${C}aa)`
                  : "rgba(255,255,255,0.05)",
                border:"none", borderRadius:8, color:"#fff",
                cursor: patchInput.trim() ? "pointer" : "default",
                display:"flex", alignItems:"center", justifyContent:"center",
                fontSize:14, transition:"all 0.25s ease", flexShrink:0,
                boxShadow: patchInput.trim() ? `0 4px 12px ${C}40` : "none",
              }}
            >↑</button>
          </div>
          <div style={{
            fontSize:7.5, color:"rgba(255,255,255,0.12)", marginTop:6,
            fontFamily:"monospace", textAlign:"center",
          }}>
            v14 Smart Patch Engine · IIT-Level Quality
          </div>
        </form>
      </div>

      {/* ── MAIN OUTPUT WORKSPACE ─────────────────────────── */}
      <div style={{ flex:1, background:"#080c10", minWidth:0 }}>
        <OutputZone
          files={files}
          previewHtml={previewHtml}
          activeColor={C}
          agentsUsed={agentsUsed}
          onEdit={onEdit}
          onHome={onHome}
        />
      </div>

      <style>{`
        @keyframes pulseDot { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes animeFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-6px)} }
      `}</style>
    </div>
  );
}
