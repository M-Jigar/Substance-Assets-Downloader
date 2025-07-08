import httpx
import os
from tqdm import tqdm

from constants import USER_QUERY, PURCHASE_QUERY, COLLECTION_QUERY




def error_handler_default(response: httpx.Response):

    msg = {
        400: "Bad request — possibly invalid payload or missing ID.",
        401: "Unauthorized — check your access token.",
        403: "Forbidden — token might lack permission.",
        404: "Not Found — the resource doesn't exist.",
        429: "Rate limited — slow down your requests.",
        500: "Internal Server Error — server is down.",
    }

    try:
        response.raise_for_status()
        return response.json()
    
    except httpx.HTTPStatusError as e:

        if response.status_code in msg:
            print(msg[response.status_code])

        else:
            print(response.text)

    except (httpx.RequestError, ValueError) as e:

        raise SystemExit(f"❌ Terminating: {e}")


def get_user_data(ims_sid: str) -> dict:

    url = "https://adobeid-na1.services.adobe.com/ims/check/v6/token?jslVersion=v2-v0.31.0-2-g1e8a8a8"

    payload = {
        "client_id": "substance-source",
        "scope": "account_type,openid,AdobeID,read_organizations",
    }

    cookies = {
        "ims_sid": ims_sid,
    }

    headers = {
        "Origin": "https://substance3d.adobe.com",
        "Referer": "https://substance3d.adobe.com/",
        "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
    }

    user_data = error_handler_default(httpx.post(url, headers=headers, cookies=cookies, data=payload))

    access_token = user_data['access_token']
    purchased_assets = get_user_assets(token=access_token)
    user_data["purchased_assets"] = purchased_assets
    
    return user_data

def get_user_assets(token: str) -> list:

    headers = {
        "Authorization": f"Bearer {token}",
    }
    
    payload = {
        "query": USER_QUERY,
    }

    user_query_json = error_handler_default(httpx.post('https://source-api.substance3d.com/beta/graphql', headers=headers, json=payload))

    # A list of already purchased assets by the user.
    purchased_assets = user_query_json['data']['account']['assetIds']

    return purchased_assets


def get_collection_data(collection_id: str, page: int, limit: int) -> dict:

    payload = {
    
        "variables": {
            "collectionId": collection_id,
            "limit": limit,
            "page": page,
        },

        "query": COLLECTION_QUERY,
    }

    collection_json = error_handler_default(httpx.post('https://source-api.substance3d.com/beta/graphql', json=payload))

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


def purchase_asset(token: str, asset_id: str) -> dict:

    headers = {
        "Authorization": f"Bearer {token}",
    }

    payload = {
        "operationName": "PurchaseAsset",
        "variables": {"assetId": asset_id},
        "query": PURCHASE_QUERY,
    }

    reponse = error_handler_default(httpx.post('https://source-api.substance3d.com/beta/graphql', headers=headers, json=payload))
    return reponse


def download_attachment(url: str, token: str, file_name: str, file_path: str, file_size: int) -> None:

    with httpx.stream('GET', f"{url}?accessToken={token}", follow_redirects=True) as download_response:
        download_response.raise_for_status()
        progress = tqdm(desc=file_name, total=file_size, unit='B', unit_scale=True, unit_divisor=1024, colour="green")  

        with open(file_path, "wb") as binaryfile:
            for chunk in download_response.iter_bytes(chunk_size=8192):
                binaryfile.write(chunk)
                progress.update(len(chunk))

    return None