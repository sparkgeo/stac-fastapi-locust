"""Database ingestion script."""
import json
import os

import click
import requests
from pystac import Catalog
import shutil
from tempfile import TemporaryDirectory

DEFAULT_SOURCE = os.path.join(
    os.path.dirname(__file__), "setup_data", "collection.json"
)
STAC_API_BASE_URL = "http://localhost:8083"


def parse_source(source, tmp_dir):
    try:
        shutil.unpack_archive(source, tmp_dir)
        fpath_catalog = os.path.join(tmp_dir, "catalog.json")
        fpath_collection = os.path.join(tmp_dir, "collection.json")

        if os.path.exists(fpath_catalog):
            return fpath_catalog
        elif os.path.exists(fpath_collection):
            return fpath_collection
        else:
            err_msg = "No catalog.json or collection.json found."
            click.secho(err_msg)
            raise ValueError(err_msg)

    except ValueError:
        # If file type isn't compressed file
        if os.path.splitext(source)[1].lower() == ".json":
            return source
        else:
            err_msg = "JSON or compressed file required."
            click.secho(err_msg)
            raise ValueError(err_msg)


def ingest_object(object):
    if object.STAC_OBJECT_TYPE == "Catalog":
        url = f"{STAC_API_BASE_URL}"
    elif object.STAC_OBJECT_TYPE == "Collection":
        url = f"{STAC_API_BASE_URL}/collections"
    elif object.STAC_OBJECT_TYPE == "Feature":
        url = f"{STAC_API_BASE_URL}/collections/{object.collection_id}/items"

    try:
        resp = requests.post(url, json=object.to_dict())
        if resp.status_code == 200:
            print(f"Status code: {resp.status_code}")
            print(f"Added {object.STAC_OBJECT_TYPE}: {object.id}")
        elif resp.status_code == 409:
            print(f"Status code: {resp.status_code}")
            print(f"{object.STAC_OBJECT_TYPE}: {object.id} already exists")
    except requests.ConnectionError:
        click.secho("Failed to connect.")


@click.command()
@click.argument("source", default=DEFAULT_SOURCE)
def ingest(source):
    """Ingest source STAC into the database."""
    with TemporaryDirectory() as tmp_dir:
        stac_path = parse_source(source, tmp_dir)

        root_catalog = Catalog.from_file(stac_path)
        ingest_object(root_catalog)

        # TODO check if this ingests child catalogs too
        for collection in root_catalog.get_collections():
            ingest_object(collection)

        for item in root_catalog.get_all_items():
            ingest_object(item)
