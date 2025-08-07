# server2/server2.py

import Pyro5.api
import csv

@Pyro5.api.expose
class PITDServer:
    def __init__(self):
        self.pitd_db = self.load_csv_data("pitd_data.csv")
        print("Server-2: Successfully loaded PITD records from CSV.")

    def load_csv_data(self, filepath):
        db = {}
        try:
            with open(filepath, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    tfn = row['TFN'].strip()
                    record = {
                        "start": row['Period Start'],
                        "end": row['Period End'],
                        "gross": float(row['Gross']),
                        "withheld": float(row['Withheld']),
                        "net": float(row['Net'])
                    }
                    db.setdefault(tfn, []).append(record)
        except Exception as e:
            print("Error reading CSV file:", e)
        return db

    def get_tax_data(self, tfn):
        print(f"Server-2: Received TFN request: {tfn}")
        if tfn in self.pitd_db:
            return {"status": "success", "records": self.pitd_db[tfn]}
        else:
            return {"status": "error", "message": f"No records for TFN {tfn}"}

def main():
    daemon = Pyro5.server.Daemon(port=9091)
    uri = daemon.register(PITDServer(), objectId="pitd")
    print("Server-2 (Database Server) is ready.\nURI:", uri, "\n")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
