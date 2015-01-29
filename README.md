# basic_upload_googleplay
basic python script for upload apk and obb file to google play market (primary for alpha group)

# Usage:

1. [pip](https://pip.pypa.io/en/latest/installing.html) install google-api-python-client httplib2 PyOpenSSL

2. Execute the script

  $ python upload_apks_to_google_play_console.py path_to_folder_with_apks [--recursive] service_account package_name [obb_postfix] [track] [key_file]

  * path_to_folder_with_apks - path to folder with apk/obb files
  * service_account_email - xxxxxxxxxxxx-yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy@developer.gserviceaccount.com
  * package_name - app package name
  * obb_postfix - postfix to search for obb files - for apk file takes its basename without extension and append this postfix, if the file exists it upload as obb file. By default "main.obb"
  * track - the track. Can be "alpha", "beta", "production". By default is "alpha"
  * key_file - the path to p12 credentials key. By default is "key.p12"

# TODO:

* Take package_name from apk file??