#!/usr/bin/env python3
"""
Generate high-contrast, professional, offline illustrative workflow animation GIF for README.
Strictly offline: no live API calls, no real secrets, no user paths, no network errors.
"""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

WIDTH = 860
HEIGHT = 520
REPO_ROOT = Path(__file__).resolve().parent.parent
OUTPUT_PATH = REPO_ROOT / "assets" / "workflow-demo.gif"

# Palette
BG_DARK = (18, 22, 28)
CARD_BG = (26, 32, 44)
HEADER_BG = (13, 17, 23)
TEXT_WHITE = (240, 246, 252)
TEXT_MUTED = (139, 148, 158)
TEXT_DIM = (90, 100, 115)
ACCENT_BLUE = (88, 166, 255)
ACCENT_GREEN = (63, 185, 80)
ACCENT_YELLOW = (210, 153, 34)
ACCENT_PURPLE = (187, 128, 247)
BORDER_COLOR = (48, 54, 61)

def get_font(size: int, bold: bool = False):
    try:
        # Try system font on Windows
        font_name = "consola.ttf" if not bold else "consolab.ttf"
        font_path = Path("C:/Windows/Fonts") / font_name
        if font_path.exists():
            return ImageFont.truetype(str(font_path), size)
        
        # Fallback to arial or default
        arial_name = "arial.ttf" if not bold else "arialbd.ttf"
        arial_path = Path("C:/Windows/Fonts") / arial_name
        if arial_path.exists():
            return ImageFont.truetype(str(arial_path), size)
    except Exception:
        pass
    return ImageFont.load_default()

FONT_TITLE = get_font(16, bold=True)
FONT_SUBTITLE = get_font(12, bold=False)
FONT_STEP_TITLE = get_font(14, bold=True)
FONT_STEP_DESC = get_font(12, bold=False)
FONT_STATUS = get_font(11, bold=True)
FONT_BADGE = get_font(11, bold=True)

STEPS = [
    {
        "id": "1",
        "name": "Audit",
        "action": "Scan credentials, private paths, licenses, .gitignore",
        "detail": "0 sensitive patterns, 0 local path leaks, clean files",
        "status_done": "AUDIT PASS"
    },
    {
        "id": "2",
        "name": "Test & Build",
        "action": "Run local validators, structural checks & pre-commit gates",
        "detail": "SKILL.md front matter, bilingual sync, GIF multi-frame verified",
        "status_done": "GATES PASS"
    },
    {
        "id": "3",
        "name": "Commit",
        "action": "Enforce clean working tree & conventional commit style",
        "detail": "Privacy-safe author identity & structured commit message",
        "status_done": "STAGED & COMMITTED"
    },
    {
        "id": "4",
        "name": "Explicit Approval",
        "action": "Confirm user intent before touching remote repository",
        "detail": "Explicit authorization received: public release permitted",
        "status_done": "AUTHORIZED"
    },
    {
        "id": "5",
        "name": "Create & Push",
        "action": "Initialize public repo, set bilingual metadata & push main",
        "detail": "Description & topics configured, upstream tracking established",
        "status_done": "SYNCHRONIZED"
    },
    {
        "id": "6",
        "name": "Verify",
        "action": "Verify public URL, default branch, topic tags & CI pipeline",
        "detail": "Release boundaries intact: no releases, tags or PRs created",
        "status_done": "WORKFLOW VERIFIED"
    }
]

def draw_header(draw: ImageDraw.ImageDraw):
    # Header bar
    draw.rectangle([(0, 0), (WIDTH, 42)], fill=HEADER_BG)
    draw.line([(0, 42), (WIDTH, 42)], fill=BORDER_COLOR, width=1)
    
    # Window controls (macOS style dots)
    draw.ellipse([(14, 15), (26, 27)], fill=(255, 95, 86))
    draw.ellipse([(34, 15), (46, 27)], fill=(255, 189, 46))
    draw.ellipse([(54, 15), (66, 27)], fill=(39, 201, 63))
    
    # Title
    title_text = "github-open-source-release-skill"
    draw.text((76, 12), title_text, fill=TEXT_WHITE, font=FONT_TITLE)
    
    # Right badge: OFFLINE ILLUSTRATION
    badge_text = "Offline workflow illustration — no live API calls"
    badge_w = 345
    badge_h = 22
    badge_x = WIDTH - badge_w - 14
    badge_y = 10
    
    draw.rounded_rectangle([(badge_x, badge_y), (badge_x + badge_w, badge_y + badge_h)], radius=4, fill=(40, 30, 20), outline=ACCENT_YELLOW)
    draw.text((badge_x + 8, badge_y + 4), badge_text, fill=ACCENT_YELLOW, font=FONT_BADGE)

