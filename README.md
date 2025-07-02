# Substance Assets Downloader

This tool allows you to batch download Substance 3D materials from any collections using the official GraphQL endpoint. It handles authentication, checks for existing purchases, and organizes downloads into collection-named folders.

## Features

- Downloads assets from specified Adobe Substance collections
- Verifies and purchases assets if not already owned
- Only downloads materials in Substance format (.sbsar)
- Organizes files by collection name

## Requirements

- Access to the Adobe Substance Library (Adobe Subscription)
- Valid IMS session ID
- Collection ID