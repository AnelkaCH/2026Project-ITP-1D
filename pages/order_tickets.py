import streamlit as st
from datetime import date, datetime
from services.json_service import load_ticket_types, load_accounts, save_accounts
from services.voucher_service import apply_voucher, calculate_discount, check_voucher, format_discount

def clear_order_state():
    # Clear voucher related session state
    for key in ("applied_voucher", "applied_voucher_code", "applied_voucher_ticket"):
        st.session_state.pop(key, None)


def get_current_ticket():
    for ticket in load_ticket_types():
        if ticket["id"] == st.session_state.get("current_ticket_order"):
            return ticket
    return None


def show_order_tickets():
    current_ticket = get_current_ticket()

    if current_ticket is None:
        st.error("Ticket type not found.")
        st.stop()

    email = st.session_state.current_account

    # Drop a voucher that was applied to a different ticket type
    if st.session_state.get("applied_voucher_ticket") != current_ticket["id"]:
        clear_order_state()

    st.title(f"Order Tickets. Currently ordering: {current_ticket['name']}")
    st.write(current_ticket["description"])

    st.write("When do you plan to visit the park? Please select a date below.")

    selected_date = st.date_input(
        "Select a date",
        value=date.today(),
        min_value=date.today()
    )

    # Adult tickets
    t1col1, t1col2 = st.columns([2, 3])
    with t1col1:
        st.write("### Adult Tickets")
        st.write(f"Price: ${current_ticket['adult_price']} each")
    with t1col2:
        adults = st.number_input("Number of adults", min_value=0, max_value=10, step=1)

    st.divider()

    # Child tickets
    t2col1, t2col2 = st.columns([2, 3])
    with t2col1:
        st.write("### Child Tickets")
        st.write(f"Price: ${current_ticket['child_price']} each")
    with t2col2:
        children = st.number_input("Number of children", min_value=0, max_value=10, step=1)

    st.divider()

    subtotal = (
        adults * current_ticket["adult_price"]
        + children * current_ticket["child_price"]
    )

    # Voucher section
    voucher_col, applied_voucher_col = st.columns([1, 2])

    with voucher_col:
        with st.form("voucher_form"):
            voucher_input = st.text_input(
                "Voucher code",
                key=f"voucher_code_{current_ticket['id']}"
            )
            confirm_voucher = st.form_submit_button(
                "Confirm Voucher",
                disabled=st.session_state.get("applied_voucher") is not None
            )

    if confirm_voucher:
        is_valid, found, voucher_mssg = apply_voucher(voucher_input, current_ticket, email, selected_date)

        if is_valid:
            st.session_state.applied_voucher = found
            st.session_state.applied_voucher_ticket = current_ticket["id"]
            st.rerun()
        else:
            st.error(voucher_mssg)

    applied = st.session_state.get("applied_voucher")

    if applied is not None:
        error = check_voucher(applied, current_ticket, email, selected_date)
        if error:
            clear_order_state()
            st.warning(f"Voucher removed: {error}")
            applied = None

    total_price = calculate_discount(applied, subtotal)

    with applied_voucher_col:
        if applied is not None:
            st.write("### Applied Voucher")
            st.write(applied["voucher_name"])
            st.write(f"Discount: {format_discount(applied)}")

            if st.button("Remove Voucher"):
                clear_order_state()
                st.rerun()
        else:
            st.write("### No voucher applied")

    st.subheader(f"Order Summary: ${total_price:.2f}")

    has_tickets = (adults + children) > 0
    if not has_tickets:
        st.info("Select at least one ticket to continue.")

    t4col1, t4col2, _ = st.columns([2, 2, 13])

    with t4col1:
        if st.button("Continue Purchase", disabled=not has_tickets):
            users = load_accounts()
            user = None
            for u in users:
                if u["email"] == email:
                    user = u
                    break

            if user is None:
                st.error("Account not found. Please log in again.")
                st.stop()

            voucher_id = str(applied["voucher_id"]) if applied else None

            user.setdefault("tickets", []).append({
                "type": current_ticket["name"],
                "date_of_visit": str(selected_date),
                "time_of_order": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "adults": adults,
                "children": children,
                "voucher_id": voucher_id,
                "total_price": total_price
            })

            if voucher_id is not None:
                used_vouchers = user.setdefault("used_voucher", [])
                if voucher_id not in used_vouchers:
                    used_vouchers.append(voucher_id)

            save_accounts(users)

            clear_order_state()
            st.switch_page(st.session_state.pages["home"])

    with t4col2:
        if st.button("Cancel Order"):
            clear_order_state()
            st.switch_page(st.session_state.pages["home"])