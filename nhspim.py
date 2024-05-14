import streamlit as st
import mysql.connector
import pandas as pd
import requests
import os
import toml

# Access MySQL credentials from streamlit secrets
mysql_config = st.secrets["connections_mysql"]

def create_connection():
    """Create connection to MySQL database."""
    db = mysql.connector.connect(
        user=mysql_config["username"],
        password=mysql_config["password"],
        host=mysql_config["host"],
        port=mysql_config["port"],
        database=mysql_config["database"],
        auth_plugin=mysql_config["auth_plugin"]
    )
    return db

from PIL import Image

# Load your logo
logo = Image.open('Green White Modern Minimal Plants Logo.png')


def fetch_all_gmdns(db, search_value=None):
    """Fetch all records from the 'gmdn' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all gmdn
    select_gmdn_query = """
       SELECT
        gmdn_code, 
        gmdn_term_name, 
        gmdn_term_definition 
     FROM gmdn
     """
     
    if search_value:
        search_value = "%" + search_value + "%"
        select_gmdn_query += "WHERE gmdn_term_name LIKE %s"
        
    if search_value:
         cursor.execute(select_gmdn_query, (search_value,)) 
    else:
         cursor.execute(select_gmdn_query)
    
    gmdn = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]

    cursor.close()
    return gmdn, column_names


# In[59]:


def fetch_all_eclass(db, search_value=None):
    """Fetch all records from the 'NHS_product_classification' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all eclass codes
    select_eclass_query = """
       SELECT 
         eclass_code,
         description 
       FROM nhs_product_classification
    """
    
    if search_value:
        search_value = "%" + search_value + "%"
        select_eclass_query += "WHERE description LIKE %s"
        
    if search_value:
         cursor.execute(select_eclass_query, (search_value,)) 
    else:
         cursor.execute(select_eclass_query)
         
    eclass = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]

    cursor.close()
    return eclass, column_names


# In[60]:


def fetch_all_riskclass(db):
    """Fetch all records from the 'risk_class' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all risk classes
    select_riskclass_query = "SELECT class_name, class_description, regulatory_requirements FROM risk_class"
    cursor.execute(select_riskclass_query)
    riskclass = cursor.fetchall()
    
    return riskclass


# In[61]:


def fetch_all_providers(db, search_value=None):
    """Fetch all records from the 'nhs_provider' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all NHS providers
    select_provider_query = """ 
       SELECT 
         provider_gln, 
         provider_name, 
         provider_address, 
         provider_registration_no 
       FROM nhs_provider
    """
    if search_value:
        search_value = "%" + search_value + "%"
        select_provider_query += "WHERE provider_name LIKE %s"
        
    if search_value:
         cursor.execute(select_provider_query, (search_value,)) 
    else:
        cursor.execute(select_provider_query)
    provider = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]

    cursor.close()
    return provider, column_names


# In[62]:


def fetch_all_manufacturers(db, search_value=None):
    """Fetch all records from the 'manufacturer' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all device manufacturers
    select_manufacturer_query = """
       SELECT 
          manufacturer_gln,
          manufacturer_name, 
          manufacturer_address, 
          company_registration_no, 
          customer_service_phone, 
          customer_service_email 
       FROM manufacturer
    """
    
    if search_value:
        search_value = "%" + search_value + "%"
        select_manufacturer_query += "WHERE manufacturer_name LIKE %s"
        
    if search_value:
         cursor.execute(select_manufacturer_query, (search_value,)) 
    else:
        cursor.execute(select_manufacturer_query)
        
    manufacturer = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]

    cursor.close()
    
    return manufacturer, column_names


# In[63]:


def fetch_all_suppliers(db, search_value=None):
    """Fetch all records from the 'supplier' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all device suppliers
    select_supplier_query = """
       SELECT 
          supplier_gln,
          supplier_name, 
          supplier_address, 
          company_registration_no, 
          customer_service_phone, 
          customer_service_email 
       FROM supplier
    """
    if search_value:
        search_value = "%" + search_value + "%"
        select_supplier_query += "WHERE supplier_name LIKE %s"
        
    if search_value:
         cursor.execute(select_supplier_query, (search_value,)) 
    else:
        cursor.execute(select_supplier_query)
        
    supplier = cursor.fetchall()
    # Fetch column names
    column_names = [col[0] for col in cursor.description]

    cursor.close()
    
    return supplier, column_names


