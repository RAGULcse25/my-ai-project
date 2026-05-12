import React from 'react';

/**
 * PipelineView - S.E.A.D.S. v14
 * Animated visualization of the 4-stage pipeline (Search, Plan, Code, Verify).
 */
const PipelineView = ({ currentStage = 0, progress = 0 }) => {
  const stages = [
    { name: 'Research', icon: '🔍', desc: 'Perplexity Deep Search' },
    { name: 'Planning', icon: '🧠', desc: 'DeepSeek-R1 Logic' },
    { name: 'Coding', icon: '💻', desc: 'Multi-Agent Assembly' },
    { name: 'Verification', icon: '✨', desc: 'Claude 3 Opus Audit' }
  ];

  const getColor = (i) => {
    if (i < currentStage) return '#4ade80'; // Completed
    if (i === currentStage) return '#3b82f6'; // Active
    return '#1e293b'; // Pending
  };

  return (
    <div style={{
      display: 'flex',
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      gap: '40px',
      padding: '20px',
      width: '100%',
      maxWidth: '800px'
    }}>
      {/* Overall Progress Bar */}
      <div style={{ width: '100%', height: '4px', background: '#1e293b', borderRadius: '2px', position: 'relative' }}>
        <div style={{
          position: 'absolute',
          left: 0,
          top: 0,
          height: '100%',
          width: `${progress}%`,
          background: 'linear-gradient(90deg, #3b82f6, #60a5fa)',
          boxShadow: '0 0 10px rgba(59, 130, 246, 0.5)',
          borderRadius: '2px',
          transition: 'width 0.5s cubic-bezier(0.4, 0, 0.2, 1)'
        }} />
      </div>

      {/* Stages Grid */}
      <div style={{
        display: 'grid',
        gridTemplateColumns: 'repeat(4, 1fr)',
        width: '100%',
        gap: '20px'
      }}>
        {stages.map((stage, i) => {
          const isActive = i === currentStage;
          const isDone = i < currentStage;
          const color = getColor(i);

          return (
            <div key={i} style={{
              display: 'flex',
              flexDirection: 'column',
              alignItems: 'center',
              gap: '12px',
              transition: 'all 0.4s ease',
              transform: isActive ? 'scale(1.05)' : 'scale(1)',
              opacity: (isActive || isDone) ? 1 : 0.4
            }}>
              {/* Icon Circle */}
              <div style={{
                width: '60px',
                height: '60px',
                borderRadius: '50%',
                background: isActive ? `${color}22` : isDone ? `${color}11` : '#0f172a',
                border: `2px solid ${color}`,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontSize: '24px',
                boxShadow: isActive ? `0 0 20px ${color}44` : 'none',
                position: 'relative'
              }}>
                {stage.icon}
                {isActive && (
                  <div style={{
                    position: 'absolute',
                    width: '100%',
                    height: '100%',
                    borderRadius: '50%',
                    border: '2px solid transparent',
                    borderTopColor: color,
                    animation: 'spin 1.5s linear infinite'
                  }} />
                )}
              </div>

              {/* Text */}
              <div style={{ textAlign: 'center' }}>
                <div style={{ 
                  color: color, 
                  fontWeight: 800, 
                  fontSize: '11px', 
                  textTransform: 'uppercase', 
                  letterSpacing: '1px',
                  fontFamily: "'Syne', sans-serif"
                }}>
                  {stage.name}
                </div>
                <div style={{ fontSize: '9px', color: '#64748b', marginTop: '2px', fontFamily: 'monospace' }}>
                  {stage.desc}
                </div>
              </div>
            </div>
          );
        })}
      </div>

      <style>{`
        @keyframes spin { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }
      `}</style>
    </div>
  );
};

export default PipelineView;
