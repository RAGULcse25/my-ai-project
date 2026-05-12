import React, { useState } from 'react';
import Editor from "@monaco-editor/react";

// ─── Empty Preview Fallback (fixes blank iframe bug) ─────────
const EmptyPreview = ({ onRetry, onOpenNew, hasRawHtml }) => (
  <div style={{
    width: '100%', height: '100%',
    display: 'flex', flexDirection: 'column',
    alignItems: 'center', justifyContent: 'center',
    background: 'linear-gradient(135deg, #080c14 0%, #0d1020 50%, #080c14 100%)',
    gap: 24, padding: 32, position: 'relative', overflow: 'hidden',
  }}>
    <div style={{ position:'absolute', top:'20%', left:'20%', width:200, height:200, borderRadius:'50%',
      background:'radial-gradient(circle, rgba(196,181,253,0.08) 0%, transparent 70%)',
      animation:'animeFloat 6s ease-in-out infinite', pointerEvents:'none' }} />
    <div style={{ position:'absolute', bottom:'20%', right:'20%', width:150, height:150, borderRadius:'50%',
      background:'radial-gradient(circle, rgba(249,168,212,0.06) 0%, transparent 70%)',
      animation:'animeFloat 8s ease-in-out infinite 2s', pointerEvents:'none' }} />
    <div style={{
      width:80, height:80, borderRadius:24,
      background:'rgba(196,181,253,0.08)', border:'1px solid rgba(196,181,253,0.25)',
      display:'flex', alignItems:'center', justifyContent:'center', fontSize:36,
      animation:'animeFloat 3s ease-in-out infinite',
      boxShadow:'0 0 40px rgba(196,181,253,0.15)',
    }}>🌸</div>
    <div style={{ textAlign:'center', zIndex:1 }}>
      <div style={{
        fontSize:18, fontWeight:800, fontFamily:"'Syne', sans-serif", marginBottom:10,
        background:'linear-gradient(135deg, #c4b5fd, #93c5fd, #f9a8d4)',
        WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent',
      }}>Preview Unavailable</div>
      <div style={{ fontSize:11, color:'#4b5563', fontFamily:'monospace', lineHeight:1.7, maxWidth:280 }}>
        The build didn't produce a preview HTML.<br/>
        Switch to <span style={{color:'#c4b5fd'}}>Code</span> tab to inspect output,<br/>
        or try rebuilding with a clearer prompt.
      </div>
    </div>
    <div style={{ display:'flex', gap:10, zIndex:1 }}>
      <button onClick={onRetry}
        style={{
          padding:'9px 20px', borderRadius:10, cursor:'pointer',
          background:'rgba(196,181,253,0.1)', border:'1px solid rgba(196,181,253,0.3)',
          color:'#c4b5fd', fontSize:11, fontFamily:'monospace', fontWeight:700,
          transition:'all 0.2s ease',
        }}
        onMouseEnter={e => { e.currentTarget.style.background='rgba(196,181,253,0.2)'; e.currentTarget.style.boxShadow='0 0 20px rgba(196,181,253,0.2)'; }}
        onMouseLeave={e => { e.currentTarget.style.background='rgba(196,181,253,0.1)'; e.currentTarget.style.boxShadow='none'; }}
      >↺ Refresh</button>
      {hasRawHtml && (
        <button onClick={onOpenNew}
          style={{
            padding:'9px 20px', borderRadius:10, cursor:'pointer',
            background:'rgba(147,197,253,0.1)', border:'1px solid rgba(147,197,253,0.3)',
            color:'#93c5fd', fontSize:11, fontFamily:'monospace', fontWeight:700,
            transition:'all 0.2s ease',
          }}
          onMouseEnter={e => { e.currentTarget.style.boxShadow='0 0 20px rgba(147,197,253,0.2)'; }}
          onMouseLeave={e => { e.currentTarget.style.boxShadow='none'; }}
        >↗ Open in Tab</button>
      )}
    </div>
    <style>{`@keyframes animeFloat { 0%,100%{transform:translateY(0)} 50%{transform:translateY(-10px)} }`}</style>
  </div>
);

