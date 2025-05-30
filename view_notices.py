import sqlite3

# Connect to the database
conn = sqlite3.connect('notices.db')
cursor = conn.cursor()

# Get all notices
cursor.execute("SELECT * FROM notice")
notices = cursor.fetchall()

if notices:
    print("\nCurrent Notices in Database:")
    print("-" * 50)
    for notice in notices:
        print(f"ID: {notice[0]}")
        print(f"Title: {notice[1]}")
        print(f"Description: {notice[2]}")
        print(f"Image Path: {notice[3]}")
        print(f"Category: {notice[4]}")
        print(f"Created At: {notice[5]}")
        print(f"Expires At: {notice[6]}")
        print("-" * 50)
else:
    print("No notices found in the database.")

conn.close()
