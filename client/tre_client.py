# client/tre_client.py

import Pyro5.api

# Define valid users for client-side authentication (as per assignment instructions)
valid_users = {
    "123456": "pass123",
    "654321": "test456"
}

# Define valid TFNs
valid_tfns = {"11111111", "22222222", "33333333", "44444444", "55555555"}


def is_valid_tfn(tfn):
    """Check if TFN is in the valid list"""
    return tfn in valid_tfns



def get_user_input():
    print("\n=== Welcome to PITRE Client ===")

    # Authentication
    person_id = input("Enter Person ID (6 digits): ").strip()
    password = input("Enter Password: ").strip()

    if person_id not in valid_users or valid_users[person_id] != password:
        print("Invalid login. Exiting.\n")
        exit(1)

    # TFN check
    use_tfn = input("Do you have a TFN? (yes/no): ").strip().lower()
    if use_tfn == "yes":
        tfn = input("Enter your TFN (8 digits): ").strip()

        # Validate TFN before proceeding
        if not is_valid_tfn(tfn):
            print("Invalid TFN. Exiting.")
            exit(1)

        # Only prompt for name and email if TFN is valid
        name = input("Enter your full name: ").strip()
        email = input("Enter your email address: ").strip()
        phic = input("Do you have Private Health Insurance Cover (PHIC)? (yes/no): ").strip().lower() == "yes"
        return {
            "person_id": person_id,
            "data_list": [],
            "has_phic": phic,
            "tfn": tfn,
            "name": name,
            "email": email
        }

    # Manual data entry (non-TFN or invalid TFN)
    print("\nEnter up to 26 biweekly <taxable_income, tax_withheld> pairs:")
    data_list = []
    for i in range(26):
        try:
            income = float(input(f"Record {i + 1} - Income: ").strip())
            withheld = float(input(f"Record {i + 1} - Withheld: ").strip())

            if income < 0 or withheld < 0:
                print("Values must be non-negative.")
                break
            if withheld > income:
                print("Withheld amount cannot exceed income.")
                break

            data_list.append({"income": income, "withheld": withheld})
        except Exception:
            print("Stopping input. Proceeding with current records.")
            break

    if len(data_list) == 0:
        print("No valid records entered. Exiting.")
        exit(1)

    phic = input("Do you have Private Health Insurance Cover (PHIC)? (yes/no): ").strip().lower() == "yes"
    return {
        "person_id": person_id,
        "data_list": data_list,
        "has_phic": phic,
        "tfn": None,
        "name": None,
        "email": None
    }


def main():
    print("\n=== PITRE Tax Return Estimation Client ===")
    server1_uri = input("Enter Server-1 URI (e.g. PYRO:estimator@localhost:xxxx): ").strip()
    server2_uri = input("Enter Server-2 URI (e.g. PYRO:pitd@localhost:xxxx): ").strip()

    try:
        estimator = Pyro5.api.Proxy(server1_uri)
    except Exception as e:
        print("Failed to connect to Server-1. Error:", e)
        return

    # Collect input from user
    user_data = get_user_input()
    user_data["server2_uri"] = server2_uri  # Add URI info for server1 to use

    try:
        result = estimator.estimate_tax_return(
            user_data["person_id"],
            user_data["data_list"],
            user_data["has_phic"],
            user_data["tfn"],
            user_data["name"],
            user_data["email"],
            user_data["server2_uri"]
        )
    except Exception as e:
        print("An error occurred while contacting the server:", e)
        return

    print("\n=== Tax Return Estimate ===")
    for key, value in result.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()