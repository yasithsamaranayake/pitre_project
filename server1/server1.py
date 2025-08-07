# server1/server1.py

import sys
import os
import Pyro5.api

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from shared.estimator_interface import Estimator

@Pyro5.api.expose
@Pyro5.api.expose
class EstimatorServer(Estimator):
    def estimate_tax_return(self, person_id, data_list, has_phic, tfn=None, name=None, email=None, server2_uri=None):
        if tfn:
            print(f"Server-1: Connecting to Server-2 using URI: {server2_uri}")
            pitd = Pyro5.api.Proxy(server2_uri)
            response = pitd.get_tax_data(tfn)
            if response["status"] == "error":
                return {"message": response["message"]}
            records = response["records"]
            data_list = [{"income": r["gross"], "withheld": r["withheld"]} for r in records]

        total_income = sum(entry['income'] for entry in data_list)
        total_withheld = sum(entry['withheld'] for entry in data_list)
        net_income = total_income - total_withheld
        tax = self.calculate_basic_tax(total_income)
        ml = total_income * 0.02
        mls = self.calculate_mls(total_income, has_phic)
        refund = total_income - net_income - tax - ml - mls

        result = {
            "person_id": person_id,
            "annual_income": total_income,
            "total_withheld": total_withheld,
            "net_income": net_income,
            "medicare_levy": ml,
            "mls": mls,
            "refund_or_payable": refund,
            "message": "Success"
        }
        if tfn:
            result["tfn"] = tfn
        return result

    def calculate_basic_tax(self, income):
        if income <= 18200:
            return 0
        elif income <= 45000:
            return 0.19 * (income - 18200)
        elif income <= 120000:
            return 5092 + 0.325 * (income - 45000)
        elif income <= 180000:
            return 29467 + 0.37 * (income - 120000)
        else:
            return 51667 + 0.45 * (income - 180000)

    def calculate_mls(self, income, has_phic):
        if has_phic:
            return 0.0
        if income <= 90000:
            return 0.0
        elif income <= 105000:
            return 0.01 * income
        elif income <= 140000:
            return 0.0125 * income
        else:
            return 0.015 * income

def main():
    daemon = Pyro5.server.Daemon()
    uri = daemon.register(EstimatorServer, objectId="estimator")
    print("Server-1 (Application Server) is ready.")
    print(f"URI: {uri}\n")
    daemon.requestLoop()

if __name__ == "__main__":
    main()
