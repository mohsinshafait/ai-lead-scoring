from app.services.database import get_initial_lead_features


lead = get_initial_lead_features(1)

if lead is None:
    print("Lead not found.")
else:
    print("Lead retrieved successfully.")
    print()
    
    for key, value in lead.items():
        print(f"{key}: {value}")