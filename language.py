HINDI_WORDS = {
    "hai", "hain", "nahi", "nahin", "mera", "meri", "mujhe", "kya", "kab",
    "kaise", "kaha", "kahan", "karu", "karna", "karo", "chahiye", "aapka",
    "aapki", "paisa", "paise", "wapas", "abhi", "raha", "rahi", "gaya",
    "gaye", "kat", "bhej", "badalna", "batao", "jaldi", "saaman", "lekin",
}


def is_hinglish(text):
    words = text.lower().replace("?", " ").replace(",", " ").split()
    matches = sum(1 for w in words if w in HINDI_WORDS)
    return matches >= 2