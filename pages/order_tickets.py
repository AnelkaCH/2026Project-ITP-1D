import streamlit as st
from datetime import date, datetime
from services.json_service import load_ticket_types, load_accounts, save_accounts

def increase_adult():
    st.session_state.quantity_adult += 1

def decrease_adult():
    if st.session_state.quantity_adult > 0:
        st.session_state.quantity_adult -= 1

def increase_child():
    st.session_state.quantity_child += 1

def decrease_child():
    if st.session_state.quantity_child > 0:
        st.session_state.quantity_child -= 1

def show_order_tickets():
    #Initialize variables
    ticket_types = load_ticket_types()
    current_ticket = None

    for ticket in ticket_types:
        if ticket["id"] == st.session_state.current_ticket_order:
            current_ticket = ticket
            break

    st.title("Order Tickets. Currently ordering:", current_ticket["name"])
    st.write(current_ticket["description"])

    st.write("When do you plan to visit the park? Please select a date below.")
    selected_date = st.date_input(
        "Select a date",
        value=date.today()
    )

    col1, col2, col3, col4 = st.columns([2, 1, 1, 1])

    with col1:
        st.write("### Adult Tickets")
        st.write(f"Price: ${current_ticket['adult_price']} each")
    
    with col2:
        st.button("-", key="minus", on_click=decrease_adult)

    with col3:
        st.write(f"### {st.session_state.quantity_adult}")

    with col4:
        st.button("+", key="plus", on_click=increase_adult)

    st.divider()

    col5, col6, col7, col8 = st.columns([2, 1, 1, 1])

    with col5:
        st.write("### Child Tickets")
        st.write(f"Price: ${current_ticket['child_price']} each")

    with col6:
        st.button("-", key="minus_child", on_click=decrease_child)

    with col7:
        st.write(f"### {st.session_state.quantity_child}")

    with col8:
        st.button("+", key="plus_child", on_click=increase_child)

    st.divider()

    total_adult_price = st.session_state.quantity_adult * current_ticket["adult_price"]
    total_child_price = st.session_state.quantity_child * current_ticket["child_price"]

    total_price = total_adult_price + total_child_price
    st.subheader(f"Order Summary: ${total_price:.2f}")

    col9, col10, col11 = st.columns([2, 2, 13])
    with col9:
        if st.button("Continue Purchase"):
            #Store current time
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            # Load existing accounts
            users = load_accounts()

            # Find the current user
            for user in users:
                if user["email"] == st.session_state.current_account:

                    # Add the ticket order
                    user["tickets"].append({
                        "type": current_ticket["name"],
                        "date_of_visit": str(selected_date),
                        "time_of_order": current_time,
                        "adults": st.session_state.quantity_adult,
                        "children": st.session_state.quantity_child,
                        "total_price": total_price
                    })

                    break

            # Save updated accounts
            save_accounts(users)

            st.success("Order submitted successfully!")

            st.session_state.quantity_adult = 0
            st.session_state.quantity_child = 0
            st.session_state.current_page = "home"
            st.rerun()

    with col10:
        if st.button("Cancel Order"):
            st.session_state.quantity_adult = 0
            st.session_state.quantity_child = 0
            st.session_state.current_page = "home"
            st.rerun()