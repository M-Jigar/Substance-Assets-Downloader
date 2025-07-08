OUTPUT_DIR = "./downloads"



# IMS session ID for authentication. 
# Find it in your browser by entering developer tools. 
# Navigate to Application > Cookies > https://substance3d.adobe.com/ and copy the value of ims_sid.

IMS_SID = "AdyypZEpmB4BzMwhbSwR2m3EQ_1FF7qyjWb39HPI-D0ODlAaiJ-3tWlaAgTbBVpZ_5CW7L7UeNb6CIbkjC3sIAYyg49mHADlCGXgWYgqoxrdovwuwqfEc3k9UfvXSVI16Hcn3z7x7nNBHIsDWEcgn0IGqJflue_kSq7hh1ILmb4rma4T7DQhXKzhHHIq-WleXo516wFHZ3BNyjZy60NMeHFOOX01qbZ-965VeOqRA1B1cCYsTlLVn5JKw-9IDK8tAqgCLOUsqxpyLvbkeKJ3vja2pByBizQo_zEmEL2wz5DsOzOvYQ16Eash5F_u581elYEFKZc_0KcWQzToYbeCY5emu_YfN87TgWe7yVAxPc9-eVynB2MjQN3aVgeAlUATUkRT0bqexT_Zo0Ue_lUVjrA3ETFN9W-cY-o65hBeS9aF5hG-uoz_ohqey0ts2CgmBTKJv7QsejL9q16YJu0HaEU_vZ1LmvmgoJmUEepWhLDAsFDmjME7dOtef5HC6qgGLF91mqnwe27hAotufSpaOVMAwHqZxjafNDMrxExp603JyqCoJEW9tFvCRznLWpdttgDSJaJ74qAtrOEN_QBxOqKQAs6ssbrR94zvqe9cfbeE9O-YuquJ3rJ7RWJCXCfAtQ3k9a1Pl1IHhVgD-pi4XtJYOw1ra2oHjk0LHxZGs2qzcFTt3X2X2oiXfraRD7WyrpHfClGiyCjgo6K5HJHs-Eqfodzo48NRMcTO7yh_-hLrJhRMzTmo08cnPsUdGRW4jNuHwN0h67I00gX94UK63-nQ9x4tFBGfON1_0n0sCR0A"



# Paste the ID of collections you want to download seperated by a comma
# You can find the collection ID from the collection url
# example 'https://substance3d.adobe.com/assets/collections/2fd11840b7955a9753fe52f01d334e960bf0698c' here, '2fd11840b7955a9753fe52f01d334e960bf0698c' is the collection ID.

COLLECTION_IDS = [
    'bac94086effea4e07d524b7d21b64e97b9e6e898',
    'a7bb967d6f68b1e2f7b9c8b4c60a627dfa250e2d',
    'e039c54d826416600297924a253ee6c8a12f90d2',
    'fe17f5c9f94a90699beac7ad841ab6fb90bcee04',
    '4e374faf127c44d614a98d364434013f6a2b20d6',
    '412a9bc79631db04de250ad6d9309e9d4ace40d5',
    '67ec8edad3852aecbb2cf35c9a62d9760713b2d3',
    '60befc2831536916527546b8c13176c77eca3ce9',
    'a0b7b9aa84b448b483c51aba07d57d652fbfeb94',
    '01d9222154f89ff925f08850ad98b32166226374',
]



# Set bool values (True or False) to enable or disable the type of assets to download from collection.

ASSET_TYPES = {
    "PainterSmartMaterial": True,
    "SubstanceMaterial": True,
    "SubstanceDecal": True,
}