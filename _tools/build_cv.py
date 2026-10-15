#!/usr/bin/env python3
"""Generate assets/resume.pdf from the site data, so the downloadable CV and the website never drift apart.

Sources: _config.yml (name, contact, links) and _data/*.yml (education, research, skills, projects,
experience, awards). Anything commented out in the data (for example the HSC/SSC GPA lines in
education.yml) is automatically absent from the PDF as well.

Requires:  pip install reportlab pyyaml
"""
from __future__ import annotations

import datetime as dt
from pathlib import Path
from xml.sax.saxutils import escape

import yaml
from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import HRFlowable, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "assets" / "resume.pdf"
INK, MUTED, ACCENT, RULE = colors.HexColor("#13201b"), colors.HexColor("#56615b"), colors.HexColor("#1d493c"), colors.HexColor("#c9cfc9")
MAX_PROJECTS = 7

SUMMARY = (
    "Final-year Computer Science and Engineering undergraduate at Green University of Bangladesh with applied research and project experience in machine learning, Bangla NLP, and computer vision. Skilled in Python-based data preparation, Transformer experimentation, image classification, and model evaluation. Experienced in developing AI-enabled applications and communicating technical work through research writing, documentation, mentoring, and presentations."
)


def load(name: str):
    return yaml.safe_load((ROOT / "_data" / f"{name}.yml").read_text(encoding="utf-8")) or []


def e(text) -> str:
    return escape(str(text if text is not None else ""))


def styles() -> dict[str, ParagraphStyle]:
    base = dict(fontName="Helvetica", fontSize=8.8, leading=11.5, textColor=INK)
    return {
        "name": ParagraphStyle("name", fontName="Helvetica-Bold", fontSize=25, leading=29, textColor=INK),
        "role": ParagraphStyle("role", fontName="Helvetica-Bold", fontSize=10.6, leading=14, textColor=ACCENT, spaceAfter=3),
        "contact": ParagraphStyle("contact", fontName="Helvetica", fontSize=8.8, leading=12, textColor=MUTED),
        "h": ParagraphStyle("h", fontName="Helvetica-Bold", fontSize=9.4, leading=11.5, textColor=ACCENT, spaceBefore=8, spaceAfter=1, keepWithNext=1),
        "body": ParagraphStyle("body", **base),
        "muted": ParagraphStyle("muted", **{**base, "textColor": MUTED}),
        "bold": ParagraphStyle("bold", **{**base, "fontName": "Helvetica-Bold", "fontSize": 9.3}),
        "right": ParagraphStyle("right", **{**base, "textColor": MUTED, "alignment": TA_RIGHT}),
        "ital": ParagraphStyle("ital", **{**base, "fontName": "Helvetica-Oblique", "textColor": MUTED}),
        "bullet": ParagraphStyle("bullet", **{**base, "leftIndent": 11, "bulletIndent": 1, "spaceBefore": 0.6}),
    }


