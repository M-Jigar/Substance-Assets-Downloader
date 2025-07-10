import httpx
from tqdm import tqdm

from constants import USER_QUERY, PURCHASE_QUERY, COLLECTION_QUERY




def error_handler_default(response: httpx.Response):

    try:
        response.raise_for_status()
        return response.json()
    
    except httpx.HTTPError as e:
        print(e)


def get_user_data(session: httpx.Client, ims_sid: str) -> dict:

    url = "https://adobeid-na1.services.adobe.com/ims/check/v6/token?jslVersion=v2-v0.31.0-2-g1e8a8a8"

    payload = {
        "client_id": "substance-source",
        "scope": "account_type,openid,AdobeID,read_organizations",
    }

    user_data = error_handler_default(session.post(url, data=payload))
    access_token = user_data['access_token']
    session.headers.update({"Authorization": f"Bearer {access_token}",})

    purchased_assets = get_user_assets(session=session)
    
    user_data["purchased_assets"] = purchased_assets
    
    return user_data

def get_user_assets(session: httpx.Client) -> list:

    payload = {
        "query": USER_QUERY,
    }

    user_query_json = error_handler_default(session.post('https://source-api.substance3d.com/beta/graphql', json=payload))

    purchased_assets = user_query_json['data']['account']['assetIds']

    return purchased_assets


def get_collection_data(session: httpx.Client, collection_id: str, page: int, limit: int) -> dict:

    payload = {
    
        "variables": {
            "collectionId": collection_id,
            "limit": limit,
            "page": page,
        },
        "query": COLLECTION_QUERY,
    }

    collection_json = error_handler_default(session.post('https://source-api.substance3d.com/beta/graphql', json=payload))

    collection_title = collection_json['data']['collection']['title']
    collection_total = collection_json['data']['collection']['assets']["total"]

    items_onPage = collection_json['data']['collection']['assets']["items"]
    hasMore: bool = collection_json['data']['collection']['assets']["hasMore"]

    collection_data = {
        "collection_title": collection_title,
        "collection_total": collection_total,
        "collection_items": items_onPage,
        "hasMore": hasMore,
    }

    return collection_data


def purchase_asset(session: httpx.Client, asset_id: str) -> dict:

    payload = {
        "operationName": "PurchaseAsset",
        "variables": {"assetId": asset_id},
        "query": PURCHASE_QUERY,
    }

    reponse = error_handler_default(session.post('https://source-api.substance3d.com/beta/graphql', json=payload))
    return reponse


def download_attachment(session: httpx.Client, url: str, token: str, file_name: str, file_path: str, file_size: int) -> None:

    with session.stream('GET', f"{url}?accessToken={token}", follow_redirects=True) as download_response:
        error_handler_default(download_response)
        
        progress = tqdm(desc=file_name, total=file_size, unit='B', unit_scale=True, unit_divisor=1024, colour="green")  

        with open(file_path, "wb") as binaryfile:
            for chunk in download_response.iter_bytes(chunk_size=8192):
                binaryfile.write(chunk)
                progress.update(len(chunk))

    return None