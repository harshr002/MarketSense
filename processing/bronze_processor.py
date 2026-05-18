import uuid
from datetime import datetime, timezone


def add_bronze_metadata(records, source_type):
    """
    Adds data lineage and metadata to raw records.

    This makes Bronze layer production-like:
    - unique record tracking
    - pipeline traceability
    - source classification
    """

    enriched_records = []

    for record in records:
        enriched_record = dict(record)

        enriched_record["record_id"] = str(uuid.uuid4())
        enriched_record["layer"] = "bronze"
        enriched_record["source_type"] = source_type
        enriched_record["pipeline_timestamp"] = datetime.now(
            timezone.utc
        ).isoformat()

        enriched_records.append(enriched_record)

    return enriched_records