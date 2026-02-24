import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

# ===============================
# 页面设置 Page Config
# ===============================
st.set_page_config(
    page_title="Strategic Profit Sandbox",
    page_icon="🚜",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ===============================
# 主题切换器 (放在最前面)
# ===============================
if 'theme' not in st.session_state:
    st.session_state.theme = "dark"

# ===============================
# CSS 样式定义 - 支持亮色和暗色主题
# ===============================
def get_css(theme):
    if theme == "light":
        return """
<style>
/* 隐藏 Streamlit 默认顶部导航栏 */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* 移除顶部空白 */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}

/* 主背景 - 亮色系 */
.stApp {
    background: linear-gradient(135deg, #f0f4f8 0%, #e6eef7 100%);
}

/* 侧边栏 - 亮色玻璃拟态 */
[data-testid="stSidebar"] {
    background: rgba(255, 255, 255, 0.95) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(0, 100, 200, 0.1);
}

/* 侧边栏文字 - 深灰色确保可见 */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stExpander label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #1a202c !important;
}

/* 侧边栏标题 */
[data-testid="stSidebar"] h1 {
    color: #0066cc !important;
    font-weight: 600;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* 滑块样式 - 蓝色系 */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #0066cc, #00a8e8) !important;
}

/* 下拉菜单 */
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.9) !important;
    border: 1px solid rgba(0, 100, 200, 0.3) !important;
    border-radius: 8px !important;
    color: #1a202c !important;
}

/* 主标题区域 - 亮色科技感 */
.main-title {
    background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 168, 232, 0.05) 100%);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid rgba(0, 102, 204, 0.2);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.main-title::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #0066cc, #00a8e8, #0066cc);
    animation: scanline 3s linear infinite;
}

@keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* 标题文字 - 深色 */
h1 {
    color: #1a202c !important;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem !important;
    background: linear-gradient(90deg, #0066cc, #00a8e8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2 {
    color: #0066cc !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0, 102, 204, 0.3);
}

h3 {
    color: #4a5568 !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
}

/* 副标题 */
.caption-text {
    color: #4a5568;
    font-size: 1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* KPI卡片 - 亮色玻璃拟态 */
.metric-card {
    background: rgba(255, 255, 255, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 102, 204, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 102, 204, 0.4);
    box-shadow: 0 10px 40px rgba(0, 102, 204, 0.1);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #0066cc, #00a8e8);
    opacity: 0.7;
}

.metric-label {
    color: #4a5568;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.metric-value {
    color: #1a202c;
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
}

.metric-delta {
    color: #0066cc;
    font-size: 0.9rem;
    font-weight: 500;
}

/* 风险状态标签 - 亮色适配 */
.risk-stable {
    color: #059669 !important;
    background: rgba(5, 150, 105, 0.15) !important;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.risk-high {
    color: #dc2626 !important;
    background: rgba(220, 38, 38, 0.15) !important;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* 图表容器 */
.chart-container {
    background: rgba(255, 255, 255, 0.6);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(0, 102, 204, 0.1);
    margin-bottom: 2rem;
}

/* 成功提示 */
.success-box {
    background: linear-gradient(135deg, rgba(0, 102, 204, 0.1) 0%, rgba(0, 168, 232, 0.1) 100%);
    border: 1px solid rgba(0, 102, 204, 0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #0066cc;
    font-weight: 500;
    text-align: center;
    margin-top: 2rem;
}

/* 分割线 */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 102, 204, 0.3), transparent);
    margin: 2rem 0;
}

/* 滚动条美化 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #f0f4f8;
}

::-webkit-scrollbar-thumb {
    background: #0066cc;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #00a8e8;
}

/* 确保所有输入标签可见 */
.stSlider label, .stSelectbox label {
    color: #1a202c !important;
    font-weight: 500 !important;
}
</style>
"""
    else:  # dark theme
        return """
<style>
/* 隐藏 Streamlit 默认顶部导航栏 */
#MainMenu {visibility: hidden;}
header {visibility: hidden;}
.stDeployButton {display: none;}

/* 移除顶部空白 */
.block-container {
    padding-top: 1rem !important;
    padding-bottom: 0rem !important;
}

/* 主背景 - 深蓝黑色 */
.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1f2e 100%);
}

/* 侧边栏 - 玻璃拟态效果 */
[data-testid="stSidebar"] {
    background: rgba(15, 20, 35, 0.95) !important;
    backdrop-filter: blur(10px);
    border-right: 1px solid rgba(0, 245, 255, 0.1);
}

/* 侧边栏文字 - 白色确保可见 */
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stSlider label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stExpander label,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] div {
    color: #ffffff !important;
}

/* 侧边栏标题 */
[data-testid="stSidebar"] h1 {
    color: #00f5ff !important;
    font-weight: 600;
    font-size: 1.2rem;
    letter-spacing: 0.5px;
    text-transform: uppercase;
}

/* 滑块样式 */
.stSlider > div > div > div {
    background: linear-gradient(90deg, #00f5ff, #0080ff) !important;
}

/* 下拉菜单 */
.stSelectbox > div > div {
    background: rgba(30, 35, 50, 0.8) !important;
    border: 1px solid rgba(0, 245, 255, 0.3) !important;
    border-radius: 8px !important;
    color: #ffffff !important;
}

/* 主标题区域 */
.main-title {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(0, 128, 255, 0.05) 100%);
    padding: 2rem;
    border-radius: 16px;
    border: 1px solid rgba(0, 245, 255, 0.2);
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
}

.main-title::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, #00f5ff, #0080ff, #00f5ff);
    animation: scanline 3s linear infinite;
}

@keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}

/* 标题文字 */
h1 {
    color: #ffffff !important;
    font-weight: 700 !important;
    font-size: 2.5rem !important;
    margin-bottom: 0.5rem !important;
    background: linear-gradient(90deg, #00f5ff, #0080ff);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

h2 {
    color: #00f5ff !important;
    font-weight: 600 !important;
    font-size: 1.5rem !important;
    margin-top: 2rem !important;
    margin-bottom: 1rem !important;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid rgba(0, 245, 255, 0.3);
}

h3 {
    color: #a0a8b8 !important;
    font-weight: 500 !important;
    font-size: 1.1rem !important;
}

/* 副标题 */
.caption-text {
    color: #6b7280;
    font-size: 1rem;
    letter-spacing: 1px;
    text-transform: uppercase;
}

/* KPI卡片 - 玻璃拟态 */
.metric-card {
    background: rgba(20, 25, 40, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(0, 245, 255, 0.15);
    border-radius: 16px;
    padding: 1.5rem;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.metric-card:hover {
    transform: translateY(-2px);
    border-color: rgba(0, 245, 255, 0.4);
    box-shadow: 0 10px 40px rgba(0, 245, 255, 0.1);
}

.metric-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, #00f5ff, #0080ff);
    opacity: 0.7;
}

.metric-label {
    color: #6b7280;
    font-size: 0.85rem;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 0.5rem;
}

.metric-value {
    color: #ffffff;
    font-size: 2rem;
    font-weight: 700;
    font-family: 'Inter', sans-serif;
}

.metric-delta {
    color: #00f5ff;
    font-size: 0.9rem;
    font-weight: 500;
}

/* 风险状态标签 */
.risk-stable {
    color: #10b981 !important;
    background: rgba(16, 185, 129, 0.15) !important;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
}

.risk-high {
    color: #ef4444 !important;
    background: rgba(239, 68, 68, 0.15) !important;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-size: 0.85rem;
    font-weight: 600;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.7; }
}

/* 图表容器 */
.chart-container {
    background: rgba(20, 25, 40, 0.4);
    border-radius: 16px;
    padding: 1.5rem;
    border: 1px solid rgba(0, 245, 255, 0.1);
    margin-bottom: 2rem;
}

/* 成功提示 */
.success-box {
    background: linear-gradient(135deg, rgba(0, 245, 255, 0.1) 0%, rgba(0, 128, 255, 0.1) 100%);
    border: 1px solid rgba(0, 245, 255, 0.3);
    border-radius: 12px;
    padding: 1rem 1.5rem;
    color: #00f5ff;
    font-weight: 500;
    text-align: center;
    margin-top: 2rem;
}

/* 分割线 */
hr {
    border: none;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(0, 245, 255, 0.3), transparent);
    margin: 2rem 0;
}

/* 滚动条美化 */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}

::-webkit-scrollbar-track {
    background: #0a0e1a;
}

::-webkit-scrollbar-thumb {
    background: #00f5ff;
    border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
    background: #0080ff;
}

/* 确保所有输入标签为白色 */
.stSlider label, .stSelectbox label {
    color: #ffffff !important;
    font-weight: 500 !important;
}
</style>
"""

# 应用当前主题的CSS
st.markdown(get_css(st.session_state.theme), unsafe_allow_html=True)

# ===============================
# 主题和语言切换
# ===============================
theme_option = st.sidebar.selectbox("🎨 Theme / 主题", ["Dark (深色)", "Light (亮色)"], 
                                    index=0 if st.session_state.theme == "dark" else 1)

if theme_option == "Light (亮色)" and st.session_state.theme != "light":
    st.session_state.theme = "light"
    st.rerun()
elif theme_option == "Dark (深色)" and st.session_state.theme != "dark":
    st.session_state.theme = "dark"
    st.rerun()

language = st.sidebar.selectbox("🌐 Language / 语言", ["English", "中文"], index=1)

def t(en, cn):
    return en if language == "English" else cn

# ===============================
# 标题区域 - 带装饰效果
# ===============================
st.markdown("""
<div class="main-title">
    <h1>🚜 {}</h1>
    <div class="caption-text">{}</div>
</div>
""".format(
    t("Strategic Profit Sandbox", "柳工战略利润沙盘系统"),
    t("Executive Value Chain War-Room", "价值链战略驾驶舱")
), unsafe_allow_html=True)

# ===============================
# 战略参数 Strategic Controls
# ===============================
st.sidebar.markdown(f"### ⚙️ {t('Strategic Controls', '战略参数')}")

with st.sidebar.expander(t("📊 Production", "📊 生产参数"), expanded=True):
    volume = st.slider(
        t("Production Volume (units)", "产量 (台)"),
        200, 2000, 1800, step=50,
        help=t("Annual production volume", "年度生产台数")
    )
    
    rd_rate = st.slider(
        t("R&D Capitalization %", "研发资本化比例 %"),
        0.0, 1.0, 0.6, step=0.05,
        help=t("Percentage of R&D costs capitalized", "研发费用资本化比例")
    )

with st.sidebar.expander(t("💰 Cost & Risk", "💰 成本与风险"), expanded=True):
    raw_material_increase = st.slider(
        t("Raw Material Cost Increase %", "原材料涨价 %"),
        0, 30, 10, step=1,
        help=t("Year-over-year raw material cost increase", "原材料成本同比上涨")
    )
    
    inventory_growth = st.slider(
        t("Dealer Inventory Growth %", "经销商库存增长 %"),
        0, 50, 20, step=5,
        help=t("Channel inventory growth rate", "渠道库存增长率")
    )
    
    bad_debt_rate = st.slider(
        t("Finance Bad Debt %", "金融坏账率 %"),
        0, 20, 5, step=1,
        help=t("Bad debt ratio for financing business", "金融业务坏账率")
    )
    
    service_growth = st.slider(
        t("Aftermarket Growth %", "售后市场增长率 %"),
        0, 50, 15, step=5,
        help=t("Service revenue growth rate", "售后服务收入增长率")
    )

# ===============================
# 基础模型计算
# ===============================
equipment_revenue = volume * 50
base_material_cost = volume * 30
material_cost = base_material_cost * (1 + raw_material_increase/100)

fixed_cost = 20000
variable_cost = 5 * volume
manufacturing_cost = fixed_cost + variable_cost

rd_total = 10000
rd_amort = rd_total * rd_rate / 5

service_revenue = volume * 15 * (1 + service_growth/100)
service_cost = service_revenue * 0.5

finance_revenue = volume * 8
bad_debt = finance_revenue * bad_debt_rate/100
finance_cost = volume * 3

used_profit = volume * 5

equipment_profit = equipment_revenue - material_cost - manufacturing_cost - rd_amort
service_profit = service_revenue - service_cost
finance_profit = finance_revenue - bad_debt - finance_cost

total_profit = equipment_profit + service_profit + finance_profit + used_profit

# ===============================
# KPI Dashboard - 玻璃拟态卡片
# ===============================
st.markdown(f"### 📈 {t('Executive KPIs', '核心指标')}")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t('Total Lifecycle Profit', '全生命周期利润')}</div>
        <div class="metric-value">${total_profit:,.0f}K</div>
        <div class="metric-delta">▲ {t('YoY +12%', '同比 +12%')}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    unit_cost = manufacturing_cost/volume
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t('Unit Manufacturing Cost', '单位制造成本')}</div>
        <div class="metric-value">${unit_cost:.1f}K</div>
        <div class="metric-delta">{t('Target: $35K', '目标: $35K')}</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    service_ratio = service_profit/total_profit if total_profit != 0 else 0
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t('Service Profit Ratio', '售后利润占比')}</div>
        <div class="metric-value">{service_ratio:.1%}</div>
        <div class="metric-delta">{t('Healthy >30%', '健康值 >30%')}</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    risk_class = "risk-high" if inventory_growth > 15 else "risk-stable"
    risk_text = t("HIGH RISK", "高风险") if inventory_growth > 15 else t("STABLE", "稳定")
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">{t('Channel Risk Status', '渠道风险状态')}</div>
        <div class="metric-value">
            <span class="{risk_class}">{risk_text}</span>
        </div>
        <div class="metric-delta">{t('Inventory', '库存')}: {inventory_growth}%</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

