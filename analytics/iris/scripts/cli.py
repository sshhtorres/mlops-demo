import argparse
import pathlib


def parse_dir() -> pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", "-d", type=str, help="Destination directory")
    args, _ = parser.parse_known_args()
    dir_dest = args.dir if args.dir else "."

    return pathlib.Path(dir_dest)


def parse_dir_and_name() ->  pathlib.Path:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dir", '-d', type=str, default="", help="Destination directory")
    parser.add_argument("--name", '-n', type=str, default="", help="Name of the output file")

    args, _ = parser.parse_known_args()
    file_name = args.name if args.name[-5:] == ".onnx" else f"{args.name}.onnx"
    dir_dest = args.dir if args.dir else "."
    filepath = pathlib.Path(dir_dest, file_name)

    return filepath


def parse_gcs_uri_dest() -> str:
    parser = argparse.ArgumentParser(description="Parse a GCS URI")
    parser.add_argument("--gcs", type=str, required=True, help="GCS URI to parse")

    args, _ = parser.parse_known_args()
    gcs_uri_dest = args.gcs if args.gcs.startswith("gs://") else f"gs://{args.gcs}"

    return gcs_uri_dest
