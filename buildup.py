import os
import psycopg2
import re
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")

conn = psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD)
cursor = conn.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS files (
    id SERIAL PRIMARY KEY,
    file_path VARCHAR(255) NOT NULL
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS code_chunks (
    id SERIAL PRIMARY KEY,
    chunk_content TEXT NOT NULL,
    function_name VARCHAR(255),
    function_line INTEGER,
    file_id INTEGER REFERENCES files(id)
);
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS metadata (
    id SERIAL PRIMARY KEY,
    code_chunk_id INTEGER REFERENCES code_chunks(id),
    description TEXT NOT NULL
);
''')
conn.commit()

def get_functions(file_path):
    functions = []
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for idx, line in enumerate(lines):
            match = re.match(r'\s*def\s+(\w+)\s*\(', line)
            if match:
                functions.append({
                    'name': match.group(1),
                    'line_number': idx + 1
                })
    return functions

def get_file_paths(base_dir, relative_paths):
    return [os.path.join(base_dir, path) for path in relative_paths]

def write_header(out, file_path):
    base_name = os.path.basename(file_path)
    out.write(f"\n**{base_name}**\n\n```\n")

def main():
    file_paths = get_file_paths(BASE_DIR, FILE_RELATIVE_PATHS)
    create_codebase_transcript(file_paths, OUTPUT_FILE)
    print(f"Codebase transcript saved as {OUTPUT_FILE}")

def write_code_block(out, in_file):
    code_content = in_file.read()
    out.write(f"```python\n{code_content}\n```\n")

def create_codebase_transcript(file_paths, output_file):
    file_insert = "INSERT INTO files (file_path) VALUES (%s) RETURNING id;"
    code_chunk_insert = """INSERT INTO code_chunks (chunk_content, function_name, function_line, file_id)
                           VALUES (%s, %s, %s, %s);"""

    with open(output_file, "w", newline="\n") as out:
        with psycopg2.connect(host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD) as conn:
            with conn.cursor() as cursor:   
                for file_path in file_paths:
                    if not os.path.isfile(file_path) or file_path.endswith(".env"):
                        continue

                    write_header(out, file_path)

                    cursor.execute(file_insert, (os.path.abspath(file_path),))
                    file_id = cursor.fetchone()[0]

                    with open(file_path, "r", encoding="utf-8") as f:
                        file_content = f.read()
                        out.write(f"```python\n{file_content}\n```\n")
                        functions = get_functions(file_path)
                        for func in functions:
                            cursor.execute(code_chunk_insert, (file_content, func['name'], func['line_number'], file_id))

if __name__ == "__main__":
    BASE_DIR = "/Users/jamalelakrah/Documents/GitHub/Magical-Assistant"
    FILE_RELATIVE_PATHS = [
        'tests/test_chat_history_handler.py',
        'tests/test_chatbot.py',
        'tests/test_event_parser.py',
        'tests/test_integration.py',
        'tests/test_wondrouscalendar.py',
        'buildup.py',
        'chat_history_handler.py',
        'chatbot.py',
        'event_parser.py',
        'openai_integration.py',
        'sample.env',
        'wondrouscalendar.py'
    ]
    OUTPUT_FILE = "/Users/jamalelakrah/Documents/GitHub/Magical-Assistant/output.txt"
    file_paths = get_file_paths(BASE_DIR, FILE_RELATIVE_PATHS)
    create_codebase_transcript(file_paths, OUTPUT_FILE)
    print(f"Codebase transcript saved as {OUTPUT_FILE}")
