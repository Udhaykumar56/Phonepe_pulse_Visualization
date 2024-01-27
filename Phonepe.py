import json
import streamlit as st
import pandas as pd
import requests
import psycopg2
import plotly.express as px
import plotly.graph_objects as go
from streamlit_option_menu import option_menu
from PIL import Image

#sql connection

mydb=psycopg2.connect(host="localhost",
                     user="postgres",
                     password="Born@1998",
                     database="Phonepe_data",
                     port="5432")
cursor=mydb.cursor()

#Creating DATAFRAMES FROM SQL

#Aggregated_insurance_data

cursor.execute("select * from aggregated_insurance;")
mydb.commit()
table1 = cursor.fetchall()

Agg_insurance = pd.DataFrame(table1,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_transaction_data

cursor.execute("select * from aggregated_transaction;")
mydb.commit()
table2 = cursor.fetchall()

Agg_transaction = pd.DataFrame(table2,columns = ("States", "Years", "Quarter", "Transaction_type", "Transaction_count","Transaction_amount"))

#Aggregated_user_data

cursor.execute("select * from aggregated_user;")
mydb.commit()
table3 = cursor.fetchall()

Agg_user = pd.DataFrame(table3,columns = ("States", "Years", "Quarter", "Brands", "Transaction_count","Percentage"))

#Creating DATAFRAMES FROM SQL

#Map_insurance

cursor.execute("select * from map_insurance;")
mydb.commit()
table4 = cursor.fetchall()

Map_insurance = pd.DataFrame(table4,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_transaction

cursor.execute("select * from map_transaction;")
mydb.commit()
table5 = cursor.fetchall()

Map_transaction = pd.DataFrame(table5,columns = ("States", "Years", "Quarter", "Districts", "Transaction_count","Transaction_amount"))

#Map_user

cursor.execute("select * from map_user;")
mydb.commit()
table6 = cursor.fetchall()

Map_user = pd.DataFrame(table6,columns = ("States", "Years", "Quarter", "Districts", "Registered_users","App_opens"))

#Creating DATAFRAMES FROM SQL

#Top_insurance

cursor.execute("select * from top_insurance;")
mydb.commit()
table7 = cursor.fetchall()

Top_insurance = pd.DataFrame(table7,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_transaction

cursor.execute("select * from top_transaction;")
mydb.commit()
table8 = cursor.fetchall()

Top_transaction = pd.DataFrame(table8,columns = ("States", "Years", "Quarter", "Pincodes", "Transaction_count", "Transaction_amount"))

#Top_user

cursor.execute("select * from top_user;")
mydb.commit()
table9 = cursor.fetchall()

Top_user = pd.DataFrame(table9,columns = ("States", "Years", "Quarter", "Pincodes", "Registered_users"))

def Aggre_insurance_Year(df,year):
    aiy= df[df["Years"] == year]
    aiy.reset_index(drop= True, inplace= True)

    aiyg=aiy.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_amount= px.bar(aiyg, x="States", y= "Transaction_amount",title= f"{year} TRANSACTION AMOUNT",
                           width=600, height= 650, color_discrete_sequence=px.colors.sequential.Agsunset)
        st.plotly_chart(fig_amount)
    with col2:

        fig_count= px.bar(aiyg, x="States", y= "Transaction_count",title= f"{year} TRANSACTION COUNT",
                          width=600, height= 650, color_discrete_sequence=px.colors.sequential.Bluered_r)
        st.plotly_chart(fig_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()
        

        fig_india_1= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Rainbow",
                                 range_color= (aiyg["Transaction_amount"].min(),aiyg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2= px.choropleth(aiyg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyg["Transaction_count"].min(),aiyg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{year} TRANSACTION COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2)

    return aiy

def Aggre_insurance_Y_Q(df,quarter):
    aiyq= df[df["Quarter"] == quarter]
    aiyq.reset_index(drop= True, inplace= True)

    aiyqg= aiyq.groupby("States")[["Transaction_count", "Transaction_amount"]].sum()
    aiyqg.reset_index(inplace= True)

    col1,col2= st.columns(2)

    with col1:
        fig_q_amount= px.bar(aiyqg, x= "States", y= "Transaction_amount", 
                            title= f"{aiyq['Years'].min()} AND {quarter} INSURANCE AMOUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Burg_r)
        st.plotly_chart(fig_q_amount)

    with col2:
        fig_q_count= px.bar(aiyqg, x= "States", y= "Transaction_count", 
                            title= f"{aiyq['Years'].min()} AND {quarter} INSURANCE COUNT",width= 600, height=650,
                            color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_q_count)

    col1,col2= st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response= requests.get(url)
        data1= json.loads(response.content)
        states_name_tra= [feature["properties"]["ST_NM"] for feature in data1["features"]]
        states_name_tra.sort()

        fig_india_1= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_amount", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_amount"].min(),aiyqg["Transaction_amount"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} INSURANCE AMOUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_1.update_geos(visible =False)
        
        st.plotly_chart(fig_india_1,use_container_width=True)
    with col2:

        fig_india_2= px.choropleth(aiyqg, geojson= data1, locations= "States", featureidkey= "properties.ST_NM",
                                 color= "Transaction_count", color_continuous_scale= "Sunsetdark",
                                 range_color= (aiyqg["Transaction_count"].min(),aiyqg["Transaction_count"].max()),
                                 hover_name= "States",title = f"{aiyq['Years'].min()} AND {quarter} INSURANCE COUNT",
                                 fitbounds= "locations",width =600, height= 600)
        fig_india_2.update_geos(visible =False)
        
        st.plotly_chart(fig_india_2,use_container_width=True)
    
    return aiyq

def Aggre_Transaction_type(df, state):
    df_state= df[df["States"] == state]
    df_state.reset_index(drop= True, inplace= False)

    agttg= df_state.groupby("Transaction_type")[["Transaction_count", "Transaction_amount"]].sum()
    agttg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:

        fig_hbar_1= px.bar(agttg, x= "Transaction_count", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Mint_r, width= 600, 
                        title= f"{state} TRANSACTION TYPES AND TRANSACTION COUNT",height= 500)
        st.plotly_chart(fig_hbar_1)

    with col2:

        fig_hbar_2= px.bar(agttg, x= "Transaction_amount", y= "Transaction_type", orientation="h",
                        color_discrete_sequence=px.colors.sequential.Greens_r, width= 600,
                        title= f"{state} TRANSACTION TYPES AND TRANSACTION AMOUNT", height= 500)
        st.plotly_chart(fig_hbar_2)  

    return df_state

def Aggre_user_plot_1(df,year):
    aguy= df[df["Years"] == year]
    aguy.reset_index(drop= True, inplace= True)
    
    aguyg= pd.DataFrame(aguy.groupby("Brands")["Transaction_count"].sum())
    aguyg.reset_index(inplace= True)

    fig_line_1= px.bar(aguyg, x="Brands",y= "Transaction_count", title=f"{year} BRANDS AND TRANSACTION COUNT",
                    width=1000,color_discrete_sequence=px.colors.sequential.haline_r)
    st.plotly_chart(fig_line_1)

    return aguy

def Aggre_user_plot_2(df,quarter):
    auqs= df[df["Quarter"] == quarter]
    auqs.reset_index(drop= True, inplace= True)

    fig_pie_1= px.pie(data_frame=auqs, names= "Brands", values="Transaction_count", hover_data= "Percentage",
                      width=1000,title=f"{quarter} QUARTER TRANSACTION COUNT PERCENTAGE",hole=0.5, color_discrete_sequence= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_pie_1)

    return auqs

def Aggre_user_plot_3(df,state):
    aguqy= df[df["States"] == state]
    aguqy.reset_index(drop= True, inplace= True)

    aguqyg= pd.DataFrame(aguqy.groupby("Brands")["Transaction_count"].sum())
    aguqyg.reset_index(inplace= True)

    fig_scatter_1= px.line(aguqyg, x= "Brands", y= "Transaction_count", markers= True,width=1000)
    st.plotly_chart(fig_scatter_1)

    return aguqy

def map_insure_plot_1(df,state):
    miys= df[df["States"] == state]
    miysg= miys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    miysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height=500, title= f"{state} DISTRICTS INSURANCE AMOUNT",
                              color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_bar_1)

    with col2:
        fig_map_bar_1= px.bar(miysg, x= "Districts", y= "Transaction_count",
                              width=600, height= 500, title= f"{state} DISTRICTS INSURANCE COUNT",
                              color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_bar_1)

    return miys

def map_insure_plot_2(df,state):
    mtys= df[df["States"] == state]
    mtysg= mtys.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    mtysg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_pie_1= px.pie(mtysg, names= "Districts", values= "Transaction_amount",
                              width=600, height=500, title= f"{state} DISTRICTS TRANSACTION AMOUNT",
                              hole=0.5,color_discrete_sequence= px.colors.sequential.Mint_r)
        st.plotly_chart(fig_map_pie_1)

    with col2:
        fig_map_pie_1= px.pie(mtysg, names= "Districts", values= "Transaction_count",
                              width=600, height= 500, title= f"{state.upper()} DISTRICTS TRANSACTION COUNT",
                              hole=0.5,  color_discrete_sequence= px.colors.sequential.Oranges_r)
        
        st.plotly_chart(fig_map_pie_1)
    return mtys

def map_user_plot_1(df, year):
    muy= df[df["Years"] == year]
    muy.reset_index(drop= True, inplace= True)
    muyg= muy.groupby("States")[["Registered_users", "App_opens"]].sum()
    muyg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyg, x= "States", y= ["Registered_users","App_opens"], markers= True,
                                width=1000,height=800,title= f"{year} REGISTERED USER AND APPOPENS", color_discrete_sequence= px.colors.sequential.Viridis_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muy

def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"] == quarter]
    muyq.reset_index(drop= True, inplace= True)
    muyqg= muyq.groupby("States")[["Registered_users", "App_opens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_map_user_plot_1= px.line(muyqg, x= "States", y= ["Registered_users","App_opens"], markers= True,
                                title= f"{df['Years'].min()}, {quarter} QUARTER REGISTERED USER AND APPOPENS",
                                width= 1000,height=800,color_discrete_sequence= px.colors.sequential.Rainbow_r)
    st.plotly_chart(fig_map_user_plot_1)

    return muyq

def map_user_plot_3(df, state):
    muyqs= df[df["States"] == state]
    muyqs.reset_index(drop= True, inplace= True)
    muyqsg= muyqs.groupby("Districts")[["Registered_users", "App_opens"]].sum()
    muyqsg.reset_index(inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_plot_1= px.bar(muyqsg, x= "Registered_users",y= "Districts",orientation="h",
                                    title= f"{state.upper()} REGISTERED USER",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow_r)
        st.plotly_chart(fig_map_user_plot_1)

    with col2:
        fig_map_user_plot_2= px.bar(muyqsg, x= "App_opens", y= "Districts",orientation="h",
                                    title= f"{state.upper()} APPOPENS",height=800,
                                    color_discrete_sequence= px.colors.sequential.Rainbow)
        st.plotly_chart(fig_map_user_plot_2)
    return muyqs

def top_user_plot_1(df,year):
    tuy= df[df["Years"] == year]
    tuy.reset_index(drop= True, inplace= True)

    tuyg= pd.DataFrame(tuy.groupby(["States","Quarter"])["Registered_users"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuyg, x= "States", y= "Registered_users", barmode= "group", color= "Quarter",
                            width=1000, height= 800, color_continuous_scale= px.colors.sequential.Burgyl)
    st.plotly_chart(fig_top_plot_1)

    return tuy

def top_user_plot_2(df,state):
    tuys= df[df["States"] == state]
    tuys.reset_index(drop= True, inplace= True)

    tuysg= pd.DataFrame(tuys.groupby("Quarter")["Registered_users"].sum())
    tuysg.reset_index(inplace= True)

    fig_top_plot_1= px.bar(tuys, x= "Quarter", y= "Registered_users",barmode= "group",
                           width=1000, height= 800,color= "Pincodes",hover_data="Pincodes",
                            color_continuous_scale= px.colors.sequential.Magenta)
    st.plotly_chart(fig_top_plot_1)
    return tuys

def ques1():
    brand= Agg_user[["Brands","Transaction_count"]]
    brand1= brand.groupby("Brands")["Transaction_count"].sum().sort_values(ascending=False)
    brand2= pd.DataFrame(brand1).reset_index()

    fig_brands= px.pie(brand2, values= "Transaction_count", names= "Brands", color_discrete_sequence=px.colors.sequential.dense_r,
                       title= "Top Mobile Brands of Transaction_count")
    return st.plotly_chart(fig_brands)

def ques2():
    lt= Agg_transaction[["States", "Transaction_amount"]]
    lt1= lt.groupby("States")["Transaction_amount"].sum().sort_values(ascending= True)
    lt2= pd.DataFrame(lt1).reset_index().head(10)

    fig_lts= px.bar(lt2, x= "States", y= "Transaction_amount",title= "LOWEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques3():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=False)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF HIGHEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Emrld_r)
    return st.plotly_chart(fig_htd)

def ques4():
    htd= Map_transaction[["Districts", "Transaction_amount"]]
    htd1= htd.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    htd2= pd.DataFrame(htd1).head(10).reset_index()

    fig_htd= px.pie(htd2, values= "Transaction_amount", names= "Districts", title="TOP 10 DISTRICTS OF LOWEST TRANSACTION AMOUNT",
                    color_discrete_sequence=px.colors.sequential.Greens_r)
    return st.plotly_chart(fig_htd)

def ques5():
    sa= Map_user[["States", "App_opens"]]
    sa1= sa.groupby("States")["App_opens"].sum().sort_values(ascending=False)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "App_opens", title="Top 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.deep_r)
    return st.plotly_chart(fig_sa)

def ques6():
    sa= Map_user[["States", "App_opens"]]
    sa1= sa.groupby("States")["App_opens"].sum().sort_values(ascending=True)
    sa2= pd.DataFrame(sa1).reset_index().head(10)

    fig_sa= px.bar(sa2, x= "States", y= "App_opens", title="lowest 10 States With AppOpens",
                color_discrete_sequence= px.colors.sequential.dense_r)
    return st.plotly_chart(fig_sa)

def ques7():
    stc= Agg_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=True)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH LOWEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Jet_r)
    return st.plotly_chart(fig_stc)

def ques8():
    stc= Agg_transaction[["States", "Transaction_count"]]
    stc1= stc.groupby("States")["Transaction_count"].sum().sort_values(ascending=False)
    stc2= pd.DataFrame(stc1).reset_index()

    fig_stc= px.bar(stc2, x= "States", y= "Transaction_count", title= "STATES WITH HIGHEST TRANSACTION COUNT",
                    color_discrete_sequence= px.colors.sequential.Magenta_r)
    return st.plotly_chart(fig_stc)

def ques9():
    ht= Agg_transaction[["States", "Transaction_amount"]]
    ht1= ht.groupby("States")["Transaction_amount"].sum().sort_values(ascending= False)
    ht2= pd.DataFrame(ht1).reset_index().head(10)

    fig_lts= px.bar(ht2, x= "States", y= "Transaction_amount",title= "HIGHEST TRANSACTION AMOUNT and STATES",
                    color_discrete_sequence= px.colors.sequential.Oranges_r)
    return st.plotly_chart(fig_lts)

def ques10():
    dt= Map_transaction[["Districts", "Transaction_amount"]]
    dt1= dt.groupby("Districts")["Transaction_amount"].sum().sort_values(ascending=True)
    dt2= pd.DataFrame(dt1).reset_index().head(50)

    fig_dt= px.bar(dt2, x= "Districts", y= "Transaction_amount", title= "DISTRICTS WITH LOWEST TRANSACTION AMOUNT",
                color_discrete_sequence= px.colors.sequential.Mint_r)
    return st.plotly_chart(fig_dt)

#Streamlit part

st.set_page_config(layout= "wide")

st.title(":violet[PHONEPE DATA VISUALIZATION AND EXPLORATION ]" )
st.write("")

with st.sidebar:

        select = option_menu("Menu", ["Home","Explore Data","Top Charts","About"], 
                icons=["house","graph-up-arrow","bar-chart-line", "exclamation-circle"],
                menu_icon= "menu-button-wide",
                default_index=0,
                styles={"nav-link": {"font-size": "20px", "text-align": "left", "margin": "-2px", "--hover-color": "#6F36AD"},
                        "nav-link-selected": {"background-color": "#6F36AD"}})

if select == "Home":
    img = Image.open(r"C:\Users\udhay\OneDrive\Desktop\New folder\PhonePe\img.png")
    st.image(img)
    col1,col2= st.columns([3,2],gap="medium")
        
    with col1:
        st.title(":violet[PHONEPE]")
        st.subheader(":violet[INDIA'S BEST TRANSACTION APP]")
        st.markdown("### :violet[PhonePe  is an Indian digital payments and financial technology company]")
        st.write("### :black[****FEATURES****]")
        st.write("### :violet[****Credit & Debit card linking****]")
        st.write("### :violet[****Bank Balance check****]")
        st.write("### :violet[****PIN Authorization****]")
        st.write("### :violet[****Easy Transactions****]")
        st.write("### :violet[****One App For All Your Payments****]")
        st.write("### :violet[****Multiple Payment Modes****]")
        st.write("### :violet[****PhonePe Merchants****]")
        st.write("### :violet[****Multiple Ways To Pay****]")
        st.write("### :violet[****1.Direct Transfer & More****]")
        st.write("### :violet[****2.QR Code****]")
        st.write("### :violet[****Earn Great Rewards****]")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")

    with col2:
        st.video("C:\\Users\\udhay\\OneDrive\\Desktop\\New folder\\PhonePe\\Phone pe Ad video.mp4")


if select == "Explore Data":
    tab1, tab2, tab3= st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:
        method = st.radio("**Select the Analysis Method**",["Insurance Analysis", "Transaction Analysis", "User Analysis"])

        if method == "Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years = st.selectbox("**Select the Year**", Agg_insurance["Years"].unique())

            df_agg_insur_Y= Aggre_insurance_Year(Agg_insurance,int(years))
            
            with col1,col2:
                quarters= st.selectbox("**Select the Quarter**", df_agg_insur_Y["Quarter"].unique())
                
            Aggre_insurance_Y_Q(df_agg_insur_Y, quarters)
    
        elif method == "Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_at = st.selectbox("**Select the Year**", (Agg_transaction["Years"].unique()))

            df_agg_tran_Y= Aggre_insurance_Year(Agg_transaction,years_at)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_at = st.selectbox("**Select the Quarter**", (df_agg_tran_Y["Quarter"].unique()))
            
            df_agg_tran_Y_Q = Aggre_insurance_Y_Q(df_agg_tran_Y, quarters_at)
            
            #Select the State for analyzing the Transaction type
            state_Y_Q= st.selectbox("**Select the State**",df_agg_tran_Y_Q["States"].unique())

            Aggre_Transaction_type(df_agg_tran_Y_Q,state_Y_Q)

        elif method == "User Analysis":
            year_au= st.selectbox("Select the Year_AU",Agg_user["Years"].unique())
            agg_user_Y= Aggre_user_plot_1(Agg_user,year_au)

            quarter_au= st.selectbox("Select the Quarter_AU",agg_user_Y["Quarter"].unique())
            agg_user_Y_Q= Aggre_user_plot_2(agg_user_Y,quarter_au)

            state_au= st.selectbox("**Select the State_AU**",agg_user_Y["States"].unique())
            Aggre_user_plot_3(agg_user_Y_Q,state_au)

    with tab2:
        method_map = st.radio("**Select the Analysis Method(MAP)**",["Map Insurance Analysis", "Map Transaction Analysis", "Map User Analysis"])

        if method_map == "Map Insurance Analysis":
            col1,col2,col3= st.columns(3)
            with col1:
                years_m1= st.selectbox("**Select the Year_mi**", (Map_insurance["Years"].unique()))

            df_map_insur_Y= Aggre_insurance_Year(Map_insurance,years_m1)

            col1,col2= st.columns(2)
            with col1:
                state_m1= st.selectbox("Select the State_mi", df_map_insur_Y["States"].unique())

            map_insure_plot_1(df_map_insur_Y,state_m1)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m1= st.selectbox("**Select the Quarter_mi**", (df_map_insur_Y["Quarter"].unique()))

            df_map_insur_Y_Q= Aggre_insurance_Y_Q(df_map_insur_Y, quarters_m1)

            col1,col2= st.columns(2)  
            with col1:
                state_m2= st.selectbox("Select the State", df_map_insur_Y_Q["States"].unique())            
                
            map_insure_plot_2(df_map_insur_Y_Q, state_m2)

        elif method_map == "Map Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_m2= st.selectbox("**Select the Year_mi**", (Map_transaction["Years"].unique()))

            df_map_tran_Y= Aggre_insurance_Year(Map_transaction, years_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m3= st.selectbox("Select the State_mi", df_map_tran_Y["States"].unique())

            map_insure_plot_1(df_map_tran_Y,state_m3)
            
            col1,col2= st.columns(2)
            with col1:
                quarters_m2= st.selectbox("**Select the Quarter_mi**", (df_map_tran_Y["Quarter"].unique()))

            df_map_tran_Y_Q= Aggre_insurance_Y_Q(df_map_tran_Y, quarters_m2)

            col1,col2= st.columns(2)
            with col1:
                state_m4= st.selectbox("Select the State_miy", df_map_tran_Y_Q["States"].unique())            
            
            map_insure_plot_2(df_map_tran_Y_Q, state_m4)

        elif method_map == "Map User Analysis":
            col1,col2= st.columns(2)
            with col1:
                year_mu1= st.selectbox("**Select the Year_mu**",Map_user["Years"].unique())
            map_user_Y= map_user_plot_1(Map_user, year_mu1)

            col1,col2= st.columns(2)
            with col1:
                quarter_mu1= st.selectbox("**Select the Quarter_mu**",map_user_Y["Quarter"].unique())
            map_user_Y_Q= map_user_plot_2(map_user_Y,quarter_mu1)

            col1,col2= st.columns(2)
            with col1:
                state_mu1= st.selectbox("**Select the State_mu**",map_user_Y_Q["States"].unique())
            map_user_plot_3(map_user_Y_Q, state_mu1)

    with tab3:
        method_top = st.radio("**Select the Analysis Method(TOP)**",["Top Insurance Analysis", "Top Transaction Analysis", "Top User Analysis"])

        if method_top == "Top Insurance Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t1= st.selectbox("**Select the Year_ti**", (Top_insurance["Years"].unique()))
            df_top_insur_Y= Aggre_insurance_Year(Top_insurance,years_t1)

            with col2:
                quarters_t1= st.selectbox("**Select the Quarter_ti**", (df_top_insur_Y["Quarter"].unique()))

            df_top_insur_Y_Q= Aggre_insurance_Y_Q(df_top_insur_Y, quarters_t1)

        
        elif method_top == "Top Transaction Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t2= st.selectbox("**Select the Year_tt**", (Top_transaction["Years"].unique()))
 
            df_top_tran_Y= Aggre_insurance_Year(Top_transaction,years_t2)

            
            col1,col2= st.columns(2)
            with col1:
                quarters_t2= st.selectbox("**Select the Quarter_tt**", (df_top_tran_Y["Quarter"].unique()))

            df_top_tran_Y_Q= Aggre_insurance_Y_Q(df_top_tran_Y, quarters_t2)

        elif method_top == "Top User Analysis":
            col1,col2= st.columns(2)
            with col1:
                years_t3= st.selectbox("**Select the Year_tu**", Top_user["Years"].unique())

            df_top_user_Y= top_user_plot_1(Top_user,years_t3)

            col1,col2= st.columns(2)
            with col1:
                state_t3= st.selectbox("**Select the State_tu**", df_top_user_Y["States"].unique())

            df_top_user_Y_S= top_user_plot_2(df_top_user_Y,state_t3)


if select == "Top Charts":

    ques= st.selectbox("**Select the Question**",('What are the preeminent mobile phone brands that are commonly utilized?',
                                                  'Which states have the lowest transaction amounts?',
                                                'Which districts exhibit the highest transaction amounts?',
                                                'Which are the ten districts with the lowest transaction amounts?',
                                                'Which are the top 10 states with the highest number of app opens?',
                                                'Which are the ten states with the least number of app opens?',
                                                'Which states have the lowest transaction count?',
                                                'Which states have the highest transaction count?',
                                                'Which states have the highest transaction amounts?',
                                                'Which are the top 50 districts with the lowest transaction amounts?'))
    
    if ques=="What are the preeminent mobile phone brands that are commonly utilized?":
        ques1()

    elif ques=="Which states have the lowest transaction amounts?":
        ques2()

    elif ques=="Which districts exhibit the highest transaction amounts?":
        ques3()

    elif ques=="Which are the ten districts with the lowest transaction amounts?":
        ques4()

    elif ques=="Which are the top 10 states with the highest number of app opens?":
        ques5()

    elif ques=="Which are the ten states with the least number of app opens?":
        ques6()

    elif ques=="Which states have the lowest transaction count?":
        ques7()

    elif ques=="Which states have the highest transaction count?":
        ques8()

    elif ques=="Which states have the highest transaction amounts?":
        ques9()

    elif ques=="Which are the top 50 districts with the lowest transaction amounts?":
        ques10()

# MENU 4 - ABOUT
if select == "About":
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
        img1 = Image.open(r"C:\Users\udhay\OneDrive\Desktop\New folder\PhonePe\PhonePe_Pulse.jpg")
        st.image(img1)

        st.write("**:violet[My GitHub profile]** ⬇️")
        st.write("https://github.com/Udhaykumar56")