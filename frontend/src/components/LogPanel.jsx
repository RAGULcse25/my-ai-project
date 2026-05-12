import React, { useEffect, useRef } from 'react';

const LogPanel = ({ logs = [], agents = [], status = "" }) => {
  const scrollRef = useRef(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [logs, status]);

  const getAgentColor = (name) => {
    if (name.includes("Search"))   return "#93c5fd";
    if (name.includes("Planning")) return "#c4b5fd";
    if (name.includes("Coding"))   return "#86efac";
    if (name.includes("Verify"))   return "#fcd34d";
    return "#64748b";
  };

  return (
    <div style={{
      display:'flex', flexDirection:'column', height:'100%',
      background:'#080c10', fontFamily:'JetBrains Mono, Menlo, monospace',
      fontSize:'11px', color:'#94a3b8', overflow:'hidden',
    }}>
      {/* Status bar */}
      <div style={{
        padding:'10px 14px', borderBottom:'1px solid rgba(255,255,255,0.06)',
        background:'rgba(255,255,255,0.02)',
        display:'flex', alignItems:'center', gap:10,
      }}>
        <div style={{
          width:6, height:6, borderRadius:'50%', background:'#86efac',
          boxShadow:'0 0 8px rgba(134,239,172,0.7)',
          animation:'pulseDot 2s infinite', flexShrink:0,
        }} />
        <span style={{
          color:'#e2e8f0', fontWeight:800, letterSpacing:'0.05em', fontSize:10,
          background:'linear-gradient(90deg, #c4b5fd, #93c5fd)',
          WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent',
        }}>
          {status || "SWARM IDLE"}
        </span>
      </div>

      {/* Log lines */}
      <div ref={scrollRef} style={{
        flex:1, overflowY:'auto', padding:'12px 14px',
        display:'flex', flexDirection:'column', gap:6,
        scrollbarWidth:'thin', scrollbarColor:'rgba(196,181,253,0.15) transparent',
      }}>
        {logs.map((log, i) => {
          const isAgent = log.includes("[");
          const agentName = isAgent ? log.match(/\[(.*?)\]/)?.[1] : null;
          const cleanText = isAgent ? log.replace(`[${agentName}]`, "").trim() : log;
          const isLast = i === logs.length - 1;
          const isErr = log.toLowerCase().includes("error");

          return (
            <div key={i} style={{
              display:'flex', gap:8, alignItems:'flex-start',
              animation: isLast ? 'fadeSlideIn 0.3s ease-out' : 'none',
            }}>
              <span style={{ color:'rgba(255,255,255,0.12)', minWidth:36, flexShrink:0, fontSize:9 }}>
                {String(i + 1).padStart(3, '0')}
              </span>
              {agentName && (
                <span style={{
                  color: getAgentColor(agentName), fontWeight:700,
                  background:`${getAgentColor(agentName)}12`,
                  padding:'1px 6px', borderRadius:4, fontSize:8,
                  textTransform:'uppercase', flexShrink:0,
                  border:`1px solid ${getAgentColor(agentName)}25`,
                }}>
                  {agentName}
                </span>
              )}
              <span style={{
                color: isErr ? "#fca5a5" : isLast ? "#c4b5fd" : "#64748b",
                lineHeight:1.6, fontSize:10,
              }}>
                {cleanText}
              </span>
            </div>
          );
        })}

        {/* Blinking cursor */}
        <div style={{ display:'flex', gap:8, alignItems:'center', marginTop:2 }}>
          <span style={{ color:'rgba(255,255,255,0.12)', fontSize:9 }}>
            {String(logs.length + 1).padStart(3, '0')}
          </span>
          <div style={{
            width:6, height:11, borderRadius:2,
            background:'linear-gradient(135deg, #c4b5fd, #93c5fd)',
            animation:'blink 1s infinite',
          }} />
        </div>
      </div>

      {/* Agent pills */}
      {agents.length > 0 && (
        <div style={{
          padding:'10px 12px', borderTop:'1px solid rgba(255,255,255,0.06)',
          background:'rgba(255,255,255,0.01)',
          display:'flex', flexWrap:'wrap', gap:5,
        }}>
          {agents.map((agent, i) => (
            <div key={i} style={{
              fontSize:'8px', padding:'3px 9px', borderRadius:20,
              background:'rgba(196,181,253,0.07)',
              color:'rgba(196,181,253,0.5)',
              border:'1px solid rgba(196,181,253,0.15)',
              fontFamily:'monospace',
            }}>
              {agent}
            </div>
          ))}
        </div>
      )}

      <style>{`
        @keyframes fadeSlideIn { from{opacity:0;transform:translateY(5px)} to{opacity:1;transform:translateY(0)} }
        @keyframes blink { 0%,100%{opacity:1} 50%{opacity:0} }
        @keyframes pulseDot { 0%,100%{opacity:1} 50%{opacity:0.3} }
      `}</style>
    </div>
  );
};

export default LogPanel;
