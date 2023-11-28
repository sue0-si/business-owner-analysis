import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def bar_chart(*geo):
    fig = px.bar(filtered_df,
                title="전국 인기 사업장 증감 추이",
                x="업종",
                y="사업장 차이",
                color="업종")
    return fig

dfMerged = pd.read_csv("merged.csv")
dfMerged.set_index('업종', inplace=True)
dfMerged["choose"] = False  # 컬럼 추가

dfRegion = pd.read_csv("region.csv")


st.title("전국 인기 사업장 30개")

col1, col2 = st.columns([0.5,0.5])

with col1:
    st.header("당월")
    current = st.data_editor(dfMerged)
    current["업종"] = current.index
    select = list(current[current["choose"]]["업종"])
    current["choose"] = current["업종"].isin(select)

with col2:
    tab1, tab2 = st.tabs(["사업장 증감도", "사업자 분포도"])

    with tab1:
        list = []
        for index, row in current.iterrows():
            diff = row['당월'] - row['전년동월']
            list.append({'업종': row['업종'], '사업장 차이': diff})
        
        difference_df = pd.DataFrame(list)
        filtered_df = difference_df[difference_df['업종'].isin(select)]

        st.plotly_chart(bar_chart(*select))
        
    with tab2:
        filtered_region = dfRegion[dfRegion['업종'].isin(select)]

        fig = px.scatter(filtered_region, x='시도', y='당월', color='업종', size='당월',
                title='인기 업종에 대한 전국 사업자 분포도',
                labels={'당월': '사업자 수', '시도': '지역', '업종': '업종'})
        st.plotly_chart(fig)


dfRegionSpecific = pd.read_csv("business_sum_region_specific.csv")
dfRegionJobSum = pd.read_csv("business_sum_region.csv")
dfRegionSp = pd.read_csv("business_sum_by_region.csv")


# regionOption: 선택한 값
regionOption = st.selectbox (
    'Choose a region',
    dfRegionSpecific['시도'].unique()
)

strem = dfRegionJobSum[dfRegionJobSum['시도'].isin([regionOption])]
cell_value = str(strem['당월'].iloc[0])
st.subheader("도내 사업장 총합: " + cell_value)

filtered = dfRegionSpecific[dfRegionSpecific['시도'].isin([regionOption])]
town_fig = px.scatter(filtered, x='시군구', y='당월', size="당월", color= "당월")
st.plotly_chart(town_fig)

print("Index:", dfRegionJobSum.index)
print("Columns:", dfRegionJobSum.columns)


dfRegionSp
