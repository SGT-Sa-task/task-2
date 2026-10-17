"""
main.py — Streamlit entry point for the HubSpot Contact Sync app.
"""

import streamlit as st

from services.sync_service import run_sync

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HubSpot Contact Sync",
    page_icon="🔄",
    layout="centered",
)

st.title("🔄 HubSpot Contact Sync")
st.caption("Đọc danh sách contact từ Google Sheets và đồng bộ lên HubSpot CRM.")

st.divider()

# ── Sync trigger ──────────────────────────────────────────────────────────────
if st.button("▶ Bắt đầu đồng bộ", type="primary", use_container_width=True):
    with st.spinner("Đang đồng bộ dữ liệu…"):
        try:
            result = run_sync()
        except Exception as exc:  # noqa: BLE001
            st.error(f"❌ Lỗi khi kết nối: {exc}")
            st.stop()

    # ── Summary metrics ───────────────────────────────────────────────────────
    st.divider()
    col1, col2, col3 = st.columns(3)
    col1.metric("✅ Đã tạo mới", result.created)
    col2.metric("♻️ Đã cập nhật", result.updated)
    col3.metric("❌ Thất bại", result.failed)

    if result.failed == 0:
        st.success(f"Đồng bộ hoàn tất! " f"Đã xử lý **{result.total}** contact.")
    else:
        st.warning(
            f"Đồng bộ xong với **{result.failed}** lỗi. " "Xem chi tiết bên dưới."
        )
        with st.expander("Chi tiết lỗi"):
            for err in result.errors:
                st.write(f"• {err}")
