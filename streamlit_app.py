import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import re
import io
import altair as alt

# Cấu hình trang
st.set_page_config(
    page_title="Tra cứu thông tin Cổ đông",
    page_icon="📈",
    layout="wide"
)

# ======================== CONSTANTS ========================
# Định nghĩa hằng số cho các tên cột
COL_DATE = "Ngày"
COL_TOTAL_MONEY = " Tổng "  # Note: has leading and trailing spaces
COL_DECREASE = " Giảm "  # Note: has leading and trailing spaces
COL_BALANCE = " Số dư "  # Note: has leading and trailing spaces
COL_CATEGORY = "Phân loại"
COL_BANK = "Ngân hàng"
COL_ACCOUNT = "STK"
COL_SHAREHOLDER = "Shareholder"
COL_ID = "ID"
COL_PRICE_DVDT = " Giá 1 ĐVĐT "  # Note: has leading and trailing spaces
COL_QUANTITY_DVDT = " Số lượng ĐVĐT "  # Note: has leading and trailing spaces
COL_CONTENT = "Content"

# Tên cột sau khi làm sạch
COL_TOTAL_MONEY_CLEAN = "Tổng_tiền_clean"
COL_PRICE_DVDT_CLEAN = "Giá_ĐVĐT_clean"
COL_QUANTITY_DVDT_CLEAN = "Số_lượng_ĐVĐT_clean"
COL_DATE_DATETIME = "Ngày_datetime"

@st.cache_data
def load_data():
    """Đọc và xử lý dữ liệu từ file CSV"""
    try:
        # Đọc file với encoding phù hợp
        try:
            df = pd.read_csv('data_shareholders.csv', encoding='utf-8-sig')
        except:
            try:
                df = pd.read_csv('data_shareholders.csv', encoding='cp1252')
            except:
                df = pd.read_csv('data_shareholders.csv', encoding='latin-1')
        
        # Kiểm tra xem DataFrame có dữ liệu không
        if df.empty:
            st.error("❌ **Lỗi:** File CSV không có dữ liệu")
            return None
        
        # Kiểm tra số cột
        if len(df.columns) < 9:
            st.error(f"❌ **Lỗi:** File CSV không đủ cột. Cần ít nhất 9 cột, nhưng chỉ có {len(df.columns)} cột")
            return None
        
        # Lọc chỉ lấy các dòng giao dịch chính (bỏ qua các dòng chi tiết)
        # Dòng giao dịch chính có đầy đủ thông tin trong các cột
        try:
            mask = (
                df.iloc[:, 0].notna() &  # Ngày
                df.iloc[:, 1].notna() &  # Tổng tiền
                df.iloc[:, 7].notna() &  # Shareholder
                df.iloc[:, 8].notna() &  # ID
                ~df.iloc[:, 0].astype(str).str.startswith('-')  # Không bắt đầu bằng dấu -
            )
            
            main_transactions = df[mask].copy()
            
            # Kiểm tra xem có dữ liệu sau khi lọc không
            if main_transactions.empty:
                st.error("❌ **Lỗi:** Không tìm thấy dữ liệu giao dịch hợp lệ trong file CSV")
                st.info("💡 Vui lòng kiểm tra lại định dạng dữ liệu trong file CSV")
                return None
                
        except Exception as e:
            st.error(f"❌ **Lỗi khi lọc dữ liệu:** {e}")
            return None
        
        # Đặt tên cột chuẩn - sử dụng tên cột thực tế từ CSV
        try:
            main_transactions.columns = [
                "Ngày", " Tổng ", " Giảm ", " Số dư ", "Phân loại", 
                "Ngân hàng", "STK", "Shareholder", "ID", 
                " Giá 1 ĐVĐT ", " Số lượng ĐVĐT ", "Content"
            ]
        except Exception as e:
            st.error(f"❌ **Lỗi khi đặt tên cột:** {e}")
            return None
        
        # Làm sạch dữ liệu
        def clean_money(value):
            """Chuyển đổi giá trị tiền tệ sang số"""
            if pd.isna(value):
                return 0
            value_str = str(value).replace(',', '').replace(' ', '').replace('"', '')
            try:
                return float(value_str)
            except:
                return 0
        
        try:
            main_transactions[COL_TOTAL_MONEY_CLEAN] = main_transactions[" Tổng "].apply(clean_money)
            main_transactions[COL_PRICE_DVDT_CLEAN] = main_transactions[" Giá 1 ĐVĐT "].apply(clean_money)
            main_transactions[COL_QUANTITY_DVDT_CLEAN] = main_transactions[" Số lượng ĐVĐT "].apply(clean_money)
            
            # Chuyển đổi ngày
            main_transactions[COL_DATE_DATETIME] = pd.to_datetime(main_transactions["Ngày"], format='%d/%m/%Y', errors='coerce')
            
        except Exception as e:
            st.error(f"❌ **Lỗi khi xử lý dữ liệu:** {e}")
            return None
        
        return main_transactions
        
    except FileNotFoundError:
        st.error("❌ **Lỗi:** Không tìm thấy tệp 'data_shareholders.csv'")
        st.info("💡 Vui lòng đảm bảo tệp dữ liệu nằm cùng thư mục với ứng dụng")
        return None
    except Exception as e:
        st.error(f"❌ **Lỗi không xác định:** {e}")
        return None

