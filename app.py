import streamlit as st
import requests
import xmltodict

st.title("Veracore Order Info Lookup")
order_id = st.text_input("Enter Order ID:")

# --- Button to trigger API call ---
if st.button("Get Order Info"):
    if not order_id:
        st.warning("Please enter an order ID")
    else:
        # --- SOAP request ---
        url = "https://rhu335.veracore.com/pmomsws/oms.asmx"
        headers = {
            "Content-Type": "text/xml; charset=utf-8",
            "SOAPAction": "http://omscom/GetOrderInfo"
        }

        soap_body = f"""<?xml version="1.0" encoding="utf-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:oms="http://omscom/">
           <soapenv:Header>
              <AuthenticationHeader xmlns="http://omscom/">
                 <Username>YOUR_USERNAME</Username>
                 <Password>YOUR_PASSWORD</Password>
              </AuthenticationHeader>
           </soapenv:Header>
           <soapenv:Body>
              <GetOrderInfo xmlns="http://omscom/">
                 <orderId>{order_id}</orderId>
              </GetOrderInfo>
           </soapenv:Body>
        </soapenv:Envelope>"""

        try:
            response = requests.post(url, data=soap_body, headers=headers)
            response.raise_for_status()
            
            # Parse XML response to dictionary
            data = xmltodict.parse(response.content)
            
            # Navigate to order info
            order_info = data['soap:Envelope']['soap:Body']['GetOrderInfoResponse']['GetOrderInfoResult']

            st.subheader("Order Header")
            st.write(order_info['OrdHead'])

            st.subheader("Shipping Info")
            st.write(order_info['ShipToInfo'])

            st.subheader("Ordered Items")
            for item in order_info['OfferInfo']['OfferType']:
                st.write(f"{item['OfferDesc']} - Qty: {item['OrderQty']} - Price: ${item['UnitPrice']}")
            
        except Exception as e:
            st.error(f"Error fetching order info: {e}")