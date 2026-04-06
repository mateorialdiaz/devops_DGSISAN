import os
import pymysql

def load_categories():
    with open("categories.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main():
    conn = pymysql.connect(
        host=os.environ["HESK_DB_HOST"],
        user=os.environ["HESK_DB_USER"],
        password=os.environ["HESK_DB_PASSWORD"],
        database=os.environ["HESK_DB_NAME"],
        port=int(os.environ.get("HESK_DB_PORT", 3306))
    )

    categories = load_categories()

    with conn.cursor() as cursor:
        for cat in categories:
            cursor.execute(
                "SELECT id FROM hesk_categories WHERE name = %s",
                (cat,)
            )
            exists = cursor.fetchone()

            if exists:
                print(f"[SKIP] Ya existe: {cat}")
            else:
                cursor.execute(
                    "INSERT INTO hesk_categories (name) VALUES (%s)",
                    (cat,)
                )
                print(f"[CREATE] Creada: {cat}")

    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()