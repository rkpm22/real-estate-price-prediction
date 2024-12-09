import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text

# Database Configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'qwerty',
    'database': 'RealEstateDB'
}
DATABASE_URI = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}/{db_config['database']}"
engine = create_engine(DATABASE_URI)

# Function to validate broker
def validate_broker():
    broker_id = input("Enter your Broker ID: ").strip()
    query = "SELECT * FROM Broker WHERE Broker_id = :broker_id"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), {"broker_id": broker_id})
            broker_data = result.fetchall()
            if broker_data:
                print("You are a valid broker. Welcome!")
                return broker_id
            else:
                print("Invalid Broker ID. Access denied.")
                return None
    except Exception as e:
        print(f"Error validating broker: {e}")
        return None

# Helper function for numeric input
def get_numeric_input(prompt):
    while True:
        value = input(prompt).strip()
        if value == "":  # Allow blank input
            return None
        if value.isdigit():
            return int(value)
        print("Invalid input! Please enter a valid number.")

# Function to display broker details
def show_broker_details():
    broker_id = input("Enter Broker ID (or leave blank to search by name): ").strip()
    if broker_id:
        query = "SELECT * FROM Broker WHERE Broker_id = :broker_id"
        params = {"broker_id": broker_id}
    else:
        broker_name = input("Enter Broker Name: ").strip()
        query = "SELECT * FROM Broker WHERE Broker_name LIKE :broker_name"
        params = {"broker_name": f"%{broker_name}%"}

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                print(df)
            else:
                print("No broker details found.")
    except Exception as e:
        print(f"Error fetching broker details: {e}")

# Function to search for properties
def search_properties():
    print("\nAvailable Filters:")
    print("1. Property Type")
    print("2. City")
    print("3. Suburban")
    print("4. Locality")
    print("5. Number of BHKs")
    print("6. Price Range (Min and/or Max)")
    print("7. Builder Name")
    print("8. Property Building Status (Active, Inactive, or Blank)")
    print("9. Furnishing Status (Furnished, Semi-Furnished, Unfurnished)")

    selected_filters = input("\nEnter the numbers of the filters you want to apply (comma-separated): ").strip().split(',')

    filters = {}

    # Ask relevant questions based on selected filters
    if '1' in selected_filters:
        filters["property_type"] = input("Enter property type (Apartment, Independent House, Independent Floor, Residential Plot, Villa): ").strip()
    if '2' in selected_filters:
        filters["city_name"] = input("Enter city name: ").strip()
    if '3' in selected_filters:
        filters["suburban_name"] = input("Enter suburban name: ").strip()
    if '4' in selected_filters:
        filters["locality_name"] = input("Enter locality name: ").strip()
    if '5' in selected_filters:
        filters["no_of_bhk"] = get_numeric_input("Enter number of BHKs (leave blank if not applicable): ")
    if '6' in selected_filters:
        filters["min_price"] = get_numeric_input("Enter minimum price (leave blank if not applicable): ")
        filters["max_price"] = get_numeric_input("Enter maximum price (leave blank if not applicable): ")
    if '7' in selected_filters:
        filters["builder_name"] = input("Enter builder name: ").strip()
    if '8' in selected_filters:
        filters["property_building_status"] = input("Enter property building status (Active, Inactive, or Blank): ").strip()
    if '9' in selected_filters:
        filters["is_furnished"] = input("Enter furnishing status (Furnished, Semi-Furnished, Unfurnished): ").strip()

    # Base Query
    query = """
        SELECT Property.Property_id, Property.Property_Name, Property.Price, Property.No_of_BHK, 
               Property.Property_building_status, PropertyDesc.is_furnished, Builder.Builder_name, 
               City.City_name, Suburban.Sub_urban_name, Locality.Locality_Name, Property_type.Property_type_name
        FROM Property
        LEFT JOIN PropertyDesc ON Property.Property_id = PropertyDesc.Property_id
        LEFT JOIN Builder ON Property.Builder_id = Builder.Builder_id
        LEFT JOIN Locality ON Property.Locality_ID = Locality.Locality_ID
        LEFT JOIN Suburban ON Locality.Sub_urban_ID = Suburban.Sub_urban_ID
        LEFT JOIN City ON Suburban.City_id = City.City_id
        LEFT JOIN Property_type ON Property.Property_type_id = Property_type.Property_type_id
        WHERE 1=1
    """

    params = {}
    if "property_type" in filters and filters["property_type"]:
        query += " AND Property_type.Property_type_name = :property_type"
        params["property_type"] = filters["property_type"]
    if "city_name" in filters and filters["city_name"]:
        query += " AND City.City_name = :city_name"
        params["city_name"] = filters["city_name"]
    if "suburban_name" in filters and filters["suburban_name"]:
        query += " AND Suburban.Sub_urban_name = :suburban_name"
        params["suburban_name"] = filters["suburban_name"]
    if "locality_name" in filters and filters["locality_name"]:
        query += " AND Locality.Locality_Name = :locality_name"
        params["locality_name"] = filters["locality_name"]
    if "no_of_bhk" in filters and filters["no_of_bhk"]:
        query += " AND Property.No_of_BHK = :no_of_bhk"
        params["no_of_bhk"] = filters["no_of_bhk"]
    if "min_price" in filters and filters["min_price"]:
        query += " AND Property.Price >= :min_price"
        params["min_price"] = filters["min_price"]
    if "max_price" in filters and filters["max_price"]:
        query += " AND Property.Price <= :max_price"
        params["max_price"] = filters["max_price"]
    if "builder_name" in filters and filters["builder_name"]:
        query += " AND Builder.Builder_name LIKE :builder_name"
        params["builder_name"] = f"%{filters['builder_name']}%"
    if "property_building_status" in filters and filters["property_building_status"]:
        query += " AND Property.Property_building_status = :property_building_status"
        params["property_building_status"] = filters["property_building_status"]
    if "is_furnished" in filters and filters["is_furnished"]:
        query += " AND PropertyDesc.is_furnished = :is_furnished"
        params["is_furnished"] = filters["is_furnished"]

    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), params)
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                print("\nFiltered Properties:")
                print(df)
            else:
                print("No properties found matching the selected filters.")
    except Exception as e:
        print(f"Error executing search: {e}")