# In[64]:

def fetch_all_products(db, search_value=None):
    """Fetch all records from the 'medical_device' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #fetch all medical device products
    select_product_query = """
       SELECT
         gtin, brand_name, unit_of_use, quantity_of_uou,
         item_length, item_height, item_width, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update
      
       FROM medical_device
       LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
       LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
       LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code
       LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
       LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
       LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
    """
    
    if search_value:
        search_value = "%" + search_value + "%"
        select_product_query += "WHERE brand_name LIKE %s"

    if search_value:
         cursor.execute(select_product_query, (search_value,)) 
    else:
        cursor.execute(select_product_query)

    medical_device_product = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]

    cursor.close()
    
    return medical_device_product, column_names


def fetch_trade_item_by_udi(db, udi):
    """Fetch a trade item record from the trade item table based on the UDI of the trade item device"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by udi
    
    select_trade_item_by_udi_query= """
      SELECT 
       UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_use, quantity_of_uou, unit_of_use_udi, product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update,   medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', supplier.supplier_name, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email
      
     FROM trade_item
      LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
      LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
      LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
      LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
      LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
      LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
      LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
      LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
      LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code

     WHERE trade_item.udi = %s
    """
    
    cursor.execute(select_trade_item_by_udi_query, (udi,))
    trade_item = cursor.fetchall()
   # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


def fetch_trade_item_by_gtin(db, gtin):
    """Fetch a trade item record from the trade item table based on the UDI-DI of the item trade item device"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by gtin
    select_trade_item_by_gtin_query= """
      SELECT 
       UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_use, quantity_of_uou, unit_of_use_udi, product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update,   medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', supplier.supplier_name, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email
      
     FROM trade_item
      LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
      LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
      LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
      LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
      LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
      LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
      LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
      LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
      LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code

     WHERE trade_item.gtin = %s
    """
    
    cursor.execute(select_trade_item_by_gtin_query, (gtin,))
    trade_item = cursor.fetchall()
   # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[65]:


def fetch_trade_item_by_supplier(db, supplier_gln):
    """Fetch trade item records from the trade item table based on the gln of the item supplier"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by supplier gln
    select_trade_item_by_supplier_query = """
      SELECT 
      UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, 
      expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi,
      product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, 
      single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, 
      item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update, medical_device.gmdn_code, gmdn_term_name, supplier.supplier_gln, supplier.supplier_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email
      
      
      FROM trade_item
      LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
      LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
      LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
      LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
      LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
      LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
      LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
      LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
      LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code

      WHERE supplier.supplier_gln = %s
    """
    
    cursor.execute(select_trade_item_by_supplier_query, (supplier_gln,))
    trade_item = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[66]:


def fetch_trade_item_by_manufacturer(db, manufacturer_gln):
    """Fetch trade item records from the trade item table based on the gln of manufacturer"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by manufacturer gln
    select_trade_item_by_manufacturer_query = """
      SELECT 
      UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, 
      expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi,
      product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, 
      single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, 
      item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update, medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', supplier.supplier_name, supplier.supplier_address, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email
      
      FROM trade_item
      LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
      LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
      LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
      LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
      LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
      LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
      LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
      LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
      LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code
      
      WHERE manufacturer.manufacturer_gln = %s

    """
    
    cursor.execute(select_trade_item_by_manufacturer_query, (manufacturer_gln,))
    trade_item = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[67]:


def fetch_trade_item_by_provider(db, nhs_provider_gln):
    """Fetch trade item records from the trade item table based on the gln of the NHS provider the item was supplied to"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by nhs provider gln
    select_trade_item_by_provider_query = """
     SELECT 
       UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi, product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update, medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', supplier.supplier_name, supplier.supplier_address, trade_item.nhs_provider_gln, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email
      
     FROM trade_item
      LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
      LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
      LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
      LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
      LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
      LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
      LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
      LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
      LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code
      
     WHERE nhs_provider.provider_gln = %s
    """
    
    cursor.execute(select_trade_item_by_provider_query, (nhs_provider_gln,))
    trade_item = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[68]:


