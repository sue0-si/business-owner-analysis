import streamlit as st
import pandas as pd
import plotly.express as px

# 페이지의 margin을 조절하기 위한 CSS 스타일
custom_css = """
    <style>
        body {
            margin: 20px;
        }
    </style>
"""

@st.cache_data
def bar_chart(*geo):
    fig = px.bar(filtered_df,
                title="전국 인기 사업자 증감 추이",
                x="업종",
                y="사업자 차이",
                color="업종")
    return fig

dfMerged = pd.read_csv("merged.csv")
dfMerged.set_index('업종', inplace=True)
dfMerged["선택"] = False  # 컬럼 추가

dfRegion = pd.read_csv("region.csv")

st.header("2023년 전국 인기 업종 30개 분석 및 지역별 업종 분포")

# col1 = 전처리된 데이터프레임에 유저가 선택할 수 있는 기능 넣기
col1, col2 = st.columns([0.5,0.5])
with col1:  
    current = st.data_editor(dfMerged)
    current["업종"] = current.index
    select = list(current[current["선택"]]["업종"])
    current["선택"] = current["업종"].isin(select)

# col2: 사업장 증감도와 사업자 분포도
with col2:
    tab1, tab2 = st.tabs(["사업자 증감도", "사업자 분포도"])

    # 사업장 증감도
    with tab1:
        list = []
        for index, row in current.iterrows():
            diff = row['당월'] - row['전년동월']
            list.append({'업종': row['업종'], '사업자 차이': diff})
        
        difference_df = pd.DataFrame(list)
        filtered_df = difference_df[difference_df['업종'].isin(select)]
        st.plotly_chart(bar_chart(*select))
    
    # 사업자 분포도    
    with tab2:
        filtered_region = dfRegion[dfRegion['업종'].isin(select)]

        fig = px.scatter(filtered_region, x='시도', y='당월', color='업종', size='당월',
                title='인기 업종에 대한 전국 사업자 분포도',
                labels={'당월': '사업자 수', '시도': '지역', '업종': '업종'})
        st.plotly_chart(fig)


dfRegionSpecific = pd.read_csv("business_sum_region_specific.csv")
dfRegionJobSum = pd.read_csv("business_sum_region.csv")
dfRegionSp = pd.read_csv("business_sum_by_region.csv")


# regionOption: 선택한 시/도 값
regionOption = st.selectbox (
    '시/도를 선택하세요',
    dfRegionSpecific['시도'].unique()
)

# 선택한 시/도의 총 사업장 수 나타내기
strem = dfRegionJobSum[dfRegionJobSum['시도'].isin([regionOption])]
cell_value = str(strem['당월'].iloc[0])
st.subheader("시/도내 사업자 총합: " + cell_value)

# 선택한 시/도의 시군구 별 사업장 수 그래프 그리기
filtered = dfRegionSpecific[dfRegionSpecific['시도'].isin([regionOption])]
town_fig = px.scatter(filtered, x='시군구', y='당월', size="당월", color= "당월")
st.plotly_chart(town_fig)

# 선택한 시/도에 대한 데이터만 추출
filteredSp = dfRegionSp[dfRegionSp['시도'].isin([regionOption])]
filteredTown = filteredSp['시군구'].unique()

# 라디오 버튼을 가로로 정렬
st.markdown(
    "<style>div.row-widget.stRadio > div{flex-direction:row;}</style>",
    unsafe_allow_html=True,
)

# regionSp = 선택한 시군구 값
regionSp = st.radio(
    "시군구를 선택해주세요",
    filteredTown
)

example = filteredSp[filteredSp['시군구'].isin([regionSp])]

# 선택한 시군구에 대한 업종별 사업장 수 그래프 그리기
district_fig = px.scatter(example, x='업종', y='당월', size="당월", color='당월')
st.plotly_chart(district_fig)

