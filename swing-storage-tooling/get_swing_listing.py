import os

from supabase import create_client, Client
from dotenv import load_dotenv


load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
SUPABASE_BUCKET = os.getenv("SUPABASE_BUCKET")


def get_supabase_client() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def list_all_files(supabase, bucket, fp, path=""):
    def recurse(current_path):
        offset = 0
        limit = 100

        while True:
            response = supabase.storage.from_(bucket).list(
                current_path,
                {
                    "limit": limit,
                    "offset": offset,
                    "sortBy": {"column": "name", "order": "asc"},
                },
            )
            if not response:
                break

            for item in response:
                item_name = item['name']
                full_path = f"{current_path}/{item_name}" if current_path else item_name

                if item["metadata"] is None:  # this is a folder
                    recurse(full_path)
                else:
                    fp.write(f"{full_path}\n")

            if len(response) < limit:
                break
            offset += limit

    recurse(path)


def list_swing_folders(supabase, bucket, fp):
    offset = 0
    limit = 100
    while True:
        print(f"At offset {offset}")
        response = supabase.storage.from_(bucket).list(
            "",
            {
                "limit": limit,
                "offset": offset,
                "sortBy": {"column": "created_at", "order": "asc"},
            },
        )
        if not response:
            break

        for item in response:
            item_name = item['name']
            fp.write(f"{item_name}\n")

        if len(response) < limit:
            break
        offset += limit


def list_supabase_files(swing_listing):
    sb = get_supabase_client()
    with open(swing_listing, 'w') as fp:
        list_swing_folders(sb, SUPABASE_BUCKET, fp)


def main():
    swing_listing = "swing_listing.txt"
    list_supabase_files(swing_listing)


if __name__ == "__main__":
    main()