def format_currency(amount):
    """Format số tiền theo định dạng Việt Nam"""
    return f"{amount:,.0f}".replace(',', '.')

def calculate_performance(nav, investment):
    """Tính hiệu suất đầu tư với xử lý lỗi chia cho 0"""
    if investment > 0:
        return (nav / investment - 1) * 100
    else:
        return 0

def create_download_data(shareholder_data, shareholder_name):
    """Tạo dữ liệu để download"""
    # Chuẩn bị dữ liệu export
    export_data = shareholder_data[[COL_DATE, COL_TOTAL_MONEY_CLEAN, COL_PRICE_DVDT_CLEAN, COL_QUANTITY_DVDT_CLEAN, COL_BANK]].copy()
    export_data.columns = ['Ngày chuyển tiền', 'Số tiền (VNĐ)', 'Giá ĐVĐT (VNĐ)', 'Số ĐVĐT', 'Ngân hàng']
    
    # Thêm thông tin tổng kết
    total_investment = shareholder_data[COL_TOTAL_MONEY_CLEAN].sum()
    total_dvdt = shareholder_data[COL_QUANTITY_DVDT_CLEAN].sum()
    
    summary_data = pd.DataFrame({
        'Thông tin': ['Tên cổ đông', 'Tổng số tiền đầu tư (VNĐ)', 'Tổng số ĐVĐT sở hữu', 'Số lần giao dịch'],
        'Giá trị': [shareholder_name, f"{total_investment:,.0f}", f"{total_dvdt:,.0f}", len(shareholder_data)]
    })
    
    # Tạo buffer để ghi Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        export_data.to_excel(writer, sheet_name='Lịch sử giao dịch', index=False)
        summary_data.to_excel(writer, sheet_name='Tổng kết', index=False)
    
    return buffer.getvalue()

