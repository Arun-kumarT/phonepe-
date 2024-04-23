import streamlit as st
import pandas as pd
import mysql.connector
from sqlalchemy import create_engine
import plotly.express as px


#sqlalchemy 
config = {'user':'root',    'host':'localhost','password':'1234', 'database':'phonepe'}
connection = mysql.connector.connect(**config)
cursor = connection.cursor()
engine = create_engine('mysql+mysqlconnector://root:1234@localhost/phonepe',echo=False)

cursor.execute("""select State from map_trans;""")
state_result = cursor.fetchall()
state_df = pd.DataFrame(state_result,columns=['State'])
state_list = state_df['State'].unique()


#Streamlit part

st.set_page_config(layout= "wide")

st.title(":rainbow[PHONEPE DATA VISUALIZATION AND EXPLORATION]",)
st.write('Note : Data available from 2018 to 2023')


tab1,tab2,tab3 = st.tabs(['Transaction','User','Statewise Visualization'])
with tab1:
    col1, col2, col3 = st.columns(3)
    with col1:
            sel = st.selectbox('Type',('Transaction Count','Transaction Amount'),key='sel') 
    with col2:     
            year = st.selectbox('Year',('2018','2019','2020','2021','2022','2023'),key ='year')  
    with col3:        
            quarter = st.selectbox('Quarter',('1','2','3','4'),key='quarter')

         
    cursor.execute(f"""SELECT State,sum(Transaction_count) FROM phonepe.agg_trans where Year={year} and quarter={quarter} group by State;""")
    agg_count = cursor.fetchall() 
    agg_count_df = pd.DataFrame(agg_count,columns=['State','Count'])
    agg_count_df = agg_count_df.astype({'Count':'int64'})

    cursor.execute(f"""SELECT State,sum(Transaction_amount) FROM phonepe.agg_trans where Year={year} and quarter={quarter} group by State;""")
    agg_amount = cursor.fetchall() 
    agg_amount_df = pd.DataFrame(agg_amount,columns=['State','Amount'])

    cursor.execute(f"""SELECT District,sum(Transaction_count) FROM phonepe.map_trans where Year={year} and quarter={quarter} group by District;""")
    map_year = cursor.fetchall() 
    map_count_df = pd.DataFrame(map_year,columns=['District','Transaction Count']) 
    map_count_df = map_count_df.astype({'Transaction Count':'int64'})

    cursor.execute(f"""SELECT District,sum(Transaction_amount) FROM phonepe.map_trans where Year={year} and quarter={quarter} group by District;""")
    map_amount = cursor.fetchall() 
    map_amount_df = pd.DataFrame(map_amount,columns=['District','Transaction Amount']) 
    map_amount_df = map_amount_df.astype({'Transaction Amount':'int64'})
    
    cursor.execute(f"""SELECT Pincode,sum(Transaction_amount) FROM phonepe.top_trans where Year={year} and quarter={quarter} group by Pincode;""")
    top_amount = cursor.fetchall() 
    top_amount_df = pd.DataFrame(top_amount,columns=['Pincode','Transaction Amount']) 
    top_amount_df = top_amount_df.astype({'Transaction Amount':'int64'})
    
    cursor.execute(f"""SELECT Pincode,sum(Transaction_count) FROM phonepe.top_trans where Year={year} and quarter={quarter} group by Pincode;""")
    top_count = cursor.fetchall() 
    top_count_df = pd.DataFrame(top_count,columns=['Pincode','Transaction Count']) 
    top_count_df = top_count_df.astype({'Transaction Count':'int64'})

    if sel == 'Transaction Count':                 
            fig = px.choropleth(
            agg_count_df,
            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
            featureidkey='properties.ST_NM',
            locations='State',
            color='Count',
            color_continuous_scale='speed'
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig,use_container_width=True,use_container=True)
            tabs1,tabs2,tabs3 = st.tabs(['States','Districts','Postal Codes'])
            with tabs1:
                st.write(':yellow[Top 10 States]') 
                st.dataframe(agg_count_df.nlargest(10,'Count'),hide_index=True)
            with tabs2:
                st.write(':orange[Top 10 Districts]')
                st.dataframe(map_count_df.nlargest(10,'Transaction Count'),hide_index=True)
            with tabs3:
                st.write(':violet[Top 10 Postal Codes]')
                st.dataframe(top_count_df.nlargest(10,'Transaction Count'),hide_index=True)
    elif sel == 'Transaction Amount':                 
        fig = px.choropleth(
        agg_amount_df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='State',
        color='Amount',
        color_continuous_scale='speed'
        )
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig,use_container_width=True,use_container=True)   

        tabs1,tabs2,tabs3 = st.tabs(['States','Districts','Postal Codes'])
        with tabs1:
            st.write(':red[Top 10 States]')
            st.dataframe(agg_amount_df.nlargest(10,'Amount'),hide_index=True) 
        with tabs2:
            st.write('### :blue[Top 10 Districts]')
            st.dataframe(map_amount_df.nlargest(10,'Transaction Amount'),hide_index=True)
        with tabs3:
            st.write(':green[Top 10 Postal Codes]') 
            st.dataframe(top_amount_df.nlargest(10,'Transaction Amount'),hide_index=True)

