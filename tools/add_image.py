"""把產好的角色圖轉成頁面用的 WebP：img/<id>.webp（頁面顯示，寬 480）與 img/full/<id>.webp（原尺寸，給做 3D 時參考）。
用法：python3 tools/add_image.py <角色 id> <原圖路徑>
原圖（PNG）不進 repo，只存轉好的 WebP。"""
import sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
cid, src = sys.argv[1], Path(sys.argv[2])
im = Image.open(src).convert("RGB")
full = im.copy()
full.thumbnail((1200, 1200))
full.save(ROOT / "img" / "full" / f"{cid}.webp", "WEBP", quality=90, method=6)
small = im.copy()
small.thumbnail((480, 600))
small.save(ROOT / "img" / f"{cid}.webp", "WEBP", quality=85, method=6)
print(cid, full.size, small.size)
