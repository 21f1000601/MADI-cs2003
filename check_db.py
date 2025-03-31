import sqlite3

# Connect to your SQLite database
conn = sqlite3.connect('instance/fix_it_db.sqlite3')
cursor = conn.cursor()

# Retrieve all table names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

total_relationships = 0

for table in tables:
    table_name = table[0]
    cursor.execute(f"PRAGMA foreign_key_list('{table_name}');")
    foreign_keys = cursor.fetchall()
    print(f"Table: {table_name}, Relationships: {len(foreign_keys)}")
    for fk in foreign_keys:
        # Each row from PRAGMA foreign_key_list returns:
        # id, seq, ref_table, from_column, to_column, on_update, on_delete, match
        fk_id, fk_seq, ref_table, from_column, to_column, on_update, on_delete, match = fk
        
        # Construct a descriptive relationship name based on details
        relationship_name = f"FK_{table_name}_{from_column}_to_{ref_table}_{to_column}"
        print(f"  - Relationship Name: {relationship_name}")
        print(f"    Details: From column '{from_column}' in table '{table_name}' " +
              f"references column '{to_column}' in table '{ref_table}' " +
              f"(on update: {on_update}, on delete: {on_delete}, match: {match})")
    
    total_relationships += len(foreign_keys)
    print()  # Blank line for clarity between tables

print("Total Relationships in Database:", total_relationships)

conn.close()