with tab2:
    col1,col2 = st.columns(2)
    with col1:
        year2 = st.selectbox('**Year**',('2018','2019','2020','2021','2022'),key='year2') 
    with col2:
        quarter2 = st.selectbox('**Quarter**',('1','2','3','4'),key='quarter2')
   
                     
    cursor.execute(f"""SELECT State,sum(Users_count) as Users FROM phonepe.agg_user where Year={year2} and Quarter={quarter2} group by State;""")
    us_year = cursor.fetchall()
    us_year_df = pd.DataFrame(us_year,columns=['State','Users'])
    us_year_df = us_year_df.astype({'Users':'int64'})

    cursor.execute(f"""SELECT District,sum(Total_users) FROM phonepe.map_user where Year={year2} and Quarter={quarter2} group by District;""")
    map_user = cursor.fetchall() 
    map_user_df = pd.DataFrame(map_user,columns=['District','User Count']) 
    map_user_df = map_user_df.astype({'User Count':'int64'})

    cursor.execute(f"""SELECT Pincode,sum(User_count) FROM phonepe.top_user where Year={year2} and Quarter={quarter2} group by Pincode;""")
    top_user = cursor.fetchall() 
    top_user_df = pd.DataFrame(top_user,columns=['Pincode','User Count']) 
    top_user_df = top_user_df.astype({'User Count':'int64'})

    fig = px.choropleth(
    us_year_df,
    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
    featureidkey='properties.ST_NM',
    locations='State',
    color='Users',
    color_continuous_scale='speed'
    )
    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig,use_container_width=True,use_container=True)
 
    tabs1,tabs2,tabs3 = st.tabs(['States','Districts','Postal Codes'])
    with tabs1:
        st.write('### :rainboe[Top 10 States]')
        st.dataframe(us_year_df.nlargest(10,'Users'),hide_index=True) 
    with tabs2:
        st.write('### :red[Top 10 Districts]')
        st.dataframe(map_user_df.nlargest(10,'User Count'),hide_index=True)
    with tabs3:
        st.write('### :orange[Top 10 Postal Codes]') 
        st.dataframe(top_user_df.nlargest(10,'User Count'),hide_index=True) 
with tab3:
    
    col1, col2,col3 = st.columns(3)
                  
    with col1:     
            state = st.selectbox('State',state_list,key='state')
    with col2: 
            year = st.selectbox('Year',('2018','2019','2020','2021','2022','2023'))  
    with col3:        
            quarter = st.selectbox('**Quarter**',('1','2','3','4'))

 

    cursor.execute(f"""select State,Transaction_count,Transaction_amount,Transaction_type from agg_trans where Year={year} and Quarter={quarter};""")
    agg_trans = cursor.fetchall() 
    agg_trans_df = pd.DataFrame(agg_trans,columns=['State','Transaction_count','Transaction_amount','Transaction_type'])
    agg_trans_df = agg_trans_df[agg_trans_df['State']==state]

    cursor.execute(f"""select State,users_count,Brand,users_precentage from agg_user where Year={year} and Quarter={quarter};""")
    agg_user = cursor.fetchall() 
    agg_user_df = pd.DataFrame(agg_user,columns=['State','User Count','Brand','Percentage'])
    agg_user_df = agg_user_df[agg_user_df['State']==state]
 
    cursor.execute(f"""select State,District,Total_users from map_user where Year={year} and Quarter={quarter};""")
    map_user = cursor.fetchall() 
    map_user_df = pd.DataFrame(map_user,columns=['State','District','User Count'])
    map_user_df = map_user_df[map_user_df['State']==state]
    

    cursor.execute(f"""select State,District,Transaction_count,Transaction_amount from map_trans where Year={year} and Quarter={quarter};""")
    map_trans = cursor.fetchall() 
    map_trans_df = pd.DataFrame(map_trans,columns=['State','District','Count','Amount'])
    map_trans_df = map_trans_df[map_trans_df['State']==state]
   
  
    st.write(f':green[Sum of transactions across different categories in {state} up to {year}]')
    fig = px.bar(agg_trans_df,x='Transaction_type',y='Transaction_amount',labels={'Transaction_type':'Type of Transactions','Transaction_amount':'Transaction Amount'})
    fig.update_traces(marker_color=['red','green','blue','yellow'])
    st.plotly_chart(fig)

    st.write(f':violet[Number of transactions across different categories in {state} up to {year}]')
    fig = px.pie(agg_trans_df,values='Transaction_count',names='Transaction_type',labels={'Transaction_type':'Type of Transactions','Transaction_count':'Transaction Count'})
    fig.update_traces(marker_colors=['red','blue','green','yellow','orange'])
    st.plotly_chart(fig)
    
    st.write(':yellow[District wise Transactions]')
    st.dataframe(map_trans_df,hide_index=True,use_container_width=True)


    st.write(':blue[District wise Users]')
    st.dataframe(map_user_df,hide_index=True,use_container_width=True)

