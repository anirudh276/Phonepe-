import streamlit as st
import json
import sys
import mysql.connector
import pandas as pd
import plotly.express as px
import csv
import io

mydb = mysql.connector.connect(user='root', password='', host='mydesk.tk', database='phonepe_pulse')

# create a cursor object
mycursor = mydb.cursor()

st.title('PhonePe Pulse')
metric_options = ['User', 'Transaction']
selected_metric = st.selectbox('Select User or Transaction', metric_options)

metric_options1 = ['2018', '2019','2020','2021','2022']
selected_metric1 = st.selectbox('Select a year', metric_options1)

if(selected_metric1):
    metric_options2 = ['Q1 (JAN - MAR)', 'Q2 (APR - JUN)','Q3 (JUL - SEP)','Q4 (OCT - DEC)']
    selected_metric2 = st.selectbox('Select a quarter', metric_options2)



# Create a container for the card with the "shadow" class
if(selected_metric=='User'):    
    with st.container():
        # Add content to the card
        #st.image("my_image.png")
        st.title(selected_metric)
        st.subheader("Registered PhonePe users till "+selected_metric2)
        index=metric_options2.index(selected_metric2)+1
        mycursor.execute(f"SELECT * FROM `aggregated` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

        rows = mycursor.fetchall()
        result = []
        columns = [col[0] for col in mycursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        json_result = json.dumps(result)

        json_result1=json.loads(json_result)
        st.header(json_result1[0]['registered users count'])
        
        
        
        
        
        st.subheader("PhonePe app opens in "+selected_metric2)
        mycursor1 = mydb.cursor()
        mycursor1.execute(f"SELECT * FROM `aggregated` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

        rows1 = mycursor.fetchall()
        result1 = []
        columns1 = [col[0] for col in mycursor1.description]
        for row in rows1:
            result1.append(dict(zip(columns1, row)))

        json_result1 = json.dumps(result1)

        json_result2=json.loads(json_result1)
        st.header(json_result2[0]['app opens'])
        # st.header(data['data']['aggregated']['registeredUsers'])
        
        
        
        
        
        col1, col2, col3 = st.columns(3)
        if col1.button('States'):
            st.subheader("Top 10 States")
            col4,col5=st.columns(2)
            index=metric_options2.index(selected_metric2)+1
            mycursor.execute(f"SELECT * FROM `statesuser` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

            rows = mycursor.fetchall()
            result = []
            columns = [col[0] for col in mycursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))
            json_result = json.dumps(result)

            json_result1=json.loads(json_result)
            j=1
            for i in json_result1:
                col4.write(str(j)+"  "+i['state'].capitalize())
                col5.write(i['count'])
                j+=1
        if col2.button('Districts'):
            st.subheader("Top 10 districts")
            col4,col5=st.columns(2)
            index=metric_options2.index(selected_metric2)+1
            mycursor.execute(f"SELECT * FROM `districtsusers` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

            rows = mycursor.fetchall()
            result = []
            columns = [col[0] for col in mycursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))

            json_result = json.dumps(result)

            json_result1=json.loads(json_result)
            j=1
            for i in json_result1:
                col4.write(str(j)+"  "+i['district'].capitalize())
                col5.write(i['count'])
                j+=1

        if col3.button('Pin Code'):
            st.subheader("Top 10 Pincodes")

            col4,col5=st.columns(2)
            index=metric_options2.index(selected_metric2)+1
            mycursor.execute(f"SELECT * FROM `pincodeusers` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

            rows = mycursor.fetchall()
            result = []
            columns = [col[0] for col in mycursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))

            json_result = json.dumps(result)

            json_result1=json.loads(json_result)
            j=1
            for i in json_result1:
                col4.write(str(j)+"  "+i['pincode'].capitalize())
                col5.write(i['count'])
                j+=1

    
    
    




    
if(selected_metric=='Transaction'):        
    try:
        index=metric_options2.index(selected_metric2)+1
        with open("E:/ani  proj/pulse/data/aggregated/user/country/india/{}/{}.json".format(selected_metric1,index), "r") as f:
            data = json.load(f)
            print(data)
    # code block to try
    except OSError:
        print("Could not open/read file:", f)
        sys.exit()


# Create a container for the card with the "shadow" class
if(selected_metric=='Transaction'):    
    with st.container():
        # Add content to the card
        #st.image("my_image.png")
        st.title(selected_metric)
        st.subheader("All PhonePe transactions (UPI + Cards + Wallets)")
        st.header(data['data']['aggregated']['registeredUsers'])
        st.write("Total payment value")
        st.header(12345658)
        st.write("Avg. transaction value")   
        st.header(789456532)
        st.markdown("<hr>", unsafe_allow_html=True)
        st.header("Categories")
        col1,col2=st.columns(2)
        # with open("C:/Users/Administrator/Downloads/pulse-master/data/aggregated/transaction/country/india/{}/{}.json".format(selected_metric1,index), "r") as f:
        #     data = json.load(f)
        index=metric_options2.index(selected_metric2)+1
        mycursor.execute(f"SELECT * FROM `aggregated` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")
        rows = mycursor.fetchall()
        result = []
        columns = [col[0] for col in mycursor.description]
        for row in rows:
            result.append(dict(zip(columns, row)))

        json_result = json.dumps(result)

        json_result1=json.loads(json_result)
        # for i in range(5):
        lst=['Recharge & bill payments','Peer-to-peer payments','Merchant payments','Financial Services','Others']
        print(json_result1)
        for i in lst:
            col1.write(i)
            col2.write(json_result1[0][f"{i}"])
        st.markdown("<hr>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        if col1.button('States'):
            st.subheader("Top 10 States")

            col4,col5=st.columns(2)
            index=metric_options2.index(selected_metric2)+1
            mycursor.execute(f"SELECT * FROM `statestransaction` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

            rows = mycursor.fetchall()
            result = []
            columns = [col[0] for col in mycursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))

            json_result = json.dumps(result)

            json_result1=json.loads(json_result)
            j=1
            for i in json_result1:
                col4.write(str(j)+"  "+i['state'].capitalize())
                col5.write(i['count'])
                j+=1

        if col2.button('Districts'):
            st.subheader("Top 10 districts")
            col4,col5=st.columns(2)
            index=metric_options2.index(selected_metric2)+1
            mycursor.execute(f"SELECT * FROM `districtstransaction` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

            rows = mycursor.fetchall()
            result = []
            columns = [col[0] for col in mycursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))

            json_result = json.dumps(result)

            json_result1=json.loads(json_result)
            j=1
            for i in json_result1:
                col4.write(str(j)+"  "+i['district'].capitalize())
                col5.write(i['count'])
                j+=1

        if col3.button('Pin Code'):
            st.subheader("Top 10 Pincodes")
            col4,col5=st.columns(2)
            index=metric_options2.index(selected_metric2)+1
            mycursor.execute(f"SELECT * FROM `pincodetransaction` WHERE year={selected_metric1} AND q={index} AND type='{selected_metric}'")

            rows = mycursor.fetchall()
            result = []
            columns = [col[0] for col in mycursor.description]
            for row in rows:
                result.append(dict(zip(columns, row)))

            json_result = json.dumps(result)

            json_result1=json.loads(json_result)
            j=1
            for i in json_result1:
                col4.write(str(j)+"  "+i['pincode'].capitalize())
                col5.write(i['count'])
                j+=1


if(selected_metric=="Transaction"):
    with open("E:/ani  proj/pulse/data/map/transaction/hover/country/india/{}/{}.json".format(selected_metric1,index), "r") as f:
        data = json.load(f)
        da=[]
        
        for i in data["data"]["hoverDataList"]:
            d={}
            i["name"].capitalize()
            words = i["name"].split()
            capitalized_words = [word.capitalize() for word in words]
            capitalized_state_name = " ".join(capitalized_words)
           
            d["state"]=capitalized_state_name
            d["count"]=i["metric"][0]["count"]
            da.append(d)
            
    csv_file = io.StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(da[0].keys())
    for data in da:
        writer.writerow(data.values())
    print(csv_file.getvalue())
    csv_file1 = io.StringIO(csv_file.getvalue())


    df = pd.read_csv(csv_file1)

    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='count',
        color_continuous_scale='Reds'
    )

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)

if(selected_metric=="User"):
    with open("E:/ani  proj/pulse/data/map/transaction/hover/country/india/{}/{}.json".format(selected_metric1,index), "r") as f0:
        dat = json.load(f0)
        da1=[]
        
        for i in dat["data"]["hoverDataList"]:
            da1.append(i["name"])
    with open("E:/ani  proj/pulse/data/map/user/hover/country/india/{}/{}.json".format(selected_metric1,index), "r") as f:
        data = json.load(f)
        da=[]
        
        for i in da1:
            d1={}
            words = i.split()
            capitalized_words = [word.capitalize() for word in words]
            capitalized_state_name = " ".join(capitalized_words)
           
            d1["state"]=capitalized_state_name
            d1["users"]=data["data"]["hoverData"][i]["registeredUsers"]
            da.append(d1)
            #print(data["data"]["hoverData"][i]["registeredUsers"])
            
    csv_file = io.StringIO()
    writer = csv.writer(csv_file)
    writer.writerow(da[0].keys())
    for data in da:
        writer.writerow(data.values())
    print(csv_file.getvalue())
    csv_file1 = io.StringIO(csv_file.getvalue())


    df = pd.read_csv(csv_file1)

    fig = px.choropleth(
        df,
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        locations='state',
        color='users',
        color_continuous_scale='Reds'
    )

    fig.update_geos(fitbounds="locations", visible=False)
    st.plotly_chart(fig)
