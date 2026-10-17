"""
main.py — Streamlit entry point for the HubSpot Contact Sync app.
"""

import streamlit as st

from core import gsheet_api
from services import sheet_storage_service
from services.sync_service import restore_created_contacts, run_sync

# ── Page configuration ────────────────────────────────────────────────────────
st.set_page_config(
    page_title="HubSpot Contact Sync",
    page_icon="🔄",
    layout="wide",
)

# ── Session State initialization ──────────────────────────────────────────────
if "recently_created_ids" not in st.session_state:
    st.session_state["recently_created_ids"] = []

st.title("🔄 HubSpot Contact Sync")
st.caption("Đọc danh sách contact từ Google Sheets và đồng bộ lên HubSpot CRM.")

st.divider()

# ── Two-column layout: Dynamic content (Left) vs Static content (Right) ───────
col_dynamic, col_static = st.columns([65, 35], gap="large")

# ==============================================================================
# ◀ LEFT COLUMN: Dynamic content (Add sheet, View saved sheets, Trigger sync)
# ==============================================================================
with col_dynamic:
    # ── 1. Add New Google Sheet Record ───────────────────────────────────────
    st.subheader("➕ Thêm Google Sheet Mới")
    with st.form("add_sheet_form", clear_on_submit=True):
        new_sheet_url = st.text_input(
            "Dán link Google Sheet:",
            placeholder="https://docs.google.com/spreadsheets/d/...",
        )
        submitted = st.form_submit_button("💾 Lưu Sheet", type="secondary")

        if submitted:
            sheet_url_clean = new_sheet_url.strip()
            if not sheet_url_clean:
                st.warning("Vui lòng nhập link Google Sheet.")
            else:
                with st.spinner("Đang kết nối đến Google Sheet để lấy thông tin…"):
                    try:
                        info = gsheet_api.get_spreadsheet_info(sheet_url_clean)
                        title = info.get("title", "")
                        sheet_id = info.get("id", "")

                        saved = sheet_storage_service.save_sheet_record(
                            name=title,
                            link=sheet_url_clean,
                            sheet_id=sheet_id,
                        )
                        if saved:
                            st.success(
                                f"✅ Đã thêm sheet thành công: **{title}** "
                                f"(ID: `{sheet_id}`)"
                            )
                            st.rerun()
                        else:
                            st.error("❌ Không thể lưu vào `storage/local-data.csv`.")
                    except Exception as exc:  # noqa: BLE001
                        st.error(
                            f"❌ Không thể truy cập Google Sheet. Vui lòng kiểm tra "
                            f"link và đảm bảo đã cấp quyền Editor cho bot.\n\n"
                            f"Chi tiết: {exc}"
                        )

    st.divider()

    # ── 2. Saved Google Sheets List & Selection ──────────────────────────────
    st.subheader("📋 Danh sách Google Sheet đã lưu")
    saved_sheets = sheet_storage_service.load_saved_sheets()

    if not saved_sheets:
        st.info(
            "Chưa có sheet nào được lưu. Hãy dán link ở form trên để thêm sheet mới."
        )
        selected_sheet_url = None
    else:
        # Display table of saved sheets
        display_data = [
            {
                "Tên Sheet": s.get("Tên của sheet", ""),
                "ID Sheet": s.get("ID Sheet", ""),
                "Truy cập lần cuối": (s.get("Truy cập lần cuối", "") or "Chưa đồng bộ"),
                "Link": s.get("Link", ""),
            }
            for s in saved_sheets
        ]
        st.dataframe(display_data, use_container_width=True)

        # Sheet selector
        sheet_options = [s.get("Link") for s in saved_sheets]

        def _format_sheet_option(link: str) -> str:
            for s in saved_sheets:
                if s.get("Link") == link:
                    last_time = s.get("Truy cập lần cuối") or "Chưa đồng bộ"
                    return f"{s.get('Tên của sheet')} ({last_time})"
            return link

        selected_sheet_url = st.selectbox(
            "Chọn Google Sheet để đồng bộ:",
            options=sheet_options,
            format_func=_format_sheet_option,
        )

        if selected_sheet_url:
            st.link_button(
                "🔗 Mở Google Sheet trong tab mới",
                url=selected_sheet_url,
                use_container_width=True,
            )

    st.divider()

    # ── 3. Sync trigger & Result Metrics ─────────────────────────────────────
    st.subheader("⚡ Thực thi Đồng bộ")

    col_btn_new, col_btn_retry, col_btn_restore = st.columns(3)
    btn_sync_new = col_btn_new.button(
        "▶ Bắt đầu đồng bộ (NEW)",
        type="primary",
        use_container_width=True,
        disabled=(selected_sheet_url is None),
    )
    btn_retry_error = col_btn_retry.button(
        "🔁 Thử lại dòng lỗi (ERROR)",
        type="secondary",
        use_container_width=True,
        disabled=(selected_sheet_url is None),
    )
    recent_ids = st.session_state.get("recently_created_ids", [])
    btn_restore = col_btn_restore.button(
        "⏪ Khôi phục (Restore)",
        type="secondary",
        use_container_width=True,
        disabled=(len(recent_ids) == 0),
        help="Chỉ xóa các user vừa thêm trên HubSpot thôi, không chỉnh sửa lại sheet.",
    )

    if btn_restore:
        with st.spinner(f"Đang xóa {len(recent_ids)} contact vừa thêm trên HubSpot…"):
            del_count, del_errs = restore_created_contacts(recent_ids)
            st.session_state["recently_created_ids"] = []

            if del_count > 0:
                st.success(
                    f"✅ Đã khôi phục thành công! Đã xóa **{del_count}** contact khỏi HubSpot."
                )
            if del_errs:
                st.warning(
                    f"Có **{len(del_errs)}** lỗi xảy ra khi khôi phục. Xem chi tiết bên dưới."
                )
                with st.expander("Chi tiết lỗi khôi phục"):
                    for err in del_errs:
                        st.write(f"• {err}")

    active_mode = None
    if btn_sync_new:
        active_mode = "NEW"
    elif btn_retry_error:
        active_mode = "RETRY"

    if active_mode:
        spinner_msg = (
            "Đang đồng bộ các dòng NEW…"
            if active_mode == "NEW"
            else "Đang thử lại các dòng ERROR…"
        )
        with st.spinner(spinner_msg):
            try:
                result = run_sync(
                    sheet_url=selected_sheet_url,
                    sync_mode=active_mode,
                )
                sheet_storage_service.update_last_accessed(selected_sheet_url)
                if result.created_contact_ids:
                    st.session_state["recently_created_ids"] = (
                        result.created_contact_ids
                    )
            except Exception as exc:  # noqa: BLE001
                st.error(f"❌ Lỗi khi đồng bộ: {exc}")
                st.stop()

        # ── Summary metrics ───────────────────────────────────────────────────
        col1, col2, col3 = st.columns(3)
        col1.metric("✅ Đã tạo mới", result.created)
        col2.metric("♻️ Đã cập nhật", result.updated)
        col3.metric("❌ Thất bại", result.failed)

        if result.total == 0:
            target_label = "NEW" if active_mode == "NEW" else "ERROR"
            st.info(f"ℹ️ Không có dòng nào ở trạng thái `{target_label}` cần xử lý.")
        elif result.failed == 0:
            st.success(f"Đồng bộ hoàn tất! Đã xử lý **{result.total}** contact.")
        else:
            st.warning(
                f"Đồng bộ xong với **{result.failed}** lỗi. Xem chi tiết bên dưới."
            )
            with st.expander("Chi tiết lỗi"):
                for err in result.errors:
                    st.write(f"• {err}")


