
import hashlib
import json
import uuid

from pathlib import Path

from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma

from config import DATA_DIR, CHROMA_DIR
from embeddings.embedding_model import get_embedding_model


MANIFEST_PATH = Path(".ingestion_manifest.json")

SUPPORTED_EXTENSIONS = {".pdf", ".txt"}


def calculate_hash(file_path):
    """Generate SHA-256 hash for a document."""

    sha = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(8192), b""):
            sha.update(chunk)

    return sha.hexdigest()


def load_manifest():
    if MANIFEST_PATH.exists():
        with open(MANIFEST_PATH, "r", encoding="utf-8") as f:
            return json.load(f)

    return {}


def save_manifest(manifest):
    with open(MANIFEST_PATH, "w", encoding="utf-8") as f:
        json.dump(manifest, f, indent=4)


def load_document(file_path):
    if file_path.suffix.lower() == ".pdf":
        return PyPDFLoader(str(file_path)).load()

    if file_path.suffix.lower() == ".txt":
        return TextLoader(
            str(file_path),
            encoding="utf-8"
        ).load()

    return []


def delete_document_chunks(vectorstore, source):
    """Delete all chunks belonging to a document."""

    result = vectorstore.get(
        where={"source": source}
    )

    ids = result.get("ids", [])

    if ids:
        vectorstore.delete(ids=ids)
        print(f"Removed {len(ids)} old chunks: {source}")


def main():

    data_path = Path(DATA_DIR).resolve()
    data_path.mkdir(parents=True, exist_ok=True)

    Path(CHROMA_DIR).mkdir(parents=True, exist_ok=True)

    manifest = load_manifest()

    print("\nInitializing embedding model...")

    embeddings = get_embedding_model()

    vectorstore = Chroma(
        collection_name="rag_documents",
        persist_directory=CHROMA_DIR,
        embedding_function=embeddings
    )

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150
    )

    current_files = {
        str(path.relative_to(data_path))
        for path in data_path.rglob("*")
        if path.is_file()
        and path.suffix.lower() in SUPPORTED_EXTENSIONS
    }

    # Remove chunks for files that no longer exist.
    deleted_files = set(manifest.keys()) - current_files

    for source in deleted_files:
        delete_document_chunks(vectorstore, source)
        del manifest[source]

    new_count = 0
    skipped_count = 0
    updated_count = 0

    for file_path in data_path.rglob("*"):

        if not file_path.is_file():
            continue

        if file_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        source = str(file_path.relative_to(data_path))
        current_hash = calculate_hash(file_path)

        # Skip unchanged documents.
        if manifest.get(source) == current_hash:
            print(f"SKIPPED: {source}")
            skipped_count += 1
            continue

        is_update = source in manifest

        if is_update:
            print(f"UPDATED: {source}")
            delete_document_chunks(vectorstore, source)
            updated_count += 1
        else:
            print(f"NEW DOCUMENT: {source}")
            new_count += 1

        # Load and split the document.
        documents = load_document(file_path)
        chunks = splitter.split_documents(documents)

        if not chunks:
            print(f"No text chunks found: {source}")
            manifest[source] = current_hash
            continue

        # Store a consistent source path in metadata.
        for chunk in chunks:
            chunk.metadata["source"] = source

        # Generate deterministic IDs for each chunk.
        ids = [
            str(uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"{source}:{current_hash}:{index}"
            ))
            for index in range(len(chunks))
        ]

        # Generate embeddings and insert into ChromaDB.
        vectorstore.add_documents(
            documents=chunks,
            ids=ids
        )

        manifest[source] = current_hash

        print(f"Embedded {len(chunks)} chunks: {source}")

        save_manifest(manifest)

    save_manifest(manifest)

    print("\n========== INGESTION SUMMARY ==========")
    print(f"New documents: {new_count}")
    print(f"Updated documents: {updated_count}")
    print(f"Skipped documents: {skipped_count}")
    print(f"Deleted documents: {len(deleted_files)}")
    print("Knowledge base synchronization complete!")


if __name__ == "__main__":
    main()
