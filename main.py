import ripper_functions

from config import OUTPUT_DIR, COLLECTION_IDS, IMS_SID



# Getting User Data.
user_data = ripper_functions.get_user_data(ims_sid=IMS_SID)
user_name = user_data['name']
user_id = user_data['userId']
access_token = user_data['access_token']
purchased_assets = user_data['purchased_assets']


# Getting Collection data and Downloading the materials in it.
if COLLECTION_IDS:
    for collection_index, collection_id in enumerate(COLLECTION_IDS, start=1):

        collection_data = ripper_functions.get_collection_data(collection_id)

        collection_title = collection_data['collection_title']
        collection_items = collection_data['collection_items']
        collection_total = collection_data['collection_total']

        print(f"\n--------Collection {collection_index} of {len(COLLECTION_IDS)} | {collection_title} | Processing {collection_total} items.--------\n")

        for item_index, item in enumerate(collection_items, start=1):
            
            asset_name = item['title']
            asset_id = item['id']
            asset_type = item['__typename']

            if ripper_functions.verify_substanceMaterial(asset_type) is False:
                print(f"[{asset_name}] is a [{asset_type}] | NOT a Substance Material | Skipped")
                continue
            
            # Purchasing Asset.
            if asset_id not in purchased_assets:
                purchase_response = ripper_functions.purchase_asset(token=access_token, asset_id=asset_id)

            attachment_list = item['attachments']

            # Downloading Asset.
            for attachment in attachment_list:
                if attachment and attachment["label"] == "Substance format":

                    mat_filename = attachment['filename']
                    mat_download_url = attachment['url']
                    mat_file_size = attachment['size']
                    
                    print(f"Downloading {item_index}/{collection_total} | '{mat_filename}' | size: {round(mat_file_size / (1024 * 1024), 2)} MB")

                    ripper_functions.download_material(url=mat_download_url, token=access_token, output_dir=OUTPUT_DIR, folder_name=collection_title, file_name=mat_filename, file_size=mat_file_size)
else:
    print("No collection ID provided! Please add atleast 1collection ID in 'config.py'.")


