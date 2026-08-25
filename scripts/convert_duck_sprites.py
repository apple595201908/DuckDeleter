import sys
import os
import glob
from PIL import Image, ImageDraw
import numpy as np

sys.stdout.reconfigure(encoding='utf-8')

BRAIN_DIR = r"C:\Users\user\.gemini\antigravity-ide\brain\f459b038-eebd-4902-b804-1f0966f20e69"
ASSETS_DIR = r"c:\Users\user\Desktop\MonsterDeleter\assets"

COLS = 5
ROWS = 3

def remove_white_background(img_rgba, threshold=240):
    """Cleanly turns white / near-white background into smooth transparent alpha."""
    arr = np.array(img_rgba, dtype=np.float32)
    r, g, b, a = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2], arr[:, :, 3]
    
    # Calculate distance to pure white
    whiteness = np.minimum(np.minimum(r, g), b)
    
    t_low = threshold - 15
    t_high = threshold + 10
    
    alpha_factor = np.clip((t_high - whiteness) / (t_high - t_low), 0.0, 1.0)
    new_a = a * alpha_factor
    
    arr[:, :, 3] = new_a
    result = Image.fromarray(np.uint8(arr), mode="RGBA")
    return result

def clean_frame_corners(frame, is_kick=False):
    """Optionally cleans numbers/artifacts from top-left corners if needed."""
    if is_kick:
        w, h = frame.size
        draw = ImageDraw.Draw(frame)
        draw.rectangle([0, 0, int(w * 0.22), int(h * 0.18)], fill=(255, 255, 255, 0))
    return frame

def process_spritesheet(input_path, output_path, is_kick=False, target_size=(2000, 1600)):
    print(f"Processing {os.path.basename(input_path)} -> {os.path.basename(output_path)} ...")
    img = Image.open(input_path).convert("RGBA")
    
    orig_w, orig_h = img.size
    tile_w = orig_w / COLS
    tile_h = orig_h / ROWS
    
    out_w, out_h = target_size
    out_tile_w = out_w // COLS
    out_tile_h = out_h // ROWS
    
    final_sheet = Image.new("RGBA", (out_w, out_h), (0, 0, 0, 0))
    
    for r in range(ROWS):
        for c in range(COLS):
            box = (int(c * tile_w), int(r * tile_h), int((c + 1) * tile_w), int((r + 1) * tile_h))
            frame = img.crop(box)
            
            # Remove white background
            frame_transparent = remove_white_background(frame, threshold=242)
            
            if is_kick:
                frame_transparent = clean_frame_corners(frame_transparent, is_kick=True)
                
            frame_resized = frame_transparent.resize((out_tile_w, out_tile_h), Image.Resampling.LANCZOS)
            
            paste_box = (c * out_tile_w, r * out_tile_h)
            final_sheet.paste(frame_resized, paste_box)
            
    final_sheet.save(output_path, "PNG")
    print(f"Saved {output_path} ({out_w}x{out_h})")

def main():
    bg_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_select_bg_*.jpg")))
    walk_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_walk_sheet_*.jpg")))
    point_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_point_sheet_*.jpg")))
    kick_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_kick_sheet_*.jpg")))
    exp_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_pop_explosion_sheet_*.jpg")))
    vic_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_victory_sheet_*.jpg")))
    fly_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_fly_sheet_*.jpg")))
    
    # 1. Background image
    if bg_files:
        bg_in = bg_files[-1]
        bg_out = os.path.join(ASSETS_DIR, "选择界面", "选择界面.png")
        bg_img = Image.open(bg_in).convert("RGBA")
        bg_img.save(bg_out, "PNG")
        print(f"Saved background to {bg_out}")
        
    # 2. Walk
    if walk_files:
        process_spritesheet(walk_files[-1], os.path.join(ASSETS_DIR, "走路动效_spritesheet_transparent.png"), target_size=(2000, 1600))
        
    # 3. Point
    if point_files:
        process_spritesheet(point_files[-1], os.path.join(ASSETS_DIR, "指着文件_spritesheet_transparent.png"), target_size=(2000, 1600))
        
    # 4. Kick / Eat
    eat_files = sorted(glob.glob(os.path.join(BRAIN_DIR, "duck_eat_sheet_*.jpg")))
    if eat_files:
        process_spritesheet(eat_files[-1], os.path.join(ASSETS_DIR, "duck_eat_spritesheet.png"), target_size=(2000, 1600))
        # Keep alias for kick phase as well
        process_spritesheet(eat_files[-1], os.path.join(ASSETS_DIR, "duck_kick_spritesheet.png"), target_size=(2000, 1600))
        process_spritesheet(eat_files[-1], os.path.join(ASSETS_DIR, "踹文件动效_spritesheet_transparent.png"), target_size=(2000, 1600))
    elif kick_files:
        process_spritesheet(kick_files[-1], os.path.join(ASSETS_DIR, "duck_kick_spritesheet.png"), is_kick=True, target_size=(2000, 1600))
        process_spritesheet(kick_files[-1], os.path.join(ASSETS_DIR, "踹文件动效_spritesheet_transparent.png"), is_kick=True, target_size=(2000, 1600))
        
    # 5. Explosion
    if exp_files:
        process_spritesheet(exp_files[-1], os.path.join(ASSETS_DIR, "爆炸_spritesheet_transparent.png"), target_size=(2000, 1600))
        
    # 6. Victory (Leo)
    if vic_files:
        process_spritesheet(vic_files[-1], os.path.join(ASSETS_DIR, "雷欧登场_spritesheet_transparent.png"), target_size=(2000, 1600))
        
    # 7. Fly
    if fly_files:
        process_spritesheet(fly_files[-1], os.path.join(ASSETS_DIR, "出场飞行动效_spritesheet_transparent.png"), target_size=(2000, 1600))

if __name__ == "__main__":
    main()
