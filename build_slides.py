from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# ---------------------------------------------------------------------------
# Theme
# ---------------------------------------------------------------------------
BG      = RGBColor(0x0F, 0x17, 0x2A)   # deep navy
ACCENT  = RGBColor(0x38, 0xBD, 0xF8)   # sky blue
WHITE   = RGBColor(0xFF, 0xFF, 0xFF)
GRAY    = RGBColor(0x94, 0xA3, 0xB8)
GREEN   = RGBColor(0x34, 0xD3, 0x99)
YELLOW  = RGBColor(0xFB, 0xBF, 0x24)
RED     = RGBColor(0xF8, 0x71, 0x71)

W = Inches(13.33)
H = Inches(7.5)


def new_prs():
    prs = Presentation()
    prs.slide_width  = W
    prs.slide_height = H
    return prs


def blank_slide(prs):
    layout = prs.slide_layouts[6]   # completely blank
    return prs.slides.add_slide(layout)


def bg(slide, color=BG):
    from pptx.util import Emu
    shape = slide.shapes.add_shape(1, 0, 0, W, H)
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def txt(slide, text, l, t, w, h, size=24, bold=False, color=WHITE,
        align=PP_ALIGN.LEFT, wrap=True):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.word_wrap = wrap
    tf = box.text_frame
    tf.word_wrap = wrap
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.color.rgb = color
    return box


def accent_bar(slide, t=Inches(1.1), h=Inches(0.05)):
    bar = slide.shapes.add_shape(1, Inches(0.6), t, Inches(12.1), h)
    bar.fill.solid()
    bar.fill.fore_color.rgb = ACCENT
    bar.line.fill.background()


def bullet_box(slide, items, l, t, w, h, size=20, color=WHITE, marker="•"):
    box = slide.shapes.add_textbox(l, t, w, h)
    box.word_wrap = True
    tf = box.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(6)
        run = p.add_run()
        run.text = f"{marker}  {item}"
        run.font.size = Pt(size)
        run.font.color.rgb = color


def colored_box(slide, label, desc, l, t, w, h, box_color):
    shape = slide.shapes.add_shape(1, l, t, w, h)
    shape.fill.solid()
    shape.fill.fore_color.rgb = box_color
    shape.line.fill.background()
    txt(slide, label, l + Inches(0.15), t + Inches(0.1), w - Inches(0.3),
        Inches(0.4), size=16, bold=True, color=BG)
    txt(slide, desc,  l + Inches(0.15), t + Inches(0.45), w - Inches(0.3),
        h - Inches(0.55), size=13, color=BG, wrap=True)


# ===========================================================================
# Slides
# ===========================================================================

prs = new_prs()