# ==============================================================================
# ▶ RIGHT COLUMN: Static content (Bot info, Permission notice, Guidelines)
# ==============================================================================
with col_static:
    # ── 1. Bot Account Information ───────────────────────────────────────────
    st.subheader("🤖 Tài khoản Bot Gmail")
    bot_email = sheet_storage_service.get_bot_account_email()

    if bot_email:
        st.caption("Google Service Account thực thi các thao tác đọc & ghi:")
        st.code(bot_email, language="")
    else:
        st.warning("⚠️ Không tìm thấy email của bot trong `storage/bot-account.txt`.")

    # ── 2. Permission Notice & Step-by-step Guide ────────────────────────────
    st.subheader("🔑 Hướng dẫn cấp quyền Editor")
    st.info(
        "⚠️ **Bắt buộc:** Bạn cần chia sẻ Google Sheet cho tài khoản Bot với quyền "
        "**Editor (Người chỉnh sửa)** để hệ thống đọc dữ liệu và ghi trạng thái.\n\n"
        "**Các bước thực hiện:**\n"
        "1. Mở file Google Sheet cần đồng bộ trên trình duyệt.\n"
        "2. Nhấn nút **Chia sẻ (Share)** ở góc trên bên phải.\n"
        "3. Dán email Bot ở trên vào ô nhập người nhận.\n"
        "4. Chọn vai trò: **Người chỉnh sửa (Editor)**.\n"
        "5. Bỏ tích 'Thông báo cho mọi người' nếu muốn, rồi nhấn **Chia sẻ (Share)**."
    )

    # ── 3. Data Format & Sync Rules ──────────────────────────────────────────
    st.subheader("📑 Quy chuẩn dữ liệu & Chức năng")
    st.markdown(
        """
        - **Cột bắt buộc:** `email` hoặc `phone`, `status`, `hubspot_id`.
        - **Chế độ đồng bộ:**
            - **▶ Bắt đầu đồng bộ (NEW):** Chỉ lọc và đồng bộ các dòng có trạng thái `NEW`.
            - **🔁 Thử lại dòng lỗi (ERROR):** Chỉ quét và thực thi lại các dòng có trạng thái `ERROR`.
            - Sau khi đồng bộ thành công, bot sẽ tự cập nhật cột `status` thành `SUCCESS` hoặc `UPDATED`, đồng thời ghi `hubspot_id`.
        - **⏪ Khôi phục (Restore):**
            - Xóa các user/contact vừa được thêm mới trên HubSpot trong lần chạy gần nhất.
            - Hoàn toàn **không chỉnh sửa hay thay đổi** dữ liệu trên Google Sheet.
        - **Cơ chế nhận diện Contact:**
            - Tra cứu theo **Email** trước.
            - Nếu không có Email, hệ thống dùng **Số điện thoại** để tìm kiếm.
        - **🔗 Mở Sheet:** Nhấn để truy cập trực tiếp Google Sheet trong tab mới.
        """
    )
