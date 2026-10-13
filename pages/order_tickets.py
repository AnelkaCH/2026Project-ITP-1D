import streamlit as st
from datetime import date, datetime
from services.json_service import load_ticket_types, load_accounts, save_accounts

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

    t1col1, t1col2 = st.columns([2, 3])

    with t1col1:
        st.write("### Adult Tickets")
        st.write(f"Price: ${current_ticket['adult_price']} each")
    
    with t1col2:
        st.session_state.adults = st.number_input("Number of adults", min_value=0, max_value=10, step=1)

    st.divider()

    t2col1, t2col2 = st.columns([2, 3])

    with t2col1:
        st.write("### Child Tickets")
        st.write(f"Price: ${current_ticket['child_price']} each")

    with t2col2:
        st.session_state.children = st.number_input("Number of children", min_value=0, max_value=10, step=1)

    st.divider()

    total_adult_price = st.session_state.adults * current_ticket["adult_price"]
    total_child_price = st.session_state.children * current_ticket["child_price"]

    total_price = total_adult_price + total_child_price
    st.subheader(f"Order Summary: ${total_price:.2f}")

    t3col1, t3col2, t3col3 = st.columns([2, 2, 13])
    with t3col1:
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
                        "adults": st.session_state.adults,
                        "children": st.session_state.children,
                        "total_price": total_price
                    })

                    break

            # Save updated accounts
            save_accounts(users)

            st.success("Order submitted successfully!")

            st.session_state.adults = 0
            st.session_state.children = 0
            st.session_state.current_page = "home"
            st.rerun()

    with t3col2:
        if st.button("Cancel Order"):
            st.session_state.adults = 0
            st.session_state.children = 0
            st.session_state.current_page = "home"
            st.rerun()