# ---------------------------------------------------------------------------
# 1. Title
# ---------------------------------------------------------------------------
s = blank_slide(prs)
bg(s)
txt(s, "Project Knowledge Hub", Inches(0.6), Inches(1.8), Inches(12), Inches(1.2),
    size=52, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
txt(s, "RAG-powered Q&A over your project documentation",
    Inches(0.6), Inches(3.1), Inches(12), Inches(0.7),
    size=26, color=ACCENT, align=PP_ALIGN.CENTER)
txt(s, "AI for Engineering  ·  2025",
    Inches(0.6), Inches(4.2), Inches(12), Inches(0.5),
    size=18, color=GRAY, align=PP_ALIGN.CENTER)

# ---------------------------------------------------------------------------
# 2. Problem
# ---------------------------------------------------------------------------
s = blank_slide(prs)
bg(s)
txt(s, "The Problem", Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
    size=36, bold=True, color=WHITE)
accent_bar(s)

bullet_box(s, [
    "Developers repeatedly ask the same questions about system design, API contracts, and requirements",
    "Knowledge is scattered across files, chat threads, and people — no single source of truth",
    "PM / BA / SA spend significant time re-answering questions that are already documented",
    "A frontend dev who needs API field names must interrupt a backend dev — or dig through documents manually",
], Inches(0.6), Inches(1.4), Inches(12), Inches(4.5), size=22)

txt(s, "Result: duplicated effort, slower delivery, and documentation gaps that compound over time.",
    Inches(0.6), Inches(6.1), Inches(12), Inches(0.8),
    size=18, color=YELLOW)

# ---------------------------------------------------------------------------
# 3. Solution
# ---------------------------------------------------------------------------
s = blank_slide(prs)
bg(s)
txt(s, "The Solution", Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
    size=36, bold=True, color=WHITE)
accent_bar(s)

txt(s, "A centralised knowledge hub where developers ask questions in natural language — and get answers grounded in the actual project documents.",
    Inches(0.6), Inches(1.3), Inches(12), Inches(1.0), size=20, color=WHITE)

colored_box(s, "✅  Found",
    "Answer drawn from documents,\nwith a clickable source citation",
    Inches(0.5), Inches(2.6), Inches(3.7), Inches(2.2), GREEN)

colored_box(s, "⚠️  Not Found (Abstain)",
    'System says "not in documents"\ninstead of guessing',
    Inches(4.5), Inches(2.6), Inches(3.9), Inches(2.2), YELLOW)

colored_box(s, "⚡  Conflict Detected",
    "Two sources disagree — both sides\nshown, system does not choose",
    Inches(8.6), Inches(2.6), Inches(4.2), Inches(2.2), RED)

txt(s, "Two design principles:   answer from documents only + always cite  ·  abstention is a feature, not a failure",
    Inches(0.6), Inches(5.2), Inches(12), Inches(0.6), size=16, color=GRAY)

# ---------------------------------------------------------------------------
# 4. Architecture
# ---------------------------------------------------------------------------
s = blank_slide(prs)
bg(s)
txt(s, "Architecture", Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
    size=36, bold=True, color=WHITE)
accent_bar(s)

# Ingestion row
txt(s, "INGESTION", Inches(0.6), Inches(1.3), Inches(2), Inches(0.4),
    size=13, bold=True, color=ACCENT)
for i, (label, x) in enumerate([
    ("Upload\n(MD / TXT / PDF)", 0.6),
    ("Parse &\nChunk", 3.0),
    ("Embed\n(multilingual-e5)", 5.4),
    ("ChromaDB\n(vector store)", 7.8),
]):
    box = s.shapes.add_shape(1, Inches(x), Inches(1.75), Inches(2.1), Inches(1.0))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0x1E, 0x3A, 0x5F)
    box.line.color.rgb = ACCENT
    txt(s, label, Inches(x + 0.1), Inches(1.8), Inches(1.9), Inches(0.9),
        size=14, color=WHITE, align=PP_ALIGN.CENTER)
    if i < 3:
        txt(s, "→", Inches(x + 2.15), Inches(2.0), Inches(0.5), Inches(0.5),
            size=20, color=ACCENT, align=PP_ALIGN.CENTER)

# Query row
txt(s, "QUERY", Inches(0.6), Inches(3.2), Inches(2), Inches(0.4),
    size=13, bold=True, color=GREEN)
for i, (label, x) in enumerate([
    ("User\nQuestion", 0.6),
    ("Embed\nQuery", 3.0),
    ("Similarity\nSearch (top-k)", 5.4),
    ("LLM +\nPrompt", 7.8),
    ("Answer +\nCitation", 10.2),
]):
    box = s.shapes.add_shape(1, Inches(x), Inches(3.65), Inches(2.1), Inches(1.0))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0x0F, 0x2E, 0x1A)
    box.line.color.rgb = GREEN
    txt(s, label, Inches(x + 0.1), Inches(3.7), Inches(1.9), Inches(0.9),
        size=14, color=WHITE, align=PP_ALIGN.CENTER)
    if i < 4:
        txt(s, "→", Inches(x + 2.15), Inches(3.95), Inches(0.5), Inches(0.5),
            size=20, color=GREEN, align=PP_ALIGN.CENTER)

# Tech stack
txt(s, "Streamlit  ·  ChromaDB  ·  sentence-transformers (multilingual-e5-small)  ·  OpenAI-compatible LLM via GitHub Models  ·  PyMuPDF",
    Inches(0.6), Inches(5.3), Inches(12), Inches(0.5),
    size=15, color=GRAY, align=PP_ALIGN.CENTER)

