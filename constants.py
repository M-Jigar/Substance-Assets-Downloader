USER_QUERY = """query UserAssets {
  user {
    name
  }
  account {
    assetIds
  }
}
"""

PURCHASE_QUERY = """mutation PurchaseAsset($assetId: String!) {
  purchaseAsset(assetId: $assetId) {
    id
  }
}
"""

COLLECTION_QUERY = """query Collection($collectionId: String!, $page: Int, $limit: Int) {
  collection(id: $collectionId) {
    title
    assets(page: $page, limit: $limit) {
      total
      items {
        title
        id
        __typename
        attachments {
          ... on DownloadAttachment {
            id
            label
            filename
            url
            size
          }
        }
      }
      hasMore
    }
  }
}
"""