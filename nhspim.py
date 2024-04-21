import streamlit as st
import mysql.connector
import pandas as pd



# In[240]:


db = st.connection('mysql', type = 'sql')


# In[241]:


def fetch_all_gmdns(db):
    """Fetch all records from the 'gmdn' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all gmdn
    select_gmdn_query = "SELECT * from gmdn"
    cursor.execute(select_gmdn_query)
    gmdn = cursor.fetchall()
    
    return gmdn


# In[242]:


def fetch_all_eclass(db):
    """Fetch all records from the 'NHS_product_classification' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all eclass codes
    select_eclass_query = "SELECT * from nhs_product_classification"
    cursor.execute(select_eclass_query)
    eclass = cursor.fetchall()
    
    return eclass


# In[243]:


def fetch_all_riskclass(db):
    """Fetch all records from the 'risk_class' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all risk classes
    select_riskclass_query = "SELECT * from risk_class"
    cursor.execute(select_riskclass_query)
    riskclass = cursor.fetchall()
    
    return riskclass


# In[244]:


def fetch_all_providers(db):
    """Fetch all records from the 'nhs_provider' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all NHS providers
    select_provider_query = "SELECT * from nhs_provider"
    cursor.execute(select_provider_query)
    provider = cursor.fetchall()
    
    return provider


# In[245]:


def fetch_all_manufacturers(db):
    """Fetch all records from the 'manufacturer' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all device manufacturers
    select_manufacturer_query = "SELECT * from manufacturer"
    cursor.execute(select_manufacturer_query)
    manufacturer = cursor.fetchall()
    
    return manufacturer


# In[246]:


def fetch_all_suppliers(db):
    """Fetch all records from the 'supplier' table."""
    cursor = db.cursor()
    
    #Select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch all device suppliers
    select_supplier_query = "SELECT * from supplier"
    cursor.execute(select_supplier_query)
    supplier = cursor.fetchall()
    
    return supplier


# In[247]:


def fetch_trade_item_by_gtin(db, gtin):
    """Fetch a trade item record from the trade item table based on the UDI-DI of the item"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by gtin
    select_trade_item_by_gtin_query= """
      SELECT 
      gtin, brand_name, serial_number, batch_number, manufacturing_date, 
      expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi,
      item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, 
      manufacturer_catalog_mpc,nhs_provider_provider_gln, nhs_eclass_code
      
      FROM trade_item
      WHERE gtin = %s
    """
    
    cursor.execute(select_trade_item_by_gtin_query, (gtin,))
    trade_item = cursor.fetchone()
    
    #cursor close
    return trade_item


# In[248]:


def fetch_trade_item_by_supplier(db, supplier_supplier_gln):
    """Fetch trade item records from the trade item table based on the gln of the item supplier"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by supplier gln
    select_trade_item_by_supplier_query = """
      SELECT 
      gtin, brand_name, supplier_supplier_gln, supplier.supplier_name, serial_number, batch_number, manufacturing_date, 
      expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi,
      item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, 
      manufacturer_catalog_mpc,nhs_provider_provider_gln, nhs_eclass_code
      
      FROM trade_item
       LEFT JOIN supplier on supplier.supplier_gln = trade_item.supplier_supplier_gln
      WHERE supplier_supplier_gln = %s
    """
    
    cursor.execute(select_trade_item_by_supplier_query, (supplier_supplier_gln,))
    trade_item = cursor.fetchall()
    
    #cursor close
    return trade_item


# In[249]:


def fetch_trade_item_by_manufacturer(db, manufacturer_manufacturer_gln):
    """Fetch trade item records from the trade item table based on the gln of manufacturer"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by manufacturer gln
    select_trade_item_by_manufacturer_query = """
      SELECT 
      gtin, brand_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, 
      serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use,
      quantity_of_uou, unit_of_use_udi, item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, nhs_eclass_code
      
      FROM trade_item
       LEFT JOIN manufacturer_catalog on manufacturer_catalogue.manufacturer_product_code = trade_item.manufacturer_catalog_mpc
       LEFT JOIN manufacturer on manufacturer.manufacturer_gln = manufacturer_catalog.manufacturer_manufacturer_gln
      WHERE manufacturer.manufacturer_gln = %s

    """
    
    cursor.execute(select_trade_item_by_manufacturer_query, (manufacturer_manufacturer_gln,))
    trade_item = cursor.fetchall()
    
    #cursor close
    return trade_item


