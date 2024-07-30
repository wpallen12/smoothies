# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom smoothie!
    """
)


#Giving names to the order
name_on_order = st.text_input('Name On Smoothie') 
st.write('The name on your Smoothie will be:', name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
st.dataframe(data=my_dataframe, use_container_width=True)

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe
)

# CLEAN UP THE LIST TO NOT SHOW ANYTHING UNLESS INGREDIENTS HAVE BEEN SELECTED
# All this if block is saying is if the ingredients list exists(is not null) display it as a list and also write it

#if ingredients_list:
    #st.write(ingredients_list)
   # st.text(ingredients_list)
# We want our ingreients list table to be a string
if ingredients_list:
    ingredients_string = '' #setting ingredients string to be empty
    #add a for loop to go through each row in the ingredients list
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '#the += simply adds to what is already in the variable, so each time the loop runs a new fruit will be added to the string 
    
    #st.write(ingredients_string)


    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!')

import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response.json())
fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)

