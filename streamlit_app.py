import streamlit as st
import plotly.express as px
import pandas as pd
import numpy as np
import streamlit as st 
import random


class Business_Date:
    def __init__(self, date):
        self.date = date
        self.time = [5,6,7,8,9,10,11,12]
        self.time_clk = len(self.time)

        self.revenue = [None for _ in range(self.time_clk)]
        self.bill_num = [None for _ in range(self.time_clk)]
    
    def init(self):
        print(self.r)




def gen_data():

    data_list = [Business_Date(20250707), Business_Date(20250708), Business_Date(20250709)]
    # for i in range(len(data_list)):
    #     data_list[i].revenue = [random.randint(0, 1000) for _ in range(data_list[i].time_clk)]
    #     data_list[i].bill_num = [random.randint(0, 20) for _ in range(data_list[i].time_clk)]

    # for i in range(len(data_list)):
    #     print(data_list[i].date)
    #     print(data_list[i].time)
    #     print(data_list[i].revenue)
    #     print(data_list[i].bill_num)

    database = []
    for date in data_list:
        for hour in [5,6,7,8,9,10,11,12]:
            revenue = np.random.randint(0, 1000)
            database.append({
                "日期": str(date.date),
                "小時": hour,
                "revenue": revenue
            })

    return database


# 畫泡泡圖

def plot_scatter(database):
    # 建立資料表
    df = pd.DataFrame(database)

    # 計算總金額與比例
    total_revenue = df['revenue'].sum()
    df["revenue占比"] = df["revenue"] / total_revenue * 100

    # 畫圖
    fig = px.scatter(
        df,
        x="小時",
        y="revenue",
        size="revenue占比",
        color="日期",
        hover_data=["日期", "revenue", "revenue占比"],
        title="📊 各時段營收圖（大小依數據總營收占比）",
        size_max=50
    )

    fig.update_layout(height=600, xaxis=dict(dtick=1))  # 每小時顯示刻度
    fig.update_traces(marker=dict(line=dict(width=1, color='DarkSlateGrey')))

    # 顯示圖表與表格
    st.title("🧮日期 × 小時 × 營收 Dashboard")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df)




if __name__ == '__main__':
    a = gen_data()
    plot_scatter(a)



