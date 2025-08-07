# server2/pitd_db.py

# Simulated PITD database for 2 TFN users (up to 26 records each)
PITD_DB = {
    "33142123": [  # TFN
        {"start": "2024-07-01", "end": "2024-07-14", "gross": 3000, "withheld": 600, "net": 2400},
        {"start": "2024-07-15", "end": "2024-07-28", "gross": 3100, "withheld": 620, "net": 2480}
    ],
    "88881234": [
        {"start": "2024-07-01", "end": "2024-07-14", "gross": 4000, "withheld": 800, "net": 3200}
    ]
}