def fetch_trade_item_by_gmdn(db, gmdn_code):
    """Fetch trade item records from the trade item table based on gmdn codes"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by gmdn code
    select_trade_item_by_gmdn_query = """
      SELECT 
         UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi, product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update, medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', supplier.supplier_name, supplier.supplier_address, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email

      
      FROM trade_item
        LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
        LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
        LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
        LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
        LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
        LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
        LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
        LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
        LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code

      WHERE gmdn.gmdn_code = %s

    """
    
    cursor.execute(select_trade_item_by_gmdn_query, (gmdn_code,))
    trade_item = cursor.fetchall()
   # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[69]:


def fetch_trade_item_by_eclass(db, nhs_eclass_code):
    """Fetch trade item records from the trade item table based on  NHS eclass codes """
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by eclass code
    select_trade_item_by_eclass_query = """
       SELECT 
         UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi, product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update, medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', supplier.supplier_name, supplier.supplier_address, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email


      FROM trade_item
        LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
        LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
        LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
        LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
        LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
        LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
        LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
        LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
        LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code
        
      WHERE nhs_eclass_code = %s

    """
    
    cursor.execute(select_trade_item_by_eclass_query, (nhs_eclass_code,))
    trade_item = cursor.fetchall()
    # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[70]:


def fetch_trade_item_by_riskclass(db, risk_class):
    """Fetch trade item records from the trade item table based on the Risk class """
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by risk class code
    select_trade_item_by_riskclass_query = """
      SELECT 
         UDI, trade_item.gtin, brand_name, serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi, product_description, item_length, item_height, item_width, unit_of_dimension, item_weight AS 'item_weight (g)', item_volume AS 'item_volume (cubic cm)', storage_handling, single_use, restricted_no_of_use, sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, item_mri_compatible, medical_device.gmn, item_model.market_availability_date, item_model.lifecycle_status, item_model.last_status_update, medical_device.gmdn_code, gmdn_term_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, nhs_eclass_code, description AS 'eClass description', risk_class_name AS 'Risk Class', supplier.supplier_name, supplier.supplier_address, nhs_provider.provider_name, manufacturer_catalog.manufacturer_reference_no, authorized_rep.rep_name AS 'Authorized Rep Name', authorized_rep.contact_number, authorized_rep.email
     

      FROM trade_item
        LEFT JOIN medical_device ON medical_device.gtin = trade_item.gtin
        LEFT JOIN supplier ON supplier.supplier_gln = trade_item.supplier_gln
        LEFT JOIN nhs_provider ON nhs_provider.provider_gln = trade_item.nhs_provider_gln
        LEFT JOIN manufacturer_catalog ON manufacturer_catalog.manufacturer_reference_no = medical_device.manufacturer_reference_no
        LEFT JOIN manufacturer ON manufacturer_catalog.manufacturer_manufacturer_gln = manufacturer.manufacturer_gln
        LEFT JOIN authorized_rep ON manufacturer_catalog.authorized_rep_rep_id = authorized_rep.rep_id
        LEFT JOIN item_model ON item_model.gmn = medical_device.gmn
        LEFT JOIN gmdn ON gmdn.gmdn_code = medical_device.gmdn_code
        LEFT JOIN nhs_product_classification ON nhs_product_classification.eclass_code = medical_device.nhs_eclass_code
        
      WHERE medical_device.risk_class_name = %s

    """
    
    cursor.execute(select_trade_item_by_riskclass_query, (risk_class,))
    trade_item = cursor.fetchall()
    
    # Fetch column names
    column_names = [col[0] for col in cursor.description]
    
    # Close cursor
    cursor.close()
    
    return trade_item, column_names


# In[71]:


def add_download_button(df, title):
        csv = df.to_csv(index=False).encode()
        st.download_button(
            label=f"Download {title} as CSV",
            data=csv,
            file_name=f"{title.lower().replace(' ', '_')}_results.csv",
            mime='text/csv'
        )


# In[72]:


def search_trade_items(db):
    search_option = st.selectbox("Select search option from dropdown", ["UDI", "GTIN", "Supplier GLN", "Manufacturer GLN", "Provider GLN", "GMDN Code", "NHS eClass Code", "Risk Class"], key="search_option")
    search_value = st.text_input("Enter search value",key="search_value")
    
    if st.button("Search"):
        if search_option == "UDI":
            trade_item = fetch_trade_item_by_udi(db, search_value)
        elif search_option == "GTIN":
            trade_item = fetch_trade_item_by_gtin(db, search_value)
        elif search_option == "Supplier GLN":
            trade_item = fetch_trade_item_by_supplier(db, search_value)
        elif search_option == "Manufacturer GLN":
            trade_item = fetch_trade_item_by_manufacturer(db, search_value)
        elif search_option == "Provider GLN":
            trade_item = fetch_trade_item_by_provider(db, search_value)
        elif search_option == "GMDN Code":
            trade_item = fetch_trade_item_by_gmdn(db, search_value)
        elif search_option == "NHS eClass Code":
            trade_item = fetch_trade_item_by_eclass(db, search_value)
        elif search_option == "Risk Class":
            trade_item = fetch_trade_item_by_riskclass(db, search_value)
            
            
        if trade_item:
            st.subheader("Trade Items")
            trade_item_data, column_names = trade_item
            
            # Create DataFrame with fetched data and column names
            df = pd.DataFrame(trade_item_data, columns=column_names)
            st.dataframe(df)
            
            add_download_button(df, "Trade Items")
        else:
            st.write("No Trade Items found")


# In[73]:


def main():
    #Title and sidebar
    st.title("NHS MedTech Product Information Management System")
    db = create_connection()
    
    

    #create database (db)
   
    #config['database'] = 'NHS_PIM'
    #db = create_connection()
    
    menu = ["Home", "Search Trade Items", "Medical Devices", "Suppliers", "Manufacturers", "NHS Provider", "GMDN", "NHS eClass", "Risk Class"]
    options = st.sidebar.radio("Select option : ", menu)

    
    if options == "Home":
        st.image(logo, use_column_width=5)
        st.subheader("Welcome to the NHS' MedTech Product Information Management System")

        with st.expander("**About the NHS PIM**"):
            st.markdown("""
            The NHS PIM system is designed to revolutionize the way product information is managed within the National Health Service (NHS) procurement ecosystem. With the aim of improving data sharing, enhancing supply chain efficiency, and ensuring patient safety, our system serves as a centralized platform for storing, accessing, and managing vital product information.
            
            The purpose of the NHS PIM system is to address the challenges faced by the NHS in managing product data, such as outdated information, inconsistent records, and manual data entry processes. By providing a comprehensive database of standardized and up-to-date product information, our system empowers healthcare providers, procurement teams, and other stakeholders to make informed decisions and streamline their operations.
            
            Users of the system can expect to access a wide range of product data, including details on Medical devices, Suppliers, Manufacturers, GMDNs, Risk Classes, NHS Provider trusts, the NHS product classification system, and Trade Items supplied to the NHS across all its providers. From specifications and usage instructions to regulatory approvals and safety information, the PIM system provides a wealth of valuable information at your fingertips.
            
            Whether you're a healthcare professional searching for specific product details, a procurement officer managing inventory, or a patient seeking information on medical devices, the NHS PIM system is here to support you. 
            
            Explore our user-friendly interface and unlock the potential of centralized product information management for the NHS!
            
            """)
        
        with st.expander("**Access Guide**"):
            
             st.markdown("""
             Navigate from the sidebar to access the database
             1. Search for medical device trade items from the 'Search Trade Items' tab
             2. Select Search option from dropdown and input search value
             3. Lookup medical device information from 'Medical Devices' page
             4. Lookup all other pages for corresponding information

             You can view a comprehensive data dictionary in [Glossary of terms](https://docs.google.com/spreadsheets/d/1m1Ty2fqvT6VlAo9CiAVMFjsHZaOecX8-ghPnITdVDQw/edit?usp=sharing)

             Kindly leave a review of the system [here](https://forms.gle/xfu1ebp2Kyeds4Ai9).
        """)

    
    elif options == "Search Trade Items":
        search_trade_items(db)
        
        
    elif options == "Medical Devices":
        #get search value from user
        search_value = st.text_input("Filter by brand name")
        
        #fetch optional filtering
        medical_device_product = fetch_all_products(db, search_value=search_value)
        if medical_device_product:
            st.subheader("All Medical Device Products:")
            medical_device_data, column_names = medical_device_product
            
            # Create DataFrame with fetched data and column names
            df = pd.DataFrame(medical_device_data, columns = column_names)
            
            if search_value:
                df = df[df['brand_name'].str.contains(search_value, case=False, na=False)]
            st.dataframe(df)
            
            add_download_button(df, "Medical Device Products")
        else:
            st.write("No Medical Devices found")

          
    elif options == "Suppliers":
        #get search value from user
        search_value = st.text_input("Filter by supplier name")
        
        #fetch with optional filtering
        supplier = fetch_all_suppliers(db, search_value=search_value)
        if supplier:
            st.subheader("All Medical Tech Suppliers: ")
            supplier_data, column_names = supplier
            
            df = pd.DataFrame(supplier_data, columns=column_names)
            
            if search_value:
                df = df[df['supplier_name'].str.contains(search_value, case=False, na=False)]
            st.dataframe(df)
            add_download_button(df, "Medical Tech Suppliers")
        else:
            st.write("No Suppliers found")
        
    elif options == "Manufacturers":
        #get search value from user
        search_value = st.text_input("Filter by manufacturer name")
        
        #fetch with optional filtering
        manufacturer = fetch_all_manufacturers(db, search_value=search_value)
        if manufacturer:
            st.subheader("All Medical Tech Manufacturers: ")
            manufacturer_data, column_names = manufacturer
            
            df = pd.DataFrame(manufacturer_data, columns=column_names)
            
            if search_value:
                df = df[df['manufacturer_name'].str.contains(search_value, case=False, na=False)]
            st.dataframe(df)
            add_download_button(df, "Medical Tech Manufacturers")
        else:
            st.write("No Manufacturers found")
        
    elif options == "NHS Provider":
        #get search value from user
        search_value = st.text_input("Filter by NHS Provider")
        
        #fetch with optional filtering

        provider = fetch_all_providers(db, search_value=search_value)
        if provider:
            st.subheader("All NHS Providers: ")
            provider_data, column_names = provider
            
            df = pd.DataFrame(provider_data, columns=column_names)
            
            if search_value:
                df = df[df['provider_name'].str.contains(search_value, case=False, na=False)]

            st.dataframe(df)
            add_download_button(df, "NHS Providers")
        else:
            st.write("No NHS Provider found")
        
    elif options == "GMDN":
        #get search value from user
        search_value = st.text_input("Filter by GMDN term name")
        
        #fetch optional filtering
        gmdn = fetch_all_gmdns(db, search_value=search_value)
        if gmdn:
            st.subheader("All GMDNs: ")
            
            gmdn_data, column_names = gmdn
            
            df = pd.DataFrame(gmdn_data, columns=column_names)
            
            if search_value:
                df = df[df['gmdn_term_name'].str.contains(search_value, case=False, na=False)]

            st.dataframe(df) 
            add_download_button(df, "GMDNs")
        else:
            st.write("No GMDN found")
            
    elif options == "NHS eClass":
        #get search value from user
        search_value = st.text_input("Filter by eclass description")
        
        #fetch optional filtering
        eclass = fetch_all_eclass(db, search_value=search_value)
        if eclass:
            st.subheader("All NHS eClass codes: ")
            
            eclass_data, column_names = eclass
            
            df = pd.DataFrame(eclass_data, columns=column_names)
            
            if search_value:
                df = df[df['description'].str.contains(search_value, case=False, na=False)]

            st.dataframe(df)
            add_download_button(df, "NHS eClass codes")
        else:
            st.write("No NHS eClass codes found")
            
    elif options == "Risk Class":
        riskclass = fetch_all_riskclass(db)
        if riskclass:
            st.subheader("All Risk Classes: ")
            df = pd.DataFrame(riskclass, columns=['class_name', 'class_description', 'regulatory_requirements'])
            st.dataframe(df)
            add_download_button(df, "Risk Classes")
        else:
            st.write("No Risk Classes found")
        
    db.close()
    
    

if __name__ == "__main__":
    main()
        

