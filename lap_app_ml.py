# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
import streamlit as st
import pickle 
import numpy as np
import pandas as pd
import seaborn as sns 
st.set_option('deprecation.showPyplotGlobalUse', False)

def main():
    activities=['EDA','Pre-Prosessed Data','Prediction','About']    
    choices = st.sidebar.selectbox('Select Activities',activities)
    if choices == 'EDA':
       st.subheader("Exploratory Data Analysis")
       data = st.file_uploader('Upload Data set', 
                               type=['csv','xlsx', 'txt'])
       if data is not None:
           df=pd.read_csv(data)
           st.dataframe(df.head())
           if st.checkbox("show Details no. of records"):
               st.write(df.shape)
           if st.checkbox("show Columns"):
               st.write(df.columns.to_list()) 
    elif choices == 'Pre-Prosessed Data':
       pipe = pickle.load(open('pipe.pickle','rb'))
       df1 = pickle.load(open('df1.pickle','rb'))
       st.dataframe(df1.head())
       if st.checkbox("show Details no. of records"):
           st.write(df1.shape)
       if st.checkbox("show Columns"):
           st.write(df1.columns.to_list()) 
           all_col_name = df1.columns.to_list()
           type_of_plot = st.selectbox("Select type of plot", ["bar","distplot"])
           selected_col = st.multiselect("Select col to plot", all_col_name)
           if st.button("Genarate Plot"):
               st.bar_chart(selected_col)
               st.success("Genarating PLot of {} for {}".format(type_of_plot, selected_col))
           if st.checkbox("Corelation Plot(Seaborn)"):
               st.write(sns.heatmap(df1.corr(), annot=True))
               st.pyplot()
           
    elif choices == 'Prediction':
       pipe = pickle.load(open('pipe.pickle','rb'))
       df1 = pickle.load(open('df1.pickle','rb'))
       st.dataframe(df1.head())
       company = st.selectbox("Select Brand", df1["Company"].unique())
       lap_typ = st.selectbox("Select Laptop Type", df1["TypeName"].unique())
       ram = st.selectbox("Select RAM(in GB)", [2,4,6,8,12,16,24,32,64])
       weight = st.number_input("Weight of the Laptop")
       if weight == 0:
           st.warning("Please Enter Weight")
        #Touch screen
       touchscreen = st.selectbox("TouchScreen", ['No', 'Yes'])
        #IPS
       ips = st.selectbox("IPS", ['No', 'Yes'])
        #screen size
       screen_size = st.number_input('Screen Size(in inches)')
       if screen_size == 0:
           st.warning("Please Enter Size of Screen in inches")
       
        # resolution
       resolution = st.selectbox('Screen Resolution',['1920x1080','1366x768','1600x900','3840x2160','3200x1800','2880x1800','2560x1600','2560x1440','2304x1440'])
        #cpu
       cpu = st.selectbox('CPU',df1['Cpu name'].unique())
       hdd = st.selectbox('HDD(in GB)',[0,128,256,512,1024,2048])
       ssd = st.selectbox('SSD(in GB)',[0,8,128,256,512,1024])
       gpu = st.selectbox('GPU',df1['Gpu name'].unique())
       os = st.selectbox('OS',df1['os'].unique())
  

       if st.button('Predict Price'):
           ppi = None
           if touchscreen == "Yes":
               touchscreen = 1
           else:
               touchscreen = 0
           if ips == "Yes":
               ips = 1
           else:
               ips = 0
           X_res = int(resolution.split('x')[0])
           Y_res = int(resolution.split('x')[1])
           ppi = ((X_res ** 2) + (Y_res**2)) ** 0.5 / screen_size
           query = np.array([company,lap_typ,ram,weight,touchscreen,
                             ips,os,cpu,gpu,ppi,hdd,ssd])
           query = query.reshape(1, 12)
           prediction = str(int(np.exp(pipe.predict(query)[0])))
           st.title("The predicted price of this configuration is " + prediction)
           
           #accu = df1["Price"] == prediction
           if df1["Price"] == prediction:
               print("Accurate Prediction")
           else :
               print("Not Accurate")
    elif choices == 'About':
       pass




if __name__ == '__main__' :
    main()
    