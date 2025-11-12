

import os
from pathlib import Path


OLLAMA_URL = "http://localhost:11434/api/chat"
OLLAMA_MODEL_NAME = "llama3"


# Main dirs and file paths
PROJ_DIR = Path(os.path.abspath(__file__)).parent

DOCS_DIR = os.path.join(PROJ_DIR, "docs")
DOCS_SUMMARY_PATH = os.path.join(DOCS_DIR, "summary.csv")

RAG_DIR = os.path.join(PROJ_DIR, "rag")
RAG_EMBEDDING_PATH = os.path.join(RAG_DIR, "embedding.csv")


# Document dirs and paths
DOCS_BLOCKCHAIN_DIR = os.path.join(DOCS_DIR, "blockchain")
DOCS_BLOCKCHAIN_QUEUE_DIR = os.path.join(DOCS_BLOCKCHAIN_DIR, "queue")
DOCS_BLOCKCHAIN_COMPLETED_DIR = os.path.join(DOCS_BLOCKCHAIN_DIR, "completed")
DOCS_BLOCKCHAIN_REFERENCE_DIR = os.path.join(DOCS_BLOCKCHAIN_DIR, "reference")

DOCS_FINANCE_DIR = os.path.join(DOCS_DIR, "finance")
DOCS_FINANCE_QUEUE_DIR = os.path.join(DOCS_FINANCE_DIR, "queue")
DOCS_FINANCE_COMPLETED_DIR = os.path.join(DOCS_FINANCE_DIR, "completed")
DOCS_FINANCE_REFERENCE_DIR = os.path.join(DOCS_FINANCE_DIR, "reference")

DOCS_MACHINE_LEARNING_DIR = os.path.join(DOCS_DIR, "machine_learning")
DOCS_MACHINE_LEARNING_QUEUE_DIR = os.path.join(DOCS_MACHINE_LEARNING_DIR, "queue")
DOCS_MACHINE_LEARNING_COMPLETED_DIR = os.path.join(DOCS_MACHINE_LEARNING_DIR, "completed")
DOCS_MACHINE_LEARNING_REFERENCE_DIR = os.path.join(DOCS_MACHINE_LEARNING_DIR, "reference")

DOCS_STATISTICS_DIR = os.path.join(DOCS_DIR, "statistics")
DOCS_STATISTICS_QUEUE_DIR = os.path.join(DOCS_STATISTICS_DIR, "queue")
DOCS_STATISTICS_COMPLETED_DIR = os.path.join(DOCS_STATISTICS_DIR, "completed")
DOCS_STATISTICS_REFERENCE_DIR = os.path.join(DOCS_STATISTICS_DIR, "reference")

DOCS_MISC_DIR = os.path.join(DOCS_DIR, "misc")
DOCS_MISC_QUEUE_DIR = os.path.join(DOCS_MISC_DIR, "queue")
DOCS_MISC_COMPLETED_DIR = os.path.join(DOCS_MISC_DIR, "completed")
DOCS_MISC_REFERENCE_DIR = os.path.join(DOCS_MISC_DIR, "reference")

