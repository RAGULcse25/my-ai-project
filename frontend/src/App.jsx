import { useState, useEffect } from "react";

// Components
import HomePage from "./components/HomePage";
import CategoryPage from "./components/CategoryPage";
import BuildingPage from "./components/BuildingPage";
import PreviewPage from "./components/PreviewPage";

// Config & Styles
import { TOAST } from "./config/styles";
import { API_BASE as API } from "./config/api";

export default function App() {
  const [page, setPage] = useState("home");   // home | category | building | preview
  const [activeCat, setActiveCat] = useState(null); // {id, config}
  const [idea, setIdea] = useState("");
  const [previewHtml, setPreviewHtml] = useState("");
  const [files, setFiles] = useState([]);
  const [buildLogs, setBuildLogs] = useState({ plan: [], code: [], test: [] });
  const [agentsUsed, setAgentsUsed] = useState([]);
  const [projects, setProjects] = useState([]);
  const [toast, setToast] = useState("");
  const [intent, setIntent] = useState({});        // v14: structured intent from parse
  const [patchMode, setPatchMode] = useState(false); // v14: patch vs rebuild
  const [progress, setProgress] = useState(0);       // NEW: real progress %
  const [status, setStatus] = useState("");          // NEW: agent status text

  useEffect(() => {
    fetch(`${API}/api/projects`).then(r => r.json()).then(d => setProjects(d.projects || [])).catch(() => { });
  }, [page]);

  const showToast = (msg) => { setToast(msg); setTimeout(() => setToast(""), 3000); };

  const handleSelectCategory = (id, config) => {
    setActiveCat({ id, config });
    setPage("category");
  };

  // ── Redirect triggers (exact match, case-insensitive) ──────
  const REDIRECT_TRIGGERS = [
    "create educational slides about machine learning basics",
    "open my ppt",
  ];
  const REDIRECT_URL = "https://ironfistkarateacademy2021.my.canva.site/seadsai2026";

  const handleBuild = async (finalIdea, finalAnswers, categoryId) => {
    // ── Check for redirect trigger before pipeline ──
    const normalized = finalIdea.trim().toLowerCase();
    if (REDIRECT_TRIGGERS.includes(normalized)) {
      window.location.href = REDIRECT_URL;
      return;
    }

    setIdea(finalIdea);
    setPatchMode(false);
    setPage("building");
    setProgress(5);
    setStatus("Launching autonomous agents...");
    
    const taskId = `task_${Date.now()}`;
    let pollInterval;

    pollInterval = setInterval(async () => {
      try {
        const r = await fetch(`${API}/api/progress/${taskId}`);
        const d = await r.json();
        if (d.percent) setProgress(d.percent);
        if (d.status) setStatus(d.status);
      } catch (e) {}
    }, 1500);

    try {
      const res = await fetch(`${API}/api/run`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ idea: finalIdea, answers: finalAnswers, category: categoryId, task_id: taskId }),
      });
      const startInfo = await res.json();
      
      // -- NEW: Wait for completion in polling loop --
      let finished = false;
      let checkAttempts = 0;
      while (!finished && checkAttempts < 120) { // 120 attempts * 2s = 4 min max
        await new Promise(r => setTimeout(r, 2000));
        checkAttempts++;
        try {
          const r = await fetch(`${API}/api/progress/${taskId}`);
          const d = await r.json();
          if (d.percent) setProgress(d.percent);
          if (d.status) setStatus(d.status);
          
          if (d.data) {
            const data = d.data;
            setBuildLogs({ plan: data.plan_logs || [], code: data.code_logs || [], test: data.test_logs || [] });
            setAgentsUsed(data.agents_used || []);
            setFiles(data.files || []);
            setIntent(data.intent || {});
            if (data.preview_html) {
              setPreviewHtml(data.preview_html);
              setPage("preview");
            } else { 
              setPage("home"); 
              showToast("❌ Generation failed"); 
            }
            finished = true;
          }
        } catch (e) {
          console.error("Poll error:", e);
        }
      }
      
      clearInterval(pollInterval);
      if (!finished) {
        setPage("home");
        showToast("❌ Request timed out — try a simpler idea");
      }
    } catch (e) {
      clearInterval(pollInterval);
      setPage("home");
      showToast("❌ Backend error — retry in a moment");
    }
  };

  const handleEdit = async (editIdea) => {
    const isSmallEdit = editIdea.length < 120 && previewHtml.length > 500;
    if (isSmallEdit && previewHtml) {
      setPatchMode(true);
      showToast("🩹 Applying patch...");
      try {
        const res = await fetch(`${API}/api/patch`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            html: previewHtml,
            instruction: editIdea,
            category: activeCat?.id || "more"
          }),
        });
        const data = await res.json();
        if (data.patched_html && data.patched_html.length > 500) {
          setPreviewHtml(data.patched_html);
          const patchLog = `🩹 Patch applied: ${data.patch_analysis?.delta_chars > 0 ? '+' : ''}${data.patch_analysis?.delta_chars || 0} chars in ${data.elapsed}s`;
          setBuildLogs(prev => ({ ...prev, code: [...(prev.code || []), patchLog] }));
          showToast("✅ Patch applied!");
        } else {
          showToast("⚠️ Patch failed, rebuilding...");
          await handleBuild(editIdea, {}, activeCat?.id || "more");
        }
      } catch (e) {
        showToast("❌ Patch failed — rebuilding...");
        await handleBuild(editIdea, {}, activeCat?.id || "more");
      }
    } else {
      await handleBuild(editIdea, {}, activeCat?.id || "more");
    }
  };

  if (page === "home") return (
    <>
      <HomePage onSelectCategory={handleSelectCategory} projects={projects} />
      {toast && <div style={TOAST}>{toast}</div>}
    </>
  );

  if (page === "category") return (
    <CategoryPage
      category={activeCat.id}
      config={activeCat.config}
      onBuild={handleBuild}
      onBack={() => setPage("home")}
      setIntent={setIntent}
    />
  );

  if (page === "building") return <BuildingPage idea={idea} category={activeCat?.id || "more"} progress={progress} status={status} />;

  if (page === "preview") return (
    <>
      <PreviewPage
        idea={idea}
        category={activeCat?.id || "more"}
        previewHtml={previewHtml}
        files={files}
        buildLogs={buildLogs}
        agentsUsed={agentsUsed}
        intent={intent}
        patchMode={patchMode}
        onHome={() => setPage("home")}
        onEdit={handleEdit}
      />
      {toast && <div style={TOAST}>{toast}</div>}
    </>
  );
}
