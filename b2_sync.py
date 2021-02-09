from b2sdk.v1 import InMemoryAccountInfo, DownloadDestLocalFile, DoNothingProgressListener
from b2sdk.v1 import B2Api
from os import environ as env
from os import makedirs

# Retrieve all relevant credentials / info from environment
application_key_id = env['B2_APPLICATION_ID']
application_key = env['B2_APPLICATION_KEY']
application_realm = env['B2_APPLICATION_REALM']
bucket_name = env['B2_BUCKET_NAME']

# Authenticate using credentials
info = InMemoryAccountInfo()  # store credentials, tokens and cache in memory
b2_api = B2Api(info)
b2_api.authorize_account(application_realm, application_key_id, application_key)
bucket = b2_api.get_bucket_by_name(bucket_name)

subreddit_models_dir = 'subreddit-clfs'
directory_prefix = f'tmp/backend-ml/{subreddit_models_dir}'
makedirs(directory_prefix)

subreddits = \
[
  "Futurology",
  "science"
]

for subreddit in subreddits:
    for extension in [ ".vec", ".bin" ]:
        b2_filename = f'{subreddit_models_dir}/model_{subreddit}{extension}'
        local_file_path = f'{directory_prefix}/model_{subreddit}{extension}'
        download_dest = DownloadDestLocalFile(local_file_path)
        progress_listener = DoNothingProgressListener()
        bucket.download_file_by_name(b2_filename, download_dest, progress_listener)