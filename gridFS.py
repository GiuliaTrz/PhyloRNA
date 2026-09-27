#!/usr/bin/env python3

import argparse
import logging
import mimetypes
import os
import sys
from pathlib import Path

from pymongo import MongoClient
from gridfs import GridFS


def configure_logging(verbose: bool):
    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def upload_directory(directory: Path, fs: GridFS):
    uploaded = 0
    failed = 0

    logging.info("Scansione directory: %s", directory)

    for path in sorted(directory.rglob("*")):
        if not path.is_file():
            continue

        rel_path = path.relative_to(directory)
        mime_type, _ = mimetypes.guess_type(path)

        logging.info("Caricamento: %s", rel_path)
        logging.debug("Percorso assoluto: %s", path)
        logging.debug("Dimensione: %d byte", path.stat().st_size)

        try:
            with path.open("rb") as f:
                file_id = fs.put(
                    f,
                    filename=path.name,
                    contentType=mime_type,
                    metadata={
                        "relative_path": str(rel_path),
                        "original_path": str(path),
                    },
                )

            logging.info(
                "OK - %s -> GridFS id=%s",
                rel_path,
                file_id,
            )
            uploaded += 1

        except Exception:
            logging.exception("Errore durante il caricamento di %s", rel_path)
            failed += 1

    logging.info("----------------------------------------")
    logging.info("Upload completato")
    logging.info("File caricati : %d", uploaded)
    logging.info("Errori        : %d", failed)


def main():
    parser = argparse.ArgumentParser(
        description="Carica ricorsivamente una directory su MongoDB GridFS."
    )

    parser.add_argument(
        "directory",
        help="Directory da caricare",
    )

    parser.add_argument(
        "--mongo-uri",
        default="mongodb://localhost:27017",
        help="URI MongoDB",
    )

    parser.add_argument(
        "--database",
        default="test",
        help="Database MongoDB",
    )

    parser.add_argument(
        "--bucket",
        default="fs",
        help="Bucket GridFS",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Abilita logging verboso",
    )

    args = parser.parse_args()

    configure_logging(args.verbose)

    directory = Path(args.directory)

    if not directory.exists():
        logging.error("La directory non esiste: %s", directory)
        sys.exit(1)

    if not directory.is_dir():
        logging.error("%s non Ã¨ una directory", directory)
        sys.exit(1)

    logging.info("Connessione a MongoDB...")
    logging.debug("URI: %s", args.mongo_uri)

    client = MongoClient(args.mongo_uri, tlsAllowInvalidCertificates=True)
    db = client[args.database]
    fs = GridFS(db, collection=args.bucket)

    logging.info("Database: %s", args.database)
    logging.info("Bucket: %s", args.bucket)

    upload_directory(directory, fs)


if __name__ == "__main__":
    main()