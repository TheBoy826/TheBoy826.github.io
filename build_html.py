"""Generate standalone HTML quiz app with embedded question data."""
import json

# Load question bank
with open("questions.json", "r", encoding="utf-8") as f:
    bank = json.load(f)

# Build compact data structure
data = {
    "s": bank["single"],   # single choice
    "m": bank["multi"],    # multi choice
    "j": bank["judge"],    # judge
}

# Convert to compact JSON (no indent, no spaces)
json_str = json.dumps(data, ensure_ascii=False, separators=(",", ":"))

# Read the HTML template
with open("template.html", "r", encoding="utf-8") as f:
    template = f.read()

# Inject the data
output = template.replace("__DATA_PLACEHOLDER__", json_str)

# Write the standalone file
with open("毛中特刷题.html", "w", encoding="utf-8") as f:
    f.write(output)

# Stats
size_kb = len(output) / 1024
print(f"Generated 毛中特刷题.html ({size_kb:.0f} KB)")
print(f"  Single: {len(bank['single'])} questions")
print(f"  Multi: {len(bank['multi'])} questions")
print(f"  Judge: {len(bank['judge'])} questions")
print(f"  Total: {bank['counts']['total']} questions")
print("Done!")
