from storages.backends.s3boto3 import S3Boto3Storage

class StaticStorage(S3Boto3Storage):
    bucket_name = 'bootshaus-id-storage'
    custom_domain = '{}.nyc3.digitaloceanspaces.com'.format(bucket_name)
    location = 'static'

class MediaStorage(S3Boto3Storage):
    bucket_name = 'bootshaus-id-storage'
    custom_domain = '{}.nyc3.digitaloceanspaces.com'.format(bucket_name)
    location = 'media'

