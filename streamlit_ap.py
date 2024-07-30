# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd
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
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)
#st.stop()

pd_df=my_dataframe.to_pandas()
#st.dataframe(pd_df)
#st.stop

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections=5
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
        
        search_on=pd_df.loc[pd_df['FRUIT_NAME'] == fruit_chosen, 'SEARCH_ON'].iloc[0]
        st.write('The search value for ', fruit_chosen,' is ', search_on, '.')

        st.subheader(fruit_chosen + 'Nutrition Information')
        fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_chosen)
        fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
    
    #st.write(ingredients_string)


    
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients)
            values ('""" + ingredients_string + """','"""+name_on_order+"""')"""

    #st.write(my_insert_stmt)
    time_to_insert = st.button('Submit Order')

    
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        
        st.success('Your Smoothie is ordered!')


