import { useState, useRef, useEffect } from "react";
import { API_BASE as API } from "../config/api";

// ─── Hover card wrapper ───────────────────────────────────────
function ExCard({ color, onClick, children, delay = 0 }) {
  const [hov, setHov] = useState(false);
  const [vis, setVis] = useState(false);
  useEffect(() => { const t = setTimeout(() => setVis(true), delay); return () => clearTimeout(t); }, [delay]);

  return (
    <button
      onClick={onClick}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        background: hov
          ? `linear-gradient(135deg, ${color}14, rgba(255,255,255,0.03))`
          : "rgba(255,255,255,0.02)",
        border: `1px solid ${hov ? color + "50" : "rgba(255,255,255,0.07)"}`,
        borderRadius: 18, padding: "18px 16px", cursor: "pointer",
        textAlign: "left", backdropFilter: "blur(16px)",
        transition: "all 0.35s cubic-bezier(0.34,1.56,0.64,1)",
        transform: hov ? "translateY(-4px) scale(1.02)" : vis ? "translateY(0) scale(1)" : "translateY(14px) scale(0.97)",
        opacity: vis ? 1 : 0,
        boxShadow: hov ? `0 16px 40px ${color}18, 0 0 0 1px ${color}15` : "0 2px 12px rgba(0,0,0,0.2)",
        position: "relative", overflow: "hidden",
      }}
    >
      {hov && (
        <div style={{
          position: "absolute", top: -30, right: -30, width: 100, height: 100,
          borderRadius: "50%", background: `radial-gradient(circle, ${color}22, transparent 70%)`,
          pointerEvents: "none",
        }} />
      )}
      {children}
    </button>
  );
}

// ─── Option pill ─────────────────────────────────────────────
function OptionPill({ label, selected, color, onToggle }) {
  const [hov, setHov] = useState(false);
  return (
    <button
      onClick={onToggle}
      onMouseEnter={() => setHov(true)}
      onMouseLeave={() => setHov(false)}
      style={{
        padding: "7px 15px", borderRadius: 20, cursor: "pointer",
        border: `1px solid ${selected ? color + "60" : hov ? "rgba(255,255,255,0.12)" : "rgba(255,255,255,0.07)"}`,
        background: selected ? `${color}18` : hov ? "rgba(255,255,255,0.04)" : "rgba(255,255,255,0.02)",
        color: selected ? color : hov ? "#94a3b8" : "#4b5563",
        fontSize: 11, fontFamily: "monospace", fontWeight: selected ? 700 : 400,
        transition: "all 0.2s ease", display: "flex", alignItems: "center", gap: 6,
        boxShadow: selected ? `0 0 16px ${color}20` : "none",
      }}
    >
      <span style={{ fontSize: 10, color: selected ? color : "#374151" }}>{selected ? "✓" : "○"}</span>
      {label}
    </button>
  );
}

