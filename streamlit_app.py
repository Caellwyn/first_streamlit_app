import streamlit
import pandas as pd


streamlit.title('My Parents New Healthy Diner')

streamlit.header('🥐Breakfast Menu')
streamlit.text('🥣Omega 3 & Blueberry Oatmeal')
streamlit.text('🥤Kale, Spinach & Rocket Smoothie')
streamlit.text('🥚Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞Avocado Toast')

streamlit.header('🥝🥭Built Your Own Fruit Smoothie🍍🍓')

my_fruit_list = pd.read_csv('https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt')
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they pick the fruit they want to include
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page
streamlit.dataframe(fruits_to_show)

#New Section to display fruityvice api response
streamlit.header('Fruityvale Fruit Advice')

import requests, time
fruityvice_normalized = pd.DataFrame()
fruit_choices = streamlit.text_input('what fruit(s) would you like information about?  Separate fruits with a comma', 'Kiwi')
fruit_choices = fruit_choices.split(',')

for fruit in fruit_choices:
  fruit = fruit.strip()
  fruityvice_response = (requests.get(f"https://fruityvice.com/api/fruit/{fruit}"))
  time.sleep(1)
# streamlit.text(fruityvice_response.json())
# normalize json
  fruityvice_normalized = pd.concat([fruityvice_normalized, pd.json_normalize(fruityvice_response.json())])
# output as table
cols = ['id','name'] + [col for col in fruityvice_normalized.columns if col not in ['id','name']]
fruityvice_normalized = fruityvice_normalized[cols]
streamlit.dataframe(fruityvice_normalized)

import snowflake.connector

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_row = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_row)

new_fruit = streamlit.text_input("Would you like to add a fruit?", "jackfruit")

if new_fruit:
  my_cur.execute('insert into pc_rivery.public.fruit_load_list values (new_fruit)
  streamlit.text(f'Thanks for adding {new_fruit}!')
