import streamlit as st
import pandas as pd
import math


# Load your DataFrame
# Replace 'your_data.csv' with the path to your actual data file
df = pd.read_csv('estimation_cleaned.csv')

# Function to predict delivery time
def prediction(warehouse_id1, pincode_id1):
    zone1 = int(pincode_id1 / 100000)
    sub_zone1 = int(pincode_id1 / 10000)
    sorting_district1 = int(pincode_id1 / 1000)
    return predictionHelper(warehouse_id1, pincode_id1, zone1, sub_zone1, sorting_district1)

def predictionHelper(warehouse_id1, pincode_id1, zone1, sub_zone1, sorting_district1):
    l = ['pincode_id', 'sorting_district', 'sub_zone', 'zone']
    l2 = [pincode_id1, sorting_district1, sub_zone1, zone1]
    for i in range(len(l)):
        temp = df[(df[l[i]] == l2[i]) & (df['warehouse_id'] == warehouse_id1)]['delivery_time']
        if not temp.empty:
            return math.ceil(temp.mean())
    for i in range(len(l)):
        temp = df[(df[l[i]] == l2[i])]['delivery_time']
        if not temp.empty:
            return math.ceil(temp.mean())
    # If no match found, return a default value or handle appropriately
    return None

# Streamlit UI
def main():
    st.title('Delivery Estimation App')
    # warehouse_id = st.number_input('Enter Warehouse ID', min_value=1)
    pincode_id = st.number_input('Enter Pincode ID', min_value=100000, max_value=999999)
    warehouse_id = st.selectbox(
   'Warehouse ID',
   ("14","28","61","66", "68", "86","96","117","134","150","173","175"),
   index=None,
   placeholder="select from available warehouses",
)

    if st.button('Predict Delivery Time'):
        if warehouse_id and pincode_id:
            delivery_time = prediction(warehouse_id, pincode_id)
            if delivery_time:
                st.success(f'Estimated Delivery Time: {delivery_time} days')
            else:
                st.warning('No matching data found for the given inputs.')
        else:
            st.warning('Please enter valid inputs.')

if __name__ == '__main__':
    main()
