import streamlit as st  # 顯示 Checkbox 功能 :contentReference[oaicite:0]{index=0}
import pandas as pd
import numpy as np
import random
from plotly.subplots import make_subplots
import plotly.graph_objects as go  # 顯示 Slider 功能 :contentReference[oaicite:1]{index=1}

# 固定隨機種子
SEED = 42
random.seed(SEED)
np.random.seed(SEED)

@st.cache_data(show_spinner=False)
def gen_data():
    """
    產生N天的隨機營收與帳單數資料
    使用 st.cache_data 快取，避免重複計算
    """
    dates = [20250707, 20250708, 20250709, 20250710, 20250711, 20250712, 20250713, 20250714, 20250715, 20250716, 20250717]
    rows = []
    for date in dates:
        for hour in range(5, 13):
            rows.append({
                "日期": str(date),
                "小時": hour,
                "revenue": np.random.randint(0, 1000),
                "bill_num": np.random.randint(0, 50),
            })
    return pd.DataFrame(rows)

def main():
    # 下拉選單：選擇要顯示的頁面
    option = st.selectbox(
        "請選擇報表",
        ["Welcome", "各時段營收與帳單數", "每日營收與帳單數"]
    )

    if option == "Welcome":
        # 顯示指定圖檔（請替換為實際路徑或 URL）
        st.image("dancing_cat.gif", use_container_width=True)
        return

    
    elif option == "各時段營收與帳單數":

        # 進入「各時段營收與帳單數」頁面
        st.title("營業額分析")
        st.subheader("各時段營收與帳單數")

        # 產生資料並計算佔比
        df = gen_data()
        df["revenue/total (%)"] = df["revenue"] / df["revenue"].sum() * 100
        print('Total revenue = ', df["revenue"].sum())

        # 1. 先建立圖表的位置（空白容器）
        chart_placeholder = st.empty()

        # 2. 接著顯示控制項：先 Checkbox，再 Slider
        show_rev = st.checkbox("顯示 營收（氣泡）", True)     # :contentReference[oaicite:2]{index=2}
        show_bill = st.checkbox("顯示 帳單數（虛線）", False)
        max_diameter = st.slider(
            "泡泡最大直徑 (像素)",
            min_value=10,
            max_value=70,
            value=50,
            step=5
        )  # :contentReference[oaicite:3]{index=3}

        # 3. 計算 sizeref（用於 Plotly 氣泡大小）
        max_pct = df["revenue/total (%)"].max()
        sizeref = 2 * max_pct / (max_diameter ** 2)

        # 4. 繪製 Plotly 圖表
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        dash_styles = ["dash", "dot", "dashdot"]
        for i, date in enumerate(sorted(df["日期"].unique())):
            d = df[df["日期"] == date]
            if show_rev:
                fig.add_trace(
                    go.Scatter(
                        x=d["小時"], y=d["revenue"],
                        mode="markers",
                        name=f"{date} 營收",
                        marker=dict(size=d["revenue/total (%)"], sizemode="area", sizeref=sizeref),
                        hovertemplate="日期：%{text}<br>營收：%{y}<br>占比：%{marker.size:.2f}%",
                        text=[date] * len(d),
                    ),
                    secondary_y=False
                )
            if show_bill:
                fig.add_trace(
                    go.Scatter(
                        x=d["小時"], y=d["bill_num"],
                        mode="lines+markers",
                        name=f"{date} 帳單數",
                        line=dict(dash=dash_styles[i % 3], width=2),
                        hovertemplate="日期：%{text}<br>帳單數：%{y}",
                        text=[date] * len(d),
                    ),
                    secondary_y=True
                )

        if not (show_rev or show_bill):
            st.warning("請至少勾選一個選項，以顯示圖表。")
        else:
            fig.update_layout(
                title=" ",
                xaxis=dict(title="小時", dtick=1),
                legend=dict(orientation="h", y=1.02, x=1, xanchor="right", yanchor="bottom")
            )
            fig.update_yaxes(title_text="營收", secondary_y=False)
            fig.update_yaxes(title_text="帳單數", secondary_y=True, side="right")
            # 這裡將圖表填入之前建立的空白容器，讓圖表位於 Checkbox 與 Slider 之上
            chart_placeholder.plotly_chart(fig, use_container_width=True)

        # 顯示原始資料表格
        st.dataframe(df)


    elif option == "每日營收與帳單數":
        pass


    else:
        pass

if __name__ == "__main__":
    main()
