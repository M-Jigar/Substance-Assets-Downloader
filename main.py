import httpx
import os
import ripper_functions
from config import OUTPUT_DIR, COLLECTION_IDS, IMS_SID, ASSET_TYPES

default_headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36",
            "Origin": "https://substance3d.adobe.com/",
            "Referer": "https://substance3d.adobe.com/",
}

session = httpx.Client()
session.headers.update(default_headers)
session.cookies.set("ims_sid", IMS_SID)


user_data = ripper_functions.get_user_data(session=session, ims_sid=IMS_SID)          # will also update session headers with the token
user_name = user_data['name']
user_id = user_data['userId']
access_token = user_data['access_token']
purchased_assets = user_data['purchased_assets']


if COLLECTION_IDS:
    for collection_index, collection_id in enumerate(COLLECTION_IDS, start=1):

        page = 0
        hasMore = True
        limit = 100     # 100 is max for the given API.

        while hasMore == True: 

            collection_data = ripper_functions.get_collection_data(session=session, collection_id=collection_id, page=page, limit=limit)

            collection_title = collection_data['collection_title']
            collection_total = collection_data['collection_total']
            collection_items = collection_data['collection_items']

            print(f"\n--------Collection {collection_index} of {len(COLLECTION_IDS)} | {collection_title} | Total: {collection_total} | Page {page} of {(collection_total + limit - 1) // limit}--------\n")

            for item_index, item in enumerate(collection_items, start=1):
                cumulative_index = page * limit + item_index
                
                asset_name = item['title']
                asset_id = item['id']
                asset_type = item['__typename']


                # Verifying Asset.
                if not ASSET_TYPES.get(asset_type, False):
                    print(f"[{asset_name}] is a [{asset_type}] which is not enabled to download in config.py")
                    continue

                # Purchasing Asset.
                if asset_id not in purchased_assets:
                    purchase_response = ripper_functions.purchase_asset(session=session , asset_id=asset_id)

                attachment_list = item['attachments']

                # Downloading Asset.
                for attachment in attachment_list:
                    if attachment and attachment["label"] == "Substance format":

                        mat_filename = attachment['filename']
                        mat_download_url = attachment['url']
                        mat_file_size = attachment['size']

                        file_path = os.path.join(OUTPUT_DIR, collection_title, mat_filename)
                        

                        # Skips the file its already downloaded.
                        if os.path.exists(file_path) and os.path.getsize(file_path) == mat_file_size:
                            print(f"Already exists, Skipped | {mat_filename}")
                            continue
                        else:
                            print(f"Downloading {cumulative_index}/{collection_total} | '{mat_filename}' | {asset_type} | size: {round(mat_file_size / (1024 * 1024), 2)} MB")
                            os.makedirs(os.path.dirname(file_path), exist_ok=True)

                        ripper_functions.download_attachment(
                            session=session,
                            url=mat_download_url,
                            token=access_token,

                            file_name=mat_filename,
                            file_path=file_path,
                            file_size=mat_file_size
                        )

            page += 1
            hasMore = collection_data['hasMore']

else:
    print("No collection ID provided! Please add atleast 1collection ID in 'config.py'.")


