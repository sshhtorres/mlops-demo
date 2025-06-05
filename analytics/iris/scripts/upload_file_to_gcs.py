import pathlib

from google.cloud import storage

from .cli import parse_gcs_uri_dest, parse_dir_and_name


def upload_file_to_gcs(local_file: pathlib.Path, blob_uri: str):
    assert blob_uri.startswith("gs://")

    _, blob_path = blob_uri.split("gs://", 1)
    bucket_name, *blob_parts = blob_path.split("/")
    blob_name = "/".join(blob_parts)

    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.upload_from_filename(local_file)


if __name__ == "__main__":
    gcs_uri_dest = parse_gcs_uri_dest()
    local_file = parse_dir_and_name()

    blob_uri = f"{gcs_uri_dest.rstrip('/')}/{local_file.name}"
    upload_file_to_gcs(local_file, blob_uri)
    print(f'Uploaded "{local_file}" to "{blob_uri}"')
