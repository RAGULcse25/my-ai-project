// ─────────────────────────────────────────────────────────────
// S.E.A.D.S. v14 — IIT-Level Design System
// Unified token system used across all components
// ─────────────────────────────────────────────────────────────

export const COLORS = {
  bg0:      "#070b14",   // deepest background
  bg1:      "#0d1117",   // card background
  bg2:      "#131920",   // input / secondary bg
  border:   "#1e2530",   // subtle border
  border2:  "#374151",   // secondary border
  text:     "#f1f5f9",   // primary text
  text2:    "#94a3b8",   // secondary text
  text3:    "#64748b",   // muted text
  text4:    "#374151",   // very muted
  accent:   "#6366f1",   // primary brand blue-purple
  accent2:  "#8b5cf6",   // purple variant
  accent3:  "#a855f7",   // magenta-purple variant
  green:    "#22c55e",   // success
  red:      "#ef4444",   // error
  yellow:   "#f59e0b",   // warning
};

export const FONTS = {
  display: "'Syne', sans-serif",
  mono:    "'JetBrains Mono', monospace",
  body:    "'Inter', system-ui, sans-serif",
};

export const RADIUS = {
  sm: 6,
  md: 10,
  lg: 14,
  xl: 18,
  pill: 999,
};

// ── CategoryPage styles ──────────────────────────────────────
export const PS = {
  root: {
    display: "flex", flexDirection: "column",
    height: "100vh", background: COLORS.bg0,
    color: COLORS.text, overflow: "hidden",
  },
  header: {
    display: "flex", alignItems: "center", gap: 14,
    padding: "14px 24px", borderBottom: `1px solid ${COLORS.border}`,
    flexShrink: 0, background: "rgba(7,11,20,0.95)",
    backdropFilter: "blur(16px)",
  },
  backBtn: {
    background: "none", border: `1px solid ${COLORS.border}`,
    borderRadius: RADIUS.md, color: COLORS.text3,
    cursor: "pointer", padding: "7px 14px",
    fontSize: 11, fontFamily: FONTS.mono,
    transition: "all 0.2s ease",
  },
  catIcon: {
    width: 46, height: 46, borderRadius: RADIUS.lg,
    display: "flex", alignItems: "center",
    justifyContent: "center", fontSize: 22, flexShrink: 0,
  },
  content: {
    flex: 1, overflowY: "auto",
    padding: "28px 24px",
    display: "flex", flexDirection: "column",
    gap: 22, alignItems: "center",
    maxWidth: 980, margin: "0 auto", width: "100%",
    scrollbarWidth: "thin", scrollbarColor: `${COLORS.border} transparent`,
  },
  examplesGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(175px, 1fr))",
    gap: 12, width: "100%",
  },
  exampleCard: {
    background: COLORS.bg1, border: `1px solid ${COLORS.border}`,
    borderRadius: RADIUS.xl, padding: "18px 16px",
    cursor: "pointer", textAlign: "left",
    transition: "all 0.25s cubic-bezier(0.34,1.56,0.64,1)",
    fontFamily: FONTS.mono,
  },
  divider: {
    display: "flex", alignItems: "center", gap: 12,
    width: "100%", maxWidth: 600,
  },
  dividerLine: { flex: 1, height: 1, background: COLORS.border },
  dividerText: {
    fontSize: 9, color: COLORS.text4,
    letterSpacing: "2px", textTransform: "uppercase",
    whiteSpace: "nowrap", fontFamily: FONTS.mono,
  },
  inputWrap: { width: "100%", maxWidth: 640 },
  searchBox: {
    display: "flex", alignItems: "center",
    background: COLORS.bg1, border: `2px solid ${COLORS.border}`,
    borderRadius: 14, padding: "10px 10px 10px 16px",
    transition: "all 0.25s ease",
  },
  searchInput: {
    flex: 1, background: "none", border: "none",
    outline: "none", fontSize: 14, color: COLORS.text,
    fontFamily: FONTS.display, padding: "5px 6px",
  },
  sendBtn: {
    width: 42, height: 42, borderRadius: 10,
    border: "none", cursor: "pointer",
    fontSize: 18, fontWeight: 700,
    transition: "all 0.2s", flexShrink: 0,
  },
};

