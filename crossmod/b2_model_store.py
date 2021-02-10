from b2sdk.v1 import InMemoryAccountInfo, DownloadDestLocalFile, SimpleProgressListener
from b2sdk.v1 import B2Api
from os import environ as env
from os import makedirs, path

def b2_download_models():
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
    norm_models_dir = 'norm-clfs'
    directory_prefix = f'tmp/backend-ml/{subreddit_models_dir}'
    for directory in [ subreddit_models_dir, norm_models_dir ]:
        full_directory = path.join(directory_prefix, directory)
        if not path.exists(full_directory):
            makedirs(full_directory)

    subreddits = \
    [
      "Futurology",
      "science"
    ]

    for subreddit in subreddits:
        for extension in [ ".vec", ".bin" ]:
            b2_filename = f'{subreddit_models_dir}/model_{subreddit}{extension}'
            local_file_path = f'{directory_prefix}/model_{subreddit}{extension}'
            if path.exists(local_file_path):
                print(f'Model {extension} for subreddit {subreddit} exists!')
                continue
            download_dest = DownloadDestLocalFile(local_file_path)
            progress_listener = SimpleProgressListener(f'Downloading model: model_{subreddit}{extension}')
            bucket.download_file_by_name(b2_filename, download_dest, progress_listener)

#def b2_download_models():
#    # Retrieve all relevant credentials / info from environment
#    application_key_id = CrossmodConsts.B2_APPLICATION_ID
#    application_key = CrossmodConsts.B2_APPLICATION_KEY
#    application_realm = CrossmodConsts.B2_APPLICATION_REALM
#    bucket_name = CrossmodConsts.B2_BUCKET_NAME
#
#    # Authenticate using credentials
#    info = InMemoryAccountInfo()  # store credentials, tokens and cache in memory
#    b2_api = B2Api(info)
#    b2_api.authorize_account(application_realm, application_key_id, application_key)
#    bucket = b2_api.get_bucket_by_name(bucket_name)
#
#    subreddit_models_dir = 'subreddit-clfs'
#    directory_prefix = os.path.join(CrossmodConsts.MODELS_DIRECTORY, subreddit_models_dir)
#    if not path.exists(directory_prefix):
#        makedirs(directory_prefix)
#
#    subreddits = \
#    [
#      "Futurology",
#      "science"
#    ]
#
#    for subreddit in subreddits:
#        for extension in [ ".vec", ".bin" ]:
#            b2_filename = f'{subreddit_models_dir}/model_{subreddit}{extension}'
#            local_file_path = f'{directory_prefix}/model_{subreddit}{extension}'
#            if path.exists(local_file_path):
#                print(f'Model {extension} for subreddit {subreddit} exists!')
#                continue
#            download_dest = DownloadDestLocalFile(local_file_path)
#            progress_listener = SimpleProgressListener()
#            bucket.download_file_by_name(b2_filename, download_dest, progress_listener)
#

if __name__ == '__main__':
    b2_download_models()