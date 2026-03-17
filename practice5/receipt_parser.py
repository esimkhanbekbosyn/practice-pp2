import re
import json
with open("raw.txt", "r", encoding="utf-8") as file:
    text = file.read()

datetime_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4})\s+(\d{2}:\d{2}:\d{2})", text)
date = datetime_match.group(1) if datetime_match else "Not found"
time = datetime_match.group(2) if datetime_match else "Not found"

payment_match = re.search(r"(Банковская карта|Наличные|Карта)", text)
payment_method = payment_match.group(1) if payment_match else "Not found"

total_match = re.search(r"ИТОГО:\s*\n\s*([\d ]+,\d{2})", text)
if total_match:
    total_amount = total_match.group(1).replace(" ", "")
else:
    total_amount = "Not found"

products = []
pattern = r"\d+\.\s*\n(.+?)\n\d+,\d{3}\s*x\s*[\d ]+,\d{2}\n([\d ]+,\d{2})"
matches = re.findall(pattern, text)
for name, cost in matches:
    products.append({
        "name": " ".join(name.split()),
        "cost": cost.replace(" ", "")
    })
result = {
    "date": date,
    "time": time,
    "payment_method": payment_method,
    "total_amount": total_amount,
    "products": products
}
print(json.dumps(result, indent=4, ensure_ascii=False))