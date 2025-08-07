# shared/estimator_interface.py
import Pyro5.api

@Pyro5.api.expose
class Estimator:
    def estimate_tax_return(self, person_id, data_list, has_phic):
        """
        data_list = list of dicts: [{'income': float, 'withheld': float}, ...]
        has_phic = boolean
        Returns a dictionary with computed tax data
        """
        return {
            "person_id": person_id,
            "annual_income": 0,
            "total_withheld": 0,
            "net_income": 0,
            "medicare_levy": 0,
            "mls": 0,
            "refund_or_payable": 0,
            "message": "Not implemented yet."
        }