// ─── Main OutputZone ──────────────────────────────────────────
const OutputZone = ({
  files = [],
  previewHtml = "",
  activeColor = "#6366f1",
  onEdit,
  onHome,
  agentsUsed = []
}) => {
  const [fileIdx, setFileIdx] = useState(0);
  const [viewMode, setViewMode] = useState('split');
  const [ikey, setIkey] = useState(0);

  const currentFile = files[fileIdx] || { name: "index.html", content: "<!-- Generating... -->" };
  const getFileName = (file) => file?.name || file?.filename || 'index.html';
  const hasPreview = previewHtml && previewHtml.trim().length > 50 && previewHtml.trim().toLowerCase().endsWith('</html>');

  const getLanguage = (name) => {
    if (!name || typeof name !== 'string') return 'html';
    if (name.endsWith('.js') || name.endsWith('.jsx')) return 'javascript';
    if (name.endsWith('.ts') || name.endsWith('.tsx')) return 'typescript';
    if (name.endsWith('.css')) return 'css';
    if (name.endsWith('.py')) return 'python';
    if (name.endsWith('.json')) return 'json';
    return 'html';
  };

  const handleOpenNew = () => {
    const w = window.open();
    w.document.write(previewHtml);
  };

  const viewModes = [
    { mode: 'split',   label: '⊞ Split'   },
    { mode: 'preview', label: '◉ Preview' },
    { mode: 'code',    label: '≺/≻ Code'  },
  ];

  return (
    <div style={{ display:'flex', flexDirection:'column', height:'100%', background:'#080c14' }}>

      {/* ── Tab Bar ────────────────────────────────────────── */}
      <div style={{
        height:'48px', borderBottom:'1px solid rgba(255,255,255,0.06)',
        display:'flex', alignItems:'center', padding:'0 16px', gap:'12px',
        background:'rgba(8,12,20,0.97)', backdropFilter:'blur(20px)',
      }}>

        {/* View mode toggles */}
        <div style={{
          display:'flex', background:'rgba(255,255,255,0.03)',
          borderRadius:10, padding:3, border:'1px solid rgba(255,255,255,0.06)', gap:2,
        }}>
          {viewModes.map(({ mode, label }) => {
            const active = viewMode === mode;
            return (
              <button key={mode} onClick={() => setViewMode(mode)} style={{
                fontSize:'9px', padding:'5px 12px', border:'none', borderRadius:7,
                background: active ? `${activeColor}28` : 'transparent',
                color: active ? '#f0f4ff' : '#4b5563',
                cursor:'pointer', fontWeight:700, letterSpacing:'0.5px',
                transition:'all 0.25s ease',
                boxShadow: active ? `0 0 12px ${activeColor}20` : 'none',
                outline: active ? `1px solid ${activeColor}25` : 'none',
              }}>{label}</button>
            );
          })}
        </div>

        <div style={{ height:'16px', width:'1px', background:'rgba(255,255,255,0.06)' }} />

        {/* File tabs */}
        <div style={{ flex:1, display:'flex', overflowX:'auto', gap:2, scrollbarWidth:'none' }}>
          {files.map((f, i) => {
            const active = fileIdx === i;
            return (
              <button key={i} onClick={() => setFileIdx(i)} style={{
                fontSize:'10px', padding:'6px 14px',
                background: active ? 'rgba(255,255,255,0.06)' : 'transparent',
                border:'none', borderBottom:`2px solid ${active ? activeColor : 'transparent'}`,
                borderRadius: active ? '6px 6px 0 0' : '6px',
                color: active ? '#e2e8f0' : '#4b5563',
                cursor:'pointer', whiteSpace:'nowrap',
                fontFamily:'JetBrains Mono, monospace',
                transition:'all 0.2s ease',
              }}>{getFileName(f)}</button>
            );
          })}
        </div>

        {/* Action buttons */}
        <div style={{ display:'flex', gap:8, alignItems:'center' }}>
          <button onClick={() => setIkey(k => k + 1)} title="Reload preview" style={{
            width:32, height:32, borderRadius:10,
            background:'rgba(255,255,255,0.04)', border:'1px solid rgba(255,255,255,0.08)',
            color:'#94a3b8', cursor:'pointer', fontSize:16, transition:'all 0.2s ease',
            display:'flex', alignItems:'center', justifyContent:'center',
          }}
            onMouseEnter={e => { e.currentTarget.style.background='rgba(196,181,253,0.12)'; e.currentTarget.style.borderColor='rgba(196,181,253,0.35)'; e.currentTarget.style.color='#c4b5fd'; }}
            onMouseLeave={e => { e.currentTarget.style.background='rgba(255,255,255,0.04)'; e.currentTarget.style.borderColor='rgba(255,255,255,0.08)'; e.currentTarget.style.color='#94a3b8'; }}
          >↺</button>

          <button onClick={handleOpenNew} style={{
            fontSize:'10px', padding:'0 16px', height:32, borderRadius:10,
            background:`linear-gradient(135deg, ${activeColor}, ${activeColor}99)`,
            border:'none', color:'#fff', fontWeight:800, cursor:'pointer',
            fontFamily:'monospace', letterSpacing:'0.5px',
            boxShadow:`0 4px 16px ${activeColor}40`, transition:'all 0.2s ease',
          }}
            onMouseEnter={e => { e.currentTarget.style.transform='translateY(-1px)'; e.currentTarget.style.boxShadow=`0 8px 24px ${activeColor}55`; }}
            onMouseLeave={e => { e.currentTarget.style.transform='translateY(0)'; e.currentTarget.style.boxShadow=`0 4px 16px ${activeColor}40`; }}
          >DEPLOY ✦</button>
        </div>
      </div>

      {/* ── Main Content ────────────────────────────────────── */}
      <div style={{
        flex:1, display:'grid',
        gridTemplateColumns: viewMode === 'split' ? '1.1fr 0.9fr' : '1fr',
        overflow:'hidden',
      }}>

        {/* EDITOR */}
        {(viewMode === 'split' || viewMode === 'code') && (
          <div style={{ height:'100%', borderRight: viewMode === 'split' ? '1px solid rgba(255,255,255,0.06)' : 'none' }}>
            <Editor
              height="100%"
              language={getLanguage(getFileName(currentFile))}
              value={currentFile.content}
              theme="vs-dark"
              options={{
                minimap:{ enabled:false }, fontSize:12,
                fontFamily:'JetBrains Mono, Menlo, monospace',
                padding:{ top:16 }, scrollBeyondLastLine:false,
                lineNumbers:'on', glyphMargin:false,
                folding:true, automaticLayout:true,
              }}
            />
          </div>
        )}

        {/* PREVIEW */}
        {(viewMode === 'split' || viewMode === 'preview') && (
          <div style={{ height:'100%', position:'relative', overflow:'hidden' }}>
            {hasPreview ? (
              <>
                <iframe
                  key={ikey}
                  srcDoc={previewHtml}
                  title="S.E.A.D.S. Live Preview"
                  style={{ width:'100%', height:'100%', border:'none', background:'#fff' }}
                  sandbox="allow-scripts allow-same-origin allow-forms allow-popups"
                />
                {/* Live badge */}
                <div style={{
                  position:'absolute', bottom:16, right:16,
                  background:'rgba(8,12,20,0.85)', padding:'6px 14px',
                  borderRadius:20, fontSize:'9px', fontWeight:700, color:'#fff',
                  pointerEvents:'none', backdropFilter:'blur(12px)',
                  border:`1px solid ${activeColor}30`,
                  display:'flex', gap:8, alignItems:'center',
                  boxShadow:'0 4px 20px rgba(0,0,0,0.3)',
                }}>
                  <span style={{ color:activeColor, animation:'pulseDot 1.5s ease infinite' }}>●</span>
                  LIVE PREVIEW (SANDBOXED)
                </div>
              </>
            ) : (
              <EmptyPreview
                onRetry={() => setIkey(k => k + 1)}
                onOpenNew={handleOpenNew}
                hasRawHtml={!!previewHtml}
              />
            )}
          </div>
        )}
      </div>
    </div>
  );
};

export default OutputZone;
