"""
main.py — Streamlit entry point for the HubSpot Contact Sync app.
"""

import streamlit as st

from core import gsheet_api, hubspot_api
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
if "hubspot_cursor" not in st.session_state:
    st.session_state["hubspot_cursor"] = ""

st.title("🔄 HubSpot CRM Integration Hub")
st.caption(
    "Đồng bộ liên hệ từ Google Sheets lên HubSpot và tra cứu danh bạ HubSpot CRM."
)

tab_sync, tab_contacts = st.tabs(["🔄 Đồng bộ Google Sheet", "👥 Danh bạ HubSpot CRM"])


def _render_sync_tab() -> None:
    """Render the Google Sheet synchronization view."""
    col_dynamic, col_static = st.columns([65, 35], gap="large")

    # ==========================================================================
    # ◀ LEFT COLUMN: Dynamic content (Add sheet, View saved sheets, Trigger sync)
    # ==========================================================================
    with col_dynamic:
        # ── 1. Add New Google Sheet Record ───────────────────────────────────
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
                                st.error(
                                    "❌ Không thể lưu vào " "`storage/local-data.csv`."
                                )
                        except Exception as exc:  # noqa: BLE001
                            st.error(
                                "❌ Không thể truy cập Google Sheet. Vui lòng "
                                "kiểm tra link và đảm bảo đã cấp quyền "
                                "Editor cho bot.\n\n"
                                f"Chi tiết: {exc}"
                            )

        st.divider()

        # ── 2. Saved Google Sheets List & Selection ──────────────────────────
        st.subheader("📋 Danh sách Google Sheet đã lưu")
        saved_sheets = sheet_storage_service.load_saved_sheets()

        if not saved_sheets:
            st.info(
                "Chưa có sheet nào được lưu. Hãy dán link ở form trên "
                "để thêm sheet mới."
            )
            selected_sheet_url = None
        else:
            # Display table of saved sheets
            display_data = [
                {
                    "Tên Sheet": s.get("Tên của sheet", ""),
                    "ID Sheet": s.get("ID Sheet", ""),
                    "Truy cập lần cuối": (
                        s.get("Truy cập lần cuối", "") or "Chưa đồng bộ"
                    ),
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

        # ── 3. Sync trigger & Result Metrics ─────────────────────────────────
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
            help="Chỉ xóa các user vừa thêm trên HubSpot thôi, "
            "không chỉnh sửa lại sheet.",
        )

        if btn_restore:
            with st.spinner(
                f"Đang xóa {len(recent_ids)} contact vừa thêm trên HubSpot…"
            ):
                del_count, del_errs = restore_created_contacts(recent_ids)
                st.session_state["recently_created_ids"] = []

                if del_count > 0:
                    st.success(
                        f"✅ Đã khôi phục thành công! Đã xóa **{del_count}** "
                        "contact khỏi HubSpot."
                    )
                if del_errs:
                    st.warning(
                        f"Có **{len(del_errs)}** lỗi xảy ra khi khôi phục. "
                        "Xem chi tiết bên dưới."
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

            # ── Summary metrics ───────────────────────────────────────────────
            col1, col2, col3 = st.columns(3)
            col1.metric("✅ Đã tạo mới", result.created)
            col2.metric("♻️ Đã cập nhật", result.updated)
            col3.metric("❌ Thất bại", result.failed)

            if result.total == 0:
                target_label = "NEW" if active_mode == "NEW" else "ERROR"
                st.info(
                    f"ℹ️ Không có dòng nào ở trạng thái `{target_label}` " "cần xử lý."
                )
            elif result.failed == 0:
                st.success(f"Đồng bộ hoàn tất! Đã xử lý **{result.total}** contact.")
            else:
                st.warning(
                    f"Đồng bộ xong với **{result.failed}** lỗi. "
                    "Xem chi tiết bên dưới."
                )
                with st.expander("Chi tiết lỗi"):
                    for err in result.errors:
                        st.write(f"• {err}")

    # ==========================================================================
    # ▶ RIGHT COLUMN: Static content (Bot info, Permission notice, Guidelines)
    # ==========================================================================
    with col_static:
        # ── 1. Bot Account Information ───────────────────────────────────────
        st.subheader("🤖 Tài khoản Bot Gmail")
        bot_email = sheet_storage_service.get_bot_account_email()

        if bot_email:
            st.caption("Google Service Account thực thi các thao tác đọc & ghi:")
            st.code(bot_email, language="")
        else:
            st.warning(
                "⚠️ Không tìm thấy email của bot trong `storage/bot-account.txt`."
            )

        # ── 2. Permission Notice & Step-by-step Guide ────────────────────────
        st.subheader("🔑 Hướng dẫn cấp quyền Editor")
        st.info(
            "⚠️ **Bắt buộc:** Bạn cần chia sẻ Google Sheet cho tài khoản Bot "
            "với quyền **Editor (Người chỉnh sửa)** để hệ thống đọc dữ liệu "
            "và ghi trạng thái.\n\n"
            "**Các bước thực hiện:**\n"
            "1. Mở file Google Sheet cần đồng bộ trên trình duyệt.\n"
            "2. Nhấn nút **Chia sẻ (Share)** ở góc trên bên phải.\n"
            "3. Dán email Bot ở trên vào ô nhập người nhận.\n"
            "4. Chọn vai trò: **Người chỉnh sửa (Editor)**.\n"
            "5. Bỏ tích 'Thông báo cho mọi người' nếu muốn, "
            "rồi nhấn **Chia sẻ (Share)**."
        )

        # ── 3. Data Format & Sync Rules ──────────────────────────────────────
        st.subheader("📑 Quy chuẩn dữ liệu & Chức năng")
        st.markdown(
            "- **Cột bắt buộc:** `email` hoặc `phone`, `status`, `hubspot_id`.\n"
            "- **Chuẩn hóa số điện thoại Việt Nam:**\n"
            "    - Tự động kiểm tra tính hợp lệ của số di động VN "
            "(các đầu số 03x, 05x, 07x, 08x, 09x).\n"
            "    - Tự động chuẩn hóa về định dạng quốc tế `+84xxxxxxxxx` "
            "trước khi tạo hoặc cập nhật Contact lên HubSpot CRM.\n"
            "    - Nếu số điện thoại không hợp lệ, dòng sẽ được đánh dấu `ERROR` "
            "kèm thông báo lỗi cụ thể.\n"
            "- **Chế độ đồng bộ:**\n"
            "    - **▶ Bắt đầu đồng bộ (NEW):** Chỉ lọc và đồng bộ các dòng "
            "có trạng thái `NEW`.\n"
            "    - **🔁 Thử lại dòng lỗi (ERROR):** Chỉ quét và thực thi lại "
            "các dòng có trạng thái `ERROR`.\n"
            "    - Sau khi đồng bộ thành công, bot sẽ tự cập nhật cột `status` "
            "thành `SUCCESS` hoặc `UPDATED`, đồng thời ghi `hubspot_id`.\n"
            "- **⏪ Khôi phục (Restore):**\n"
            "    - Xóa các user/contact vừa được thêm mới trên HubSpot "
            "trong lần chạy gần nhất.\n"
            "    - Hoàn toàn **không chỉnh sửa hay thay đổi** "
            "dữ liệu trên Google Sheet.\n"
            "- **Cơ chế nhận diện Contact:**\n"
            "    - Tra cứu theo **Email** trước.\n"
            "    - Nếu không có Email, hệ thống dùng **Số điện thoại** "
            "để tìm kiếm.\n"
            "- **🔗 Mở Sheet:** Nhấn để truy cập trực tiếp Google Sheet "
            "trong tab mới."
        )


def _render_contacts_tab() -> None:
    """Render the HubSpot CRM Contacts directory view."""
    col_hs_dynamic, col_hs_static = st.columns([65, 35], gap="large")

    with col_hs_dynamic:
        st.subheader("🔍 Tra cứu Danh sách Contact HubSpot")
        st.caption("Truy vấn trực tiếp danh bạ CRM thông qua HubSpot Contacts API v3.")

        with st.form("hubspot_query_form"):
            col_q1, col_q2 = st.columns(2)
            limit_val = col_q1.number_input(
                "Số lượng liên hệ mỗi trang (Limit):",
                min_value=1,
                max_value=100,
                value=10,
                step=5,
                help="HubSpot API cho phép tối đa 100 contact trên một lần gọi.",
            )
            after_val = col_q2.text_input(
                "Mã con trỏ trang kế tiếp (After cursor):",
                value=st.session_state.get("hubspot_cursor", ""),
                placeholder="Để trống nếu muốn lấy từ đầu...",
                help="Dán mã cursor từ lần trước để chuyển sang trang sau.",
            )
            btn_fetch_contacts = st.form_submit_button(
                "📥 Lấy danh sách Contact", type="primary"
            )

        if btn_fetch_contacts:
            with st.spinner("Đang tải dữ liệu từ HubSpot CRM..."):
                try:
                    contacts_list, next_token = hubspot_api.get_formatted_contacts(
                        limit=int(limit_val),
                        after=after_val.strip() or None,
                    )
                    st.session_state["hubspot_cursor"] = next_token or ""
                    st.session_state["loaded_contacts"] = contacts_list
                    st.session_state["loaded_next_cursor"] = next_token or ""
                except Exception as exc:  # noqa: BLE001
                    st.error(f"❌ Không thể lấy dữ liệu từ HubSpot: {exc}")

        # Display results if available in session state
        if "loaded_contacts" in st.session_state:
            contacts_list = st.session_state["loaded_contacts"]
            next_token = st.session_state.get("loaded_next_cursor", "")

            if not contacts_list:
                st.info("ℹ️ Không tìm thấy liên hệ nào trên HubSpot CRM.")
            else:
                st.success(f"✅ Đã tải thành công **{len(contacts_list)}** liên hệ.")

                display_df_data = [
                    {
                        "ID": c["id"],
                        "Họ và Tên": c["name"],
                        "Email": c["email"],
                        "Số điện thoại": c["phone"],
                    }
                    for c in contacts_list
                ]
                st.dataframe(
                    display_df_data,
                    use_container_width=True,
                    column_config={
                        "ID": st.column_config.TextColumn("ID HubSpot"),
                        "Họ và Tên": st.column_config.TextColumn(
                            "Họ và Tên (Firstname + Lastname)"
                        ),
                        "Email": st.column_config.TextColumn("Email"),
                        "Số điện thoại": st.column_config.TextColumn("Số điện thoại"),
                    },
                )

                if next_token:
                    st.info(f"📌 **Cursor trang kế tiếp (`after`):** `{next_token}`")
                    st.caption(
                        "💡 Bạn có thể bấm nút 'Lấy danh sách Contact' lần nữa "
                        "để xem tiếp trang sau (con trỏ đã được tự động điền)."
                    )
                else:
                    st.info("🏁 Đã tới trang cuối cùng! Không còn contact nào nữa.")

    with col_hs_static:
        st.subheader("📖 Hướng dẫn sử dụng")
        st.markdown(
            "- **Mục đích:**\n"
            "    - Xem trực tiếp các contact hiện có trên HubSpot CRM mà không "
            "cần đăng nhập vào giao diện HubSpot web.\n"
            "    - Kiểm tra xem liên hệ vừa đồng bộ từ Google Sheet đã lên "
            "HubSpot hay chưa.\n\n"
            "- **Ý nghĩa tham số:**\n"
            "    - **Limit (Giới hạn):** Số lượng bản ghi trả về cho mỗi lần "
            "yêu cầu (Từ 1 đến 100 bản ghi).\n"
            "    - **After (Con trỏ Cursor):** HubSpot CRM v3 sử dụng cơ chế "
            "phân trang dựa trên con trỏ (Cursor-based pagination). "
            "Để xem trang tiếp theo, hệ thống cung cấp một mã token `after`. "
            "Chỉ cần giữ nguyên hoặc dán token này vào ô tìm kiếm.\n\n"
            "- **Cấu trúc trường hiển thị:**\n"
            "    - `ID`: Mã định danh nội bộ duy nhất của Contact trên HubSpot.\n"
            "    - `Họ và Tên`: Kết hợp giữa `firstname` và `lastname`.\n"
            "    - `Email`: Địa chỉ email của liên hệ.\n"
            "    - `Số điện thoại`: Số di động đã được chuẩn hóa `+84`.\n\n"
            "- **Lưu ý:**\n"
            "    - Để quay về trang đầu tiên, chỉ cần xóa trắng ô "
            "**After cursor** và bấm nút tìm kiếm."
        )


with tab_sync:
    _render_sync_tab()

with tab_contacts:
    _render_contacts_tab()
