# basic_upload_googleplay
basic python script for upload apk and obb file to google play market (primary for alpha group)

# Usage:

1. pip install google-api-python-client httplib2

2. Execute the script

```bash
  $ python upload_apks_to_google_play_console.py service_account_email key_p12_file_path track apk_file_path obb_file_path

  service_account_email - XXXXXXXX-YYYYYYYYYYYYYY@developer.gserviceaccount.com
  key_p12_file_path - Key from google developer console
  track - The track. Can be "alpha", "beta", "production"
  apk_file_path - path to apk file
  obb_file_path - path to obb file, in this version must have "bin" extension
