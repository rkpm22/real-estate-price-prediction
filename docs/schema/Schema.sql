-- Create the database
CREATE DATABASE IF NOT EXISTS RealEstateDB;
USE RealEstateDB;

-- City Table
CREATE TABLE City (
  City_id INT PRIMARY KEY,              -- Primary key for unique identification of cities
  City_name VARCHAR(255) NOT NULL       -- City name cannot be NULL
);

-- Property Type Table
CREATE TABLE Property_type (
  Property_type_id INT PRIMARY KEY,  -- Auto-incrementing primary key
  Property_type_name VARCHAR(255) NOT NULL  -- Property type name cannot be NULL
);


-- Builder Table
CREATE TABLE Builder (
  Builder_id INT PRIMARY KEY,           -- Primary key for unique identification of builders
  Builder_name VARCHAR(255) NOT NULL    -- Builder name cannot be NULL
);

-- Suburban Table
CREATE TABLE Suburban (
  Sub_urban_ID INT PRIMARY KEY,         -- Primary key for unique identification of suburbs
  Sub_urban_name VARCHAR(255) NOT NULL, -- Suburb name cannot be NULL
  City_id INT NOT NULL,                 -- Foreign key to City table
  FOREIGN KEY (City_id) REFERENCES City(City_id) ON DELETE CASCADE ON UPDATE CASCADE  -- Enforce referential integrity
);

-- Locality Table
CREATE TABLE Locality (
  Locality_ID INT PRIMARY KEY,          -- Primary key for unique identification of localities
  Locality_Name VARCHAR(255) NOT NULL,  -- Locality name cannot be NULL
  Sub_urban_ID INT,                     -- Foreign key to Suburban table
  FOREIGN KEY (Sub_urban_ID) REFERENCES Suburban(Sub_urban_ID) ON DELETE CASCADE ON UPDATE CASCADE -- Enforce referential integrity
);

-- Property Table
CREATE TABLE Property (
  Property_id INT PRIMARY KEY,          -- Primary key for unique identification of properties
  Property_Name VARCHAR(255) NOT NULL,  -- Property name cannot be NULL
  Property_status VARCHAR(255) NOT NULL,-- Property status (e.g., Available, Sold)
  Property_type_id INT NOT NULL,        -- Foreign key to Property_type table
  Price BIGINT NOT NULL,                -- Property price cannot be NULL
  Size INT NOT NULL,                    -- Property size (e.g., in square feet)
  Price_per_unit_area INT NOT NULL,     -- Price per unit area (e.g., per square foot)
  Property_building_status VARCHAR(30),
  No_of_BHK INT NOT NULL,               -- Number of BHK (Bedroom-Hall-Kitchen)
  Locality_ID INT,                      -- Foreign key to Locality table
  Posted_On DATE NOT NULL,              -- Date when property was posted
  Builder_id INT NOT NULL,              -- Foreign key to Builder table
  FOREIGN KEY (Property_type_id) REFERENCES Property_type(Property_type_id) ON DELETE CASCADE ON UPDATE CASCADE, -- Enforce referential integrity
  FOREIGN KEY (Locality_ID) REFERENCES Locality(Locality_ID) ON DELETE SET NULL ON UPDATE CASCADE, -- Enforce referential integrity
  FOREIGN KEY (Builder_id) REFERENCES Builder(Builder_id) ON DELETE CASCADE ON UPDATE CASCADE -- Enforce referential integrity
);

-- Property Description Table
CREATE TABLE PropertyDesc (
  Property_id INT,                      -- Foreign key referring to Property table
  Description TEXT,                      -- Description of the property
  is_furnished VARCHAR(255) NOT NULL,    -- Whether the property is furnished or not
  is_Apartment BOOLEAN NOT NULL,         -- Whether the property is an apartment or not
  is_commercial BOOLEAN NOT NULL,        -- Whether the property is commercial or not
  is_studio BOOLEAN NOT NULL,            -- Whether the property is a studio or not
  is_PentaHouse BOOLEAN NOT NULL,        -- Whether the property is a penthouse or not
  is_plot BOOLEAN NOT NULL,              -- Whether the property is a plot or not
  is_RERA_registered BOOLEAN NOT NULL,   -- Whether the property is RERA registered or not
  is_ready_to_move BOOLEAN NOT NULL,     -- Whether the property is ready to move or not
  FOREIGN KEY (Property_id) REFERENCES Property(Property_id) ON DELETE CASCADE ON UPDATE CASCADE -- Enforce referential integrity
);

-- Broker Table
CREATE TABLE Broker (
  Broker_id INT PRIMARY KEY,            -- Primary key for unique identification of brokers
  Broker_name VARCHAR(255) NOT NULL,     -- Broker name cannot be NULL
  Broker_contact VARCHAR(255), 			 -- Broker contact number (optional)
  Broker_company VARCHAR(255),
  Broker_rating FLOAT,                   -- Broker rating (optional)
  City_id INT,                           -- Foreign key to City table
  FOREIGN KEY (City_id) REFERENCES City(City_id) ON DELETE SET NULL ON UPDATE CASCADE -- Enforce referential integrity
);

-- Broker-Property Table (Many-to-Many Relationship)
CREATE TABLE BrokerProperty (
  Broker_id INT NOT NULL,                -- Foreign key to Broker table
  Property_id INT NOT NULL,              -- Foreign key to Property table
  FOREIGN KEY (Broker_id) REFERENCES Broker(Broker_id) ON DELETE CASCADE ON UPDATE CASCADE, -- Enforce referential integrity
  FOREIGN KEY (Property_id) REFERENCES Property(Property_id) ON DELETE CASCADE ON UPDATE CASCADE, -- Enforce referential integrity
  PRIMARY KEY (Broker_id, Property_id)   -- Composite primary key: unique combination of Broker_id and Property_id
);

-- Location Details Table
CREATE TABLE LocationDetails (
  Location_id INT PRIMARY KEY AUTO_INCREMENT,           -- Primary key for unique identification of locations
  Longitude FLOAT,                       -- Longitude of the location
  Latitude FLOAT,                        -- Latitude of the location
  Locality_ID INT NOT NULL,              -- Foreign key to Locality table
  FOREIGN KEY (Locality_ID) REFERENCES Locality(Locality_ID) ON DELETE CASCADE ON UPDATE CASCADE -- Enforce referential integrity
);
