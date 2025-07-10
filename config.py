OUTPUT_DIR = "./downloads"



# IMS session ID for authentication. 
# Find it in your browser by entering developer tools. 
# Navigate to Application > Cookies > https://substance3d.adobe.com/ and copy the value of ims_sid.

IMS_SID = "ENTER_YOUR_ID"



# Paste the ID of collections you want to download seperated by a comma
# You can find the collection ID from the collection url
# example 'https://substance3d.adobe.com/assets/collections/2fd11840b7955a9753fe52f01d334e960bf0698c' here, '2fd11840b7955a9753fe52f01d334e960bf0698c' is the collection ID.

COLLECTION_IDS = [
    '01d9222154f89ff925f08850ad98b32166226374',
]



# Set bool values (True or False) to enable or disable the type of assets to download from collection.

ASSET_TYPES = {
    "PainterSmartMaterial": True,
    "SubstanceMaterial": True,
    "SubstanceDecal": True,
}