def main():
    st.title("🏦 Hệ thống Tra cứu Thông tin Cổ đông")
    st.markdown("---")
    
    # Tải dữ liệu
    df = load_data()
    if df is None:
        st.error("❌ **Lỗi:** Không thể tải được file dữ liệu. Vui lòng kiểm tra lại file `data_shareholders.csv` và đảm bảo tên cột đã chính xác.")
        st.info("💡 **Các bước kiểm tra:**")
        st.info("1. Đảm bảo file `data_shareholders.csv` tồn tại trong thư mục")
        st.info("2. Kiểm tra định dạng CSV có đúng không")
        st.info("3. Đảm bảo file có ít nhất 9 cột dữ liệu")
        st.info("4. Kiểm tra encoding của file (UTF-8, CP1252, hoặc Latin-1)")
        st.stop()
    
    # Kiểm tra bổ sung: đảm bảo DataFrame có dữ liệu và các cột cần thiết
    if df.empty:
        st.error("❌ **Lỗi:** DataFrame rỗng sau khi tải dữ liệu")
        st.stop()
    
    # Kiểm tra các cột cần thiết có tồn tại không
    required_columns = [COL_ID, COL_SHAREHOLDER, COL_TOTAL_MONEY_CLEAN, COL_PRICE_DVDT_CLEAN, COL_QUANTITY_DVDT_CLEAN]
    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        st.error(f"❌ **Lỗi:** Thiếu các cột cần thiết: {missing_columns}")
        st.info(f"💡 Các cột hiện có: {list(df.columns)}")
        st.stop()
    
    # Sidebar cho nhập thông tin và hướng dẫn
    st.sidebar.header("🔍 Tra cứu thông tin")
    
    # Nhập ID cổ đông
    shareholder_id = st.sidebar.text_input(
        "Nhập ID cổ đông:",
        placeholder="VD: NGUYENVANABC345678",
        help="Họ tên viết liền không dấu + 6-8 số cuối STK"
    ).upper()
    
    # Nhập giá ĐVĐT hiện tại
    current_price = st.sidebar.number_input(
        "Giá ĐVĐT hiện tại (VNĐ):",
        min_value=0.0,
        value=10000.0,
        step=100.0,
        format="%.0f",
        help="Nhập giá trị ĐVĐT hiện tại để tính NAV"
    )
    
    # Nút tra cứu
    search_button = st.sidebar.button("🔍 Tra cứu", type="primary")
    
    # Nút làm mới dữ liệu
    st.sidebar.markdown("---")
    if st.sidebar.button("🔄 Làm mới dữ liệu", help="Tải lại dữ liệu mới nhất từ file"):
        st.cache_data.clear()
        st.rerun()
    
    # Thêm hướng dẫn vào sidebar
    st.sidebar.markdown("---")
    st.sidebar.subheader("📖 Hướng dẫn sử dụng")
    
    with st.sidebar.expander("💡 Cách tra cứu", expanded=False):
        st.markdown("""
        **Các bước:**
        1. Nhập ID cổ đông
        2. Nhập giá ĐVĐT hiện tại  
        3. Nhấn "🔍 Tra cứu"
        
        **Format ID:**
        - Họ tên viết liền không dấu
        - + 6-8 số cuối STK
        - VD: NGUYENVANABC345678
        """)
    
    with st.sidebar.expander("📊 Thông tin hiển thị", expanded=False):
        st.markdown("""
        **Kết quả bao gồm:**
        - Tổng số tiền đầu tư
        - Tổng số ĐVĐT sở hữu
        - NAV hiện tại
        - Hiệu suất đầu tư (%)
        - Lịch sử chi tiết (có thể mở rộng)
        - Biểu đồ tích lũy (nếu có nhiều giao dịch)
        - **Nút tải báo cáo Excel** 📥
        """)
    
    # Hiển thị ID mẫu giả định trong sidebar (để bảo vệ thông tin thật)
    sample_examples = [
        "NGUYENVANABC345678",
        "TRANVANDEFG123456", 
        "LEHIEUQUANG987654"
    ]
    
    with st.sidebar.expander("🔍 Ví dụ ID", expanded=False):
        st.markdown("**Các ví dụ ID (giả định):**")
        st.markdown("*Đây chỉ là ví dụ format, vui lòng nhập ID thật của bạn*")
        for idx, id_example in enumerate(sample_examples):
            st.code(id_example, language=None)
        
        st.markdown("**📝 Cách tạo ID:**")
        st.markdown("""
        - Họ tên: NGUYEN VAN ABC
        - STK: 12345678  
        - ➡️ ID: **NGUYENVANABC345678**
        """)
    
    # Xử lý tìm kiếm và lưu kết quả vào session state
    if search_button and shareholder_id:
        # Lưu kết quả tìm kiếm vào session state
        search_data = df[df[COL_ID].str.upper() == shareholder_id].copy()
        st.session_state.search_results = {
            'shareholder_id': shareholder_id,
            'current_price': current_price,
            'data': search_data,
            'search_performed': True
        }
    
    # Reset search khi thay đổi ID
    if search_button and not shareholder_id:
        st.warning("⚠️ Vui lòng nhập ID cổ đông để tra cứu")
        if 'search_results' in st.session_state:
            del st.session_state.search_results
    
    # Hiển thị kết quả từ session state (để tránh mất dữ liệu khi slider thay đổi)
    if 'search_results' in st.session_state and st.session_state.search_results['search_performed']:
        search_data = st.session_state.search_results
        result_shareholder_id = search_data['shareholder_id'] 
        base_price = search_data['current_price']
        shareholder_data = search_data['data']
        
        if shareholder_data.empty:
            st.error(f"❌ Không tìm thấy thông tin cho ID: **{result_shareholder_id}**")
            
            # Hiển thị gợi ý
            col1, col2 = st.columns(2)
            with col1:
                st.info("💡 **Kiểm tra lại:**")
                st.write("- Format: Họ tên không dấu + 6-8 số cuối STK")
                st.write("- Viết hoa toàn bộ")
                st.write("- Không có khoảng trắng")
                
            with col2:
                st.info("🔍 **Ví dụ format:**")
                st.write("• NGUYENVANABC345678")
                st.write("• TRANVANDEFG123456")
                st.write("• LEHIEUQUANG987654")
                     
        else:
            # Sắp xếp theo ngày
            shareholder_data = shareholder_data.sort_values(COL_DATE_DATETIME)
            
            # Thông tin cổ đông với lời chào cá nhân hóa
            shareholder_name = shareholder_data[COL_SHAREHOLDER].iloc[0]
            st.success(f"👋 **Xin chào, {shareholder_name}!** Dưới đây là thông tin đầu tư của bạn.")
            st.markdown(f"🆔 **ID:** {result_shareholder_id}")
            
            # Tính toán các chỉ số cơ bản với xử lý lỗi
            total_investment = shareholder_data[COL_TOTAL_MONEY_CLEAN].sum()
            total_dvdt = shareholder_data[COL_QUANTITY_DVDT_CLEAN].sum()
            base_nav = total_dvdt * base_price
            base_performance = calculate_performance(base_nav, total_investment)
            
            # Tạo 2 cột chính
            col1, col2 = st.columns([3, 2])
            
            with col1:
                st.subheader("📊 Tổng kết Đầu tư")
                
                # Tạo 2 hàng metrics
                metric_col1, metric_col2 = st.columns(2)
                
                with metric_col1:
                    st.metric(
                        label="💰 Tổng tiền đầu tư",
                        value=f"{format_currency(total_investment)} VNĐ"
                    )
                    
                    st.metric(
                        label="💎 NAV hiện tại",
                        value=f"{format_currency(base_nav)} VNĐ",
                        delta=f"{format_currency(base_nav - total_investment)} VNĐ"
                    )
                
                with metric_col2:
                    st.metric(
                        label="📈 Tổng ĐVĐT sở hữu",
                        value=f"{format_currency(total_dvdt)} ĐVĐT"
                    )
                    
                    # Hiển thị hiệu suất với màu sắc
                    if base_performance >= 0:
                        st.metric(
                            label="🚀 Hiệu suất đầu tư",
                            value=f"{base_performance:.2f}%",
                            delta=f"+{base_performance:.2f}%"
                        )
                    else:
                        st.metric(
                            label="📉 Hiệu suất đầu tư", 
                            value=f"{base_performance:.2f}%",
                            delta=f"{base_performance:.2f}%"
                        )
                
                # Sử dụng expander cho lịch sử giao dịch chi tiết
                with st.expander("📋 Xem chi tiết lịch sử giao dịch", expanded=False):
                    # Tạo bảng hiển thị với thông tin đầy đủ và giá mua trung bình
                    display_data = shareholder_data[[COL_DATE, COL_TOTAL_MONEY_CLEAN, COL_PRICE_DVDT_CLEAN, COL_QUANTITY_DVDT_CLEAN, COL_BANK]].copy()
                    
                    # Tính toán các cột tích lũy và giá mua trung bình
                    display_data['Tích_lũy_tiền'] = display_data[COL_TOTAL_MONEY_CLEAN].cumsum()
                    display_data['Tích_lũy_ĐVĐT'] = display_data[COL_QUANTITY_DVDT_CLEAN].cumsum()
                    
                    # Tính giá mua trung bình (tránh chia cho 0)
                    display_data['Giá_mua_trung_bình'] = np.where(
                        display_data['Tích_lũy_ĐVĐT'] > 0,
                        display_data['Tích_lũy_tiền'] / display_data['Tích_lũy_ĐVĐT'],
                        0
                    )
                    
                    # Đổi tên cột cho thân thiện
                    display_data.columns = [
                        'Ngày chuyển tiền', 'Số tiền đầu tư (VNĐ)', 'Giá ĐVĐT (VNĐ)', 
                        'Số ĐVĐT mua', 'Ngân hàng', 'Tích lũy tiền (VNĐ)', 
                        'Tích lũy ĐVĐT', 'Giá mua TB (VNĐ)'
                    ]
                    
                    # Hiển thị với định dạng số đẹp
                    st.dataframe(
                        display_data.style.format({
                            'Số tiền đầu tư (VNĐ)': '{:,.0f}',
                            'Giá ĐVĐT (VNĐ)': '{:,.0f}',
                            'Số ĐVĐT mua': '{:,.3f}',
                            'Tích lũy tiền (VNĐ)': '{:,.0f}',
                            'Tích lũy ĐVĐT': '{:,.3f}',
                            'Giá mua TB (VNĐ)': '{:,.0f}'
                        }),
                        use_container_width=True
                    )
                    
                    # Nút tải báo cáo
                    try:
                        excel_data = create_download_data(shareholder_data, shareholder_name)
                        st.download_button(
                            label="📥 Tải báo cáo Excel",
                            data=excel_data,
                            file_name=f"Bao_cao_dau_tu_{result_shareholder_id}_{datetime.now().strftime('%Y%m%d')}.xlsx",
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            help="Tải xuống báo cáo đầu tư chi tiết dạng Excel"
                        )
                    except Exception as e:
                        st.warning(f"⚠️ Không thể tạo file Excel: {e}")
                        st.info("💡 Vui lòng cài đặt: `pip install openpyxl`")
                    
                    # Thống kê nhanh
                    st.markdown("**📈 Thống kê nhanh:**")
                    stats_col1, stats_col2, stats_col3 = st.columns(3)
                    with stats_col1:
                        st.metric("Số lần giao dịch", len(shareholder_data))
                    with stats_col2:
                        st.metric("Tổng đầu tư", f"{format_currency(total_investment)} VNĐ")
                    with stats_col3:
                        if len(shareholder_data) > 1:
                            last_date = shareholder_data[COL_DATE_DATETIME].max().strftime('%d/%m/%Y')
                            st.metric("Lần gần nhất", last_date)
                        else:
                            first_date = shareholder_data[COL_DATE_DATETIME].min().strftime('%d/%m/%Y')
                            st.metric("Ngày đầu tư", first_date)
            
            with col2:
                st.subheader("🎯 Mô phỏng What-if")
                st.markdown("*Thay đổi giá để xem NAV khác nhau:*")
                
                # Slider cho tính năng What-if
                min_price = max(1000, base_price * 0.5)
                max_price = base_price * 2
                
                whatif_price = st.slider(
                    "Giá ĐVĐT giả định (VNĐ):",
                    min_value=int(min_price),
                    max_value=int(max_price),
                    value=int(base_price),
                    step=100,
                    format="%d",
                    help="Kéo thanh trượt để xem NAV thay đổi real-time",
                    key="whatif_slider"  # Thêm key để tránh conflict
                )
                
                # Tính toán real-time với xử lý lỗi
                whatif_nav = total_dvdt * whatif_price
                whatif_performance = calculate_performance(whatif_nav, total_investment)
                nav_difference = whatif_nav - base_nav
                performance_difference = whatif_performance - base_performance
                
                # Hiển thị kết quả What-if
                st.markdown("**🔮 Kết quả mô phỏng:**")
                
                st.metric(
                    label="NAV giả định",
                    value=f"{format_currency(whatif_nav)} VNĐ",
                    delta=f"{format_currency(nav_difference)} VNĐ"
                )
                
                st.metric(
                    label="Hiệu suất giả định",
                    value=f"{whatif_performance:.2f}%",
                    delta=f"{performance_difference:.2f}%"
                )
                
                # Hiển thị bảng so sánh
                st.markdown("**📊 Bảng so sánh:**")
                comparison_data = pd.DataFrame({
                    'Chỉ số': ['Giá ĐVĐT', 'NAV', 'Hiệu suất'],
                    'Hiện tại': [
                        f"{format_currency(base_price)} VNĐ",
                        f"{format_currency(base_nav)} VNĐ", 
                        f"{base_performance:.2f}%"
                    ],
                    'Giả định': [
                        f"{format_currency(whatif_price)} VNĐ",
                        f"{format_currency(whatif_nav)} VNĐ",
                        f"{whatif_performance:.2f}%"
                    ]
                })
                st.dataframe(comparison_data, use_container_width=True, hide_index=True)
            
            # Biểu đồ nâng cao với Altair (nếu có nhiều giao dịch)
            if len(shareholder_data) > 1:
                st.subheader("📈 Biểu đồ Lịch sử Đầu tư")
                
                # Chuẩn bị dữ liệu cho biểu đồ
                chart_data = shareholder_data.copy()
                chart_data['Tích lũy tiền'] = chart_data[COL_TOTAL_MONEY_CLEAN].cumsum()
                chart_data['Tích lũy ĐVĐT'] = chart_data[COL_QUANTITY_DVDT_CLEAN].cumsum()
                
                # Tính giá mua trung bình cho tooltip
                chart_data['Giá mua TB'] = np.where(
                    chart_data['Tích lũy ĐVĐT'] > 0,
                    chart_data['Tích lũy tiền'] / chart_data['Tích lũy ĐVĐT'],
                    0
                )
                
                chart_col1, chart_col2 = st.columns(2)
                
                with chart_col1:
                    st.markdown("**💰 Tích lũy số tiền đầu tư**")
                    
                    chart_invest = alt.Chart(chart_data).mark_line(
                        point=alt.OverlayMarkDef(filled=False, fill="white", size=50),
                        strokeWidth=3,
                        color='#1f77b4'
                    ).encode(
                        x=alt.X(f'{COL_DATE_DATETIME}:T', title='Ngày', axis=alt.Axis(format='%d/%m')),
                        y=alt.Y('Tích lũy tiền:Q', title='Tổng tiền đầu tư (VNĐ)', axis=alt.Axis(format=',.0f')),
                        tooltip=[
                            alt.Tooltip(f'{COL_DATE_DATETIME}:T', title='Ngày giao dịch', format='%d/%m/%Y'),
                            alt.Tooltip(f'{COL_TOTAL_MONEY_CLEAN}:Q', title='Tiền đầu tư thêm', format=',.0f'),
                            alt.Tooltip('Tích lũy tiền:Q', title='Tổng tiền tích lũy', format=',.0f'),
                            alt.Tooltip('Giá mua TB:Q', title='Giá mua trung bình', format=',.0f')
                        ]
                    ).interactive()
                    
                    st.altair_chart(chart_invest, use_container_width=True)
                
                with chart_col2:
                    st.markdown("**📈 Tích lũy ĐVĐT sở hữu**")
                    
                    chart_units = alt.Chart(chart_data).mark_line(
                        point=alt.OverlayMarkDef(filled=False, fill="white", size=50),
                        strokeWidth=3,
                        color='#ff7f0e'
                    ).encode(
                        x=alt.X(f'{COL_DATE_DATETIME}:T', title='Ngày', axis=alt.Axis(format='%d/%m')),
                        y=alt.Y('Tích lũy ĐVĐT:Q', title='Tổng ĐVĐT sở hữu', axis=alt.Axis(format=',.1f')),
                        tooltip=[
                            alt.Tooltip(f'{COL_DATE_DATETIME}:T', title='Ngày giao dịch', format='%d/%m/%Y'),
                            alt.Tooltip(f'{COL_PRICE_DVDT_CLEAN}:Q', title='Giá tại ngày mua', format=',.0f'),
                            alt.Tooltip(f'{COL_QUANTITY_DVDT_CLEAN}:Q', title='ĐVĐT mua thêm', format=',.3f'),
                            alt.Tooltip('Tích lũy ĐVĐT:Q', title='Tổng ĐVĐT tích lũy', format=',.3f'),
                            alt.Tooltip('Giá mua TB:Q', title='Giá mua trung bình', format=',.0f')
                        ]
                    ).interactive()
                    
                    st.altair_chart(chart_units, use_container_width=True)
    
    # Thông tin footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666; font-size: 14px;'>
            🏦 Hệ thống Tra cứu Thông tin Cổ đông | Được xây dựng bằng Streamlit
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 