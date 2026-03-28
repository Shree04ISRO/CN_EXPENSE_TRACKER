def predict_category(text):
    text = text.lower()
    if "pizza" in text or "burger" in text or "food" in text or "biryani" in text or "grocery" in text or "restaurant" in text:
        return "Food"
    if "uber" in text or "bus" in text or "train" in text or "flight" in text or "travel" in text:
        return "Travel"
    if "amazon" in text or "dress" in text or "shirt" in text or "shopping" in text or "clothes" in text:
        return "Shopping"
    if "electricity" in text or "water" in text or "bill" in text or "internet" in text or "phone" in text:
        return "Bills"
    return "Other"
