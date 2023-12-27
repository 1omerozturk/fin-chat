import streamlit as st
import plotly.express as px
import pandas as pd
import os
import warnings
warnings.filterwarnings("ignore")

cs_css="""
    .my-class{
        background:tranparent;
        font-family: cursive;
        font-size:55px;
        color:white;
       font-weight:bold; 
    }
    .center{
        display: flex;
        justify-content: center;
        align-items: center;
    }
st.set_page_config(page_title="Dashboard",
                   
                   page_icon=":bar_chart:", layout="wide")
    """
st.markdown("""
            <div class='center'>
            <p class='my-class'>
            Example Dahboard DBA💲
            </p>
            </div>
            """
            ,unsafe_allow_html=True)
st.markdown(f'<style>{cs_css}</style>', unsafe_allow_html=True)
fl = st.file_uploader(":file_folder: Upload a file",
                      type=(["csv", "txt", "xlsx", "xls"]))
if fl is not None:
    filename = fl.name
    st.write(filename)
    df = pd.read_excel(filename)
else:
    os.chdir(r"C:\Users\omero\Desktop\Dashboard")
    df = pd.read_excel("Superstore.xls")

st.divider()
st.divider()

col1, col2 = st.columns((2))
df["Order Date"] = pd.to_datetime(df["Order Date"])


# minimum ve maksimum tarih girişi

startDate = pd.to_datetime(df["Order Date"]).min()
endDate = pd.to_datetime(df["Order Date"]).max()


with col1:
    date1 = pd.to_datetime(st.date_input("Start Date", startDate))

with col2:
    date2 = pd.to_datetime(st.date_input("End Date", endDate))


df = df[(df["Order Date"] >= date1) & (df["Order Date"] <= date2)].copy()


# Filtreleme işlemi için
st.sidebar.header("Choose your filter: ")


# Bölge oluşturma
region = st.sidebar.multiselect("Pick your Region", df["Region"].unique())
if not region:
    df2 = df.copy()
else:
    df2 = df[df["Region"].isin(region)]
    
    
# Alt Bölge oluşturma
state = st.sidebar.multiselect("Pick the State", df2["State"].unique())

if not state:
    df3 = df2.copy()

else:
    df3 = df2[df2["State"].isin(state)]

# Şehirlere göre filtreleme

city = st.sidebar.multiselect("Pick the City", df3["City"].unique())

if not region and not state and not city:
    filtered_df = df
elif not state and not city:
    filtered_df = df[df['Region'].isin(region)]
elif not region and not city:
    filtered_df = df[df['State'].isin(state)]
elif state and city:
    filtered_df = df3[df3['State'].isin(state) & df3["City"].isin(city)]

elif region and city:
    filtered_df = df3[df3['Region'].isin(region) & df3["City"].isin(city)]

elif region and state:
    filtered_df = df3[df3['Region'].isin(region) & df3["City"].isin(state)]
elif city:
    filtered_df=df3[df3["City"].isin(city)]
    
else:
    filtered_df=df3[df3["Region"].isin(region) & df3["State"].isin(state) & df3["City"].isin(city)]

# Kategoriye göre filtrelenmiş

category_df=filtered_df.groupby(by=["Category"],as_index=False)["Sales"].sum()

with col1:
    st.subheader("Category wise Sales")
    fig=px.bar(category_df,x="Category",y="Sales",text=['${:,.2f}'.format(x) for x in category_df["Sales"]],
               template="seaborn")
    st.plotly_chart(fig,use_container_width=True,height=200)
    
with col2:
    st.subheader("Region wise Salses")
    fig=px.pie(filtered_df,values="Sales",names="Region",hole=0.5)
    fig.update_traces(text=filtered_df["Region"],textposition="outside")
    st.plotly_chart(fig, use_container_width=True)
    
cl1,cl2=st.columns(2)

