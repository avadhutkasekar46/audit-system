import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# 1. Initialize data storage
client_data = []

def add_client():
    name = input("\nEnter Client Name: ")
    print("Select Standard(s): GOTS, OCS, GRS, RCS, BCI (comma separated)")
    standards = input("Standards: ").upper()
    
    issue_date_str = input("Issue Date (YYYY-MM-DD): ")
    expiry_date_str = input("Expiry Date (YYYY-MM-DD): ")
    
    # Convert strings to dates
    expiry_date = datetime.strptime(expiry_date_str, "%Y-%m-%d")
    today = datetime.now()
    
    # Logic for status
    if expiry_date < today:
        status = "Expired"
    elif expiry_date <= today + timedelta(days=30):
        status = "Near Expiry"
    else:
        status = "Active"

    client_data.append({
        "Client": name,
        "Standards": standards,
        "Issue Date": issue_date_str,
        "Expiry Date": expiry_date,
        "Status": status
    })
    print(f"\n✅ Data for {name} added successfully!")

def show_visuals():
    if not client_data:
        print("No data available to visualize.")
        return
        
    df = pd.DataFrame(client_data)
    status_counts = df['Status'].value_counts()
    
    # Define colors for the chart
    colors = {'Active': 'green', 'Near Expiry': 'orange', 'Expired': 'red'}
    current_colors = [colors.get(x, 'blue') for x in status_counts.index]

    plt.figure(figsize=(8, 5))
    status_counts.plot(kind='bar', color=current_colors)
    plt.title('Client Certificate Status Overview')
    plt.xlabel('Status')
    plt.ylabel('Number of Clients')
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

# Main Loop
while True:
    print("\n--- Certification Tracker ---")
    print("1. Add Client Data")
    print("2. View Visual Report")
    print("3. Exit")
    choice = input("Select an option: ")
    
    if choice == '1':
        add_client()
    elif choice == '2':
        show_visuals()
    elif choice == '3':
        break
