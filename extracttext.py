from PyPDF2 import PdfReader

reader = PdfReader("./100_Cases_in_Clinical_Medicine.pdf")

topics = ["History", "Examination", "ANSWER", "Questions", "KEY POINTS", "INVESTIGATIONS", "•"]

i = 0
j = 0
data = {}
for page in reader.pages[14:269]:
    text = page.extract_text()
    *topic, text = text.split("History")
    text = text.strip()

    if len(topic) > 0:
        topic = topic[0].strip()
        for t in "123456789:":
            topic = topic.replace(t, "")
        topic = list(filter(lambda x: x , topic.split(" ")))
        data[i] = {"topic": topic}
        print(i)
        j = i
        i += 1

    for t in topics:
        text = text.replace(t, "")
    text = ".".join([t for t in text.split(".") if len(t) > 15 and "Fig" not in t and "?" not in t])
    text = text.strip()
    while True:
        for t in "123456789":
            if text.startswith(t):
                text = text[1:]
                break
        else:
            break
        continue
    
    if data[j].get("content"):
        data[j]["content"] += " " + text
    else:
        data[j]["content"] = text

with open("data.json", "w", encoding="utf8") as f:
    import json
    json.dump(data, f, indent=4, ensure_ascii=False)