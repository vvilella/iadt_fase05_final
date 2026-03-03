from datetime import datetime

def render_markdown(detections, threats) -> str:
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    md = []
    md.append(f"# STRIDE Report\n\nGenerated: {now}\n")

    md.append("## Component Inventory\n")
    md.append("| # | Type | Confidence | BBox (x1,y1,x2,y2) |\n|---:|---|---:|---|")
    for i, d in enumerate(detections, start=1):
        md.append(f"| {i} | {getattr(d,'label', 'unknown')} | {getattr(d,'confidence', 0.0):.2f} | {getattr(d,'bbox', None)} |")

    md.append("\n## Threats (STRIDE)\n")
    md.append("| Component | STRIDE | Vulnerabilities | Mitigations |\n|---|---|---|---|")
    for t in threats:
        vulns = "<br>".join(getattr(t, "vulnerabilities", []))
        mits = "<br>".join(getattr(t, "mitigations", []))
        md.append(f"| {getattr(t,'component_label','?')} | {getattr(t,'stride_category','?')} | {vulns} | {mits} |")

    md.append("")
    return "\n".join(md)

def export_markdown(md: str, out_path: str) -> None:
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(md)
