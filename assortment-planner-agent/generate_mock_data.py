import json
import random
from datetime import datetime, timedelta

CATEGORIES = ["Beverages", "Snacks", "Dairy", "Produce"]
PRODUCTS = [
    {"id": f"prod_{i+1}", "name": f"Product_{i+1}", "category": random.choice(CATEGORIES)}
    for i in range(50)
]

def generate_sales():
    sales_data = []
    for product in PRODUCTS:
        for day in range(30):
            date = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
            sales = random.randint(0, 20)
            sales_data.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "date": date,
                "units_sold": sales
            })
    return sales_data

def generate_returns():
    return_data = []
    for product in PRODUCTS:
        for day in range(30):
            date = (datetime.now() - timedelta(days=day)).strftime("%Y-%m-%d")
            returns = random.randint(0, 5)
            return_data.append({
                "product_id": product["id"],
                "product_name": product["name"],
                "category": product["category"],
                "date": date,
                "units_returned": returns
            })
    return return_data

if __name__ == "__main__":
    with open("mock_past_sales.json", "w") as f:
        json.dump(generate_sales(), f, indent=2)
    with open("mock_return_patterns.json", "w") as f:
        json.dump(generate_returns(), f, indent=2)