txt(s, "Entirely free to run  ·  No paid API required during development",
    Inches(0.6), Inches(5.9), Inches(12), Inches(0.5),
    size=15, color=ACCENT, align=PP_ALIGN.CENTER)

# ---------------------------------------------------------------------------
# 5. Demo
# ---------------------------------------------------------------------------
s = blank_slide(prs)
bg(s)
txt(s, "Demo", Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
    size=36, bold=True, color=WHITE)
accent_bar(s)

scenarios = [
    (GREEN,  "✅  Found",
     'Q: "What fields does the Order API return?"\n→  Answer with source citation\n     (api-spec.md › Order Endpoints)'),
    (YELLOW, "⚠️  Abstain",
     'Q: "Does the system support GDPR?"\n→  "ไม่พบข้อมูลเรื่องนี้ในเอกสาร"\n     No hallucination.'),
    (RED,    "⚡  Conflict",
     'Q: "What is the payment timeout?"\n→  api-spec.md says 30s\n     system-architecture.md says 60s\n     Both shown. No winner picked.'),
]
for i, (color, title, body) in enumerate(scenarios):
    x = Inches(0.5 + i * 4.25)
    box = s.shapes.add_shape(1, x, Inches(1.4), Inches(4.0), Inches(4.5))
    box.fill.solid()
    box.fill.fore_color.rgb = RGBColor(0x1A, 0x22, 0x3A)
    box.line.color.rgb = color
    txt(s, title, x + Inches(0.15), Inches(1.5), Inches(3.7), Inches(0.5),
        size=18, bold=True, color=color)
    txt(s, body, x + Inches(0.15), Inches(2.1), Inches(3.7), Inches(3.5),
        size=16, color=WHITE, wrap=True)

txt(s, "Documents page: upload MD / TXT / PDF  ·  view indexed files  ·  delete to remove from vector store",
    Inches(0.6), Inches(6.2), Inches(12), Inches(0.5),
    size=15, color=GRAY, align=PP_ALIGN.CENTER)

# ---------------------------------------------------------------------------
# 6. Future Directions
# ---------------------------------------------------------------------------
s = blank_slide(prs)
bg(s)
txt(s, "Future Directions", Inches(0.6), Inches(0.4), Inches(10), Inches(0.7),
    size=36, bold=True, color=WHITE)
accent_bar(s)

cols = [
    (ACCENT, "Deeper Intelligence", [
        "Documentation Gap Report — rank unanswered topics so teams know what's missing",
        "Corpus-wide conflict detection — scan entire knowledge base, not just retrieved chunks",
        "Cross-file reasoning — answers that synthesise information across multiple documents",
    ]),
    (GREEN, "Richer Sources", [
        "Raw codebase indexing — chunk by function boundary, auto-generate API reference docs",
        "Hybrid search — keyword + semantic for precise variable / function name lookups",
        "Auto-sync with git — re-index on every push, keep answers current",
    ]),
    (YELLOW, "Team & Enterprise", [
        "PM / BA / SA self-service upload — owners manage their own documents",
        "Multi-project support — separate knowledge bases per team or service",
        "Integration with Jira, Confluence, Slack — meet developers where they work",
    ]),
]
for i, (color, title, items) in enumerate(cols):
    x = Inches(0.4 + i * 4.3)
    header = s.shapes.add_shape(1, x, Inches(1.4), Inches(4.0), Inches(0.5))
    header.fill.solid()
    header.fill.fore_color.rgb = color
    header.line.fill.background()
    txt(s, title, x + Inches(0.1), Inches(1.45), Inches(3.8), Inches(0.45),
        size=16, bold=True, color=BG, align=PP_ALIGN.CENTER)
    bullet_box(s, items, x, Inches(2.0), Inches(4.1), Inches(4.5),
               size=15, color=WHITE)


prs.save("knowledge-hub-pitch.pptx")
print("Saved: knowledge-hub-pitch.pptx")