// ── HomePage styles (legacy compatibility) ───────────────────
export const H = {
  root: {
    display: "flex", width: "100vw", height: "100vh",
    background: COLORS.bg0, color: COLORS.text, overflow: "hidden",
  },
  sidebar: {
    width: 220, flexShrink: 0,
    background: "rgba(8,12,16,0.92)",
    borderRight: `1px solid ${COLORS.border}`,
    display: "flex", flexDirection: "column", overflow: "hidden",
    backdropFilter: "blur(20px)",
  },
  brand: {
    display: "flex", alignItems: "center", gap: 10,
    padding: "18px 16px", borderBottom: `1px solid ${COLORS.border}`,
  },
  brandIcon: {
    width: 36, height: 36, borderRadius: 10,
    background: "linear-gradient(135deg,#6366f1,#8b5cf6,#a855f7)",
    display: "flex", alignItems: "center",
    justifyContent: "center", fontSize: 18,
    boxShadow: "0 0 20px rgba(99,102,241,0.4)",
  },
  brandName: {
    fontSize: 15, fontWeight: 900, color: "#fff",
    fontFamily: FONTS.display, letterSpacing: "0.5px",
  },
  brandSub: {
    fontSize: 8.5, color: COLORS.text4,
    fontFamily: FONTS.mono, letterSpacing: "0.5px",
  },
  sectionLabel: {
    padding: "8px 14px", fontSize: 8, color: COLORS.text4,
    letterSpacing: "2px", textTransform: "uppercase",
    fontFamily: FONTS.mono,
  },
  main: {
    flex: 1, overflowY: "auto",
    padding: "32px 24px",
    display: "flex", justifyContent: "center",
    scrollbarWidth: "thin", scrollbarColor: `${COLORS.border} transparent`,
  },
  center: {
    width: "100%", maxWidth: 920,
    display: "flex", flexDirection: "column",
    alignItems: "center", gap: 24,
  },
  workspaceBadge: {
    display: "flex", alignItems: "center", gap: 8,
    background: COLORS.bg2, border: `1px solid ${COLORS.border}`,
    borderRadius: 30, padding: "6px 16px 6px 8px", cursor: "pointer",
  },
  avatar: {
    width: 26, height: 26, borderRadius: "50%",
    background: "linear-gradient(135deg,#6366f1,#a855f7)",
    display: "flex", alignItems: "center",
    justifyContent: "center", fontSize: 11,
    fontWeight: 700, color: "#fff",
  },
  headline: {
    fontSize: "clamp(24px,4vw,44px)", fontWeight: 900,
    fontFamily: FONTS.display, lineHeight: 1.1,
    background: "linear-gradient(135deg,#f9fafb 0%,#c7d2fe 50%,#a5b4fc 100%)",
    WebkitBackgroundClip: "text", WebkitTextFillColor: "transparent",
    textAlign: "center",
  },
  catGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(210px, 1fr))",
    gap: 14, width: "100%",
  },
  catCard: {
    background: COLORS.bg1, border: `1px solid ${COLORS.border}`,
    borderRadius: 18, padding: 20,
    cursor: "pointer", textAlign: "left",
    transition: "all 0.3s cubic-bezier(0.34,1.56,0.64,1)",
  },
  catCardIcon: {
    width: 50, height: 50, borderRadius: 14,
    display: "flex", alignItems: "center",
    justifyContent: "center", fontSize: 24, marginBottom: 12,
  },
  catCardLabel: {
    fontSize: 15, fontWeight: 800, color: COLORS.text,
    fontFamily: FONTS.display, marginBottom: 5,
  },
  catCardDesc: {
    fontSize: 10, color: COLORS.text3,
    fontFamily: FONTS.mono, lineHeight: 1.5,
  },
};

// ── Toast ────────────────────────────────────────────────────
export const TOAST = {
  position: "fixed", bottom: 24, right: 24,
  background: "rgba(13,17,23,0.95)",
  border: `1px solid ${COLORS.border}`,
  borderRadius: 12, padding: "12px 20px",
  fontSize: 12, color: COLORS.text,
  zIndex: 9999, fontFamily: FONTS.mono,
  backdropFilter: "blur(16px)",
  boxShadow: "0 8px 32px rgba(0,0,0,0.4)",
  animation: "slideUp 0.3s cubic-bezier(0.34,1.56,0.64,1) both",
};