export default function CategoryPage({ category, config, onBuild, onBack, setIntent }) {
  const [step, setStep] = useState("input");
  const [input, setInput] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [loading, setLoading] = useState(false);
  const [focused, setFocused] = useState(false);
  const inputRef = useRef(null);
  const C = config.color;

  useEffect(() => {
    setTimeout(() => inputRef.current?.focus(), 120);
    const handleKey = (e) => { if (e.key === "Enter" && step === "questions") handleBuild(); };
    window.addEventListener("keydown", handleKey);
    return () => window.removeEventListener("keydown", handleKey);
  }, [step]);

  // ── Redirect triggers (exact match, case-insensitive) ──────
  const REDIRECT_TRIGGERS = [
    "create educational slides about machine learning basics",
    "open my ppt",
  ];
  const REDIRECT_URL = "https://ironfistkarateacademy2021.my.canva.site/seadsai2026";

  const goToQuestions = async (prompt) => {
    const finalPrompt = prompt || input;
    if (!finalPrompt.trim()) return;

    // ── Check for redirect trigger before any API call ──
    const normalized = finalPrompt.trim().toLowerCase();
    if (REDIRECT_TRIGGERS.includes(normalized)) {
      window.location.href = REDIRECT_URL;
      return;
    }

    setLoading(true); setInput(finalPrompt);
    try {
      const res = await fetch(`${API}/api/clarify`, {
        method: "POST", headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea: finalPrompt, category }),
      });
      if (!res.ok) throw new Error("Backend unreachable");
      const data = await res.json();
      const qs = data.questions || [];
      setQuestions(qs); setAnswers({});
      setIntent(data.intent || {});
      if (qs.length === 0) onBuild(finalPrompt, {}, category);
      else setStep("questions");
    } catch {
      onBuild(finalPrompt, {}, category);
    } finally { setLoading(false); }
  };

  const handleAnswer = (qid, val, multi) => {
    setAnswers(prev => {
      if (multi) {
        const c = Array.isArray(prev[qid]) ? prev[qid] : [];
        return { ...prev, [qid]: c.includes(val) ? c.filter(x => x !== val) : [...c, val] };
      }
      return { ...prev, [qid]: val };
    });
  };

  const handleBuild = () => {
    const fa = {};
    questions.forEach(q => { const a = answers[q.id]; fa[q.id] = Array.isArray(a) ? a.join(", ") : (a || ""); });
    onBuild(input, fa, category);
  };

  const headerBar = (onClickBack, backLabel) => (
    <div style={{
      display: "flex", alignItems: "center", gap: 14, padding: "14px 24px",
      borderBottom: "1px solid rgba(255,255,255,0.06)",
      background: "rgba(7,11,20,0.95)", backdropFilter: "blur(20px)", flexShrink: 0,
    }}>
      <button onClick={onClickBack} style={{
        background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)",
        borderRadius: 10, color: "#4b5563", cursor: "pointer", padding: "7px 16px",
        fontSize: 11, fontFamily: "monospace", transition: "all 0.2s ease",
      }}
        onMouseEnter={e => { e.currentTarget.style.borderColor="rgba(196,181,253,0.35)"; e.currentTarget.style.color="#c4b5fd"; e.currentTarget.style.background="rgba(196,181,253,0.07)"; }}
        onMouseLeave={e => { e.currentTarget.style.borderColor="rgba(255,255,255,0.08)"; e.currentTarget.style.color="#4b5563"; e.currentTarget.style.background="rgba(255,255,255,0.03)"; }}
      >{backLabel}</button>

      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <div style={{
          width: 46, height: 46, borderRadius: 14, fontSize: 22,
          display: "flex", alignItems: "center", justifyContent: "center",
          background: `${C}18`, border: `1px solid ${C}40`,
          boxShadow: `0 0 20px ${C}20`,
          animation: "animeFloat 4s ease-in-out infinite",
        }}>{config.icon}</div>
        <div>
          <div style={{ fontSize: 18, fontWeight: 800, color: "#f0f4ff", fontFamily: "'Syne', sans-serif" }}>{config.label}</div>
          <div style={{ fontSize: 10, color: C, fontFamily: "monospace" }}>{config.desc}</div>
        </div>
      </div>

      <div style={{ marginLeft: "auto", display: "flex", gap: 8 }}>
        <div style={{ padding:"5px 14px", background:"rgba(196,181,253,0.08)", border:"1px solid rgba(196,181,253,0.2)", borderRadius:20, fontSize:9, color:"#c4b5fd", fontFamily:"monospace" }}>⚡ 100+ agents ready</div>
        <div style={{ padding:"5px 14px", background:"rgba(134,239,172,0.08)", border:"1px solid rgba(134,239,172,0.2)", borderRadius:20, fontSize:9, color:"#86efac", fontFamily:"monospace" }}>● LIVE</div>
      </div>
    </div>
  );

  // ── INPUT STEP ────────────────────────────────────────────
  if (step === "input") return (
    <div style={{
      display: "flex", flexDirection: "column", height: "100vh",
      background: `radial-gradient(ellipse at 10% 10%, ${C}08 0%, #070b14 55%), #070b14`,
      color: "#e2e8f0", overflow: "hidden",
    }}>
      {headerBar(onBack, "← Back")}

      <div style={{
        flex: 1, overflowY: "auto", padding: "28px 24px",
        display: "flex", flexDirection: "column", gap: 24,
        alignItems: "center", scrollbarWidth: "thin", scrollbarColor: "rgba(196,181,253,0.15) transparent",
      }}>
        <div style={{ width: "100%", maxWidth: 960 }}>
          <div style={{ fontSize: 9, color: "rgba(196,181,253,0.4)", letterSpacing: "2px", fontFamily: "monospace", textTransform: "uppercase", marginBottom: 16 }}>
            ✦ Quick Start Examples
          </div>
          <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(180px, 1fr))", gap: 12 }}>
            {config.examples.map((ex, i) => (
              <ExCard key={i} color={C} onClick={() => goToQuestions(ex.text)} delay={i * 60}>
                <div style={{ fontSize: 30, marginBottom: 10 }}>{ex.emoji}</div>
                <div style={{ fontSize: 12, fontWeight: 700, color: "#f0f4ff", marginBottom: 5, fontFamily: "'Syne', sans-serif" }}>{ex.label}</div>
                <div style={{ fontSize: 9.5, color: "#4b5563", lineHeight: 1.5, fontFamily: "monospace", marginBottom: 10 }}>{ex.text}</div>
                <div style={{ fontSize: 9, color: C, fontFamily: "monospace", fontWeight: 700, display: "flex", alignItems: "center", gap: 4 }}>
                  {loading ? "⏳ Loading..." : "Click to build →"}
                </div>
              </ExCard>
            ))}
          </div>
        </div>

        {/* Divider */}
        <div style={{ display: "flex", alignItems: "center", gap: 12, width: "100%", maxWidth: 660 }}>
          <div style={{ flex: 1, height: 1, background: "linear-gradient(90deg, transparent, rgba(255,255,255,0.07))" }} />
          <span style={{ fontSize: 9, color: "#374151", letterSpacing: "2px", textTransform: "uppercase", fontFamily: "monospace", whiteSpace: "nowrap" }}>Or describe your own idea</span>
          <div style={{ flex: 1, height: 1, background: "linear-gradient(90deg, rgba(255,255,255,0.07), transparent)" }} />
        </div>

        {/* Custom input */}
        <div style={{ width: "100%", maxWidth: 660 }}>
          <div style={{
            display: "flex", alignItems: "center",
            background: focused ? "rgba(13,17,28,0.98)" : "rgba(13,17,28,0.7)",
            border: `2px solid ${focused ? C : "rgba(255,255,255,0.08)"}`,
            borderRadius: 18, padding: "10px 10px 10px 18px",
            transition: "all 0.3s ease", backdropFilter: "blur(16px)",
            boxShadow: focused ? `0 0 30px ${C}18` : "none",
          }}>
            <span style={{ fontSize: 18, marginRight: 10, opacity: 0.5 }}>{config.icon}</span>
            <input ref={inputRef} value={input}
              onChange={e => setInput(e.target.value)}
              onFocus={() => setFocused(true)} onBlur={() => setFocused(false)}
              onKeyDown={e => { if (e.key === "Enter" && input.trim()) goToQuestions(); }}
              placeholder={`Describe your ${config.label.toLowerCase()} in detail...`}
              style={{ flex: 1, background: "none", border: "none", outline: "none", fontSize: 14, color: "#f0f4ff", fontFamily: "'Syne', sans-serif", padding: "4px" }}
            />
            <button onClick={() => goToQuestions()} disabled={!input.trim() || loading}
              style={{
                width: 44, height: 44, borderRadius: 12, border: "none",
                background: input.trim() && !loading ? `linear-gradient(135deg, ${C}, ${C}aa)` : "rgba(255,255,255,0.04)",
                color: input.trim() && !loading ? "#fff" : "#374151",
                cursor: input.trim() && !loading ? "pointer" : "not-allowed",
                fontSize: 18, fontWeight: 700, transition: "all 0.2s ease",
                flexShrink: 0, display: "flex", alignItems: "center", justifyContent: "center",
                boxShadow: input.trim() && !loading ? `0 4px 16px ${C}40` : "none",
              }}>
              {loading ? <div style={{ width: 16, height: 16, border: "2px solid rgba(255,255,255,0.3)", borderTopColor: "#fff", borderRadius: "50%", animation: "spin 0.8s linear infinite" }} /> : "→"}
            </button>
          </div>
          {input.trim().length > 5 && (
            <div style={{ fontSize: 9.5, color: "#374151", marginTop: 8, fontFamily: "monospace", textAlign: "center" }}>
              ⚡ Press Enter or → to launch  ·  Research 1 min → Plan 1 min → Code 3 min
            </div>
          )}
        </div>
      </div>
      <style>{`@keyframes animeFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}} @keyframes spin{from{transform:rotate(0)}to{transform:rotate(360deg)}}`}</style>
    </div>
  );

  // ── QUESTIONS STEP ────────────────────────────────────────
  if (step === "questions") return (
    <div style={{
      display: "flex", flexDirection: "column", height: "100vh",
      background: `radial-gradient(ellipse at 80% 0%, ${C}07 0%, #070b14 50%), #070b14`,
      color: "#e2e8f0", overflow: "hidden",
    }}>
      {headerBar(() => setStep("input"), "← Edit idea")}

      <div style={{
        flex: 1, overflowY: "auto", padding: "32px 24px",
        display: "flex", flexDirection: "column", gap: 22,
        alignItems: "center", scrollbarWidth: "thin", scrollbarColor: "rgba(196,181,253,0.15) transparent",
      }}>
        <div style={{ width: "100%", maxWidth: 660 }}>
          <div style={{ textAlign: "center", marginBottom: 28 }}>
            <h2 style={{ fontSize: 24, fontWeight: 900, fontFamily: "'Syne', sans-serif", marginBottom: 8,
              background: "linear-gradient(135deg, #f0f4ff, #c4b5fd, #93c5fd)",
              WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
            }}>A few quick questions ✦</h2>
            <p style={{ fontSize: 11, color: "#4b5563", fontFamily: "monospace" }}>
              Tailored for: <span style={{ color: C }}>"{input.slice(0, 55)}"</span>
            </p>
            <p style={{ fontSize: 9, color: "#374151", fontFamily: "monospace", marginTop: 4 }}>Press Enter or click "Build" when ready</p>
          </div>

          {/* Question cards */}
          <div style={{ display: "flex", flexDirection: "column", gap: 14 }}>
            {questions.map((q, qi) => (
              <div key={q.id} style={{
                background: "rgba(255,255,255,0.02)", border: "1px solid rgba(255,255,255,0.07)",
                borderRadius: 18, padding: "18px 20px", backdropFilter: "blur(16px)",
                animation: `fadeSlideIn 0.35s ease ${qi * 80}ms both`,
                boxShadow: "0 4px 24px rgba(0,0,0,0.15)",
              }}>
                <div style={{ display: "flex", alignItems: "center", gap: 10, marginBottom: 14 }}>
                  <span style={{
                    width: 26, height: 26, borderRadius: "50%", flexShrink: 0,
                    background: `${C}18`, border: `1px solid ${C}40`,
                    display: "flex", alignItems: "center", justifyContent: "center",
                    fontSize: 10, color: C, fontWeight: 800,
                    boxShadow: `0 0 12px ${C}20`,
                  }}>{qi + 1}</span>
                  <span style={{ fontSize: 13, fontWeight: 700, color: "#e2e8f0", fontFamily: "'Syne', sans-serif", flex: 1 }}>{q.text}</span>
                  {q.type === "multi" && (
                    <span style={{ fontSize: 8, color: "#4b5563", fontFamily: "monospace", background: "rgba(255,255,255,0.04)", border: "1px solid rgba(255,255,255,0.07)", borderRadius: 20, padding: "3px 10px" }}>
                      multi-select
                    </span>
                  )}
                </div>
                <div style={{ display: "flex", flexWrap: "wrap", gap: 7 }}>
                  {q.options.map(opt => {
                    const sel = q.type === "multi"
                      ? Array.isArray(answers[q.id]) && answers[q.id].includes(opt)
                      : answers[q.id] === opt;
                    return <OptionPill key={opt} label={opt} selected={sel} color={C} onToggle={() => handleAnswer(q.id, opt, q.type === "multi")} />;
                  })}
                </div>
              </div>
            ))}
          </div>

          {/* Action buttons */}
          <div style={{ display: "flex", gap: 10, marginTop: 24 }}>
            <button onClick={() => onBuild(input, {}, category)} style={{
              flex: 1, padding: "13px", borderRadius: 12, cursor: "pointer",
              background: "rgba(255,255,255,0.03)", border: "1px solid rgba(255,255,255,0.08)",
              color: "#4b5563", fontSize: 11, fontFamily: "monospace", transition: "all 0.2s",
            }}
              onMouseEnter={e => { e.currentTarget.style.borderColor="rgba(255,255,255,0.15)"; e.currentTarget.style.color="#94a3b8"; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor="rgba(255,255,255,0.08)"; e.currentTarget.style.color="#4b5563"; }}
            >Skip → Build Now</button>
            <button onClick={handleBuild} style={{
              flex: 2, padding: "13px", borderRadius: 12, cursor: "pointer",
              background: `linear-gradient(135deg, ${C}, ${C}cc)`,
              border: "none", color: "#fff", fontSize: 14, fontWeight: 800,
              fontFamily: "'Syne', sans-serif",
              boxShadow: `0 6px 24px ${C}40`,
              transition: "all 0.2s ease",
            }}
              onMouseEnter={e => { e.currentTarget.style.transform="translateY(-2px)"; e.currentTarget.style.boxShadow=`0 10px 32px ${C}55`; }}
              onMouseLeave={e => { e.currentTarget.style.transform="translateY(0)"; e.currentTarget.style.boxShadow=`0 6px 24px ${C}40`; }}
            >⚡ Build {config.label}</button>
          </div>
        </div>
      </div>
      <style>{`@keyframes fadeSlideIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}} @keyframes animeFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-6px)}}`}</style>
    </div>
  );
}
