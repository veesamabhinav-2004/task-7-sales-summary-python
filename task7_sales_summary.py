import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Connect to database
conn = sqlite3.connect("sales_data.db")

# Step 2: Create sales table
conn.execute("""
CREATE TABLE IF NOT EXISTS sales (
    product TEXT,
    quantity INTEGER,
    price REAL
)
""")

# Step 3: Insert sample data
conn.execute("DELETE FROM sales")

conn.executemany("""
INSERT INTO sales (product, quantity, price)
VALUES (?, ?, ?)
""", [
    ("Laptop", 10, 800),
    ("Phone", 20, 500),
    ("Tablet", 15, 300),
    ("Headphones", 25, 100)
])

conn.commit()

# Step 4: Run SQL query
query = """
SELECT product,
       SUM(quantity) AS total_qty,
       SUM(quantity * price) AS revenue
FROM sales
GROUP BY product
"""

df = pd.read_sql_query(query, conn)

# Step 5: Print results
print("Sales Summary:")
print(df)

# Step 6: Create bar chart
df.plot(kind='bar', x='product', y='revenue')

plt.title("Revenue by Product")
plt.ylabel("Revenue")
plt.xlabel("Product")

# Step 7: Save chart
plt.savefig("sales_chart.png")

plt.show()

# Close connection
conn.close()