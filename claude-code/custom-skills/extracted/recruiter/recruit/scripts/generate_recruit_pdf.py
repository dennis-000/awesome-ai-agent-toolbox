#!/usr/bin/env python3
"""
AI Recruiter Team — Professional PDF Report Generator

Generates a polished, multi-page recruiting analysis PDF using ReportLab.
Output: RECRUIT-REPORT.pdf (or --demo for RECRUIT-REPORT-sample.pdf).

Usage:
  python3 generate_recruit_pdf.py                        # Demo mode
  python3 generate_recruit_pdf.py --demo                 # Demo mode (explicit)
  python3 generate_recruit_pdf.py data.json              # From JSON
  python3 generate_recruit_pdf.py data.json output.pdf   # JSON with custom output

Requires: reportlab>=4.0.0
"""

import sys
import json
import os
from datetime import datetime

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.lib.units import inch
    from reportlab.lib.colors import HexColor, white, black
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table,
                                     TableStyle, PageBreak, KeepTogether)
    from reportlab.graphics.shapes import Drawing, Rect, Circle, String, Line
except ImportError:
    print("Error: reportlab is required. Install with: pip install reportlab")
    sys.exit(1)


# ---------------------------------------------------------------------------
# Color palette — Professional Recruiting Theme (Royal Blue + Gold + Green)
# ---------------------------------------------------------------------------
COLORS = {
    "navy": HexColor("#1e3a8a"),              # Royal blue (primary)
    "navy_dark": HexColor("#0f2461"),         # Darker navy
    "navy_light": HexColor("#3b82f6"),        # Lighter blue accent
    "gold": HexColor("#d4af37"),              # Accent gold
    "gold_light": HexColor("#f1e4a8"),        # Light gold
    "green": HexColor("#10b981"),             # Success green
    "green_light": HexColor("#34d399"),
    "orange": HexColor("#f59e0b"),            # Caution orange
    "yellow": HexColor("#fbbf24"),
    "red": HexColor("#ef4444"),               # Danger red
    "red_dark": HexColor("#b91c1c"),
    "gray": HexColor("#6b7280"),
    "light_bg": HexColor("#f1f5f9"),          # Soft background
    "cream": HexColor("#fafbfc"),
    "text": HexColor("#1f2937"),
    "text_light": HexColor("#6b7280"),
    "border": HexColor("#e2e8f0"),
    "header_bg": HexColor("#1e3a8a"),         # Navy table headers
    "row_alt": HexColor("#f1f5f9"),
    "white": white,
    "black": black,
}


def score_color(score):
    if score >= 70:
        return COLORS["green"]
    elif score >= 55:
        return COLORS["orange"]
    elif score >= 40:
        return COLORS["yellow"]
    else:
        return COLORS["red"]


def score_grade(score):
    if score >= 85: return "A+"
    if score >= 70: return "A"
    if score >= 55: return "B"
    if score >= 40: return "C"
    if score >= 25: return "D"
    return "F"


def score_signal(score):
    if score >= 85: return "READY TO HIRE"
    if score >= 70: return "STRONG"
    if score >= 55: return "AVERAGE"
    if score >= 40: return "BELOW AVERAGE"
    if score >= 25: return "POOR"
    return "CRITICAL"


def signal_color(score):
    if score >= 70: return COLORS["green"]
    if score >= 55: return COLORS["orange"]
    if score >= 40: return COLORS["yellow"]
    return COLORS["red"]


# ---------------------------------------------------------------------------
# Graphics — gauge, bar chart
# ---------------------------------------------------------------------------
def draw_score_gauge(score, size=160):
    """Hiring Readiness Score circular gauge with color-coded ring."""
    d = Drawing(size + 20, size + 20)
    cx = size / 2 + 10
    cy = size / 2 + 10

    # Outer ring
    d.add(Circle(cx, cy, size / 2,
                 fillColor=COLORS["light_bg"], strokeColor=COLORS["navy"], strokeWidth=2))

    # Score ring (filled)
    color = score_color(score)
    inner_r = size / 2 - 10
    d.add(Circle(cx, cy, inner_r,
                 fillColor=color, strokeColor=None))

    # White center
    d.add(Circle(cx, cy, inner_r - 16,
                 fillColor=COLORS["white"], strokeColor=None))

    # Score text
    d.add(String(cx, cy + 4, str(int(score)),
                 fontSize=40, fillColor=COLORS["navy"],
                 textAnchor="middle", fontName="Helvetica-Bold"))

    d.add(String(cx, cy - 20, "/ 100",
                 fontSize=11, fillColor=COLORS["gray"],
                 textAnchor="middle", fontName="Helvetica"))

    return d


