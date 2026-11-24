"""發布前檢查：img/ 底下只准 WebP，頁面小圖寬不超過 480；characters.json 每個角色的圖都要存在、三種台詞都要有。
不合格就以退出碼 1 結束（CI 會擋）。用法：python3 tools/check.py"""
import json, sys
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
bad = []
for p in (ROOT / "img").rglob("*"):
    if p.is_file() and p.suffix.lower() != ".webp":
        bad.append(f"不是 WebP：{p.relative_to(ROOT)}")
for p in (ROOT / "img").glob("*.webp"):
    if Image.open(p).width > 480:
        bad.append(f"頁面小圖太寬：{p.name}")
data = json.loads((ROOT / "characters.json").read_text("utf-8"))
for c in data["characters"]:
    for f in (f"img/{c['id']}.webp", f"img/full/{c['id']}.webp"):
        if not (ROOT / f).exists():
            bad.append(f"{c['name']} 缺圖：{f}")
    for k in ("greet", "happy", "unhappy"):
        if not c["lines"].get(k):
            bad.append(f"{c['name']} 缺台詞：{k}")
print("\n".join(bad) or f"通過：{len(data['characters'])} 個角色")
sys.exit(1 if bad else 0)
