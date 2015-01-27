#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Uploads an apk to the alpha track."""

import argparse
import sys
import httplib2
from apiclient.discovery import build
from oauth2client import client

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('service_account',
                       help='The service account email. Example: XXXXXXXX-YYYYYYYYYYYYYY@developer.gserviceaccount.com')
argparser.add_argument('key_file',
                       help='The path to p12 credentials key. Example: key.p12')
argparser.add_argument('track',
                       help='The track. Can be "alpha", "beta", "production"')
argparser.add_argument('package_name',
                       help='The package name. Example: com.android.sample')
argparser.add_argument('apk_file',
                       nargs='?',
                       help='The path to the APK file to upload.')
argparser.add_argument('obb_file',
                       nargs='?',
                       help='The path to the OBB file to upload. MUST have bin extention!!!')


def main(argv):
  flags = argparser.parse_args()

  # Process flags and read their values.
  package_name = flags.package_name
  apk_file = flags.apk_file
  obb_file = flags.obb_file
  key_file = flags.key_file
  service_account = flags.service_account
  track_name = flags.track

  # Load the key in PKCS 12 format that you downloaded from the Google APIs
  # Console when you created your Service account.
  f = file(key_file, 'rb')
  key = f.read()
  f.close()

  # Create an httplib2.Http object to handle our HTTP requests and authorize it
  # with the Credentials. Note that the first parameter, service_account_name,
  # is the Email address created for the Service account. It must be the email
  # address associated with the key that was created.
  credentials = client.SignedJwtAssertionCredentials(
    service_account,
    key,
    scope='https://www.googleapis.com/auth/androidpublisher')
  http = httplib2.Http()
  http = credentials.authorize(http)

  service = build('androidpublisher', 'v2', http=http)

  try:
    edit_request = service.edits().insert(body={}, packageName=package_name)
    result = edit_request.execute()
    edit_id = result['id']

    print 'Start uploading %s' % apk_file

    apk_response = service.edits().apks().upload(
        editId=edit_id,
        packageName=package_name,
        media_body=apk_file).execute()
    print 'APK with version code %d has been uploaded' % apk_response['versionCode']

    print 'Start uploading %s' % obb_file
    obb_response = service.edits().expansionfiles().upload(
        apkVersionCode=apk_response['versionCode'],
        expansionFileType='main',
        editId=edit_id,
        packageName=package_name,
        media_body=obb_file).execute()

    print 'OBB %s has been uploaded' % obb_response['expansionFile']

    track_response = service.edits().tracks().update(
        editId=edit_id,
        track=track_name,
        packageName=package_name,
        body={u'versionCodes': [apk_response['versionCode']]}).execute()

    print 'Track %s is set for version code(s) %s' % (
        track_response['track'], str(track_response['versionCodes']))

    commit_request = service.edits().commit(
        editId=edit_id, packageName=package_name).execute()

    print 'Edit "%s" has been committed' % (commit_request['id'])

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