def build() -> Path:
    cfg = yaml.safe_load((ROOT / "_config.yml").read_text(encoding="utf-8"))
    st = styles()
    width = A4[0] - 36 * mm - 12  # minus the frame's 6pt padding on each side
    story: list = []

    def section(title: str) -> None:
        story.append(Paragraph(e(title.upper()), st["h"]))
        rule = HRFlowable(width="100%", thickness=0.6, color=RULE, spaceBefore=1, spaceAfter=4)
        rule.keepWithNext = True
        story.append(rule)

    def row(left: str, right: str = "", left_style="bold", sub: str = "", sub_right: str = "") -> Table:
        cells = [[Paragraph(left, st[left_style]), Paragraph(right, st["right"])]]
        if sub or sub_right:
            cells.append([Paragraph(sub, st["ital"]), Paragraph(sub_right, st["right"])])
        t = Table(cells, colWidths=[width * 0.72, width * 0.28])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 0), ("TOPPADDING", (0, 0), (-1, -1), 0), ("BOTTOMPADDING", (0, 0), (-1, -1), 0)]))
        return t

    def bullets(items) -> list:
        return [Paragraph(e(i), st["bullet"], bulletText="•") for i in (items or [])]

    # ---- header
    story.append(Paragraph(e(cfg["name"]), st["name"]))
    story.append(Paragraph(e(cfg["role"]), st["role"]))
    story.append(Paragraph(f'{e(cfg["email"])}  |  {e(cfg["location"])}', st["contact"]))
    links = [("GitHub", cfg.get("github_url")), ("LinkedIn", cfg.get("linkedin_url")), ("IEEE Collabratec", cfg.get("ieee_url"))]
    story.append(Paragraph("  |  ".join(f'<a href="{e(u)}" color="#1d493c">{n}</a>' for n, u in links if u), st["contact"]))

    section("Profile")
    story.append(Paragraph(e(SUMMARY), st["body"]))

    section("Education")
    for ed in load("education"):
        when = ed.get("year") or ed.get("status") or ""
        story.append(KeepTogether([row(e(ed["institution"]), e(when), sub=f'{e(ed["degree"])} · {e(ed.get("location", ""))}')] + bullets(ed.get("highlights")) + [Spacer(1, 3)]))

    section("Research")
    for item in load("research"):
        status = item.get("status", "")
        repo = f'<a href="{e(item["github"])}" color="#1d493c">GitHub</a>' if item.get("github") else ""
        block = [row(e(item["title"]), repo, left_style="bold"), Paragraph(f'{e(item.get("type", ""))} · {e(status)}', st["muted"]), Paragraph(e(item.get("description", "")), st["body"])]
        block += bullets((item.get("key_points") or []) + (item.get("key_findings") or []))
        story.append(KeepTogether(block + [Spacer(1, 3)]))

    section("Technical expertise")
    for g in load("skills"):  # one small table per row so a page break can fall between categories
        t = Table([[Paragraph(f'<b>{e(g["category"])}</b>', st["body"]), Paragraph(e(", ".join(g["skills"])), st["body"])]], colWidths=[width * 0.27, width * 0.73])
        t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0), ("RIGHTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 1.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.5)]))
        story.append(t)

    section("Selected projects")
    for proj in load("projects")[:MAX_PROJECTS]:
        parts = []
        if proj.get("github"):
            parts.append(f'<a href="{e(proj["github"])}" color="#1d493c">GitHub</a>')
        if proj.get("demo"):
            parts.append(f'<a href="{e(proj["demo"])}" color="#1d493c">Live demo</a>')
        link = " | ".join(parts)
        tags = e(", ".join(proj.get("tags", [])[:5]))
        points = proj.get("highlights") or [proj.get("description", "")]
        story.append(KeepTogether([row(e(proj["title"]), link, sub=tags)] + bullets(points[:2]) + [Spacer(1, 3)]))

    section("Experience & leadership")
    for r in load("experience"):
        story.append(KeepTogether([row(f'{e(r["title"])} · <font name="Helvetica" color="#56615b">{e(r["organization"])}</font>', f'{e(r["start_date"])} – {e(r["end_date"])}'), Paragraph(e(r.get("description", "")), st["body"]), Spacer(1, 3)]))

    section("Awards, membership & service")
    for a in load("awards"):
        year = f' ({e(a["year"])})' if a.get("year") else ""
        story.append(Paragraph(f'<b>{e(a["title"])}</b> · {e(a["organization"])}{year}', st["bullet"], bulletText="•"))

    def decorate(canvas, doc):
        canvas.saveState()
        canvas.setFont("Helvetica", 7.6)
        canvas.setFillColor(MUTED)
        canvas.drawString(18 * mm, 10 * mm, f'{cfg["name"]} · Curriculum vitae · Updated {dt.date.today():%B %Y}')
        canvas.drawRightString(A4[0] - 18 * mm, 10 * mm, f"Page {doc.page}")
        canvas.restoreState()

    OUT.parent.mkdir(parents=True, exist_ok=True)
    doc = SimpleDocTemplate(str(OUT), pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm, topMargin=14 * mm, bottomMargin=17 * mm,
                            title=f'{cfg["name"]} - CV', author=cfg["name"], subject="Curriculum vitae")
    doc.build(story, onFirstPage=decorate, onLaterPages=decorate)
    return OUT


if __name__ == "__main__":
    print("Wrote", build())
