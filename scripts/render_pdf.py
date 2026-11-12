#!/usr/bin/env python3
"""Render a 3-page editorial PDF communication report from a session JSON payload."""

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TEMPLATE = ROOT / "templates" / "report-certificate.html"
CERT_DATA_RE = re.compile(
    r'(<script\s+id="cert-data"\s+type="application/json">)(.*?)(</script>)',
    re.DOTALL,
)


def inject_payload(template_html: str, payload: dict) -> str:
    """Replace the embedded cert-data JSON block inside the HTML template."""
    encoded = json.dumps(payload, indent=2, ensure_ascii=False).replace("</", "<\\/")
    replaced, count = CERT_DATA_RE.subn(rf"\1\n{encoded}\n\3", template_html, count=1)
    if count != 1:
        raise ValueError("Template missing <script id=\"cert-data\" type=\"application/json\"> block")
    return replaced


def render_pdf(html_text: str, output_pdf: Path, html_out: Path | None = None, chrome_bin: str = "google-chrome") -> None:
    """Write rendered HTML and print an A4 PDF via headless Chrome."""
    output_pdf.parent.mkdir(parents=True, exist_ok=True)
    tmp_path = None
    try:
        if html_out is not None:
            html_out.parent.mkdir(parents=True, exist_ok=True)
            html_path = html_out
        else:
            fd, raw = tempfile.mkstemp(suffix=".html", prefix="report_")
            os.close(fd)
            tmp_path = Path(raw)
            html_path = tmp_path

        html_path.write_text(html_text, encoding="utf-8")
        cmd = [
            chrome_bin,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--no-pdf-header-footer",
            f"--print-to-pdf={output_pdf.resolve()}",
            html_path.resolve().as_uri(),
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    finally:
        if tmp_path is not None and tmp_path.exists():
            tmp_path.unlink()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("payload_json", type=Path, help="JSON matching cert-data schema")
    parser.add_argument("output_pdf", type=Path, help="Destination PDF path")
    parser.add_argument("--template", type=Path, default=DEFAULT_TEMPLATE)
    parser.add_argument("--save-html", type=Path, default=None, help="Optional path to keep populated HTML")
    parser.add_argument("--chrome", type=str, default="google-chrome")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload_json.read_text(encoding="utf-8"))
        template_html = args.template.read_text(encoding="utf-8")
        populated = inject_payload(template_html, payload)
        render_pdf(populated, args.output_pdf, html_out=args.save_html, chrome_bin=args.chrome)
        print(json.dumps({"rendered_pdf": str(args.output_pdf)}, indent=2))
        return 0
    except (OSError, ValueError, json.JSONDecodeError, subprocess.CalledProcessError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