# In[250]:


def fetch_trade_item_by_provider(db, nhs_provider_provider_gln):
    """Fetch trade item records from the trade item table based on the gln of the NHS provider the item was supplied to"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by nhs provider gln
    select_trade_item_by_provider_query = """
      SELECT 
      gtin, brand_name, supplier_supplier_gln, supplier.supplier_name, serial_number, batch_number, manufacturing_date, 
      expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi,
      item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, 
      manufacturer_catalog_mpc,nhs_provider_provider_gln, nhs_eclass_code
      
      FROM trade_item
       LEFT JOIN nhs_provider on nhs_provider.provider_gln = trade_item.nhs_provider_provider_gln
      WHERE nhs_provider.provider_gln = %s
    """
    
    cursor.execute(select_trade_item_by_provider_query, (nhs_provider_provider_gln,))
    trade_item = cursor.fetchall()
    
    #cursor close
    return trade_item


# In[251]:


def fetch_trade_item_by_gmdn(db, gmdn_gmdn_code):
    """Fetch trade item records from the trade item table based on gmdn codes"""
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by gmdn code
    select_trade_item_by_gmdn_query = """
      SELECT 
      gtin, brand_name, serial_number, batch_number, manufacturing_date, 
      expiry_date, udi_pi, unit_of_issue, unit_of_use, quantity_of_uou, unit_of_use_udi,
      item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, 
      manufacturer_catalog_mpc,nhs_provider_provider_gln, nhs_eclass_code
      
      FROM trade_item
      WHERE gmdn_gmdn_code = %s

    """
    
    cursor.execute(select_trade_item_by_gmdn_query, (gmdn_gmdn_code,))
    trade_item = cursor.fetchall()
    
    #cursor close
    return trade_item


# In[252]:


def fetch_trade_item_by_eclass(db, nhs_eclass_code):
    """Fetch trade item records from the trade item table based on  NHS eclass codes """
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by eclass code
    select_trade_item_by_eclass_query = """
      SELECT 
      gtin, brand_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, 
      serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use,
      quantity_of_uou, unit_of_use_udi, item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, nhs_eclass_code
      
      FROM trade_item
      WHERE nhs_eclass_code = %s

    """
    
    cursor.execute(select_trade_item_by_eclass_query, (nhs_eclass_code,))
    trade_item = cursor.fetchall()
    
    #cursor close
    return trade_item


# In[253]:


def fetch_trade_item_by_riskclass(db, risk_class_class_name):
    """Fetch trade item records from the trade item table based on the Risk class """
    cursor = db.cursor()
    
    #select database
    cursor.execute("USE NHS_PIM")
    
    #Fetch trade items by risk class code
    select_trade_item_by_riskclass_query = """
      SELECT 
      gtin, brand_name, manufacturer.manufacturer_name, manufacturer.manufacturer_address, 
      serial_number, batch_number, manufacturing_date, expiry_date, udi_pi, unit_of_issue, unit_of_use,
      quantity_of_uou, unit_of_use_udi, item_length_cm, item_height_cm, item_width_cm, item_weight_gram, item_volume_ccm, 
      unit_of_dimension, product_description, storage_handling, single_use, restricted_no_of_use,
      sterile, sterilize_before_use, sterilization_method, item_contains_latex, item_contains_dehp, 
      item_mri_compatible, item_model_gmn, gmdn_gmdn_code, nhs_eclass_code
      
      FROM trade_item
      left join item_model on item_model.GMN = trade_item.item_model_gmn
      left join risk_class on risk_class.class_name = item_model.risk_class_class_name
      WHERE risk_class_class_name = %s

    """
    
    cursor.execute(select_trade_item_by_riskclass_query, (risk_class_class_name,))
    trade_item = cursor.fetchall()
    
    #cursor close
    return trade_item


# In[254]:


def search_trade_items(db):
    search_option = st.selectbox("Select search option", ["GTIN", "Supplier GLN", "Manufacturer GLN", "Provider GLN", "GMDN Code", "NHS eClass Code", "Risk Class"], key="search_option")
    search_value = st.text_input("Enter search value",key="search_value")
    
    if st.button("Search"):
        if search_option == "GTIN":
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
            df = pd.DataFrame([trade_item], columns = ['gtin', 'brand_name', 'serial_number', 'batch_number','manufacturing_date', 'expiry_date', 'udi_pi', 'unit_of_issue', 'unit_of_use', 'quantity_of_uou', 'unit_of_use_udi', 'item_length_cm', 'item_height_cm', 'item_width_cm', 'item_weight_gram', 'item_volume_ccm', 'unit_of_dimension', 'product_description', 'storage_handling', 'single_use', 'restricted_no_of_use', 'sterile', 'sterilize_before_use', 'sterilization_method', 'item_contains_latex', 'item_contains_dehp', 'item_mri_compatible','supplier_supplier_gln', 'item_model_gmn', 'gmdn_gmdn_code', 'manufacturer_catalog_mpc','nhs_provider_provider_gln', 'nhs_eclass_code']) 
            st.dataframe(df)
        else:
            st.write("No Trade Items found")


# In[255]:


def main():
    #Title and sidebar
    st.title("NHS Product Information Management System")
    db = create_connection()
    
    #create database (db)
   
    #config['database'] = 'NHS_PIM'
    #db = create_connection()
    
    menu = ["Home", "Search Products", "Suppliers", "Manufacturers", "NHS Provider", "GMDN", "NHS eClass", "Risk Class"]
    options = st.sidebar.radio("Select option : ", menu)
    if options == "Home":
        st.subheader("Welcome to the NHS' Product Information Management System")
        st.write("Navigate from the sidebar to access database")
        
    elif options == "Search Products":
        search_trade_items(db)
        
    elif options == "Suppliers":
        supplier = fetch_all_suppliers(db)
        if supplier:
            st.subheader("All Medical Tech Manufacturers: ")
            df = pd.DataFrame(supplier, columns=['supplier_gln', 'supplier_name', 'supplier_address', 'company_registration_no', 'customer_service_phone', 'customer_service_email'])
            st.dataframe(df)
        else:
            st.write("No Suppliers found")
        
    elif options == "Manufacturers":
        manufacturer = fetch_all_manufacturers(db)
        if manufacturer:
            st.subheader("All Medical Tech Manufacturers: ")
            df = pd.DataFrame(manufacturer, columns=['manufacturer_gln', 'manufacturer_name', 'manufacturer_address', 'company_registration_no', 'customer_service_phone', 'customer_service_email'])
            st.dataframe(df)
        else:
            st.write("No Manufacturers found")
        
    elif options == "NHS Provider":
        provider = fetch_all_providers(db)
        if provider:
            st.subheader("All NHS Providers: ")
            df = pd.DataFrame(provider, columns=['provider_gln', 'provider_name', 'provider_address', 'provider_registration_no'])
            st.dataframe(df)
        else:
            st.write("No NHS Provider found")
        
    elif options == "GMDN":
        gmdn = fetch_all_gmdns(db)
        if gmdn:
            st.subheader("All GMDNs: ")
            df = pd.DataFrame(gmdn, columns=['gmdn_code', 'gmdn_term_name', 'gmdn_term_definition'])
            st.dataframe(df)
        else:
            st.write("No GMDN found")
            
    elif options == "NHS eClass":
        eclass = fetch_all_eclass(db)
        if eclass:
            st.subheader("All NHS eClass codes: ")
            df = pd.DataFrame(eclass, columns=['eclass_code', 'description'])
            st.dataframe(df)
        else:
            st.write("No NHS eClass codes found")
            
    elif options == "Risk Class":
        riskclass = fetch_all_riskclass(db)
        if riskclass:
            st.subheader("All Risk Classes: ")
            df = pd.DataFrame(riskclass, columns=['class_name', 'class_description', 'regulatory_requirements'])
            st.dataframe(df)
        else:
            st.write("No Risk Classes found")
        
    db.close()
    

if __name__ == "__main__":
    main()
        




