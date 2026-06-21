import csv
import random
from datetime import datetime, timedelta

products = [
    ("P001", "Laptop", "Electronics", 899.99),
    ("P002", "Smartphone", "Electronics", 699.99),
    ("P003", "Headphones", "Electronics", 149.99),
    ("P004", "Running Shoes", "Footwear", 89.99),
    ("P005", "T-Shirt", "Clothing", 29.99),
    ("P006", "Jeans", "Clothing", 59.99),
    ("P007", "Coffee Maker", "Appliances", 79.99),
    ("P008", "Blender", "Appliances", 49.99),
    ("P009", "Novel Book", "Books", 14.99),
    ("P010", "Textbook", "Books", 79.99),
    ("P011", "Sofa", "Furniture", 599.99),
    ("P012", "Office Chair", "Furniture", 249.99),
    ("P013", "Face Cream", "Beauty", 34.99),
    ("P014", "Shampoo", "Beauty", 12.99),
    ("P015", "Yoga Mat", "Sports", 39.99),
]

cities = [
    ("Karachi", "Sindh"),
    ("Lahore", "Punjab"),
    ("Islamabad", "Federal"),
    ("Peshawar", "KPK"),
    ("Quetta", "Balochistan"),
    ("Multan", "Punjab"),
    ("Faisalabad", "Punjab"),
    ("Rawalpindi", "Punjab"),
]

start_date = datetime(2023, 1, 1)

with open("ecommerce_data.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([
        "order_id", "product_id", "product_name", "category",
        "price", "quantity", "total_amount", "city", "province",
        "order_date", "customer_id"
    ])
    
    for i in range(1, 10001):
        product = random.choice(products)
        city_info = random.choice(cities)
        quantity = random.randint(1, 5)
        total = round(product[3] * quantity, 2)
        order_date = start_date + timedelta(days=random.randint(0, 364))
        
        writer.writerow([
            f"ORD{i:05d}",
            product[0],
            product[1],
            product[2],
            product[3],
            quantity,
            total,
            city_info[0],
            city_info[1],
            order_date.strftime("%Y-%m-%d"),
            f"CUST{random.randint(1000, 9999)}"
        ])

print("Dataset generated: ecommerce_data.csv")
print("Total records: 10,000")