with cl1:
    with st.expander(":orange[Category_ViewData]"):
        st.write(category_df.style.background_gradient(cmap="Blues"))
        csv=category_df.to_csv(index=False).encode("utf-8")
        st.download_button(":blue[Download Data]",data=csv,file_name="Category.csv",mime="text/csv",
                           help="Click here to download the data as a CSV file")

with cl2:
    with st.expander(":orange[Region_ViewData]"):
        region=filtered_df.groupby(by="Region",as_index=False)["Sales"].sum()
        st.write(region.style.background_gradient(cmap="Oranges"))
        csv=region.to_csv(index=False).encode("utf-8")
        st.download_button(":blue[Download Data]",data=csv,file_name="Region.csv",mime="text/csv",
                           help="Click here to download the data as a CSV file")


st.divider()
st.divider()


# Tarihe göre filtreleme
filtered_df["month_year"]=filtered_df["Order Date"].dt.to_period("M")
st.subheader("Time Series Analysis")

linechart=pd.DataFrame(filtered_df.groupby(filtered_df["month_year"].dt.strftime("%Y : %b"))["Sales"].sum()).reset_index()
fig2=px.line(linechart,x="month_year",y="Sales",labels={"Sales": "Amount"},height=500,width=1000,template="gridon")
st.plotly_chart(fig2,use_container_width=True)


with st.expander(":green[View Data of TimeSeries:]"):
    st.write(linechart.T.style.background_gradient(cmap="Blues"))
    csv=linechart.to_csv(index=False).encode("utf-8")
    st.download_button(":blue[Download Data]",data=csv,file_name="TimeSeries.csv",mime="text/csv")
    


st.divider()
st.divider()

# Satışlara göre filtreleme
st.subheader("Hierarchical view of Sales using TreeMap")
fig3=px.treemap(filtered_df,path=["Region","Category","Sub-Category"],values="Sales",hover_data=["Sales"],
                color="Sub-Category")
fig3.update_layout(width=800,height=650)
st.plotly_chart(fig3,use_container_width=True)

st.divider()
st.divider()


chart1,chart2=st.columns((2))

with chart1:
    st.subheader("Segment wise Sales")
    fig=px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark" )
    fig.update_traces(text=filtered_df["Segment"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)

with chart2:
    st.subheader("Category wise Sales")
    fig=px.pie(filtered_df,values="Sales",names="Segment",template="plotly_dark")
    fig.update_traces(text=filtered_df["Segment"],textposition="inside")
    st.plotly_chart(fig,use_container_width=True)



# Grafikleri özet olarak gösterme
import plotly.figure_factory as ff

st.subheader(":point_down: Month wise Sub-Category Sales Summary")
with st.expander(":green[Summary_Table]"):
    df_sample=df[0:5][["Region","State","City","Category","Sales","Profit","Quantity"]]
    fig=ff.create_table(df_sample,colorscale="Cividis")
    st.plotly_chart(fig,use_container_width=True)

    st.markdown("Month wise sub-Category Table")
    filtered_df["month"]=filtered_df["Order Date"].dt.month_name()
    sub_category_Year=pd.pivot_table(data=filtered_df,values="Sales",index=["Sub-Category"],columns="month")
    st.write(sub_category_Year.style.background_gradient(cmap="Blues"))


data1=px.scatter(filtered_df,x="Sales",y="Profit",size="Quantity")
data1["layout"].update(title="Relationship between Sales and Profits using Scatter Plot.",
                       titlefont=dict(size=20),xaxis=dict(title="Sales",titlefont=dict(size=19)),
                       yaxis=dict(title="Profits",titlefont=dict(size=19))
                       )
st.plotly_chart(data1,use_container_width=True)

# Verileri liste şeklinde görüntüleme
with st.expander(":green[View Data]"):
    st.write(filtered_df.iloc[:500,1:20:2].style.background_gradient(cmap="Oranges"))

# Verileri indirme
csv=df.to_csv(index=False).encode("utf-8")
st.download_button(":blue[Download Data]",data=csv,file_name="Data.csv",mime="text/scv")
      
      