# 根据主题选择图表模板
chart_template = "plotly_white" if st.session_state.theme == "light" else "plotly_dark"
chart_bgcolor = "rgba(255,255,255,0)" if st.session_state.theme == "light" else "rgba(0,0,0,0)"
grid_color = "rgba(0,0,0,0.1)" if st.session_state.theme == "light" else "rgba(255,255,255,0.1)"
text_color = "#1a202c" if st.session_state.theme == "light" else "white"

# 颜色方案
if st.session_state.theme == "light":
    primary_color = "#0066cc"
    secondary_color = "#00a8e8"
    danger_color = "#dc2626"
    colors = ["#0066cc", "#00a8e8", "#6366f1", "#8b5cf6"]
else:
    primary_color = "#00f5ff"
    secondary_color = "#0080ff"
    danger_color = "#ef4444"
    colors = ["#00f5ff", "#0080ff", "#6366f1", "#8b5cf6"]

# ===============================
# 图表区域 - 两列布局
# ===============================
col_left, col_right = st.columns([3, 2])

with col_left:
    # 生命周期利润瀑布图
    st.markdown(f"### 📊 {t('Lifecycle Profit Waterfall', '生命周期利润瀑布')}")
    
    fig = go.Figure(go.Waterfall(
        measure=["relative", "relative", "relative", "relative", "total"],
        x=[
            t("Equipment", "主机销售"),
            t("Aftermarket", "售后服务"),
            t("Finance", "金融业务"),
            t("Used Equipment", "二手机"),
            t("Total Profit", "总利润")
        ],
        y=[equipment_profit, service_profit, finance_profit, used_profit, total_profit],
        text=[f"${x:,.0f}K" for x in [equipment_profit, service_profit, finance_profit, used_profit, total_profit]],
        textposition="outside",
        connector={"line": {"color": f"rgba(0, 102, 204, 0.3)" if st.session_state.theme == "light" else "rgba(0, 245, 255, 0.3)", "width": 2}},
        increasing={"marker": {"color": primary_color}},
        decreasing={"marker": {"color": danger_color}},
        totals={"marker": {"color": secondary_color}}
    ))
    
    fig.update_layout(
        template=chart_template,
        paper_bgcolor=chart_bgcolor,
        plot_bgcolor=chart_bgcolor,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        font=dict(family="Inter, sans-serif", color=text_color),
        xaxis=dict(
            tickfont=dict(size=11),
            gridcolor=grid_color
        ),
        yaxis=dict(
            title=t("Profit ($K)", "利润 (千美元)"),
            gridcolor=grid_color,
            zerolinecolor=f"rgba(0, 102, 204, 0.5)" if st.session_state.theme == "light" else "rgba(0, 245, 255, 0.5)"
        ),
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_right:
    # 价值链利润结构环图
    st.markdown(f"### 🥧 {t('Value Chain Structure', '价值链结构')}")
    
    profit_df = pd.DataFrame({
        "Chain": [
            t("Equipment", "主机"),
            t("Service", "售后"),
            t("Finance", "金融"),
            t("Used", "二手机")
        ],
        "Profit": [equipment_profit, service_profit, finance_profit, used_profit],
        "Color": colors
    })
    
    fig3 = go.Figure(data=[go.Pie(
        labels=profit_df["Chain"],
        values=profit_df["Profit"],
        hole=0.6,
        marker=dict(colors=profit_df["Color"], line=dict(color="rgba(255,255,255,0.8)" if st.session_state.theme == "light" else "rgba(20,25,40,0.8)", width=2)),
        textinfo="label+percent",
        textfont=dict(size=11, color=text_color),
        hovertemplate="%{label}<br>$%{value:,.0f}K<br>%{percent}<extra></extra>"
    )])
    
    fig3.update_layout(
        template=chart_template,
        paper_bgcolor=chart_bgcolor,
        plot_bgcolor=chart_bgcolor,
        height=400,
        margin=dict(l=20, r=20, t=40, b=20),
        showlegend=False,
        annotations=[dict(
            text=f"${total_profit:,.0f}K",
            x=0.5, y=0.5,
            font=dict(size=20, color=text_color, family="Inter"),
            showarrow=False
        )]
    )
    
    st.plotly_chart(fig3, use_container_width=True)

# ===============================
# 底部图表区域
# ===============================
col_bottom1, col_bottom2 = st.columns(2)

with col_bottom1:
    # 制造敏感性曲线
    st.markdown(f"### 📈 {t('Manufacturing Sensitivity', '制造敏感性分析')}")
    
    volumes_range = np.arange(200, 2000, 50)
    unit_cost_curve = (fixed_cost/volumes_range) + 5
    
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=volumes_range,
        y=unit_cost_curve,
        mode='lines',
        name=t("Unit Cost", "单位成本"),
        line=dict(color=primary_color, width=3),
        fill='tozeroy',
        fillcolor=f"rgba(0, 102, 204, 0.1)" if st.session_state.theme == "light" else "rgba(0, 245, 255, 0.1)"
    ))
    
    # 添加当前产量标记
    current_unit_cost = (fixed_cost/volume) + 5
    fig2.add_trace(go.Scatter(
        x=[volume],
        y=[current_unit_cost],
        mode='markers',
        name=t("Current Position", "当前位置"),
        marker=dict(color=danger_color, size=12, symbol="diamond",
                   line=dict(color="white", width=2))
    ))
    
    fig2.update_layout(
        template=chart_template,
        paper_bgcolor=chart_bgcolor,
        plot_bgcolor=chart_bgcolor,
        height=350,
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis=dict(
            title=t("Production Volume", "产量 (台)"),
            gridcolor=grid_color
        ),
        yaxis=dict(
            title=t("Unit Cost ($K)", "单位成本 (千美元)"),
            gridcolor=grid_color
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            font=dict(color=text_color)
        )
    )
    
    st.plotly_chart(fig2, use_container_width=True)

