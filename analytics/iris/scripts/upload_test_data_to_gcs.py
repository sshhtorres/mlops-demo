import pathlib

from google.cloud import storage

from .cli import parse_gcs_uri_dest, parse_dir
from .data import X_TEST_DATA_FILE_NAME, Y_TEST_DATA_FILE_NAME
from .upload_file_to_gcs import upload_file_to_gcs


def upload_test_data_to_gcs(local_data_dir, gcs_uri_dest):
    for file_name in [X_TEST_DATA_FILE_NAME, Y_TEST_DATA_FILE_NAME]:
        filepath = pathlib.Path(local_data_dir) / file_name
        blob_uri = f"{gcs_uri_dest.rstrip('/')}/{file_name}"
        upload_file_to_gcs(filepath, blob_uri)


if __name__ == "__main__":
    data_dir = parse_dir()
    gcs_uri_dest = parse_gcs_uri_dest()
    upload_test_data_to_gcs(data_dir, gcs_uri_dest)
    print(f'Uploaded data files from "{data_dir}" to "{gcs_uri_dest}"')
