# Spotify Fix Deprecated (Relink liked songs)

Simple tool to replace "deprecated" (not available) albums/tracks with available ones

## Installation
```pip install -r pip_requirements.txt```

## Usage
Create an app in https://developer.spotify.com/dashboard/applications \
You can use any valid url for the redirect uri: `http://example.com/callback` \
Create `secrets.json` file
```json
{
	"spotify-api-clientid": "",
	"spotify-api-secret": "",
	"spotify-api-redirect_uri": ""
}
```

Run `main.py COUNTRY_CODE`
