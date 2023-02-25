import streamlit
import pandas as pd
import requests, time
import snowflake.connector
from urllib.error import URLError

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

def get_fruityvice_data(fruit_choices):
    fruit_choices = fruit_choices.split(',')
    fruityvice_normalized = pd.DataFrame()

    for fruit in fruit_choices:
      fruit = fruit.strip()
      fruityvice_response = (requests.get(f"https://fruityvice.com/api/fruit/{fruit}"))
      time.sleep(1)
    # streamlit.text(fruityvice_response.json())
    # normalize json
      fruityvice_normalized = pd.concat([fruityvice_normalized, pd.json_normalize(fruityvice_response.json())])
    # return as table
    cols = ['id','name'] + [col for col in fruityvice_normalized.columns if col not in ['id','name']]
    return fruityvice_normalized[cols]

  #New Section to display fruityvice api response
streamlit.header('Fruityvale Fruit Advice')
try:
  fruit_choices = streamlit.text_input('what fruit(s) would you like information about?  Separate fruits with a comma.')
  if not fruit_choices:
    streamlit.error("please select a fruit to get information.")
  else:
    fruityvice_normalized = get_fruityvice_data(fruit_choices)
    streamlit.dataframe(fruityvice_normalized)

except URLError as e:
  streamlit.error()

streamlit.header("The fruit load list contains:")

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
if streamlit.button('Get Fruit Load List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute(f"insert into pc_rivery_db.public.fruit_load_list values ('{new_fruit}')")
    return f'Thanks for adding {new_fruit}!'

new_fruit = streamlit.text_input("Would you like to add a fruit?")
if streamlit.button('Add a Fruit to the List'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    thanks = insert_row_snowflake(new_fruit)
    streamlit.text(thanks)
