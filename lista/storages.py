from storages.backends.s3boto3 import S3Boto3Storage


class ResolutionStorage(S3Boto3Storage):
   location = 'Plantillas Bases'
   default_acl = 'private'
   file_overwrite = True