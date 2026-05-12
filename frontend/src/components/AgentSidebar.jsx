import React from 'react';

const AgentSidebar = ({ agents = [], activeAgent = "" }) => {
  return (
    <div style={{
      display:'flex', flexDirection:'column', height:'100%',
      background:'rgba(7,11,20,0.98)', width:'100%',
    }}>
      {/* Header */}
      <div style={{
        padding:'16px 14px 12px',
        borderBottom:'1px solid rgba(255,255,255,0.06)',
        background:'rgba(255,255,255,0.01)',
      }}>
        <div style={{
          fontSize:'9px', fontWeight:800, letterSpacing:'2px',
          textTransform:'uppercase', marginBottom:4,
          background:'linear-gradient(135deg, #c4b5fd, #93c5fd)',
          WebkitBackgroundClip:'text', WebkitTextFillColor:'transparent',
        }}>
          Autonomous Swarm
        </div>
        <div style={{ fontSize:'9px', color:'#374151', fontFamily:'monospace' }}>
          {agents.length} ACTIVE AGENTS
        </div>
      </div>

      {/* Agent list */}
      <div style={{
        flex:1, overflowY:'auto', padding:'10px 10px',
        display:'flex', flexDirection:'column', gap:5,
        scrollbarWidth:'none',
      }}>
        {agents.map((agent, i) => {
          const isActive = agent === activeAgent;
          return (
            <div key={i} style={{
              display:'flex', alignItems:'center', gap:8,
              padding:'7px 10px', borderRadius:10,
              background: isActive ? 'rgba(196,181,253,0.1)' : 'rgba(255,255,255,0.02)',
              border: isActive ? '1px solid rgba(196,181,253,0.3)' : '1px solid rgba(255,255,255,0.04)',
              transition:'all 0.25s ease',
              boxShadow: isActive ? '0 0 16px rgba(196,181,253,0.12)' : 'none',
              animation:`fadeIn 0.3s ease ${i * 40}ms both`,
            }}>
              {/* Status dot */}
              <div style={{
                width:6, height:6, borderRadius:'50%', flexShrink:0,
                background: isActive ? '#86efac' : '#1e2530',
                boxShadow: isActive ? '0 0 8px rgba(134,239,172,0.6)' : 'none',
                transition:'all 0.25s ease',
                animation: isActive ? 'pulseDot 2s ease infinite' : 'none',
              }} />
              {/* Name */}
              <div style={{
                fontSize:'10px', fontFamily:'JetBrains Mono, monospace',
                color: isActive ? '#e2e8f0' : '#4b5563',
                fontWeight: isActive ? 700 : 400,
                transition:'color 0.25s',
                overflow:'hidden', textOverflow:'ellipsis', whiteSpace:'nowrap',
              }}>
                {agent}
              </div>
              {/* Active badge */}
              {isActive && (
                <div style={{
                  marginLeft:'auto', fontSize:'7px', color:'#86efac',
                  fontWeight:800, fontFamily:'monospace', flexShrink:0,
                  animation:'pulseDot 1.5s ease infinite',
                }}>
                  ▶
                </div>
              )}
            </div>
          );
        })}

        {agents.length === 0 && (
          <div style={{
            textAlign:'center', marginTop:32, color:'#1e2530',
            fontSize:'10px', fontFamily:'monospace', lineHeight:1.8,
          }}>
            ◌<br/>Awaiting<br/>Command
          </div>
        )}
      </div>

      <style>{`
        @keyframes pulseDot { 0%,100%{opacity:1} 50%{opacity:0.4} }
        @keyframes fadeIn { from{opacity:0;transform:translateX(-8px)} to{opacity:1;transform:translateX(0)} }
      `}</style>
    </div>
  );
};

export default AgentSidebar;