def draw_footer(draw: ImageDraw.ImageDraw, active_step_idx: int, all_done: bool = False):
    # Footer bar
    draw.rectangle([(0, HEIGHT - 32), (WIDTH, HEIGHT)], fill=HEADER_BG)
    draw.line([(0, HEIGHT - 32), (WIDTH, HEIGHT - 32)], fill=BORDER_COLOR, width=1)
    
    # Progress indicator
    total = len(STEPS)
    completed = total if all_done else max(0, active_step_idx)
    pct = int((completed / total) * 100)
    
    status_summary = f"Pipeline Status: {completed}/{total} steps completed ({pct}%)" if not all_done else "Pipeline Complete: 6/6 steps passed safely [Release Ready]"
    color = ACCENT_GREEN if all_done else (ACCENT_BLUE if completed > 0 else TEXT_MUTED)
    draw.text((16, HEIGHT - 24), status_summary, fill=color, font=FONT_SUBTITLE)
    
    note_text = "Standard AI Agent Release Pipeline: Audit -> Gate -> Commit -> Approve -> Push -> Verify"
    draw.text((WIDTH - 490, HEIGHT - 24), note_text, fill=TEXT_MUTED, font=FONT_SUBTITLE)

def create_frame(active_step: int, all_done: bool = False) -> Image.Image:
    im = Image.new("RGB", (WIDTH, HEIGHT), BG_DARK)
    draw = ImageDraw.Draw(im)
    
    draw_header(draw)
    draw_footer(draw, active_step, all_done)
    
    # Layout 6 steps in 2 columns x 3 rows
    col_w = (WIDTH - 42) // 2
    row_h = 135
    start_x = 14
    start_y = 52
    
    for i, step in enumerate(STEPS):
        col = i % 2
        row = i // 2
        
        x0 = start_x + col * (col_w + 14)
        y0 = start_y + row * (row_h + 12)
        x1 = x0 + col_w
        y1 = y0 + row_h
        
        # Step state: 0=pending, 1=running, 2=passed
        if all_done:
            state = 2
        elif i < active_step:
            state = 2
        elif i == active_step:
            state = 1
        else:
            state = 0
            
        # Draw card container
        if state == 2:
            card_border = (46, 117, 60)
            card_fill = (20, 32, 25)
        elif state == 1:
            card_border = ACCENT_BLUE
            card_fill = (22, 35, 52)
        else:
            card_border = BORDER_COLOR
            card_fill = CARD_BG
            
        draw.rounded_rectangle([(x0, y0), (x1, y1)], radius=6, fill=card_fill, outline=card_border, width=1 if state != 1 else 2)
        
        # Step number & title
        step_header = f"Step {step['id']}: {step['name']}"
        title_color = TEXT_WHITE if state in (1, 2) else TEXT_MUTED
        draw.text((x0 + 12, y0 + 10), step_header, fill=title_color, font=FONT_STEP_TITLE)
        
        # Status badge top-right of card
        if state == 2:
            badge_t = f"[OK] {step['status_done']}"
            badge_c = ACCENT_GREEN
            bg_b = (25, 45, 30)
        elif state == 1:
            badge_t = "[RUNNING] Processing..."
            badge_c = ACCENT_BLUE
            bg_b = (25, 40, 60)
        else:
            badge_t = "[PENDING] Queued"
            badge_c = TEXT_DIM
            bg_b = (30, 35, 42)
            
        bw = 140 if state != 2 else 150
        draw.rounded_rectangle([(x1 - bw - 10, y0 + 8), (x1 - 10, y0 + 26)], radius=3, fill=bg_b, outline=badge_c, width=1)
        draw.text((x1 - bw - 5, y0 + 11), badge_t, fill=badge_c, font=FONT_STATUS)
        
        # Action line
        action_text = f"> {step['action']}"
        draw.text((x0 + 12, y0 + 42), action_text, fill=TEXT_MUTED if state == 0 else (210, 225, 245), font=FONT_STEP_DESC)
        
        # Detail line
        detail_color = ACCENT_GREEN if state == 2 else (ACCENT_BLUE if state == 1 else TEXT_DIM)
        prefix = "+ " if state == 2 else ("* " if state == 1 else "  ")
        draw.text((x0 + 12, y0 + 70), f"{prefix}{step['detail']}", fill=detail_color, font=FONT_STEP_DESC)
        
        # Micro progress bar inside card
        pb_y = y0 + 104
        pb_w = col_w - 24
        draw.rounded_rectangle([(x0 + 12, pb_y), (x0 + 12 + pb_w, pb_y + 8)], radius=3, fill=(15, 18, 22))
        if state == 2:
            draw.rounded_rectangle([(x0 + 12, pb_y), (x0 + 12 + pb_w, pb_y + 8)], radius=3, fill=ACCENT_GREEN)
        elif state == 1:
            draw.rounded_rectangle([(x0 + 12, pb_y), (x0 + 12 + int(pb_w * 0.65), pb_y + 8)], radius=3, fill=ACCENT_BLUE)
            
    return im

def main():
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
    frames = []
    durations = []
    
    # Frame 0: Initial starting / scan stage
    frames.append(create_frame(active_step=0))
    durations.append(1000)
    
    # Frames 1..5: Progressing through each step
    for s in range(1, 6):
        frames.append(create_frame(active_step=s))
        durations.append(1100)
        
    # Frame 6: All steps completed
    frames.append(create_frame(active_step=6, all_done=True))
    durations.append(2500)
    
    # Save as animated GIF
    frames[0].save(
        OUTPUT_PATH,
        save_all=True,
        append_images=frames[1:],
        duration=durations,
        loop=0,
        optimize=True
    )
    print(f"Generated {len(frames)} frames workflow GIF at {OUTPUT_PATH}")

if __name__ == "__main__":
    main()
