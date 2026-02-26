import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT

# ── Palette ───────────────────────────────────────────────────────────────────
NAVY      = colors.HexColor("#0d2137")
NAVY_MID  = colors.HexColor("#163354")
GOLD      = colors.HexColor("#c9a84c")
GOLD_LITE = colors.HexColor("#e8c97a")
RED_FLAG  = colors.HexColor("#c0392b")
WHITE     = colors.HexColor("#f8f6f1")
LIGHT_BG  = colors.HexColor("#f0ede6")
GREY_TXT  = colors.HexColor("#555555")
GREY_LINE = colors.HexColor("#dddddd")

W, H = A4
ML = MR = 18 * mm
MT = MB = 15 * mm
CONTENT_W = W - ML - MR

# ── Styles ────────────────────────────────────────────────────────────────────
def styles():
    return {
        "title": ParagraphStyle("title",
            fontName="Times-Bold", fontSize=22, textColor=WHITE,
            leading=28, alignment=TA_LEFT),
        "subtitle": ParagraphStyle("subtitle",
            fontName="Times-Italic", fontSize=11, textColor=GOLD_LITE,
            leading=16, alignment=TA_LEFT),
        "section": ParagraphStyle("section",
            fontName="Times-Bold", fontSize=13, textColor=NAVY,
            leading=18, spaceBefore=12, spaceAfter=4),
        "factor_name": ParagraphStyle("factor_name",
            fontName="Helvetica-Bold", fontSize=9.5, textColor=NAVY,
            leading=13),
        "remark": ParagraphStyle("remark",
            fontName="Helvetica", fontSize=8.5, textColor=GREY_TXT,
            leading=13, spaceBefore=2),
        "body": ParagraphStyle("body",
            fontName="Helvetica", fontSize=9.5, textColor=NAVY,
            leading=14),
        "small": ParagraphStyle("small",
            fontName="Helvetica", fontSize=8, textColor=GREY_TXT,
            leading=12),
        "score_big": ParagraphStyle("score_big",
            fontName="Times-Bold", fontSize=52, textColor=GOLD,
            leading=58, alignment=TA_CENTER),
        "score_label": ParagraphStyle("score_label",
            fontName="Helvetica", fontSize=9, textColor=WHITE,
            leading=12, alignment=TA_CENTER, spaceAfter=2),
        "verdict": ParagraphStyle("verdict",
            fontName="Times-Bold", fontSize=15, textColor=WHITE,
            leading=20, alignment=TA_CENTER),
        "group_header": ParagraphStyle("group_header",
            fontName="Times-Bold", fontSize=11, textColor=NAVY_MID,
            leading=16, spaceBefore=10, spaceAfter=4),
        "profile_key": ParagraphStyle("profile_key",
            fontName="Helvetica-Bold", fontSize=9, textColor=NAVY,
            leading=13),
        "profile_val": ParagraphStyle("profile_val",
            fontName="Helvetica", fontSize=9, textColor=GREY_TXT,
            leading=13),
        "footer": ParagraphStyle("footer",
            fontName="Helvetica", fontSize=7.5, textColor=GREY_TXT,
            leading=11, alignment=TA_CENTER),
        "cta_head": ParagraphStyle("cta_head",
            fontName="Times-Bold", fontSize=12, textColor=GOLD_LITE,
            leading=16, alignment=TA_CENTER),
        "cta_body": ParagraphStyle("cta_body",
            fontName="Helvetica", fontSize=9, textColor=WHITE,
            leading=13, alignment=TA_CENTER),
    }

def score_bar(score, max_score=5, width=60, height=7):
    """Draw a mini score bar as a Table cell."""
    filled = int(round((score / max_score) * width))
    empty = width - filled
    bar_color = GOLD if score >= 4 else (colors.HexColor("#2980b9") if score == 3 else RED_FLAG)
    data = [[""]]
    t = Table(data, colWidths=[filled * mm / 3], rowHeights=[height])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), bar_color),
        ("LINEABOVE",  (0, 0), (-1, -1), 0, colors.white),
        ("LINEBELOW",  (0, 0), (-1, -1), 0, colors.white),
    ]))
    return t

def get_verdict(score):
    if score >= 85:
        return "Excellent Fit"
    elif score >= 70:
        return "Strong Fit"
    elif score >= 55:
        return "Good Fit"
    else:
        return "Partial Fit — Consider Carefully"

def importance_dots(imp, max_imp=5):
    filled = "●" * imp
    empty  = "○" * (max_imp - imp)
    return filled + empty