def create_bar_chart(categories, scores, width=470, height=200):
    """Horizontal bar chart for category scores."""
    d = Drawing(width, height)

    bar_height = 22
    gap = 14
    max_bar_width = width - 220
    start_y = height - 25
    label_x = 5
    bar_x = 190

    for i, (cat, score) in enumerate(zip(categories, scores)):
        y = start_y - i * (bar_height + gap)

        # Category label
        d.add(String(label_x, y + 6, cat[:28],
                     fontSize=9, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica"))

        # Background bar
        d.add(Rect(bar_x, y, max_bar_width, bar_height,
                   fillColor=COLORS["light_bg"], strokeColor=None, rx=3))

        # Score bar
        bar_width = max((score / 100) * max_bar_width, 2)
        color = score_color(score)
        d.add(Rect(bar_x, y, bar_width, bar_height,
                   fillColor=color, strokeColor=None, rx=3))

        # Score label
        d.add(String(bar_x + max_bar_width + 10, y + 6, f"{int(score)}/100",
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="start", fontName="Helvetica-Bold"))

    return d


def create_funnel_chart(stages, counts, width=470, height=200):
    """Funnel chart showing application -> hire conversion."""
    d = Drawing(width, height)

    bar_count = len(stages)
    if bar_count == 0:
        return d
    bar_width = (width - 60) / bar_count - 12
    max_height = height - 50
    base_y = 25
    max_count = max(counts) if counts else 1

    for i, (stage, count) in enumerate(zip(stages, counts)):
        x = 30 + i * ((width - 60) / bar_count)
        bar_h = (count / max_count) * max_height if max_count > 0 else 0

        # Funnel-style color gradient navy to gold
        if i == 0:
            color = COLORS["navy"]
        elif i == bar_count - 1:
            color = COLORS["green"]
        else:
            color = COLORS["navy_light"]

        d.add(Rect(x, base_y, bar_width, bar_h,
                   fillColor=color, strokeColor=None))

        # Count label
        d.add(String(x + bar_width / 2, base_y + bar_h + 4, str(int(count)),
                     fontSize=10, fillColor=COLORS["text"],
                     textAnchor="middle", fontName="Helvetica-Bold"))

        # Stage label
        short = stage[:13]
        d.add(String(x + bar_width / 2, base_y - 12, short,
                     fontSize=8, fillColor=COLORS["text"],
                     textAnchor="middle", fontName="Helvetica"))

    return d


# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
def get_styles():
    styles = getSampleStyleSheet()
    custom = {
        "title": ParagraphStyle("RTitle", parent=styles["Title"],
                                fontSize=30, textColor=COLORS["navy"],
                                spaceAfter=6, fontName="Helvetica-Bold", leading=36),
        "name": ParagraphStyle("RName", parent=styles["Title"],
                               fontSize=24, textColor=COLORS["navy_dark"],
                               spaceAfter=4, fontName="Helvetica-Bold", leading=30),
        "subtitle": ParagraphStyle("RSubtitle", parent=styles["Normal"],
                                   fontSize=14, textColor=COLORS["gray"],
                                   spaceAfter=6, fontName="Helvetica"),
        "heading": ParagraphStyle("RHeading", parent=styles["Heading1"],
                                  fontSize=20, textColor=COLORS["navy"],
                                  spaceBefore=14, spaceAfter=10,
                                  fontName="Helvetica-Bold"),
        "subheading": ParagraphStyle("RSub", parent=styles["Heading2"],
                                     fontSize=14, textColor=COLORS["navy_dark"],
                                     spaceBefore=12, spaceAfter=6,
                                     fontName="Helvetica-Bold"),
        "body": ParagraphStyle("RBody", parent=styles["Normal"],
                               fontSize=10, textColor=COLORS["text"],
                               spaceAfter=6, fontName="Helvetica", leading=14),
        "body_small": ParagraphStyle("RBodyS", parent=styles["Normal"],
                                     fontSize=8, textColor=COLORS["text"],
                                     spaceAfter=4, fontName="Helvetica", leading=11),
        "signal": ParagraphStyle("RSignal", parent=styles["Title"],
                                 fontSize=24, textColor=COLORS["green"],
                                 spaceAfter=4, fontName="Helvetica-Bold",
                                 alignment=1),
        "grade_large": ParagraphStyle("RGrade", parent=styles["Title"],
                                      fontSize=18, textColor=COLORS["navy"],
                                      spaceAfter=6, fontName="Helvetica-Bold",
                                      alignment=1),
        "footer": ParagraphStyle("RFooter", parent=styles["Normal"],
                                 fontSize=7, textColor=COLORS["gray"],
                                 fontName="Helvetica", leading=10),
        "disclaimer": ParagraphStyle("RDisc", parent=styles["Normal"],
                                     fontSize=6.5, textColor=COLORS["gray"],
                                     fontName="Helvetica", leading=9,
                                     spaceBefore=8),
    }
    return custom


def standard_table_style(extra=None):
    cmds = [
        ("BACKGROUND", (0, 0), (-1, 0), COLORS["header_bg"]),
        ("TEXTCOLOR", (0, 0), (-1, 0), COLORS["white"]),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [COLORS["white"], COLORS["row_alt"]]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]
    if extra:
        cmds.extend(extra)
    return TableStyle(cmds)


DISCLAIMER_TEXT = (
    "DISCLAIMER: This hiring readiness report is generated by AI for educational and research purposes only. "
    "All scores, ratings, and recommendations are AI-generated approximations based on publicly available data "
    "and provided role context. Final hiring decisions must be made by humans following EEOC and applicable "
    "employment law in your jurisdiction. Always have HR and employment counsel review job descriptions, offers, "
    "and interview content before use. The authors accept no liability for any losses or damages incurred from "
    "reliance on this report."
)


# ---------------------------------------------------------------------------
# Main report generator
# ---------------------------------------------------------------------------
def generate_report(data, output_path):
    doc = SimpleDocTemplate(
        output_path, pagesize=letter,
        rightMargin=50, leftMargin=50,
        topMargin=50, bottomMargin=50
    )

    S = get_styles()
    elements = []

    role = data.get("role_title", "Senior Backend Engineer")
    company = data.get("company", "Acme Corp")
    location = data.get("location", "San Francisco, CA / Remote-US")
    level = data.get("level", "IC5 (Senior)")
    function = data.get("function", "Engineering")
    date_str = data.get("date", datetime.now().strftime("%B %d, %Y"))
    overall_score = data.get("overall_score", 68)
    grade = score_grade(overall_score)
    signal = score_signal(overall_score)
    sig_color = signal_color(overall_score)

    # =====================================================================
    # PAGE 1 — COVER
    # =====================================================================
    elements.append(Spacer(1, 0.4 * inch))
    elements.append(Paragraph("Hiring Readiness Report", S["title"]))
    elements.append(Spacer(1, 24))
    elements.append(Paragraph(role, S["name"]))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(
        f"{function} &nbsp;&middot;&nbsp; {level} &nbsp;&middot;&nbsp; {company} &nbsp;&middot;&nbsp; {location}",
        S["subtitle"]
    ))
    elements.append(Spacer(1, 6))
    elements.append(Paragraph(f"Generated: {date_str}", S["subtitle"]))
    elements.append(Spacer(1, 28))

    # Score gauge
    gauge = draw_score_gauge(overall_score, size=160)
    elements.append(gauge)
    elements.append(Spacer(1, 18))

    color = score_color(overall_score)
    elements.append(Paragraph(
        f'Hiring Readiness Score: <font color="{color.hexval()}">{int(overall_score)}/100</font> '
        f'(Grade: <font color="{color.hexval()}">{grade}</font>)',
        S["grade_large"]
    ))
    elements.append(Spacer(1, 8))
    elements.append(Paragraph(
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SigLine", parent=S["signal"], textColor=sig_color, fontSize=22)
    ))

    elements.append(Spacer(1, 26))

    # Mini profile table on cover
    prof = data.get("profile", {})
    band = prof.get("salary_band", "$170K-$200K")
    urgency = prof.get("urgency", "Growth (not blocking)")
    hm = prof.get("hiring_manager", "VP Engineering")
    target_fill = prof.get("target_fill_days", "60 days")

    cover_tbl = [
        ["Salary Band", band, "Urgency", urgency],
        ["Hiring Manager", hm, "Target Fill", target_fill],
    ]
    cov_table = Table(cover_tbl, colWidths=[110, 130, 110, 130])
    cov_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), COLORS["light_bg"]),
        ("BACKGROUND", (2, 0), (2, -1), COLORS["light_bg"]),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
        ("FONTNAME", (2, 0), (2, -1), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("GRID", (0, 0), (-1, -1), 0.5, COLORS["border"]),
        ("TEXTCOLOR", (0, 0), (-1, -1), COLORS["text"]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING", (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
    ]))
    elements.append(cov_table)
    elements.append(Spacer(1, 20))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))
    elements.append(PageBreak())

    # =====================================================================
    # PAGE 2 — SCORE DASHBOARD
    # =====================================================================
    elements.append(Paragraph("Hiring Readiness Score Dashboard", S["heading"]))
    elements.append(Spacer(1, 6))

    cats = data.get("categories", {
        "Job Description Quality": {"score": 64, "weight": "20%"},
        "Resume Screening Rigor": {"score": 62, "weight": "20%"},
        "Interview Framework": {"score": 68, "weight": "20%"},
        "Compensation Competitiveness": {"score": 70, "weight": "20%"},
        "Employer Brand Strength": {"score": 62, "weight": "20%"},
    })

    cat_names = list(cats.keys())
    cat_scores = [cats[c].get("score", 50) if isinstance(cats[c], dict) else cats[c]
                  for c in cat_names]

    chart = create_bar_chart(cat_names, cat_scores)
    elements.append(chart)
    elements.append(Spacer(1, 14))

    # Signal badge
    elements.append(Paragraph(
        f'Hiring Readiness: <font color="{color.hexval()}">{int(overall_score)}/100</font> &nbsp;|&nbsp; '
        f'Grade: <font color="{color.hexval()}">{grade}</font> &nbsp;|&nbsp; '
        f'Signal: <font color="{sig_color.hexval()}">{signal}</font>',
        ParagraphStyle("SigBadge", parent=S["body"], fontSize=12,
                       fontName="Helvetica-Bold", alignment=1, spaceAfter=14)
    ))

    # Score breakdown table
    sd = [["Category", "Score", "Weight", "Status"]]
    for n, sc in zip(cat_names, cat_scores):
        weight = cats[n].get("weight", "--") if isinstance(cats[n], dict) else "--"
        status = "Strong" if sc >= 70 else ("Mixed" if sc >= 40 else "Weak")
        sd.append([n, f"{int(sc)}/100", weight, status])

    sd_tbl = Table(sd, colWidths=[200, 80, 60, 100])
    sd_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    for i, sc in enumerate(cat_scores, 1):
        c = score_color(sc)
        sd_extra.append(("TEXTCOLOR", (3, i), (3, i), c))
        sd_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    sd_tbl.setStyle(standard_table_style(sd_extra))
    elements.append(sd_tbl)

    elements.append(Spacer(1, 18))
    elements.append(Paragraph("Executive Summary", S["subheading"]))
    exec_summary = data.get("executive_summary",
        f"The {role} role at {company} shows mixed hiring readiness signals. The compensation band is "
        f"competitive at the 65th market percentile, and the interview framework is reasonably structured. "
        f"However, the job description carries 11 must-have requirements (vs. industry benchmark of 3-5), "
        f"likely filtering out 60-70% of qualified candidates before phone screen. Employer brand on "
        f"Glassdoor (3.8) trails the strongest peer competitor (4.4), and recent layoff coverage is "
        f"showing up in candidate reviews. Implementing the top 5 quick wins should reduce time-to-fill "
        f"from the current 70-day median to 45-50 days while improving accept rate from 65% to ~82%."
    )
    elements.append(Paragraph(exec_summary, S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 3 — JOB DESCRIPTION ANALYSIS
    # =====================================================================
    elements.append(Paragraph("Job Description Analysis", S["heading"]))
    elements.append(Spacer(1, 6))

    jd = data.get("jd_analysis", {})

    elements.append(Paragraph("Sub-Scores", S["subheading"]))
    jd_subs = jd.get("sub_scores", {
        "Clarity & Structure": 14,
        "ATS Keyword Optimization": 12,
        "Inclusivity": 15,
        "Must-Have / Nice-to-Have": 10,
        "Candidate Appeal": 13,
    })
    sub_tbl = [["Dimension", "Score / 20"]]
    for k, v in jd_subs.items():
        sub_tbl.append([k, f"{v}/20"])
    sub_t = Table(sub_tbl, colWidths=[300, 140])
    sub_t.setStyle(standard_table_style([("ALIGN", (1, 0), (1, -1), "CENTER")]))
    elements.append(sub_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("ATS Keyword Analysis", S["subheading"]))
    keywords = jd.get("ats_keywords", {
        "present": ["Python", "AWS", "Docker", "REST APIs", "PostgreSQL"],
        "missing": ["Kubernetes", "CI/CD", "microservices", "system design"],
    })
    kw_tbl = [["Status", "Keywords"]]
    kw_tbl.append(["Present", Paragraph(", ".join(keywords.get("present", [])), S["body_small"])])
    kw_tbl.append(["Missing (High Value)", Paragraph(", ".join(keywords.get("missing", [])), S["body_small"])])
    kw_t = Table(kw_tbl, colWidths=[140, 300])
    kw_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(kw_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Inclusivity Flags", S["subheading"]))
    flags = jd.get("inclusivity_flags", [
        {"term": "rockstar developer", "issue": "M-coded; suppresses female applicants", "fix": "highly skilled engineer"},
        {"term": "recent CS grad", "issue": "Age signal", "fix": "Bachelor's in CS or equivalent experience"},
    ])
    fl_tbl = [["Term", "Issue", "Replacement"]]
    for f in flags:
        fl_tbl.append([f.get("term", ""),
                       Paragraph(f.get("issue", ""), S["body_small"]),
                       Paragraph(f.get("fix", ""), S["body_small"])])
    fl_t = Table(fl_tbl, colWidths=[120, 180, 140])
    fl_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(fl_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Rewrite Recommendations", S["subheading"]))
    recs = jd.get("recommendations", [
        "Title: change to 'Senior Software Engineer (Backend)' for 2x LinkedIn search volume",
        "Lead with mission/product impact in first 2 sentences",
        "Cut must-haves from 11 to 4, move rest to nice-to-have",
        "Add explicit salary band ($170K-$220K) — legally required in 4 states",
        "Add 'Growth Path' section showing route to Staff Engineer",
    ])
    for i, r in enumerate(recs, 1):
        elements.append(Paragraph(f"{i}. {r}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 4 — CANDIDATE PIPELINE
    # =====================================================================
    elements.append(Paragraph("Candidate Pipeline Summary", S["heading"]))
    elements.append(Spacer(1, 6))

    pipeline = data.get("pipeline", {})

    elements.append(Paragraph("Current Funnel", S["subheading"]))
    funnel = pipeline.get("funnel", {
        "Applications": 200,
        "Phone Screen": 18,
        "Onsite": 6,
        "Offer": 2,
        "Hire": 1,
    })
    stages = list(funnel.keys())
    counts = list(funnel.values())
    fc = create_funnel_chart(stages, counts)
    elements.append(fc)
    elements.append(Spacer(1, 12))

    # Funnel benchmark comparison
    elements.append(Paragraph("Funnel vs Benchmark", S["subheading"]))
    funnel_rows = pipeline.get("funnel_comparison", [
        {"stage": "Application → Phone Screen", "current": "9%", "benchmark": "15-25%", "status": "Below"},
        {"stage": "Phone Screen → Onsite", "current": "33%", "benchmark": "40-60%", "status": "Below"},
        {"stage": "Onsite → Offer", "current": "33%", "benchmark": "25-40%", "status": "OK"},
        {"stage": "Offer → Accept", "current": "50%", "benchmark": "70-90%", "status": "Below"},
    ])
    fr_tbl = [["Stage Conversion", "Current", "Benchmark", "Status"]]
    for r in funnel_rows:
        fr_tbl.append([r.get("stage", ""), r.get("current", ""),
                       r.get("benchmark", ""), r.get("status", "")])
    fr_t = Table(fr_tbl, colWidths=[200, 70, 100, 70])
    fr_extra = [("ALIGN", (1, 0), (-1, -1), "CENTER")]
    for i, r in enumerate(funnel_rows, 1):
        st = r.get("status", "").lower()
        if "below" in st or "weak" in st:
            fr_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["red"]))
        elif "ok" in st or "strong" in st:
            fr_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["green"]))
        else:
            fr_extra.append(("TEXTCOLOR", (3, i), (3, i), COLORS["orange"]))
        fr_extra.append(("FONTNAME", (3, i), (3, i), "Helvetica-Bold"))
    fr_t.setStyle(standard_table_style(fr_extra))
    elements.append(fr_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Candidates", S["subheading"]))
    candidates = pipeline.get("top_candidates", [
        {"rank": 1, "name": "Candidate A", "score": 87, "rec": "Strong Phone Screen", "note": "9 yrs backend, peer co. staff-level"},
        {"rank": 2, "name": "Candidate B", "score": 78, "rec": "Phone Screen", "note": "Solid fundamentals, pivot 2 yrs ago"},
        {"rank": 3, "name": "Candidate C", "score": 72, "rec": "Phone Screen", "note": "Strong on system design"},
        {"rank": 4, "name": "Candidate D", "score": 64, "rec": "Borderline", "note": "Title fits but light on scale"},
        {"rank": 5, "name": "Candidate E", "score": 48, "rec": "Pass", "note": "Title inflation — 3 yrs total"},
    ])
    c_tbl = [["#", "Candidate", "Score", "Recommendation", "Note"]]
    for c in candidates:
        c_tbl.append([str(c.get("rank", "")), c.get("name", ""), f"{c.get('score', '')}/100",
                      c.get("rec", ""), Paragraph(c.get("note", ""), S["body_small"])])
    c_t = Table(c_tbl, colWidths=[25, 100, 55, 120, 145])
    c_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                        ("ALIGN", (0, 0), (2, -1), "CENTER")]))
    elements.append(c_t)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 5 — INTERVIEW FRAMEWORK
    # =====================================================================
    elements.append(Paragraph("Interview Framework", S["heading"]))
    elements.append(Spacer(1, 6))

    interview = data.get("interview", {})

    elements.append(Paragraph("Recommended Loop Structure", S["subheading"]))
    loop = interview.get("loop", [
        {"stage": "Recruiter Screen", "duration": "30 min", "focus": "Motivation, comp, dealbreakers"},
        {"stage": "Hiring Manager", "duration": "45 min", "focus": "Story, scope, behavioral"},
        {"stage": "Take-Home Work Sample", "duration": "2-3 hrs (paid)", "focus": "Realistic backend problem"},
        {"stage": "Technical Live", "duration": "60 min", "focus": "Walkthrough + system design"},
        {"stage": "Behavioral Panel", "duration": "60 min", "focus": "Conflict, ambiguity, ownership"},
        {"stage": "Culture Add", "duration": "45 min", "focus": "Values, diverse perspective"},
        {"stage": "Exec Final", "duration": "30 min", "focus": "Vision fit, close"},
    ])
    lp_tbl = [["Stage", "Duration", "Focus"]]
    for l in loop:
        lp_tbl.append([l.get("stage", ""), l.get("duration", ""),
                       Paragraph(l.get("focus", ""), S["body_small"])])
    lp_t = Table(lp_tbl, colWidths=[150, 100, 200])
    lp_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(lp_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Sample Behavioral Questions (STAR)", S["subheading"]))
    behavioral = interview.get("behavioral_questions", [
        "Tell me about a time you disagreed with a manager. How did it resolve?",
        "Describe a project with shifting goals. How did you operate?",
        "Walk me through your biggest professional failure. What did you change?",
        "Tell me about a project that required working across multiple teams.",
        "Tell me about feedback that changed how you work.",
    ])
    for i, q in enumerate(behavioral, 1):
        elements.append(Paragraph(f"{i}. {q}", S["body"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Sample Technical Questions", S["subheading"]))
    technical = interview.get("technical_questions", [
        "Design a URL shortener handling 10K writes/sec and 100K reads/sec.",
        "Walk through how you'd debug a 99th percentile latency spike in production.",
        "How would you scale a feature from 1K to 1M users? What breaks first?",
        "Trade-offs of building a service in microservices vs. monolith?",
        "Walk us through a system you designed from first principles.",
    ])
    for i, q in enumerate(technical, 1):
        elements.append(Paragraph(f"{i}. {q}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 6 — SALARY BENCHMARKS
    # =====================================================================
    elements.append(Paragraph("Compensation Benchmarks", S["heading"]))
    elements.append(Spacer(1, 6))

    salary = data.get("salary", {})

    elements.append(Paragraph("Market Percentile Bands", S["subheading"]))
    percentiles = salary.get("percentiles", [
        {"pct": "25th", "base": "$155K", "bonus": "$15K", "equity": "$30K/yr", "total": "$200K"},
        {"pct": "50th (median)", "base": "$185K", "bonus": "$22K", "equity": "$50K/yr", "total": "$257K"},
        {"pct": "75th", "base": "$215K", "bonus": "$30K", "equity": "$80K/yr", "total": "$325K"},
        {"pct": "90th", "base": "$245K", "bonus": "$40K", "equity": "$120K/yr", "total": "$405K"},
    ])
    p_tbl = [["Percentile", "Base", "Bonus", "Equity (annual)", "Total Comp"]]
    for p in percentiles:
        p_tbl.append([p.get("pct", ""), p.get("base", ""), p.get("bonus", ""),
                      p.get("equity", ""), p.get("total", "")])
    p_t = Table(p_tbl, colWidths=[110, 80, 80, 110, 80])
    p_t.setStyle(standard_table_style([("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    elements.append(p_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Geographic Adjustments", S["subheading"]))
    geo = salary.get("geographic", [
        {"tier": "Tier 1 (HCOL)", "cities": "SF, NYC, Boston, Seattle", "multiplier": "1.00", "band": "$185K-$215K"},
        {"tier": "Tier 2 (MCOL)", "cities": "LA, DC, Chicago, Denver", "multiplier": "0.90", "band": "$167K-$194K"},
        {"tier": "Tier 3 (Regional)", "cities": "Austin, Atlanta, Phoenix", "multiplier": "0.83", "band": "$154K-$179K"},
        {"tier": "Tier 4 (LCOL)", "cities": "Midwest, South", "multiplier": "0.75", "band": "$139K-$161K"},
        {"tier": "Remote US (national)", "cities": "Anywhere US", "multiplier": "0.85", "band": "$157K-$183K"},
    ])
    g_tbl = [["Tier", "Cities", "Multiplier", "Recommended Band"]]
    for g in geo:
        g_tbl.append([g.get("tier", ""), Paragraph(g.get("cities", ""), S["body_small"]),
                      g.get("multiplier", ""), g.get("band", "")])
    g_t = Table(g_tbl, colWidths=[120, 160, 70, 120])
    g_t.setStyle(standard_table_style([("ALIGN", (2, 0), (2, -1), "CENTER"),
                                        ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(g_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Negotiation Talking Points", S["subheading"]))
    talking = salary.get("talking_points", [
        "Lead with mission, growth, scope — not base. Light on base vs Big Tech.",
        "Equity upside is your wedge — stage, ownership %, projected exit math.",
        "Be ready to flex base 5-10% for top candidates with multiple offers.",
        "Sign-on bonus ($25K-$50K) is cheaper than raising base to close.",
        "Frame total comp incl. equity amortization, not just base.",
    ])
    for i, t in enumerate(talking, 1):
        elements.append(Paragraph(f"{i}. {t}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 7 — OFFER DETAILS
    # =====================================================================
    elements.append(Paragraph("Offer Strategy & Close Plan", S["heading"]))
    elements.append(Spacer(1, 6))

    offer = data.get("offer", {})

    elements.append(Paragraph("Recommended Offer Package", S["subheading"]))
    offer_pkg = offer.get("package", {
        "Base Salary": "$190,000",
        "Target Bonus": "12% / $22,800",
        "Equity Grant": "$200,000 RSU (4-yr vest, 1-yr cliff)",
        "Equity Refresh": "20% of initial grant at year 3",
        "Sign-on Bonus": "$25,000 (clawback 12 mo / 50% at 13-24 mo)",
        "401k Match": "5% safe harbor",
        "Health Insurance": "100% employer-paid premium",
        "PTO": "Unlimited (real culture)",
        "Start Date Target": "30 days from offer accept",
    })
    op_tbl = [["Component", "Value"]]
    for k, v in offer_pkg.items():
        op_tbl.append([k, v])
    op_t = Table(op_tbl, colWidths=[200, 240])
    op_t.setStyle(standard_table_style())
    elements.append(op_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Close Timeline", S["subheading"]))
    timeline = offer.get("timeline", [
        {"day": "Day 0", "action": "Verbal offer + same-day written follow-up", "owner": "Recruiter"},
        {"day": "Day 1", "action": "Check-in: 'How are you feeling?'", "owner": "Recruiter"},
        {"day": "Day 2-3", "action": "Hiring Manager vision/relationship call", "owner": "HM"},
        {"day": "Day 3-4", "action": "Exec sponsor brief intro (if VP+)", "owner": "Exec"},
        {"day": "Day 4-5", "action": "Address objections; final terms", "owner": "Recruiter"},
        {"day": "Day 5-7", "action": "Decision deadline — push for written acceptance", "owner": "Recruiter"},
    ])
    tl_tbl = [["When", "Action", "Owner"]]
    for t in timeline:
        tl_tbl.append([t.get("day", ""), Paragraph(t.get("action", ""), S["body_small"]),
                       t.get("owner", "")])
    tl_t = Table(tl_tbl, colWidths=[80, 280, 80])
    tl_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(tl_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Decline Risk Assessment", S["subheading"]))
    risks = offer.get("decline_risks", [
        {"risk": "Competing offer at $230K+ from Big Tech", "probability": "30%", "mitigation": "Equity refresh + sign-on flex"},
        {"risk": "Counter from current employer", "probability": "20%", "mitigation": "Emphasize growth + scope"},
        {"risk": "Family / location concerns", "probability": "15%", "mitigation": "Remote-first reassurance"},
        {"risk": "Start date conflict", "probability": "10%", "mitigation": "Flex 2 weeks"},
    ])
    rk_tbl = [["Risk", "Probability", "Mitigation"]]
    for r in risks:
        rk_tbl.append([Paragraph(r.get("risk", ""), S["body_small"]),
                       r.get("probability", ""),
                       Paragraph(r.get("mitigation", ""), S["body_small"])])
    rk_t = Table(rk_tbl, colWidths=[180, 80, 180])
    rk_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP"),
                                          ("ALIGN", (1, 0), (1, -1), "CENTER")]))
    elements.append(rk_t)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 8 — EMPLOYER BRAND
    # =====================================================================
    elements.append(Paragraph("Employer Brand Assessment", S["heading"]))
    elements.append(Spacer(1, 6))

    employer = data.get("employer", {})

    elements.append(Paragraph("Review Platform Summary", S["subheading"]))
    platforms = employer.get("platforms", [
        {"name": "Glassdoor", "rating": "3.8", "count": "218", "ceo_approval": "76%", "recommend": "68%"},
        {"name": "Indeed", "rating": "3.6", "count": "124", "ceo_approval": "n/a", "recommend": "67/100"},
        {"name": "LinkedIn (followers)", "rating": "47,000", "count": "+18% YoY", "ceo_approval": "n/a", "recommend": "n/a"},
        {"name": "Blind (sentiment)", "rating": "Mixed", "count": "n/a", "ceo_approval": "n/a", "recommend": "n/a"},
    ])
    pl_tbl = [["Platform", "Rating", "Count / Growth", "CEO Approval", "Recommend"]]
    for p in platforms:
        pl_tbl.append([p.get("name", ""), p.get("rating", ""),
                       p.get("count", ""), p.get("ceo_approval", ""),
                       p.get("recommend", "")])
    pl_t = Table(pl_tbl, colWidths=[120, 70, 100, 90, 80])
    pl_t.setStyle(standard_table_style([("ALIGN", (1, 0), (-1, -1), "CENTER")]))
    elements.append(pl_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Positives", S["subheading"]))
    positives = employer.get("positives", [
        {"theme": "Smart, mission-driven coworkers", "freq": "~32%"},
        {"theme": "Strong learning culture", "freq": "~24%"},
        {"theme": "Interesting technical problems", "freq": "~18%"},
        {"theme": "Generous PTO policy", "freq": "~14%"},
        {"theme": "Fast career growth (early)", "freq": "~10%"},
    ])
    ps_tbl = [["Theme", "Frequency"]]
    for p in positives:
        ps_tbl.append([p.get("theme", ""), p.get("freq", "")])
    ps_t = Table(ps_tbl, colWidths=[330, 110])
    ps_t.setStyle(standard_table_style([("ALIGN", (1, 0), (1, -1), "CENTER")]))
    elements.append(ps_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Top Negatives", S["subheading"]))
    negatives = employer.get("negatives", [
        {"theme": "Long hours / on-call burden", "freq": "~28%"},
        {"theme": "Comp below Big Tech peers", "freq": "~22%"},
        {"theme": "Unclear promotion path", "freq": "~18%"},
        {"theme": "Recent layoffs created fear culture", "freq": "~14%"},
        {"theme": "Middle management quality varies", "freq": "~10%"},
    ])
    ng_tbl = [["Theme", "Frequency"]]
    for n in negatives:
        ng_tbl.append([n.get("theme", ""), n.get("freq", "")])
    ng_t = Table(ng_tbl, colWidths=[330, 110])
    ng_extra = [("ALIGN", (1, 0), (1, -1), "CENTER")]
    for i in range(1, len(negatives) + 1):
        ng_extra.append(("TEXTCOLOR", (1, i), (1, i), COLORS["red"]))
    ng_t.setStyle(standard_table_style(ng_extra))
    elements.append(ng_t)
    elements.append(Spacer(1, 14))

    elements.append(Paragraph("Competitor Comparison", S["subheading"]))
    comps = employer.get("competitors", [
        {"name": company, "glassdoor": "3.8", "ceo": "76%", "differentiator": "Mission + learning, comp gap"},
        {"name": "Competitor A", "glassdoor": "4.4", "ceo": "92%", "differentiator": "Strong learning + remote-first"},
        {"name": "Competitor B", "glassdoor": "3.9", "ceo": "74%", "differentiator": "Higher comp, more demanding"},
        {"name": "Competitor C (Big Tech)", "glassdoor": "4.1", "ceo": "84%", "differentiator": "Comp + brand prestige"},
    ])
    cp_tbl = [["Company", "Glassdoor", "CEO Approval", "Differentiator"]]
    for c in comps:
        cp_tbl.append([c.get("name", "")[:30], c.get("glassdoor", ""),
                       c.get("ceo", ""), Paragraph(c.get("differentiator", ""), S["body_small"])])
    cp_t = Table(cp_tbl, colWidths=[150, 80, 90, 130])
    cp_extra = [("ALIGN", (1, 0), (2, -1), "CENTER"),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("BACKGROUND", (0, 1), (-1, 1), COLORS["gold_light"]),
                ("FONTNAME", (0, 1), (-1, 1), "Helvetica-Bold")]
    cp_t.setStyle(standard_table_style(cp_extra))
    elements.append(cp_t)

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 9 — 90-DAY ACTION PLAN
    # =====================================================================
    elements.append(Paragraph("90-Day Hiring Improvement Plan", S["heading"]))
    elements.append(Spacer(1, 6))

    plan = data.get("action_plan", {})

    elements.append(Paragraph("Week 1 — Quick Wins", S["subheading"]))
    week1 = plan.get("week_1", [
        "Add explicit salary band to JD (legal requirement in CA/CO/NY/WA)",
        "Cut must-haves from 11 to 4 (move rest to nice-to-have)",
        "Standardize 5 behavioral questions across all interviewers",
        "Set 24-hour SLA for recruiter response to applications",
        "Authorize recruiter 5-10% flex headroom for top candidates",
    ])
    for i, w in enumerate(week1, 1):
        elements.append(Paragraph(f"{i}. {w}", S["body"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Days 8-30 — Foundations", S["subheading"]))
    days_8_30 = plan.get("days_8_30", [
        "Rewrite full JD using inclusive language framework",
        "Add paid take-home work sample to senior loops",
        "Cut interview loop from 5 weeks to 2-3 weeks",
        "Implement structured scorecard rubric across all interviewers",
        "Launch employee story content series on career site + LinkedIn",
        "Address layoff narrative head-on with proactive comms",
    ])
    for i, d in enumerate(days_8_30, 1):
        elements.append(Paragraph(f"{i}. {d}", S["body"]))
    elements.append(Spacer(1, 10))

    elements.append(Paragraph("Days 31-90 — Compounding Plays", S["subheading"]))
    days_31_90 = plan.get("days_31_90", [
        "Activate employee advocacy program — 20 employees posting monthly",
        "Add equity refresh policy (20% of initial at year 3)",
        "Build outbound sourcing playbook for senior IC pipeline",
        "Implement anonymous resume screening to reduce pedigree bias",
        "Publish annual DEI metrics report — separates you from generic statements",
        "Set up 360 debrief process within 24 hrs of onsite",
    ])
    for i, d in enumerate(days_31_90, 1):
        elements.append(Paragraph(f"{i}. {d}", S["body"]))

    elements.append(PageBreak())

    # =====================================================================
    # PAGE 10 — 30/60/90 ONBOARDING + DISCLAIMER
    # =====================================================================
    elements.append(Paragraph("30/60/90 Day Onboarding Plan (Once Hired)", S["heading"]))
    elements.append(Spacer(1, 6))

    onboard = data.get("onboarding", {})

    elements.append(Paragraph("Day 1 Readiness Checklist", S["subheading"]))
    day1 = onboard.get("day_1", [
        "Hardware ready (laptop, monitor, peripherals)",
        "Accounts active (email, Slack, GitHub, tools)",
        "Access provisioned (VPN, repos, cloud, deployments)",
        "Buddy assigned + introduced",
        "Day 1 hourly agenda scheduled",
        "Welcome kit / swag prepared",
        "Manager 1:1 cadence on calendar",
        "30/60/90 check-ins scheduled BEFORE Day 1",
    ])
    for i, d in enumerate(day1, 1):
        elements.append(Paragraph(f"{i}. {d}", S["body"]))
    elements.append(Spacer(1, 12))

    elements.append(Paragraph("Milestones at 30 / 60 / 90 Days", S["subheading"]))
    milestones = onboard.get("milestones", [
        {"checkpoint": "30 Day", "above_bar": "Has shipped 2 small features; team intros complete", "at_bar": "1 small ship; immersion strong", "below_bar": "Still learning tooling; no contributions"},
        {"checkpoint": "60 Day", "above_bar": "Owning medium project; cross-functional trust built", "at_bar": "1 medium-complexity project owned end-to-end", "below_bar": "Still needs heavy guidance on owned work"},
        {"checkpoint": "90 Day", "above_bar": "Independent operator; contributing to strategy", "at_bar": "Operates with light oversight; clear at-bar reading", "below_bar": "Performance concerns surfaced; PIP consideration"},
    ])
    ms_tbl = [["Checkpoint", "Above Bar", "At Bar", "Below Bar"]]
    for m in milestones:
        ms_tbl.append([m.get("checkpoint", ""),
                       Paragraph(m.get("above_bar", ""), S["body_small"]),
                       Paragraph(m.get("at_bar", ""), S["body_small"]),
                       Paragraph(m.get("below_bar", ""), S["body_small"])])
    ms_t = Table(ms_tbl, colWidths=[70, 130, 130, 110])
    ms_t.setStyle(standard_table_style([("VALIGN", (0, 0), (-1, -1), "TOP")]))
    elements.append(ms_t)

    elements.append(Spacer(1, 22))
    elements.append(Paragraph(
        "Generated by AI Recruiter Team for Claude Code", S["footer"]
    ))
    elements.append(Paragraph(DISCLAIMER_TEXT, S["disclaimer"]))

    # Build
    doc.build(elements)
    return output_path


# ---------------------------------------------------------------------------
# Demo data
# ---------------------------------------------------------------------------
def get_demo_data():
    return {
        "role_title": "Senior Backend Engineer",
        "company": "Acme Corp",
        "location": "San Francisco, CA / Remote-US",
        "level": "IC5 (Senior)",
        "function": "Engineering",
        "date": datetime.now().strftime("%B %d, %Y"),
        "overall_score": 65,
        "profile": {
            "salary_band": "$170K-$200K base",
            "urgency": "Growth (not blocking)",
            "hiring_manager": "VP Engineering",
            "target_fill_days": "60 days",
        },
        "categories": {
            "Job Description Quality": {"score": 64, "weight": "20%"},
            "Resume Screening Rigor": {"score": 62, "weight": "20%"},
            "Interview Framework": {"score": 68, "weight": "20%"},
            "Compensation Competitiveness": {"score": 70, "weight": "20%"},
            "Employer Brand Strength": {"score": 62, "weight": "20%"},
        },
        "executive_summary": (
            "The Senior Backend Engineer role at Acme Corp shows mixed hiring readiness signals. "
            "Compensation is competitive at the 65th market percentile, and the interview framework "
            "is reasonably structured. However, the job description carries 11 must-have requirements "
            "(vs. industry benchmark of 3-5), filtering out an estimated 60-70% of qualified candidates "
            "before phone screen. Employer brand on Glassdoor (3.8) trails the strongest peer competitor "
            "(4.4), and recent layoff coverage is showing up in candidate reviews. Implementing the top "
            "5 quick wins should reduce time-to-fill from the current 70-day median to 45-50 days while "
            "improving accept rate from 65% to ~82%."
        ),
        "jd_analysis": {
            "sub_scores": {
                "Clarity & Structure": 14,
                "ATS Keyword Optimization": 12,
                "Inclusivity": 15,
                "Must-Have / Nice-to-Have": 10,
                "Candidate Appeal": 13,
            },
            "ats_keywords": {
                "present": ["Python", "AWS", "Docker", "REST APIs", "PostgreSQL"],
                "missing": ["Kubernetes", "CI/CD", "microservices", "system design"],
            },
            "inclusivity_flags": [
                {"term": "rockstar developer", "issue": "M-coded; suppresses female applicants", "fix": "highly skilled engineer"},
                {"term": "recent CS grad", "issue": "Age signal", "fix": "Bachelor's in CS or equivalent experience"},
            ],
            "recommendations": [
                "Title: change to 'Senior Software Engineer (Backend)' for 2x LinkedIn search volume",
                "Lead with mission/product impact in first 2 sentences",
                "Cut must-haves from 11 to 4, move rest to nice-to-have",
                "Add explicit salary band ($170K-$220K) — legally required in 4 states",
                "Add 'Growth Path' section showing route to Staff Engineer",
            ],
        },
        "pipeline": {
            "funnel": {
                "Applications": 200,
                "Phone Screen": 18,
                "Onsite": 6,
                "Offer": 2,
                "Hire": 1,
            },
            "funnel_comparison": [
                {"stage": "Application → Phone Screen", "current": "9%", "benchmark": "15-25%", "status": "Below"},
                {"stage": "Phone Screen → Onsite", "current": "33%", "benchmark": "40-60%", "status": "Below"},
                {"stage": "Onsite → Offer", "current": "33%", "benchmark": "25-40%", "status": "OK"},
                {"stage": "Offer → Accept", "current": "50%", "benchmark": "70-90%", "status": "Below"},
            ],
            "top_candidates": [
                {"rank": 1, "name": "Candidate A", "score": 87, "rec": "Strong Phone Screen", "note": "9 yrs backend, peer co. staff-level"},
                {"rank": 2, "name": "Candidate B", "score": 78, "rec": "Phone Screen", "note": "Solid fundamentals; pivot 2 yrs ago"},
                {"rank": 3, "name": "Candidate C", "score": 72, "rec": "Phone Screen", "note": "Strong on system design"},
                {"rank": 4, "name": "Candidate D", "score": 64, "rec": "Borderline", "note": "Title fits but light on scale"},
                {"rank": 5, "name": "Candidate E", "score": 48, "rec": "Pass", "note": "Title inflation — 3 yrs total"},
            ],
        },
        "interview": {
            "loop": [
                {"stage": "Recruiter Screen", "duration": "30 min", "focus": "Motivation, comp, dealbreakers"},
                {"stage": "Hiring Manager", "duration": "45 min", "focus": "Story, scope, behavioral"},
                {"stage": "Take-Home Work Sample", "duration": "2-3 hrs (paid)", "focus": "Realistic backend problem"},
                {"stage": "Technical Live", "duration": "60 min", "focus": "Walkthrough + system design"},
                {"stage": "Behavioral Panel", "duration": "60 min", "focus": "Conflict, ambiguity, ownership"},
                {"stage": "Culture Add", "duration": "45 min", "focus": "Values, diverse perspective"},
                {"stage": "Exec Final", "duration": "30 min", "focus": "Vision fit, close"},
            ],
            "behavioral_questions": [
                "Tell me about a time you disagreed with a manager. How did it resolve?",
                "Describe a project with shifting goals. How did you operate?",
                "Walk me through your biggest professional failure. What did you change?",
                "Tell me about a project that required working across multiple teams.",
                "Tell me about feedback that changed how you work.",
            ],
            "technical_questions": [
                "Design a URL shortener handling 10K writes/sec and 100K reads/sec.",
                "Walk through how you'd debug a 99th percentile latency spike in production.",
                "How would you scale a feature from 1K to 1M users? What breaks first?",
                "Trade-offs of building a service in microservices vs. monolith?",
                "Walk us through a system you designed from first principles.",
            ],
        },
        "salary": {
            "percentiles": [
                {"pct": "25th", "base": "$155K", "bonus": "$15K", "equity": "$30K/yr", "total": "$200K"},
                {"pct": "50th (median)", "base": "$185K", "bonus": "$22K", "equity": "$50K/yr", "total": "$257K"},
                {"pct": "75th", "base": "$215K", "bonus": "$30K", "equity": "$80K/yr", "total": "$325K"},
                {"pct": "90th", "base": "$245K", "bonus": "$40K", "equity": "$120K/yr", "total": "$405K"},
            ],
            "geographic": [
                {"tier": "Tier 1 (HCOL)", "cities": "SF, NYC, Boston, Seattle", "multiplier": "1.00", "band": "$185K-$215K"},
                {"tier": "Tier 2 (MCOL)", "cities": "LA, DC, Chicago, Denver", "multiplier": "0.90", "band": "$167K-$194K"},
                {"tier": "Tier 3 (Regional)", "cities": "Austin, Atlanta, Phoenix", "multiplier": "0.83", "band": "$154K-$179K"},
                {"tier": "Tier 4 (LCOL)", "cities": "Midwest, South", "multiplier": "0.75", "band": "$139K-$161K"},
                {"tier": "Remote US (national)", "cities": "Anywhere US", "multiplier": "0.85", "band": "$157K-$183K"},
            ],
            "talking_points": [
                "Lead with mission, growth, scope — not base. Light on base vs Big Tech.",
                "Equity upside is your wedge — stage, ownership %, projected exit math.",
                "Be ready to flex base 5-10% for top candidates with multiple offers.",
                "Sign-on bonus ($25K-$50K) is cheaper than raising base to close.",
                "Frame total comp incl. equity amortization, not just base.",
            ],
        },
        "offer": {
            "package": {
                "Base Salary": "$190,000",
                "Target Bonus": "12% / $22,800",
                "Equity Grant": "$200,000 RSU (4-yr vest, 1-yr cliff)",
                "Equity Refresh": "20% of initial grant at year 3",
                "Sign-on Bonus": "$25,000 (clawback 12 mo / 50% at 13-24 mo)",
                "401k Match": "5% safe harbor",
                "Health Insurance": "100% employer-paid premium",
                "PTO": "Unlimited (real culture)",
                "Start Date Target": "30 days from offer accept",
            },
            "timeline": [
                {"day": "Day 0", "action": "Verbal offer + same-day written follow-up", "owner": "Recruiter"},
                {"day": "Day 1", "action": "Check-in: 'How are you feeling?'", "owner": "Recruiter"},
                {"day": "Day 2-3", "action": "Hiring Manager vision/relationship call", "owner": "HM"},
                {"day": "Day 3-4", "action": "Exec sponsor brief intro (if VP+)", "owner": "Exec"},
                {"day": "Day 4-5", "action": "Address objections; final terms", "owner": "Recruiter"},
                {"day": "Day 5-7", "action": "Decision deadline — push for written acceptance", "owner": "Recruiter"},
            ],
            "decline_risks": [
                {"risk": "Competing offer at $230K+ from Big Tech", "probability": "30%", "mitigation": "Equity refresh + sign-on flex"},
                {"risk": "Counter from current employer", "probability": "20%", "mitigation": "Emphasize growth + scope"},
                {"risk": "Family / location concerns", "probability": "15%", "mitigation": "Remote-first reassurance"},
                {"risk": "Start date conflict", "probability": "10%", "mitigation": "Flex 2 weeks"},
            ],
        },
        "employer": {
            "platforms": [
                {"name": "Glassdoor", "rating": "3.8", "count": "218", "ceo_approval": "76%", "recommend": "68%"},
                {"name": "Indeed", "rating": "3.6", "count": "124", "ceo_approval": "n/a", "recommend": "67/100"},
                {"name": "LinkedIn (followers)", "rating": "47,000", "count": "+18% YoY", "ceo_approval": "n/a", "recommend": "n/a"},
                {"name": "Blind (sentiment)", "rating": "Mixed", "count": "n/a", "ceo_approval": "n/a", "recommend": "n/a"},
            ],
            "positives": [
                {"theme": "Smart, mission-driven coworkers", "freq": "~32%"},
                {"theme": "Strong learning culture", "freq": "~24%"},
                {"theme": "Interesting technical problems", "freq": "~18%"},
                {"theme": "Generous PTO policy", "freq": "~14%"},
                {"theme": "Fast career growth (early)", "freq": "~10%"},
            ],
            "negatives": [
                {"theme": "Long hours / on-call burden", "freq": "~28%"},
                {"theme": "Comp below Big Tech peers", "freq": "~22%"},
                {"theme": "Unclear promotion path", "freq": "~18%"},
                {"theme": "Recent layoffs created fear culture", "freq": "~14%"},
                {"theme": "Middle management quality varies", "freq": "~10%"},
            ],
            "competitors": [
                {"name": "Acme Corp", "glassdoor": "3.8", "ceo": "76%", "differentiator": "Mission + learning, comp gap"},
                {"name": "Competitor A", "glassdoor": "4.4", "ceo": "92%", "differentiator": "Strong learning + remote-first"},
                {"name": "Competitor B", "glassdoor": "3.9", "ceo": "74%", "differentiator": "Higher comp, more demanding"},
                {"name": "Competitor C (Big Tech)", "glassdoor": "4.1", "ceo": "84%", "differentiator": "Comp + brand prestige"},
            ],
        },
        "action_plan": {
            "week_1": [
                "Add explicit salary band to JD (legal requirement in CA/CO/NY/WA)",
                "Cut must-haves from 11 to 4 (move rest to nice-to-have)",
                "Standardize 5 behavioral questions across all interviewers",
                "Set 24-hour SLA for recruiter response to applications",
                "Authorize recruiter 5-10% flex headroom for top candidates",
            ],
            "days_8_30": [
                "Rewrite full JD using inclusive language framework",
                "Add paid take-home work sample to senior loops",
                "Cut interview loop from 5 weeks to 2-3 weeks",
                "Implement structured scorecard rubric across all interviewers",
                "Launch employee story content series on career site + LinkedIn",
                "Address layoff narrative head-on with proactive comms",
            ],
            "days_31_90": [
                "Activate employee advocacy program — 20 employees posting monthly",
                "Add equity refresh policy (20% of initial at year 3)",
                "Build outbound sourcing playbook for senior IC pipeline",
                "Implement anonymous resume screening to reduce pedigree bias",
                "Publish annual DEI metrics report",
                "Set up 360 debrief process within 24 hrs of onsite",
            ],
        },
        "onboarding": {
            "day_1": [
                "Hardware ready (laptop, monitor, peripherals)",
                "Accounts active (email, Slack, GitHub, tools)",
                "Access provisioned (VPN, repos, cloud, deployments)",
                "Buddy assigned + introduced",
                "Day 1 hourly agenda scheduled",
                "Welcome kit / swag prepared",
                "Manager 1:1 cadence on calendar",
                "30/60/90 check-ins scheduled BEFORE Day 1",
            ],
            "milestones": [
                {"checkpoint": "30 Day", "above_bar": "Has shipped 2 small features; team intros complete", "at_bar": "1 small ship; immersion strong", "below_bar": "Still learning tooling; no contributions"},
                {"checkpoint": "60 Day", "above_bar": "Owning medium project; cross-functional trust built", "at_bar": "1 medium-complexity project owned end-to-end", "below_bar": "Still needs heavy guidance"},
                {"checkpoint": "90 Day", "above_bar": "Independent operator; contributing to strategy", "at_bar": "Operates with light oversight; at-bar", "below_bar": "Performance concerns; PIP consideration"},
            ],
        },
    }


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    if len(sys.argv) < 2 or sys.argv[1] == "--demo":
        data = get_demo_data()
        output = "RECRUIT-REPORT-sample.pdf"
        generate_report(data, output)
        print(f"Sample report generated: {output}")
        return

    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else "RECRUIT-REPORT.pdf"

    with open(input_file, "r") as f:
        data = json.load(f)

    generate_report(data, output_file)
    print(f"Report generated: {output_file}")


if __name__ == "__main__":
    main()
