from pathlib import Path
import unicodedata

root = Path("C:/Users/43106789808/Desktop/Henry/Fuga do Museu")
updated = 0
for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8")
    cleaned = "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(ch)
    )
    if cleaned != text:
        path.write_text(cleaned, encoding="utf-8")
        updated += 1

remaining = []
for path in root.rglob("*.py"):
    text = path.read_text(encoding="utf-8")
    bad = sorted({ch for ch in text if ord(ch) > 127})
    if bad:
        remaining.append((str(path), " ".join(f"U+{ord(ch):04X}" for ch in bad)))

print(f"updated={updated}")
print(f"remaining_non_ascii={len(remaining)}")
for path, chars in remaining:
    print(path)
    print(chars)
