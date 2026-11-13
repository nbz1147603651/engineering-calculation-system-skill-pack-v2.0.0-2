export default function Icon({
  name,
  size = 20,
}: {
  name:
    | "arrow"
    | "download"
    | "home"
    | "plug"
    | "flow"
    | "log"
    | "check"
    | "menu"
    | "chevron";
  size?: number;
}) {
  const paths = {
    arrow: "M4 12h16m-6-6 6 6-6 6",
    download: "M12 3v12m-5-5 5 5 5-5M5 16v4h14v-4",
    home: "m3 11 9-8 9 8M6 9v12h12V9M10 21v-7h4v7",
    plug: "M8 3v5m8-5v5M6 8h12v3a6 6 0 0 1-6 6v5m-6-14v3a6 6 0 0 0 6 6",
    flow: "M12 8v5M5 17v-4h14v4M9 3h6v5H9zM2 17h6v5H2zm14 0h6v5h-6z",
    log: "M5 3h14v18H5zM9 8h6m-6 4h6m-6 4h4",
    check: "m5 12 4 4 10-10",
    menu: "M4 6h16M4 12h16M4 18h16",
    chevron: "m9 5 7 7-7 7",
  };
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.8"
      strokeLinecap="round"
      strokeLinejoin="round"
      aria-hidden="true"
    >
      <path d={paths[name]} />
    </svg>
  );
}