with col_bottom2:
    # 战略风险雷达
    st.markdown(f"### 🎯 {t('Strategic Risk Radar', '战略风险雷达')}")
    
    categories = [
        t("Inventory", "库存风险"),
        t("Raw Material", "原材料"),
        t("Finance", "金融风险"),
        t("Market", "市场风险"),
        t("R&D", "研发风险")
    ]
    
    # 计算风险值 (0-100)
    inventory_risk = min(inventory_growth * 2, 100)
    material_risk = raw_material_increase * 3
    finance_risk = bad_debt_rate * 4
    market_risk = 30 if volume < 500 else 20 if volume < 1000 else 15
    rd_risk = (1 - rd_rate) * 50
    
    values = [inventory_risk, material_risk, finance_risk, market_risk, rd_risk]
    values += values[:1]  # 闭合图形
    
    fig4 = go.Figure()
    
    fig4.add_trace(go.Scatterpolar(
        r=values,
        theta=categories + [categories[0]],
        fill='toself',
        fillcolor=f"rgba(0, 102, 204, 0.2)" if st.session_state.theme == "light" else "rgba(0, 245, 255, 0.2)",
        line=dict(color=primary_color, width=2),
        name=t("Risk Level", "风险水平")
    ))
    
    # 添加风险阈值圆
    fig4.add_trace(go.Scatterpolar(
        r=[50]*6,
        theta=categories + [categories[0]],
        mode='lines',
        line=dict(color=f"rgba(220, 38, 38, 0.5)" if st.session_state.theme == "light" else "rgba(239, 68, 68, 0.5)", width=1, dash="dash"),
        name=t("Warning Threshold", "警戒线"),
        showlegend=True
    ))
    
    fig4.update_layout(
        template=chart_template,
        paper_bgcolor=chart_bgcolor,
        plot_bgcolor=chart_bgcolor,
        height=350,
        margin=dict(l=40, r=40, t=40, b=20),
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor=grid_color,
                tickfont=dict(size=9, color=text_color)
            ),
            angularaxis=dict(
                gridcolor=grid_color,
                tickfont=dict(size=10, color=text_color)
            )
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5,
            font=dict(color=text_color)
        )
    )
    
    st.plotly_chart(fig4, use_container_width=True)

# ===============================
# 底部状态栏
# ===============================
st.markdown(f"""
<div class="success-box">
    ✅ {t('Executive Sandbox Active | Real-time Strategic Modeling', '战略沙盘运行中 | 实时战略建模')}
</div>
""", unsafe_allow_html=True)