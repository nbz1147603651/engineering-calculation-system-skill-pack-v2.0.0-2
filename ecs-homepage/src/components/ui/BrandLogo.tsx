/* ============================================
   ECS Homepage — Brand Logo Component
   ============================================ */

export default function BrandLogo({ dark = false, fullName = false }: { dark?: boolean; fullName?: boolean }) {
  return (
    <span className="brand-lockup">
      <svg
        className="brand-mark"
        viewBox="0 0 48 48"
        role="img"
        aria-label="ECS logo"
      >
        <rect className="brand-mark-bg" x="3" y="3" width="42" height="42" rx="9" />
        <path className="brand-mark-line" d="M14 16h16M14 24h11M14 32h16" />
        <path className="brand-mark-vector" d="M31 15.5l5.5 5.5-5.5 5.5" />
        <circle className="brand-mark-node" cx="35.5" cy="33.5" r="2.6" />
      </svg>
      <span className={`brand-word ${dark ? 'brand-word-dark' : ''}`}>
        {fullName ? 'Engineering Calculation System' : 'ECS'}
      </span>
    </span>
  )
}
