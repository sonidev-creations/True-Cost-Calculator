import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "truecost.db")

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print("\n===== CALCULATIONS TABLE =====")
cursor.execute("SELECT id, product_name, price_usd, verdict, savings, created_at FROM calculations")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"ID:{row[0]} | {row[1]} | ${row[2]} | {row[3]} | savings:{row[4]} | {row[5]}")
else:
    print("No data yet — search a product first!")

print("\n===== HS SEARCH LOG =====")
cursor.execute("SELECT id, search_query, matched_hs_code, matched_desc, created_at FROM hs_search_log")
rows = cursor.fetchall()
if rows:
    for row in rows:
        print(f"ID:{row[0]} | {row[1]} | HS:{row[2]} | {row[3]} | {row[4]}")
else:
    print("No data yet — search a product first!")

conn.close()