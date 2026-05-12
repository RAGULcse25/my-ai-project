import { useState, useEffect, useRef } from "react";

const API = "http://localhost:8001";

const PHASES = [
  { icon: "◆", label: "Planning",          color: "#60a5fa" },
  { icon: "◈", label: "Agents Running",    color: "#a78bfa" },
  { icon: "◉", label: "Testing",           color: "#34d399" },
  { icon: "◎", label: "Preview Ready",     color: "#fbbf24" },
];

const FILE_ICONS = { ".py":"🐍",".html":"🌐",".css":"🎨",".js":"⚡",".md":"📄",".sql":"🗄️",".txt":"📝" };
const getIcon = (n="") => FILE_ICONS[n.slice(n.lastIndexOf("."))] || "📄";

const LOADING_HTML = `<!DOCTYPE html><html><head><meta charset="UTF-8"/>
<style>*{margin:0;padding:0;box-sizing:border-box}
body{background:#080c10;display:flex;align-items:center;justify-content:center;
height:100vh;font-family:monospace}
.w{text-align:center}
.ring{width:56px;height:56px;border:2px solid #1a2436;border-top-color:#6366f1;
border-radius:50%;animation:sp 1s linear infinite;margin:0 auto 20px}
.t{font-size:11px;color:#6366f1;letter-spacing:3px;text-transform:uppercase;margin-bottom:6px}
.s{font-size:9px;color:#2d3748;letter-spacing:2px}
.agents{display:flex;gap:6px;justify-content:center;margin-top:16px;flex-wrap:wrap;max-width:300px}
.a{background:#0d1520;border:1px solid #1e2736;border-radius:4px;padding:3px 8px;
font-size:8px;color:#374151;letter-spacing:1px;animation:fade 1.5s infinite}
.a:nth-child(2n){animation-delay:.3s}
.a:nth-child(3n){animation-delay:.6s}
@keyframes sp{to{transform:rotate(360deg)}}
@keyframes fade{0%,100%{opacity:.3}50%{opacity:1}}
</style></head>
<body><div class="w">
<div class="ring"></div>
<div class="t">Building Your App</div>
<div class="s">20+ AI agents working in parallel</div>
<div class="agents" id="ag"></div>
</div>
<script>
const agents=["architect","game_logic","ui_designer","state_mgr","animation","ai_feature","integrator","database","auth","realtime","search","social","mobile","security","docs"];
const c=document.getElementById("ag");
agents.forEach(a=>{const d=document.createElement("div");d.className="a";d.textContent=a;c.appendChild(d)});
</script>
</body></html>`;

// ─────────────────────────────────────────────────────────────
// CLARIFICATION DIALOG
// ─────────────────────────────────────────────────────────────
function ClarifyDialog({ idea, questions, onSubmit, onSkip }) {
  const [answers, setAnswers] = useState({});
  const [multi, setMulti]     = useState({});

  function toggleMulti(qid, opt) {
    setMulti(prev => {
      const cur = prev[qid] || [];
      const next = cur.includes(opt) ? cur.filter(x=>x!==opt) : [...cur, opt];
      return { ...prev, [qid]: next };
    });
    setAnswers(prev => ({
      ...prev,
      [qid]: (multi[qid]||[]).includes(opt)
        ? (multi[qid]||[]).filter(x=>x!==opt).join(", ")
        : [...(multi[qid]||[]), opt].join(", ")
    }));
  }

  function handleChoice(qid, opt) {
    setAnswers(prev => ({ ...prev, [qid]: opt }));
  }

  function handleSubmit() {
    // Merge multi-select answers
    const final = { ...answers };
    Object.keys(multi).forEach(qid => {
      if (multi[qid].length) final[qid] = multi[qid].join(", ");
    });
    onSubmit(final);
  }

  const answered = questions.filter(q =>
    answers[q.id] || (multi[q.id]?.length > 0)
  ).length;

  return (
    <div style={{
      position:"fixed", inset:0, background:"#00000088",
      display:"flex", alignItems:"center", justifyContent:"center",
      zIndex:1000, backdropFilter:"blur(4px)",
      animation:"fadeIn .2s ease",
    }}>
      <div style={{
        background:"#0d1117", border:"1px solid #1e2736",
        borderRadius:16, padding:"28px 32px", width:480, maxWidth:"90vw",
        maxHeight:"85vh", overflow:"auto",
        boxShadow:"0 0 60px #6366f122",
      }}>
        {/* Header */}
        <div style={{ marginBottom:24 }}>
          <div style={{ fontSize:9, color:"#6366f1", letterSpacing:3, textTransform:"uppercase", marginBottom:6 }}>
            ◆ Quick Setup
          </div>
          <div style={{ fontSize:16, fontWeight:700, color:"#e2e8f0", marginBottom:4 }}>
            Building: <span style={{ color:"#a78bfa" }}>{idea}</span>
          </div>
          <div style={{ fontSize:10, color:"#374151" }}>
            Answer {questions.length} questions to get a better result
          </div>
        </div>

        {/* Progress bar */}
        <div style={{ background:"#1e2736", height:2, borderRadius:2, marginBottom:24, overflow:"hidden" }}>
          <div style={{
            height:"100%", borderRadius:2,
            background:"linear-gradient(90deg,#6366f1,#a78bfa)",
            width:`${(answered/questions.length)*100}%`,
            transition:"width .3s",
          }}/>
        </div>

        {/* Questions */}
        {questions.map((q, qi) => (
          <div key={q.id} style={{ marginBottom:20 }}>
            <div style={{ fontSize:11, color:"#94a3b8", marginBottom:10, display:"flex", gap:8, alignItems:"center" }}>
              <span style={{
                width:18, height:18, borderRadius:"50%",
                background: answers[q.id]||(multi[q.id]?.length>0) ? "#6366f1" : "#1e2736",
                display:"flex", alignItems:"center", justifyContent:"center",
                fontSize:9, flexShrink:0, transition:"background .2s",
              }}>{answers[q.id]||(multi[q.id]?.length>0) ? "✓" : qi+1}</span>
              {q.text}
            </div>

            <div style={{ display:"flex", flexWrap:"wrap", gap:6 }}>
              {q.options.map(opt => {
                const isMultiQ = q.type === "multi";
                const sel = isMultiQ
                  ? (multi[q.id]||[]).includes(opt)
                  : answers[q.id] === opt;
                return (
                  <button key={opt}
                    onClick={() => isMultiQ ? toggleMulti(q.id, opt) : handleChoice(q.id, opt)}
                    style={{
                      padding:"6px 14px", borderRadius:8, cursor:"pointer",
                      fontSize:10, transition:"all .15s", letterSpacing:.5,
                      background: sel ? "#6366f122" : "#0a0f16",
                      border: sel ? "1px solid #6366f1" : "1px solid #1e2736",
                      color: sel ? "#a78bfa" : "#475569",
                    }}
                  >{opt}</button>
                );
              })}
            </div>
          </div>
        ))}

        {/* Buttons */}
        <div style={{ display:"flex", gap:10, marginTop:24 }}>
          <button onClick={onSkip} style={{
            flex:1, padding:"10px", background:"transparent",
            border:"1px solid #1e2736", borderRadius:8,
            color:"#374151", cursor:"pointer", fontSize:10,
            transition:"all .2s",
          }}
          onMouseEnter={e=>e.currentTarget.style.borderColor="#374151"}
          onMouseLeave={e=>e.currentTarget.style.borderColor="#1e2736"}
          >
            Skip — Build with defaults
          </button>
          <button onClick={handleSubmit} style={{
            flex:2, padding:"10px",
            background: answered>0 ? "linear-gradient(135deg,#6366f1,#8b5cf6)" : "#1e2736",
            border:"none", borderRadius:8,
            color: answered>0 ? "#fff" : "#374151",
            cursor: answered>0 ? "pointer" : "not-allowed",
            fontSize:11, fontWeight:700, letterSpacing:1,
            transition:"all .2s",
            boxShadow: answered>0 ? "0 0 20px #6366f133" : "none",
          }}>
            ⚡ Build Now ({answered}/{questions.length} answered)
          </button>
        </div>
      </div>
    </div>
  );
}

