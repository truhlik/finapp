from storages.backends.gcloud import GoogleCloudStorage
from storages.utils import setting


class StaticFilesGoogleCloudStorage(GoogleCloudStorage):
    location = setting('GS_STATIC_LOCATION', '')
