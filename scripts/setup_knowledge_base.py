#!/usr/bin/env python3
"""Setup LabLens Knowledge Base"""

import argparse
import asyncio
import traceback

from dotenv import load_dotenv
from loguru import logger

from lablens.ingestion.knowledge_base import KnowledgeBaseBuilder

load_dotenv()


async def main() -> int | None:
    parser = argparse.ArgumentParser(description="Setup LabLens knowledge base")
    parser.add_argument(
        "--config", default="configs/default.yml", help="Config file path"
    )
    args = parser.parse_args()

    try:
        builder = KnowledgeBaseBuilder()
        await builder.build_from_config(args.config)

    except Exception as e:
        logger.error(f"Error: {e}")
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    exit(asyncio.run(main()))
