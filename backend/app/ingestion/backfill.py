from app.ingestion.ingestion import ingest_meeting

dates = [
    '20260617',
    '20260429',
    '20260318',
    '20260128',
    '20251210',
    '20251029',
    '20250917',
    '20250822',
    '20250730',
    '20250618',
    '20250507',
    '20250319',
]

for date in dates:
    try:
        result = ingest_meeting(date)
        print(result)
    except Exception as e:
        print(f"Failed for {date}: {e}")
