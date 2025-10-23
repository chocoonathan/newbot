"""
encrypted database by method: NsDev (https://github.com/SenpaiSeeker/norsodikin)
_____: https://t.me/norsodikin
_____: https://t.me/FakeCodeX
yang ganti atau hapus kredit pantat nya bisulan tuju turunan
"""

import asyncio
import getpass
import json
import sys

import aiosqlite

from keyrings import CipherHandler

METHOD = "bytes"


async def decrypt_table(cursor, cipher, table, columns):
    result = []
    try:
        await cursor.execute(f"SELECT * FROM {table}")
        rows = await cursor.fetchall()
        if not rows:
            return []

        col_names = [d[0] for d in cursor.description]

        for row in rows:
            decrypted = {}
            for i, col in enumerate(col_names):
                val = row[i]

                if col in columns and isinstance(val, (str, bytes)) and val:
                    try:
                        dec_val = cipher.decrypt(val)

                        if str(dec_val).strip().isdigit():
                            decrypted[col] = int(dec_val)
                        else:
                            decrypted[col] = dec_val
                    except Exception:
                        try:
                            decrypted[col] = int(val)
                        except Exception:
                            val_str = str(val)
                            decrypted[col] = f"(gagal decrypt: {val_str[:40]}...)"
                else:
                    decrypted[col] = val
            result.append(decrypted)

    except Exception as e:
        print(f"⚠️ Gagal decrypt tabel {table}: {e}")
    return result


async def main():
    if len(sys.argv) < 3:
        print("❌ Usage: python3 _decrypt.py <input_db> <output_json>")
        sys.exit(1)
    try:
        encryption_key = getpass.getpass(prompt="Masukkan Kunci Enkripsi Database: ")
    except Exception as e:
        print(f"\n[ERROR] Tidak dapat membaca input kunci: {e}", file=sys.stderr)
        sys.exit(1)

    if not encryption_key:
        print("\n[ERROR] Kunci enkripsi tidak boleh kosong.", file=sys.stderr)
        sys.exit(1)

    db_path = sys.argv[1]
    out_file = sys.argv[2]

    cipher = CipherHandler(key=encryption_key, method=METHOD)

    async with aiosqlite.connect(db_path) as db:
        cursor = await db.cursor()

        targets = {
            "user_prefixes": ["prefix"],
            "floods": ["flood"],
            "variabel": ["vars"],
            "expired": ["expire_date"],
            "userdata": ["depan", "belakang", "username", "mention", "full"],
            "ubotdb": ["session_string"],
            "tokens": [
                "token",
                "owner",
                "created_at",
                "usage_count",
                "max_usage",
                "usage_history",
            ],
        }

        all_data = {}

        for table, cols in targets.items():
            print(f"🔹 Decrypting {table}...")
            all_data[table] = await decrypt_table(cursor, cipher, table, cols)

    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n✅ Selesai! Hasil decrypt disimpan di: {out_file}")


if __name__ == "__main__":
    asyncio.run(main())