# Function to list properties assigned to a broker
def list_properties_assigned_to_broker():
    broker_id = input("Enter Broker ID: ").strip()
    query = """
        SELECT Property.Property_id, Property.Property_Name, Property.Price, Builder.Builder_name
        FROM BrokerProperty
        LEFT JOIN Property ON BrokerProperty.Property_id = Property.Property_id
        LEFT JOIN Builder ON Property.Builder_id = Builder.Builder_id
        WHERE BrokerProperty.Broker_id = :broker_id
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query), {"broker_id": broker_id})
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                print(df)
            else:
                print("No properties assigned to this broker.")
    except Exception as e:
        print(f"Error fetching properties for broker: {e}")

# Function for custom query
def custom_query():
    query = input("Enter your SQL query: ").strip()
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                print(df)
            else:
                print("No results found.")
    except Exception as e:
        print(f"Error executing custom query: {e}")

# Visualization Functions
def properties_per_city():
    query = "SELECT City.City_name, COUNT(Property.Property_id) AS Total_Properties FROM Property LEFT JOIN Locality ON Property.Locality_ID = Locality.Locality_ID LEFT JOIN Suburban ON Locality.Sub_urban_ID = Suburban.Sub_urban_ID LEFT JOIN City ON Suburban.City_id = City.City_id GROUP BY City.City_name"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                df.plot(kind='bar', x='City_name', y='Total_Properties', legend=False, color='skyblue')
                plt.title('Number of Properties Across Cities')
                plt.xlabel('City')
                plt.ylabel('Number of Properties')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            else:
                print("No data available for this visualization.")
    except Exception as e:
        print(f"Error fetching data: {e}")



def properties_by_broker():
    query = """
        SELECT Broker.Broker_name, COUNT(BrokerProperty.Property_id) AS Total_Properties, AVG(Broker.Broker_rating) AS Avg_Rating
        FROM Broker
        LEFT JOIN BrokerProperty ON Broker.Broker_id = BrokerProperty.Broker_id
        GROUP BY Broker.Broker_name
    """
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                df.plot(kind='bar', x='Broker_name', y='Total_Properties', legend=False, color='cyan')
                plt.title('Number of Properties Handled by Each Broker')
                plt.xlabel('Broker')
                plt.ylabel('Number of Properties')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.show()
            else:
                print("No data available for this visualization.")
    except Exception as e:
        print(f"Error fetching data: {e}")

def property_building_status_pie_chart():
    query = "SELECT Property.Property_building_status, COUNT(*) AS Count FROM Property GROUP BY Property.Property_building_status"
    try:
        with engine.connect() as connection:
            result = connection.execute(text(query))
            data = result.fetchall()
            if data:
                df = pd.DataFrame(data, columns=result.keys())
                df.set_index('Property_building_status', inplace=True)
                df.plot(kind='pie', y='Count', autopct='%1.1f%%', legend=False)
                plt.title('Distribution of Property Building Status')
                plt.ylabel('')  # Hide y-axis label
                plt.tight_layout()
                plt.show()
            else:
                print("No data available for this visualization.")
    except Exception as e:
        print(f"Error fetching data: {e}")

# Visualization menu
def trends_and_visualizations():
    while True:
        print("\nTrends and Visualizations:")
        print("1. Number of Properties Across All Cities")
        print("2. Number of Properties Handled by Each Broker and Their Average Rating")
        print("3. Distribution of Property Building Status (Pie Chart)")
        print("4. Back to Main Menu")

        choice = input("Enter your choice: ").strip()

        if choice == '1':
            properties_per_city()
        elif choice == '2':
            properties_by_broker()
        elif choice == '3':
            property_building_status_pie_chart()
        elif choice == '4':
            break
        else:
            print("Invalid choice. Please try again.")

# Main menu
def main():
    broker_id = validate_broker()
    if not broker_id:
        return

    while True:
        print("\nMenu:")
        print("1. Show Broker Details")
        print("2. Search Properties")
        print("3. List Properties Assigned to Broker")
        print("4. Custom Query")
        print("5. Trends and Visualizations")
        print("6. Exit")
        choice = input("Enter your choice: ").strip()

        if choice == '1':
            show_broker_details()
        elif choice == '2':
            search_properties()
        elif choice == '3':
            list_properties_assigned_to_broker()
        elif choice == '4':
            custom_query()
        elif choice == '5':
            trends_and_visualizations()
        elif choice == '6':
            print("Exiting the application. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