// ─────────────────────────────────────────────────────────────
// MAIN APP
// ─────────────────────────────────────────────────────────────
export default function App() {
  const [input, setInput]           = useState("");
  const [stage, setStage]           = useState("idle"); // idle|clarify|building|done
  const [questions, setQuestions]   = useState([]);
  const [currentIdea, setCurrentIdea] = useState("");
  const [logs, setLogs]             = useState([]);
  const [phase, setPhase]           = useState(-1);
  const [files, setFiles]           = useState([]);
  const [previewHTML, setPreviewHTML] = useState("");
  const [projectName, setProjectName] = useState("");
  const [projects, setProjects]     = useState([]);
  const [activeTab, setActiveTab]   = useState("preview");
  const [selectedFile, setSelectedFile] = useState(null);
  const [iframeKey, setIframeKey]   = useState(0);
  const [agentsUsed, setAgentsUsed] = useState([]);
  const [templates, setTemplates]   = useState([]);
  const [selectedTemplate, setSelectedTemplate] = useState(null);
  const [patchInput, setPatchInput] = useState("");
  const [patchLoading, setPatchLoading] = useState(false);
  const [patchLogs, setPatchLogs]   = useState([]);
  const logEndRef = useRef(null);
  const inputRef  = useRef(null);
  const patchRef  = useRef(null);

  useEffect(()=>{ logEndRef.current?.scrollIntoView({behavior:"smooth"}); },[logs]);
  useEffect(()=>{
    fetch(`${API}/api/projects`).then(r=>r.json())
      .then(d=>setProjects(d.projects||[])).catch(()=>{});
    
    fetch(`${API}/api/templates`).then(r=>r.json())
      .then(d=>setTemplates(d.templates||[])).catch(()=>{});
  },[]);

  const addLog = (text, type="log") =>
    setLogs(p=>[...p,{text,type,t:new Date().toLocaleTimeString()}]);

  // ── Step 1: User submits idea → get questions ──────────────
  async function handleIdeaSubmit() {
    if (!input.trim() || stage!=="idle") return;
    const idea = input.trim();
    setCurrentIdea(idea);
    setInput("");

    try {
      const res = await fetch(`${API}/api/clarify`,{
        method:"POST",
        headers:{"Content-Type":"application/json"},
        body:JSON.stringify({idea}),
      });
      const data = await res.json();
      if (data.questions?.length) {
        setQuestions(data.questions);
        setStage("clarify");
      } else {
        startBuild(idea, {});
      }
    } catch {
      startBuild(idea, {});
    }
  }

  // ── Step 2: User answers questions → build ─────────────────
  function startBuild(idea, answers) {
    setStage("building");
    setLogs([]);
    setFiles([]);
    setProjectName("");
    setPhase(0);
    setActiveTab("preview");
    setPreviewHTML(LOADING_HTML);
    setIframeKey(k=>k+1);

    addLog(`💡 "${idea}"`, "input");
    addLog(`📋 Requirements: ${Object.values(answers).filter(Boolean).join(", ")||"defaults"}`, "log");
    addLog("", "sp");

    doBuild(idea, answers);
  }

  async function doBuild(idea, answers) {
    try {
      // Kick off background job — returns 202 immediately
      const res = await fetch(`${API}/api/run`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({idea, answers}),
      });
      const init = await res.json();
      const task_id = init.task_id;

      if (!task_id) {
        addLog("❌ Backend did not return a task_id", "error");
        setStage("idle");
        return;
      }

      // Show animated phase placeholders while polling
      setPhase(0);
      addLog("◆  PHASE 1 — PLANNING", "phase");
      addLog("   🔍 Search Agent: researching best patterns...", "log");
      addLog("   📋 Planning Agent: decomposing architecture...", "log");

      setTimeout(() => {
        setPhase(1);
        addLog("", "sp");
        addLog("◈  PHASE 2 — AGENTS RUNNING", "phase");
        addLog("   ⚡ Coding Agent: building components...", "log");
        addLog("   🤖 Parallel agents working in background...", "agent");
      }, 3000);

      // Poll /api/progress until 100% + data ready
      let data = null;
      const MAX_POLLS = 150; // 5 min max
      for (let i = 0; i < MAX_POLLS; i++) {
        await new Promise(r => setTimeout(r, 2000));

        let prog;
        try {
          const progRes = await fetch(`${API}/api/progress/${task_id}`);
          prog = await progRes.json();
        } catch {
          continue; // network blip — retry
        }

        // Show live status bubbles from backend
        const skip = ["Waiting...", "Complete!", "Initializing S.E.A.D.S. Pipeline..."];
        if (prog.status && !skip.includes(prog.status)) {
          addLog(`   ${prog.status}`, "log");
        }

        if (prog.status?.startsWith("Error:")) {
          addLog(`❌ ${prog.status}`, "error");
          setStage("idle");
          return;
        }

        // Done!
        if (prog.percent === 100 && prog.data) {
          data = prog.data;
          break;
        }
      }

      if (!data) {
        addLog("⚠️ Build timed out — try again", "error");
        setStage("idle");
        return;
      }

      // Animate real logs from completed build
      setPhase(2);
      addLog("", "sp");
      addLog("◉  PHASE 3 — QUALITY CHECK", "phase");
      (data.test_logs || []).forEach((l, i) =>
        setTimeout(() => addLog(l, "log"), i * 100)
      );
      await new Promise(r => setTimeout(r, (data.test_logs?.length || 3) * 100 + 400));

      // Inject preview
      setPhase(3);
      addLog("", "sp");
      addLog("◎  PHASE 4 — LIVE PREVIEW", "phase");

      const html  = data.preview_html;
      const pName = data.project_name || idea.replace(/\s+/g, "_").toLowerCase();
      const fList = data.files || [];

      if (html && html.length > 100) {
        addLog("🎨 Rendering interactive app...", "log");
        setTimeout(() => {
          setPreviewHTML(html);
          setIframeKey(k => k + 1);
          setProjectName(pName);
          setFiles(fList);
          setAgentsUsed(data.agents_used || []);
          if (fList.length) setSelectedFile(fList[0]);
          setStage("done");
          addLog(`✅ ${pName.replace(/_/g, " ")} is LIVE! 🎉`, "success");
          addLog(`🤖 ${data.agents_used?.length || 0} agents collaborated`, "success");
          setProjects(p => [{name: pName}, ...p.slice(0, 9)]);
        }, 800);
      } else {
        addLog("⚠️ preview_html missing — check backend logs", "error");
        setStage("idle");
      }

    } catch (err) {
      addLog(`❌ ${err.message}`, "error");
      setStage("idle");
    }
  }


  function resetAll() {
    setLogs([]); setFiles([]); setPreviewHTML("");
    setProjectName(""); setPhase(-1); setStage("idle");
    setQuestions([]); setCurrentIdea(""); setAgentsUsed([]);
    setPatchLogs([]); setPatchInput("");
    inputRef.current?.focus();
  }

  // ── Patch / Refine handler ─────────────────────────────────
  async function handlePatch() {
    const instruction = patchInput.trim();
    if (!instruction || !previewHTML || patchLoading) return;

    setPatchLoading(true);
    setPatchLogs(p => [...p, { role: "user", text: instruction }]);
    setPatchInput("");

    try {
      const res = await fetch(`${API}/api/patch`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          html: previewHTML,
          instruction,
          category: currentIdea || "more",
        }),
      });
      const data = await res.json();

      if (!res.ok || data.status === "empty") {
        setPatchLogs(p => [...p, { role: "ai",
          text: `⚠️ ${data.error || "Improvement failed — try rephrasing."}` }]);
        return;
      }

      if (data.patched_html && data.patched_html.length > 200) {
        setPreviewHTML(data.patched_html);
        setIframeKey(k => k + 1);
        setActiveTab("preview");
        const delta = data.patch_analysis?.delta_chars ?? 0;
        const model = data.patch_analysis?.model || "DeepSeek Coder";
        setPatchLogs(p => [...p, {
          role: "ai",
          text: `✅ Improved in ${data.elapsed}s · ${delta >= 0 ? "+" : ""}${delta} chars · ${model}`,
        }]);
        addLog(`🔧 Improved: "${instruction}"`, "agent");
      } else {
        setPatchLogs(p => [...p, { role: "ai",
          text: "⚠️ Model returned no output — try a different instruction." }]);
      }
    } catch (e) {
      setPatchLogs(p => [...p, { role: "ai", text: `❌ Network error: ${e.message}` }]);
    } finally {
      setPatchLoading(false);
      setTimeout(() => patchRef.current?.scrollIntoView({ behavior: "smooth" }), 100);
    }
  }

  const LC = {
    phase:"#a78bfa",success:"#34d399",error:"#f87171",
    input:"#fbbf24",log:"#374151",agent:"#60a5fa",sp:"transparent",
  };
  const building = stage==="building";

  return (
    <div style={{display:"flex",height:"100vh",width:"100vw",background:"#060a0d",
      color:"#e2e8f0",fontFamily:"'JetBrains Mono','Fira Code',monospace",overflow:"hidden"}}>

      {/* ── CLARIFICATION DIALOG ── */}
      {stage==="clarify" && (
        <ClarifyDialog
          idea={currentIdea}
          questions={questions}
          onSubmit={ans => startBuild(currentIdea, ans)}
          onSkip={() => startBuild(currentIdea, {})}
        />
      )}

      {/* ══ SIDEBAR ══ */}
      <div style={{width:210,background:"#080c10",borderRight:"1px solid #0f1820",
        display:"flex",flexDirection:"column",flexShrink:0}}>

        <div style={{padding:"18px 16px 14px",borderBottom:"1px solid #0f1820"}}>
          <div style={{display:"flex",alignItems:"center",gap:10}}>
            <div style={{width:34,height:34,borderRadius:9,
              background:"linear-gradient(135deg,#6366f1,#8b5cf6)",
              display:"flex",alignItems:"center",justifyContent:"center",
              fontSize:17,boxShadow:"0 0 24px #6366f133"}}>⚡</div>
            <div>
              <div style={{fontSize:13,fontWeight:700,color:"#e2e8f0",letterSpacing:1}}>S.E.A.D.S.</div>
              <div style={{fontSize:8,color:"#1e2736",letterSpacing:1.5}}>AI BUILDER v3.0</div>
            </div>
          </div>
        </div>

        <div style={{padding:"10px 12px 6px"}}>
          <button onClick={resetAll} style={{
            width:"100%",padding:"8px 12px",background:"#0a0f16",
            border:"1px solid #131d2b",borderRadius:8,color:"#374151",
            cursor:"pointer",fontSize:10,display:"flex",alignItems:"center",gap:8,
            transition:"all .2s",letterSpacing:1,
          }}
          onMouseEnter={e=>{e.currentTarget.style.borderColor="#6366f150";e.currentTarget.style.color="#94a3b8";}}
          onMouseLeave={e=>{e.currentTarget.style.borderColor="#131d2b";e.currentTarget.style.color="#374151";}}>
            <span style={{fontSize:15}}>＋</span> New Thread
          </button>
        </div>

        {/* Phase tracker */}
        <div style={{padding:"6px 12px 10px",borderBottom:"1px solid #0f1820"}}>
          {PHASES.map((p,i)=>(
            <div key={i} style={{display:"flex",alignItems:"center",gap:8,
              padding:"5px 8px",borderRadius:6,marginBottom:1,
              background:phase===i?"#0d1520":"transparent",transition:"all .3s"}}>
              <span style={{fontSize:10,color:phase>i?"#34d399":phase===i?p.color:"#111d2b",transition:"color .3s"}}>
                {phase>i?"✓":p.icon}
              </span>
              <span style={{fontSize:10,color:phase>i?"#34d39970":phase===i?p.color:"#1a2436",transition:"color .3s"}}>
                {p.label}
              </span>
              {phase===i&&building&&(
                <div style={{marginLeft:"auto",width:5,height:5,borderRadius:"50%",
                  background:p.color,animation:"pulse 1s infinite"}}/>
              )}
            </div>
          ))}
        </div>

        {/* Agent list when building */}
        {(building || agentsUsed.length > 0) && (
          <div style={{padding:"8px 12px",borderBottom:"1px solid #0f1820"}}>
            <div style={{fontSize:8,color:"#1a2436",letterSpacing:2,marginBottom:6,textTransform:"uppercase"}}>
              Active Agents
            </div>
            <div style={{display:"flex",flexWrap:"wrap",gap:3}}>
              {agentsUsed.slice(0,12).map((a,i)=>(
                <span key={i} style={{
                  fontSize:7,padding:"2px 6px",borderRadius:3,letterSpacing:.5,
                  background:"#0a0f1a",border:"1px solid #1a2436",color:"#374151",
                }}>
                  {a}
                </span>
              ))}
              {agentsUsed.length>12&&(
                <span style={{fontSize:7,color:"#374151"}}>+{agentsUsed.length-12} more</span>
              )}
            </div>
          </div>
        )}

        {/* Past builds */}
        <div style={{flex:1,overflow:"auto",padding:"8px 12px"}}>
          <div style={{fontSize:8,color:"#111d2b",letterSpacing:2.5,padding:"4px 8px 8px",textTransform:"uppercase"}}>
            Past Builds
          </div>
          {projects.map((p,i)=>(
            <div key={i} style={{display:"flex",alignItems:"center",gap:7,
              padding:"5px 8px",borderRadius:6,marginBottom:1,cursor:"pointer",transition:"all .2s"}}
            onMouseEnter={e=>e.currentTarget.style.background="#0a0f16"}
            onMouseLeave={e=>e.currentTarget.style.background="transparent"}>
              <span style={{width:4,height:4,borderRadius:"50%",background:"#131d2b",flexShrink:0}}/>
              <span style={{fontSize:9,color:"#2d3748",overflow:"hidden",
                textOverflow:"ellipsis",whiteSpace:"nowrap"}}>
                {p.name?.replace(/_/g," ")||"untitled"}
              </span>
            </div>
          ))}
        </div>

        <div style={{padding:"10px 16px",borderTop:"1px solid #0f1820"}}>
          <div style={{display:"flex",alignItems:"center",gap:6,marginBottom:3}}>
            <div style={{width:5,height:5,borderRadius:"50%",background:"#34d399",boxShadow:"0 0 6px #34d399"}}/>
            <span style={{fontSize:9,color:"#2d3748"}}>5 Groq Keys Active</span>
          </div>
          <div style={{fontSize:8,color:"#1a2436",letterSpacing:.5}}>20+ Agents ⚡ Turbo Mode</div>
        </div>
      </div>

      {/* ══ MIDDLE LOG ══ */}
      <div style={{width:320,display:"flex",flexDirection:"column",
        borderRight:"1px solid #0f1820",background:"#060a0d"}}>

        <div style={{padding:"13px 18px",borderBottom:"1px solid #0f1820",
          display:"flex",alignItems:"center",gap:10}}>
          <div style={{width:7,height:7,borderRadius:"50%",
            background:building?"#fbbf24":stage==="done"?"#34d399":"#131d2b",
            boxShadow:building?"0 0 8px #fbbf24":stage==="done"?"0 0 8px #34d399":"none",
            transition:"all .3s"}}/>
          <span style={{fontSize:10,color:"#2d3748",letterSpacing:1.5,textTransform:"uppercase"}}>
            {building?"BUILDING...":projectName?projectName.replace(/_/g," ").toUpperCase():"AWAITING INPUT"}
          </span>
        </div>

        <div style={{flex:1,overflow:"auto",padding:"12px 16px",display:"flex",flexDirection:"column",gap:1}}>
          {logs.length===0&&(
            <div style={{flex:1,display:"flex",flexDirection:"column",alignItems:"center",
              justifyContent:"center",paddingTop:60}}>
              <div style={{fontSize:32,opacity:.15,marginBottom:12}}>◈</div>
              <div style={{fontSize:9,letterSpacing:3,color:"#131d2b",textTransform:"uppercase"}}>20+ Agents Ready</div>
              <div style={{fontSize:9,color:"#0f1820",marginTop:6}}>type an idea → answer questions → build</div>
            </div>
          )}
          {logs.map((log,i)=>(
            log.type==="sp"
              ? <div key={i} style={{height:5}}/>
              : <div key={i} style={{display:"flex",gap:10,alignItems:"flex-start",animation:"fadeIn .2s ease"}}>
                  {log.type!=="phase"&&(
                    <span style={{fontSize:8,color:"#0f1820",marginTop:2,flexShrink:0,width:48}}>{log.t}</span>
                  )}
                  <span style={{fontSize:10,color:LC[log.type]||"#374151",
                    fontWeight:log.type==="phase"?700:400,
                    letterSpacing:log.type==="phase"?1.5:0,lineHeight:1.7}}>
                    {log.text}
                  </span>
                </div>
          ))}
          <div ref={logEndRef}/>
        </div>

        <div style={{padding:"10px 12px",borderTop:"1px solid #0f1820",background:"#050810"}}>
          <div style={{display:"flex",gap:8,alignItems:"center",
            background:"#080c10",
            border:`1px solid ${building?"#6366f115":input.trim()?"#6366f135":"#0f1820"}`,
            borderRadius:10,padding:"8px 12px",transition:"border-color .3s"}}>
            <span style={{color:"#1a2436",fontSize:13}}>›</span>
            <input ref={inputRef} value={input}
              onChange={e=>setInput(e.target.value)}
              onKeyDown={e=>e.key==="Enter"&&handleIdeaSubmit()}
              placeholder={building?"Building...":"create chess game, free fire, linkedin..."}
              disabled={building||stage==="clarify"}
              style={{flex:1,background:"transparent",border:"none",outline:"none",
                color:"#94a3b8",fontSize:10,fontFamily:"inherit",letterSpacing:.5}}/>
            <button onClick={handleIdeaSubmit}
              disabled={building||!input.trim()||stage==="clarify"}
              style={{width:26,height:26,borderRadius:6,
                background:building?"#0f1820":input.trim()?"#6366f1":"#0f1820",
                border:"none",cursor:building||!input.trim()?"not-allowed":"pointer",
                display:"flex",alignItems:"center",justifyContent:"center",
                fontSize:11,transition:"all .2s",
                boxShadow:input.trim()&&!building?"0 0 14px #6366f155":"none"}}>
              {building?"⏸":"▶"}
            </button>
          </div>
          {stage==="idle"&&(
            <div style={{fontSize:8,color:"#131d2b",marginTop:5,textAlign:"center",letterSpacing:1}}>
              Press Enter → Answer questions → 20+ agents build your app
            </div>
          )}
        </div>
      </div>

      {/* ══ RIGHT PREVIEW ══ */}
      <div style={{flex:1,display:"flex",flexDirection:"column",overflow:"hidden"}}>

        <div style={{display:"flex",alignItems:"center",borderBottom:"1px solid #0f1820",
          background:"#060a0d",padding:"0 16px",gap:2}}>
          {[
            {id:"preview",label:"◎  Canvas Preview"},
            {id:"templates",label:"🗃️  Templates"},
            {id:"files",  label:"📁  Files"},
            {id:"code",   label:"📝  Code"},
          ].map(tab=>(
            <button key={tab.id} onClick={()=>setActiveTab(tab.id)} style={{
              padding:"11px 14px",background:"transparent",border:"none",cursor:"pointer",
              fontSize:9,letterSpacing:1.5,textTransform:"uppercase",
              color:activeTab===tab.id?"#e2e8f0":"#1a2436",
              borderBottom:activeTab===tab.id?"2px solid #6366f1":"2px solid transparent",
              transition:"all .2s"}}>
              {tab.label}
            </button>
          ))}
          <div style={{marginLeft:"auto",display:"flex",gap:8,alignItems:"center"}}>
            {agentsUsed.length>0&&(
              <div style={{fontSize:8,color:"#374151",letterSpacing:1,
                background:"#0a0f16",border:"1px solid #131d2b",
                borderRadius:20,padding:"3px 10px"}}>
                🤖 {agentsUsed.length} agents
              </div>
            )}
            {building&&(
              <div style={{display:"flex",alignItems:"center",gap:6,background:"#fbbf2410",
                border:"1px solid #fbbf2420",borderRadius:20,padding:"3px 10px",
                fontSize:9,color:"#fbbf24"}}>
                <div style={{width:5,height:5,borderRadius:"50%",background:"#fbbf24",animation:"pulse 1s infinite"}}/>
                Building...
              </div>
            )}
            {stage==="done"&&(
              <div style={{display:"flex",alignItems:"center",gap:6,background:"#34d39910",
                border:"1px solid #34d39920",borderRadius:20,padding:"3px 10px",
                fontSize:9,color:"#34d399",letterSpacing:1}}>
                <div style={{width:5,height:5,borderRadius:"50%",background:"#34d399",boxShadow:"0 0 6px #34d399"}}/>
                LIVE
              </div>
            )}
          </div>
        </div>

        {/* Preview iframe + Refine chat */}
        {activeTab==="preview"&&(
          <div style={{flex:1,position:"relative",overflow:"hidden",background:"#060a0d",display:"flex",flexDirection:"column"}}>

            {/* Iframe */}
            <div style={{flex:1,position:"relative",overflow:"hidden"}}>
              {previewHTML ? (
                <iframe key={iframeKey} srcDoc={previewHTML}
                  style={{width:"100%",height:"100%",border:"none"}}
                  sandbox="allow-scripts allow-same-origin allow-forms allow-modals"
                  title="live-preview"/>
              ) : (
                <div style={{height:"100%",display:"flex",flexDirection:"column",
                  alignItems:"center",justifyContent:"center"}}>
                  <div style={{fontSize:40,opacity:.1,marginBottom:12}}>◎</div>
                  <div style={{fontSize:9,color:"#131d2b",letterSpacing:3,textTransform:"uppercase"}}>Live Preview</div>
                  <div style={{fontSize:8,color:"#0f1820",marginTop:6}}>Build something to see it here</div>
                </div>
              )}
            </div>

            {/* ── Refine / Patch Chat Bar ── only shown when project is LIVE */}
            {stage === "done" && previewHTML && (
              <div style={{
                borderTop:"1px solid #0f1820",
                background:"#070b0f",
                padding:"0",
                flexShrink:0,
              }}>

                {/* Patch history log */}
                {patchLogs.length > 0 && (
                  <div style={{
                    maxHeight:140, overflowY:"auto",
                    padding:"10px 16px",
                    display:"flex",flexDirection:"column",gap:6,
                    borderBottom:"1px solid #0f1820",
                  }}>
                    {patchLogs.map((m, i) => (
                      <div key={i} style={{
                        display:"flex", gap:8, alignItems:"flex-start",
                        justifyContent: m.role==="user" ? "flex-end" : "flex-start",
                        animation:"fadeIn .2s ease",
                      }}>
                        {m.role==="ai" && (
                          <div style={{width:18,height:18,borderRadius:"50%",
                            background:"linear-gradient(135deg,#6366f1,#8b5cf6)",
                            display:"flex",alignItems:"center",justifyContent:"center",
                            fontSize:9,flexShrink:0}}>⚡</div>
                        )}
                        <div style={{
                          fontSize:9, lineHeight:1.6,
                          padding:"5px 10px",
                          borderRadius: m.role==="user" ? "10px 10px 2px 10px" : "10px 10px 10px 2px",
                          background: m.role==="user" ? "#1e2736" : "#0d1520",
                          border: m.role==="user" ? "1px solid #2d3748" : "1px solid #1a2d4a",
                          color: m.role==="user" ? "#94a3b8" : "#60a5fa",
                          maxWidth:"75%",
                        }}>{m.text}</div>
                        {m.role==="user" && (
                          <div style={{width:18,height:18,borderRadius:"50%",
                            background:"#1e2736",border:"1px solid #2d3748",
                            display:"flex",alignItems:"center",justifyContent:"center",
                            fontSize:9,flexShrink:0}}>U</div>
                        )}
                      </div>
                    ))}
                    <div ref={patchRef}/>
                  </div>
                )}

                {/* Input row */}
                <div style={{padding:"10px 12px"}}>
                  <div style={{
                    display:"flex", alignItems:"center", gap:8,
                    background:"#080c10",
                    border:`1px solid ${patchLoading?"#6366f160":patchInput.trim()?"#6366f140":"#131d2b"}`,
                    borderRadius:10, padding:"7px 12px",
                    transition:"border-color .3s",
                    boxShadow: patchInput.trim() ? "0 0 20px #6366f115" : "none",
                  }}>
                    <span style={{fontSize:9,color:"#6366f1",fontWeight:700,letterSpacing:1,flexShrink:0,
                      whiteSpace:"nowrap"}}>
                      {patchLoading ? "⏳" : "✦"} {patchLoading ? "PATCHING..." : "REFINE · PATCH · ENHANCE"}
                    </span>
                    <div style={{width:1,height:14,background:"#1a2436",flexShrink:0}}/>
                    <input
                      value={patchInput}
                      onChange={e => setPatchInput(e.target.value)}
                      onKeyDown={e => e.key==="Enter" && handlePatch()}
                      placeholder={previewHTML ? "Make the navbar sticky... Add dark mode... Change colors..." : "Build a project first..."}
                      disabled={patchLoading || !previewHTML}
                      style={{
                        flex:1, background:"transparent", border:"none", outline:"none",
                        color:"#94a3b8", fontSize:10, fontFamily:"inherit", letterSpacing:.5,
                      }}
                    />
                    <button
                      onClick={handlePatch}
                      disabled={patchLoading || !patchInput.trim() || !previewHTML}
                      style={{
                        padding:"4px 12px",
                        background: patchLoading ? "#0f1820" : patchInput.trim() ? "linear-gradient(135deg,#6366f1,#8b5cf6)" : "#0f1820",
                        border:"none", borderRadius:7, cursor: patchLoading||!patchInput.trim() ? "not-allowed" : "pointer",
                        fontSize:10, fontWeight:700, color: patchInput.trim()&&!patchLoading ? "#fff" : "#374151",
                        transition:"all .2s",
                        boxShadow: patchInput.trim()&&!patchLoading ? "0 0 16px #6366f155" : "none",
                        letterSpacing:1,
                      }}
                    >
                      {patchLoading ? (
                        <span style={{display:"flex",alignItems:"center",gap:5}}>
                          <span style={{width:8,height:8,border:"1.5px solid #6366f1",borderTopColor:"transparent",
                            borderRadius:"50%",display:"inline-block",animation:"spin 0.7s linear infinite"}}/>
                          Patching
                        </span>
                      ) : "↑ Apply"}
                    </button>
                  </div>
                  <div style={{fontSize:8,color:"#1a2436",marginTop:4,letterSpacing:.5,textAlign:"center"}}>
                    v14 Smart Patch Engine · IIT-Level · Powered by DeepSeek Coder via OpenRouter
                  </div>
                </div>
              </div>
            )}

          </div>
        )}

        {/* 🗃️ Templates Tab */}
        {activeTab==="templates" && (
          <div style={{flex:1,overflow:"auto",padding:28,background:"#060a0d",animation:"fadeIn .4s ease"}}>
            <div style={{marginBottom:32}}>
              <div style={{fontSize:9,color:"#6366f1",letterSpacing:4,textTransform:"uppercase",marginBottom:8}}>
                ◆ Core Engine Templates
              </div>
              <div style={{fontSize:18,fontWeight:800,color:"#e2e8f0",letterSpacing:0.5}}>
                Template <span style={{color:"#a78bfa"}}>Architecture</span> Swarm
              </div>
              <div style={{fontSize:10,color:"#374151",marginTop:6}}>
                Ready to deploy: {templates.length} curated design frameworks
              </div>
            </div>
            
            <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))",gap:20}}>
              {templates.map((t,i)=>(
                <div key={i} 
                  onClick={async ()=>{
                    setSelectedTemplate(t);
                    const res = await fetch(`${API}/api/template-details?name=${encodeURIComponent(t.name)}`);
                    const data = await res.json();
                    if(data.success) {
                      setPreviewHTML(data.content);
                      setIframeKey(k=>k+1);
                      setActiveTab("preview");
                      setInput(t.name.split("/").pop().replace(".html","").replace(/_/g," "));
                      addLog(`🎨 Hooked into template: ${t.name}`, "agent");
                    }
                  }}
                  style={{
                    background:"#080c10", border:selectedTemplate?.name===t.name?"1px solid #6366f188":"1px solid #131d2b",
                    borderRadius:14, padding:"24px", cursor:"pointer", transition:"all.3s cubic-bezier(0.4, 0, 0.2, 1)",
                    boxShadow:selectedTemplate?.name===t.name?"0 10px 30px #6366f115":"none",
                    position:"relative", overflow:"hidden"
                  }}
                  onMouseEnter={e=>{
                    if(selectedTemplate?.name!==t.name) e.currentTarget.style.borderColor="#6366f150";
                    e.currentTarget.style.transform="translateY(-4px)";
                  }}
                  onMouseLeave={e=>{
                    if(selectedTemplate?.name!==t.name) e.currentTarget.style.borderColor="#131d2b";
                    e.currentTarget.style.transform="translateY(0)";
                  }}>
                  {/* Glass accent */}
                  <div style={{position:"absolute", top:-10, right:-10, width:60, height:60, 
                    background:"linear-gradient(135deg, #6366f120, transparent)", borderRadius:"50%", filter:"blur(20px)"}}/>
                  
                  <div style={{fontSize:38,marginBottom:16,filter:"drop-shadow(0 4px 8px rgba(0,0,0,0.5))"}}>
                    {t.name.toLowerCase().includes("game")?"🎮":
                     t.name.toLowerCase().includes("dash")?"📊":
                     t.name.toLowerCase().includes("link")?"👥":
                     t.name.toLowerCase().includes("ecommerce")?"🛍️":
                     t.name.toLowerCase().includes("port")?"👤":"🌐"}
                  </div>
                  
                  <div style={{fontSize:12,color:"#f8fafc",fontWeight:700,marginBottom:6,
                    letterSpacing:0.5,overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>
                    {t.name.split("/").pop().replace(".html","").replace(/_/g," ").toUpperCase()}
                  </div>
                  
                  <div style={{fontSize:9,color:"#475569",marginBottom:14,fontFamily:"monospace"}}>
                    FOLDER: <span style={{color:"#6366f188"}}>{t.folder}</span>
                  </div>
                  
                  <div style={{display:"flex",justifyContent:"space-between",alignItems:"center",marginTop:"auto"}}>
                    <div style={{display:"flex",flexDirection:"column"}}>
                      <span style={{fontSize:7,color:"#1e293b",letterSpacing:1,textTransform:"uppercase"}}>Framework Size</span>
                      <span style={{fontSize:10,color:"#6366f1",fontWeight:600}}>{(t.size/1024).toFixed(1)} KB</span>
                    </div>
                    <button style={{
                      padding:"7px 14px", background:"linear-gradient(135deg,#6366f1,#8b5cf6)", border:"none",
                      borderRadius:8, color:"#fff", fontSize:9, fontWeight:700, cursor:"pointer",
                      boxShadow:"0 4px 12px #6366f144", transition:"all.2s"
                    }}>PREVIEW</button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Files tab */}
        {activeTab==="files"&&(
          <div style={{flex:1,overflow:"auto",padding:20}}>
            {files.length===0
              ? <div style={{color:"#131d2b",fontSize:10,textAlign:"center",marginTop:80}}>No files yet</div>
              : <div style={{display:"grid",gridTemplateColumns:"repeat(auto-fill,minmax(180px,1fr))",gap:10}}>
                  {files.map((f,i)=>(
                    <div key={i} onClick={()=>{setSelectedFile(f);setActiveTab("code");}}
                      style={{background:"#080c10",border:"1px solid #0f1820",borderRadius:10,
                        padding:"16px",cursor:"pointer",transition:"all .2s"}}
                      onMouseEnter={e=>{e.currentTarget.style.borderColor="#6366f150";e.currentTarget.style.background="#0c1118";}}
                      onMouseLeave={e=>{e.currentTarget.style.borderColor="#0f1820";e.currentTarget.style.background="#080c10";}}>
                      <div style={{fontSize:26,marginBottom:10}}>{getIcon(f.name||"")}</div>
                      <div style={{fontSize:10,color:"#94a3b8",marginBottom:4}}>{f.name}</div>
                      <div style={{fontSize:9,color:"#1a2436"}}>{f.size} chars</div>
                    </div>
                  ))}
                </div>
            }
          </div>
        )}

        {/* Code tab */}
        {activeTab==="code"&&(
          <div style={{display:"flex",flex:1,overflow:"hidden"}}>
            <div style={{width:145,borderRight:"1px solid #0f1820",overflow:"auto",padding:"8px",background:"#060a0d"}}>
              {files.map((f,i)=>(
                <div key={i} onClick={()=>setSelectedFile(f)}
                  style={{padding:"5px 9px",borderRadius:5,cursor:"pointer",fontSize:9,
                    display:"flex",alignItems:"center",gap:5,marginBottom:1,transition:"all .15s",
                    background:selectedFile?.name===f.name?"#0d1520":"transparent",
                    color:selectedFile?.name===f.name?"#94a3b8":"#1e2736"}}
                  onMouseEnter={e=>{if(selectedFile?.name!==f.name)e.currentTarget.style.background="#080c10";}}
                  onMouseLeave={e=>{if(selectedFile?.name!==f.name)e.currentTarget.style.background="transparent";}}>
                  <span>{getIcon(f.name||"")}</span>
                  <span style={{overflow:"hidden",textOverflow:"ellipsis",whiteSpace:"nowrap"}}>{f.name}</span>
                </div>
              ))}
            </div>
            <div style={{flex:1,overflow:"auto",padding:"14px 18px",background:"#050810"}}>
              {selectedFile
                ? <pre style={{fontSize:10,lineHeight:1.9,color:"#374151",whiteSpace:"pre-wrap",wordBreak:"break-all"}}>
                    {(selectedFile.content||"# empty").split("\n").map((line,i)=>(
                      <span key={i}>
                        <span style={{color:"#0f1820",userSelect:"none",marginRight:14,
                          display:"inline-block",minWidth:28,textAlign:"right"}}>{i+1}</span>
                        <span style={{color:
                          line.trim().startsWith("#")||line.trim().startsWith("//")?"#1e2736"
                          :/^\s*(def |class |function )/.test(line)?"#a78bfa"
                          :/^\s*(import |from |const |let |var )/.test(line)?"#60a5fa"
                          :/^\s*(return |if |else|for |while )/.test(line)?"#f472b6"
                          :"#374151"
                        }}>{line}</span>{"\n"}
                      </span>
                    ))}
                  </pre>
                : <div style={{color:"#131d2b",fontSize:10,textAlign:"center",marginTop:80}}>Select a file</div>
              }
            </div>
          </div>
        )}
      </div>

      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;600;700&display=swap');
        *{box-sizing:border-box}
        ::-webkit-scrollbar{width:3px;height:3px}
        ::-webkit-scrollbar-track{background:transparent}
        ::-webkit-scrollbar-thumb{background:#131d2b;border-radius:2px}
        @keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}
        @keyframes fadeIn{from{opacity:0;transform:translateY(3px)}to{opacity:1;transform:translateY(0)}}
        @keyframes spin{to{transform:rotate(360deg)}}
      `}</style>
    </div>
  );
}