def generate_pdf(profile, factor_details, final_score, group_scores):
    S = styles()
    buf = io.BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=ML, rightMargin=MR,
        topMargin=MT, bottomMargin=MB,
        title="BVI Flag Suitability Report",
        author="Jejo Joy",
    )

    story = []
    date_str = datetime.now().strftime("%d %B %Y")
    verdict = get_verdict(final_score)

    # ── HEADER BANNER (navy table) ────────────────────────────────────────────
    header_data = [[
        Paragraph("BVI Flag Suitability Report", S["title"]),
        Paragraph(f"BVI Flag Suitability Report<br/>{date_str}", S["subtitle"]),
    ]]
    header_table = Table(header_data, colWidths=[CONTENT_W * 0.6, CONTENT_W * 0.4])
    header_table.setStyle(TableStyle([
        ("BACKGROUND",  (0, 0), (-1, -1), NAVY),
        ("VALIGN",      (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",  (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING",(0,0), (-1,-1),  14),
        ("LEFTPADDING", (0, 0), (0, -1),  14),
        ("RIGHTPADDING",(-1,0), (-1,-1),  14),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))

    # ── SCORE PANEL ───────────────────────────────────────────────────────────
    score_data = [[
        Paragraph("BVI SUITABILITY SCORE", S["score_label"]),
        Paragraph(str(final_score), S["score_big"]),
        Paragraph("out of 100", S["score_label"]),
        Paragraph(verdict, S["verdict"]),
    ]]
    score_table = Table(
        score_data,
        colWidths=[CONTENT_W * 0.25] * 4,
        rowHeights=[72],
    )
    score_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), NAVY_MID),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LINEAFTER",     (0, 0), (2, 0),   0.5, colors.HexColor("#2a4a6e")),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 10))

    # ── PROFILE SUMMARY ───────────────────────────────────────────────────────
    story.append(Paragraph("Your Vessel Profile", S["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=GOLD, spaceAfter=6))

    profile_labels = [
        ("Vessel Use",       profile.get("vessel_use", "—")),
        ("Cruising Area",    profile.get("cruising_area", "—")),
        ("UBO Residency",    profile.get("ubo_residency", "—")),
        ("Ownership",        profile.get("ownership", "—")),
        ("Jurisdiction",     profile.get("jurisdiction", "—")),
        ("Vessel Stage",     profile.get("vessel_stage", "—")),
    ]
    pdata = []
    for i in range(0, len(profile_labels), 3):
        row = []
        for label, val in profile_labels[i:i+3]:
            cell = [Paragraph(label, S["profile_key"]), Paragraph(val, S["profile_val"])]
            row.append(cell)
        while len(row) < 3:
            row.append("")
        pdata.append(row)

    ptable = Table(pdata, colWidths=[CONTENT_W / 3] * 3)
    ptable.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), LIGHT_BG),
        ("TOPPADDING",    (0, 0), (-1, -1), 8),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 8),
        ("LEFTPADDING",   (0, 0), (-1, -1), 10),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 10),
        ("LINEBELOW",     (0, 0), (-1, -2), 0.5, GREY_LINE),
        ("VALIGN",        (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(ptable)
    story.append(Spacer(1, 12))

    # ── CATEGORY SCORES ───────────────────────────────────────────────────────
    story.append(Paragraph("Score by Category", S["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=GOLD, spaceAfter=6))

    gs_data = [["Category", "Score", "Visual"]]
    for grp, sc in group_scores.items():
        bar_len = int(sc / 5)  # 0-20 chars
        bar_str = "█" * bar_len + "░" * (20 - bar_len)
        bar_color = GOLD if sc >= 70 else (colors.HexColor("#2980b9") if sc >= 50 else RED_FLAG)
        gs_data.append([
            Paragraph(grp, S["body"]),
            Paragraph(f"<b>{sc}</b>", S["body"]),
            Paragraph(f'<font color="#{bar_color.hexval()[2:]}">{bar_str}</font>', S["body"]),
        ])

    gs_table = Table(gs_data, colWidths=[CONTENT_W * 0.45, CONTENT_W * 0.1, CONTENT_W * 0.45])
    gs_table.setStyle(TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  NAVY),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  WHITE),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  9),
        ("TOPPADDING",    (0, 0), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [WHITE, LIGHT_BG]),
        ("LINEBELOW",     (0, 0), (-1, -1), 0.3, GREY_LINE),
        ("VALIGN",        (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(gs_table)
    story.append(Spacer(1, 14))

    # ── FACTOR DETAIL BY GROUP ────────────────────────────────────────────────
    story.append(Paragraph("Detailed Factor Analysis", S["section"]))
    story.append(HRFlowable(width=CONTENT_W, thickness=1, color=GOLD, spaceAfter=8))

    GROUPS_ORDER = [
        "Financial", "Reputation & Legal Standing",
        "Commercial & Operational Framework", "Administration & Compliance",
        "Service & Support", "Corporate & Information",
    ]
    GROUP_ICONS = {
        "Financial": "💰",
        "Reputation & Legal Standing": "⚖",
        "Commercial & Operational Framework": "⚓",
        "Administration & Compliance": "📋",
        "Service & Support": "🤝",
        "Corporate & Information": "🏛",
    }

    for group_name in GROUPS_ORDER:
        gf = [f for f in factor_details if f["group"] == group_name]
        if not gf:
            continue

        icon = GROUP_ICONS.get(group_name, "")
        grp_header = Table(
            [[Paragraph(f"{group_name}", S["group_header"])]],
            colWidths=[CONTENT_W],
        )
        grp_header.setStyle(TableStyle([
            ("BACKGROUND",    (0, 0), (-1, -1), colors.HexColor("#e8f0f8")),
            ("LEFTPADDING",   (0, 0), (-1, -1), 10),
            ("TOPPADDING",    (0, 0), (-1, -1), 5),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ("LINEBELOW",     (0, 0), (-1, -1), 1.5, NAVY_MID),
        ]))
        story.append(grp_header)
        story.append(Spacer(1, 4))

        for f in gf:
            stars     = "★" * f["bvi_score"] + "☆" * (5 - f["bvi_score"])
            imp_dots  = importance_dots(f["importance"])
            imp_color = "#c9a84c"

            row_data = [[
                [
                    Paragraph(f["name"], S["factor_name"]),
                    Paragraph(f["remark"], S["remark"]),
                ],
                Paragraph(f'<font color="#c9a84c"><b>{stars}</b></font><br/>'
                          f'<font size="7" color="#888">BVI Rating</font>', S["small"]),
                Paragraph(f'<font color="{imp_color}"><b>{imp_dots}</b></font><br/>'
                          f'<font size="7" color="#888">Your Priority</font>', S["small"]),
            ]]

            row_table = Table(
                row_data,
                colWidths=[CONTENT_W * 0.62, CONTENT_W * 0.19, CONTENT_W * 0.19],
            )
            row_table.setStyle(TableStyle([
                ("VALIGN",        (0, 0), (-1, -1), "TOP"),
                ("TOPPADDING",    (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                ("LEFTPADDING",   (0, 0), (0, -1),  4),
                ("RIGHTPADDING",  (-1,0), (-1,-1),  4),
                ("LINEBELOW",     (0, 0), (-1, -1), 0.3, GREY_LINE),
            ]))
            story.append(KeepTogether(row_table))

        story.append(Spacer(1, 8))

    # ── SPECIAL NOTES ─────────────────────────────────────────────────────────
    notes = []
    p = profile
    if p.get("ubo_residency") == "EU" and p.get("vessel_use") == "Commercial" and p.get("cruising_area") == "EU":
        notes.append("For an EU-resident UBO operating commercially within EU waters, an EU flag such as Malta may offer structural VAT advantages. We recommend discussing your specific tax position with a maritime tax advisor before making a final decision.")
    if p.get("jurisdiction") == "Other (not listed)":
        notes.append("Your nationality or incorporation jurisdiction is not directly on the BVI eligible list. Incorporating a BVI company or a company in an eligible jurisdiction resolves this — BVI's corporate registry makes this a straightforward step.")

    if notes:
        story.append(Paragraph("Important Notes", S["section"]))
        story.append(HRFlowable(width=CONTENT_W, thickness=1, color=GOLD, spaceAfter=6))
        for note in notes:
            note_table = Table(
                [[Paragraph(f"⚠  {note}", S["body"])]],
                colWidths=[CONTENT_W],
            )
            note_table.setStyle(TableStyle([
                ("BACKGROUND",    (0,0),(-1,-1), colors.HexColor("#fff8e6")),
                ("LEFTPADDING",   (0,0),(-1,-1), 10),
                ("TOPPADDING",    (0,0),(-1,-1), 8),
                ("BOTTOMPADDING", (0,0),(-1,-1), 8),
                ("LINEBELOW",     (0,0),(-1,-1), 0.5, GOLD),
            ]))
            story.append(note_table)
            story.append(Spacer(1, 6))

    # ── CTA PANEL ─────────────────────────────────────────────────────────────
    story.append(Spacer(1, 10))
    cta_data = [[
        Paragraph("Ready to Register?", S["cta_head"]),
        Paragraph(
            "Get in touch to discuss your specific situation and explore the registration process.<br/>"
            "<b>Jejo Joy</b>  ·  jejojoy.neelankavil@bvimaritime.vg",
            S["cta_body"]
        ),
    ]]
    cta_table = Table(cta_data, colWidths=[CONTENT_W * 0.35, CONTENT_W * 0.65])
    cta_table.setStyle(TableStyle([
        ("BACKGROUND",    (0,0),(-1,-1), NAVY),
        ("TOPPADDING",    (0,0),(-1,-1), 14),
        ("BOTTOMPADDING", (0,0),(-1,-1), 14),
        ("LEFTPADDING",   (0,0),(-1,-1), 14),
        ("RIGHTPADDING",  (0,0),(-1,-1), 14),
        ("VALIGN",        (0,0),(-1,-1), "MIDDLE"),
        ("LINEAFTER",     (0,0),(0,-1),  0.5, colors.HexColor("#2a4a6e")),
    ]))
    story.append(cta_table)

    # ── FOOTER ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width=CONTENT_W, thickness=0.5, color=GREY_LINE))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        f"Generated by the BVI Flag Suitability Tool  ·  {date_str}  ·  "
        "This report is for guidance purposes only and does not constitute legal or financial advice.",
        S["footer"]
    ))

    doc.build(story)
    buf.seek(0)
    return buf.getvalue()
