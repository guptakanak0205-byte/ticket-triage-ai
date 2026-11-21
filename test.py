import pandas as pd

data = {
    "ticket": ["I was charged twice", "App keeps crashing", "Where is my order?"],
    "category": ["billing", "technical", "delivery"]
}

df = pd.DataFrame(data)
print(df)