import streamlit as st
import random
import pandas as pd
import datetime
import re
from audio_recorder_streamlit import audio_recorder
from src.rag_pipeline import AgriRAG


# ==============================================================================
# PAGE CONFIG
# ==============================================================================

st.set_page_config(
    page_title="AgriChain - Mandi Portal",
    layout="wide"
)


# ==============================================================================
# 🎨 COLOR CUSTOMIZATION CENTER
# ==============================================================================

custom_css = """
<style>

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');


/* ============================================================
   GLOBAL
   ============================================================ */

html, body, [class*="css"], .stMarkdown,
p, div, span, label,
h1, h2, h3, h4, h5, h6 {

    font-family: 'Inter', sans-serif !important;

    color: #19324D !important;
}


/* ============================================================
   MAIN PAGE
   ============================================================ */

.stApp {

    background-color: #F8FAFC !important;
}


/* ============================================================
   LEFT SIDEBAR
   ============================================================ */

[data-testid="stSidebar"] {

    background-color: #F4F7F5 !important;

    border-right: 1px solid #D9E2E7 !important;
}


/* ============================================================
   SIDEBAR NORMAL OPTIONS
   ============================================================ */

.stRadio label {

    background-color: #FFFFFF !important;

    border: 1px solid #D9E2E7 !important;

    padding: 14px 20px !important;

    border-radius: 8px !important;

    cursor: pointer;

    width: 100%;
}


/* ============================================================
   SIDEBAR SELECTED OPTION
   ============================================================ */

.stRadio label:has(input:checked) {

    background-color: #EAF6F1 !important;

    border: 1px solid #72B89B !important;
}


/* ============================================================
   TOP NAVIGATION TABS
   ============================================================ */

.stTabs [data-baseweb="tab"] {

    background-color: #FFFFFF !important;

    border: 1px solid #D9E2E7 !important;

    border-radius: 8px !important;
}


.stTabs [aria-selected="true"] {

    background-color: #EAF6F1 !important;

    border: 1px solid #B7DCCE !important;

    border-bottom: 3px solid #2D8B6E !important;
}


/* ============================================================
   FARMER BOOKING FORM
   ============================================================ */

[data-testid="column"]:nth-of-type(1)
[data-testid="stVerticalBlockBorderWrapper"] {

    background-color: #FFFFFF !important;

    border: 1px solid #CFE2DE !important;

    border-radius: 16px !important;
}


/* ============================================================
   🟦 LIVE QUEUE CARD
   ============================================================ */

.st-key-live_queue_card {

    background-color: #F1F7FD !important;

    border: 1px solid #BFD7EC !important;

    border-radius: 16px !important;

    padding: 4px !important;
}


.st-key-live_queue_card h3 {

    color: #234F70 !important;

    font-size: 20px !important;
}


.st-key-live_queue_card p,
.st-key-live_queue_card label {

    color: #29465E !important;

    font-size: 14px !important;
}


/* ============================================================
   🟦 LIVE QUEUE NUMBER
   ============================================================ */

.queue-number-box {

    background-color: #E8F2FF !important;

    border: 1px solid #B8D4F0 !important;

    border-radius: 10px;

    padding: 14px;

    text-align: center;

    margin-top: 10px;

    margin-bottom: 12px;
}


.queue-number {

    color: #1F3B5C !important;

    font-size: 42px !important;

    font-weight: 700;

    line-height: 1;
}


/* ============================================================
   🟦 LIVE QUEUE METRIC TEXT SIZE
   ============================================================ */

.st-key-live_queue_card [data-testid="stMetricValue"] {

    font-size: 26px !important;

    line-height: 1.1 !important;

    font-weight: 700 !important;
}


.st-key-live_queue_card [data-testid="stMetricLabel"] {

    font-size: 13px !important;

    line-height: 1.3 !important;
}


.st-key-live_queue_card [data-testid="stMetricDelta"] {

    font-size: 11px !important;
}


/* ============================================================
   🟦 LIVE QUEUE TABLE TEXT
   ============================================================ */

.st-key-live_queue_card [data-testid="stDataFrame"] {

    font-size: 13px !important;
}


/* ============================================================
   🟨 SMS LOG CARD
   ============================================================ */

.st-key-sms_log_card {

    background-color: #FFF9E8 !important;

    border: 1px solid #E8D79A !important;

    border-radius: 16px !important;

    padding: 4px !important;

    margin-top: 12px !important;
}


.st-key-sms_log_card h3 {

    color: #5A4A22 !important;
}


.st-key-sms_log_card p,
.st-key-sms_log_card label {

    color: #5A4A22 !important;
}


/* ============================================================
   🟨 SMS TABLE AREA
   ============================================================ */

.st-key-sms_log_card [data-testid="stDataFrame"] {

    border-radius: 10px !important;
}


/* ============================================================
   🟩 SYSTEM INFORMATION CARD
   ============================================================ */

.st-key-system_information_card {

    background-color: #F8FAFC !important;

    border: 1px solid #D9E2E7 !important;

    border-radius: 16px !important;

    padding: 8px !important;

    margin-top: 12px !important;
}


.st-key-system_information_card h3 {

    color: #193A59 !important;

    font-size: 20px !important;
}


.st-key-system_information_card p {

    color: #64748B !important;

    font-size: 13px !important;
}


/* ============================================================
   SYSTEM INFORMATION METRICS
   ============================================================ */

.st-key-system_information_card [data-testid="stMetric"] {

    background-color: #FFFFFF !important;

    border: 1px solid #D9E2E7 !important;

    border-radius: 12px !important;

    padding: 12px !important;

    min-height: 105px !important;
}


.st-key-system_information_card [data-testid="stMetricValue"] {

    font-size: 25px !important;

    line-height: 1.1 !important;

    font-weight: 700 !important;
}


.st-key-system_information_card [data-testid="stMetricLabel"] {

    font-size: 12px !important;

    line-height: 1.3 !important;
}


/* ============================================================
   CENTER STAFF PORTAL BOXES
   ============================================================ */

[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(1) {

    background-color: #F4F0FF !important;

    border-color: #E6DDF8 !important;
}


[data-testid="stVerticalBlockBorderWrapper"]:nth-of-type(2) {

    background-color: #F0FDF4 !important;

    border-color: #D1FAE5 !important;
}


/* ============================================================
   GOVERNMENT ADMIN PORTAL BOXES
   ============================================================ */

div.element-container:nth-of-type(1)
[data-testid="stVerticalBlockBorderWrapper"] {

    background-color: #F0F9FF !important;

    border-color: #E0F2FE !important;
}


div.element-container:nth-of-type(2)
[data-testid="stVerticalBlockBorderWrapper"] {

    background-color: #FFF7ED !important;

    border-color: #FFEDD5 !important;
}


div.element-container:nth-of-type(3)
[data-testid="stVerticalBlockBorderWrapper"] {

    background-color: #F8FAFC !important;

    border-color: #E2E8F0 !important;
}


div.element-container:nth-of-type(4)
[data-testid="stVerticalBlockBorderWrapper"] {

    background-color: #FDF2F8 !important;

    border-color: #FCE7F3 !important;
}


div.element-container:nth-of-type(5)
[data-testid="stVerticalBlockBorderWrapper"] {

    background-color: #FFFBF3 !important;

    border-color: #EBDDBE !important;
}


/* ============================================================
   🌿 LIGHT GREEN BUTTONS
   ============================================================ */

[data-testid="stFormSubmitButton"] > button,
.stButton > button {

    background-color: #DCEFE7 !important;

    color: #1F4D3D !important;

    border: 1px solid #A8D3C2 !important;

    border-radius: 8px !important;

    font-weight: 600 !important;

    padding: 0.55rem 1.1rem !important;

    transition: all 0.2s ease !important;
}


[data-testid="stFormSubmitButton"] > button:hover,
.stButton > button:hover {

    background-color: #CFE7DD !important;

    color: #173D31 !important;

    border: 1px solid #8FC6B0 !important;
}


/* ============================================================
   INPUT BOXES
   ============================================================ */

.stTextInput input,
.stNumberInput input,
.stDateInput input {

    background-color: #F8FAFC !important;

    border: 1px solid #CBD8E3 !important;

    border-radius: 8px !important;

    color: #19324D !important;
}


.stTextInput input:focus,
.stNumberInput input:focus,
.stDateInput input:focus {

    border-color: #72B89B !important;

    box-shadow: 0 0 0 1px #72B89B !important;
}


/* ============================================================
   SELECT BOX
   ============================================================ */

.stSelectbox div[data-baseweb="select"] > div {

    background-color: #F1F4F8 !important;

    border-color: #CBD8E3 !important;

    border-radius: 8px !important;
}


/* ============================================================
   STATUS COLORS
   ============================================================ */

.status-success {

    color: #195C50 !important;

    background-color: #EAF6F1 !important;
}


.status-processing {

    color: #A87924 !important;

    background-color: #F8EED8 !important;
}


.status-rejected {

    color: #E05252 !important;

    background-color: #FCE8E8 !important;
}


.status-waiting {

    color: #3C6FAD !important;

    background-color: #E5EFFB !important;
}


/* ============================================================
   METRIC CARDS
   ============================================================ */

[data-testid="stMetric"] {

    background-color: #FFFFFF !important;

    border: 1px solid #D9E2E7 !important;

    border-radius: 12px !important;

    padding: 12px !important;
}


/* ============================================================
   ALERT BOXES
   ============================================================ */

[data-testid="stAlert"] {

    border-radius: 10px !important;
}


/* ============================================================
   DIVIDERS
   ============================================================ */

hr {

    border-color: #D9E2E7 !important;
}

</style>
"""

st.markdown(custom_css, unsafe_allow_html=True)


# ==============================================================================
# RAG
# ==============================================================================

@st.cache_resource
def load_rag():
    return AgriRAG()


rag = load_rag()


# ==============================================================================
# MSP RATES
# ==============================================================================

MSP_RATES = {

    "Paddy (Common)": 2300.0,

    "Paddy (Grade-A)": 2320.0,

    "Wheat": 2275.0

}


# ==============================================================================
# HELPER FUNCTIONS
# ==============================================================================

def sanitize_mobile(raw_number: str) -> str:

    cleaned = re.sub(
        r"\D",
        "",
        str(raw_number or "")
    )

    if len(cleaned) == 12 and cleaned.startswith("91"):

        cleaned = cleaned[2:]

    elif len(cleaned) == 11 and cleaned.startswith("0"):

        cleaned = cleaned[1:]

    return cleaned


def dispatch_simulated_sms(
    to_mobile: str,
    message_text: str
):

    ts = datetime.datetime.now().strftime("%I:%M %p")

    clean_phone = sanitize_mobile(to_mobile)

    log_entry = {

        "timestamp": ts,

        "to": clean_phone,

        "message": message_text

    }

    st.session_state.sms_gateway_log.insert(
        0,
        log_entry
    )

    st.toast(
        f"SMS delivered to +91 {clean_phone}"
    )


def color_status(val):

    if val in ["Completed", "Sent to Bank"]:

        return (
            "color: #195C50; "
            "font-weight: 600; "
            "background-color: #EAF6F1; "
            "border-radius: 4px; "
            "padding: 2px 6px;"
        )

    elif val == "Processing":

        return (
            "color: #A87924; "
            "font-weight: 600; "
            "background-color: #F8EED8; "
            "border-radius: 4px; "
            "padding: 2px 6px;"
        )

    elif val == "Rejected":

        return (
            "color: #E05252; "
            "font-weight: 600; "
            "background-color: #FCE8E8; "
            "border-radius: 4px; "
            "padding: 2px 6px;"
        )

    elif val in [
        "Waiting",
        "Pending Validation",
        "Delayed / Congested"
    ]:

        return (
            "color: #3C6FAD; "
            "font-weight: 600; "
            "background-color: #E5EFFB; "
            "border-radius: 4px; "
            "padding: 2px 6px;"
        )

    return ""


def apply_styler_map(
    styler_obj,
    func,
    subset=None
):

    if hasattr(styler_obj, "map"):

        return styler_obj.map(
            func,
            subset=subset
        )

    return styler_obj.applymap(
        func,
        subset=subset
    )


# ==============================================================================
# INITIALIZE SESSION STATE
# ==============================================================================

if "mandi_centers" not in st.session_state:

    st.session_state.mandi_centers = [

        "Mandi Yard - Hub 1",

        "FCI Procurement Center - North",

        "Cooperative Society Mandi"

    ]


if "center_bottlenecks" not in st.session_state:

    st.session_state.center_bottlenecks = {

        center: "Normal Operations"

        for center in st.session_state.mandi_centers

    }


if "queue_data" not in st.session_state:

    today_str = datetime.date.today().strftime(
        "%Y-%m-%d"
    )

    est_bank_date = (
        datetime.date.today()
        + datetime.timedelta(days=2)
    ).strftime("%Y-%m-%d")

    st.session_state.queue_data = [

        {

            "token": "13",

            "farmer": "Sriram",

            "mobile": "9876543210",

            "aadhaar": "[Aadhaar Redacted]",

            "crop": "Paddy (Common)",

            "mandi": "FCI Procurement Center - North",

            "quintals": 1.0,

            "rate": 2300.0,

            "amount": 2300.0,

            "quality": "Grade A",

            "est_payment_date": est_bank_date,

            "date": today_str,

            "slot": "11:00 AM - 01:00 PM",

            "status": "Waiting",

            "payment_status": "Pending Validation"

        }

    ]


if "staff_accounts" not in st.session_state:

    st.session_state.staff_accounts = [

        {

            "username": "staff_ramesh",

            "center": "Mandi Yard - Hub 1"

        },

        {

            "username": "staff_suresh",

            "center": "FCI Procurement Center - North"

        }

    ]


if "sms_gateway_log" not in st.session_state:

    st.session_state.sms_gateway_log = [

        {

            "timestamp": "10:15 AM",

            "to": "9876543210",

            "message":
                "Token #13 registered for FCI Procurement Center."

        }

    ]


# ==============================================================================
# SIDEBAR
# ==============================================================================

st.sidebar.markdown(
    "<h2 style='color: #176B52;'>🌱 AgriProcureHub</h2>",
    unsafe_allow_html=True
)

st.sidebar.caption(
    "Smarter Farming • Better Tomorrow"
)

st.sidebar.write("---")

st.sidebar.write(
    "**Select User Role:**"
)

role = st.sidebar.radio(
    "User Role",
    [
        "🌱Farmer Portal",
        "🏢Center Staff Portal",
        "🏛️Government Admin Portal"
    ],
    label_visibility="collapsed"
)


# ==============================================================================
# 1. FARMER PORTAL
# ==============================================

if role == "🌱Farmer Portal":

    st.markdown(
        "<h1 style='color: #172B40;'>🌾AI Agri-Advisor & Token Queue</h1>",
        unsafe_allow_html=True
    )


    tab1, tab2, tab3 = st.tabs(

        [

            "Token Queue System",

            "Track Payment & Status",

            "🤖AI Agri-Advisor"

        ]

    )


    # ============================================================
    # TOKEN QUEUE SYSTEM
    # ============================================================

    with tab1:

        col_form, col_queue = st.columns(

            [1.2, 1],

            gap="large"

        )


        # ========================================================
        # BOOKING FORM
        # ========================================================

        with col_form:

            with st.container(border=True):

                st.markdown(

                    "<h3 style='color: #173A4D;'> Book Mandi Entry Pass</h3>",

                    unsafe_allow_html=True

                )

                st.write(
                    "Register your crop delivery and receive a digital token."
                )

                selected_mandi = st.selectbox(
                    "Select Mandi Center / मंडी केंद्र चुनें / మండీ కేంద్రం ఎంచుకోండి",
                    st.session_state.mandi_centers,
                    key="unified_mandi"
                )

                current_status = (
                    st.session_state.center_bottlenecks.get(
                        selected_mandi,
                        "Normal Operations"
                    )
                )

                if current_status != "Normal Operations":

                    st.warning(

                        f"⚠️ **Center Advisory ({selected_mandi})**: "
                        f"{current_status}. "
                        f"Expect adjusted queue movement."

                    )


                with st.form(
                    "token_form",
                    border=False
                ):

                    farmer_name = st.text_input(
                        "Farmer Name / किसान का नाम / రైతు పేరు"
                    )

                    farmer_phone = st.text_input(

                        "Mobile Number / मोबाइल नंबर / మొబైల్ నంబర్",

                        value="8143719699"

                    )

                    aadhaar = st.text_input(

                        "Aadhaar Number / आधार (अंतिम 4 अंक) / ఆధార్",

                        max_chars=12

                    )

                    crop_type = st.selectbox(

                        "Crop Type / फसल का प्रकार / పంట రకం",

                        list(MSP_RATES.keys())

                    )

                    quantity = st.number_input(

                        "Estimated Quantity (in Quintals) / मात्रा / పరిమాణం",

                        min_value=0.5,

                        value=1.0,

                        step=0.5

                    )

                    booking_date = st.date_input(

                        "Booking Date / बुकिंग की तारीख / బుకింగ్ తేదీ",

                        min_value=datetime.date.today(),

                        value=datetime.date.today()

                    )

                    time_slot = st.selectbox(

                        "Preferred Time Slot / पसंदीदा समय स्लॉट / ఇష్టమైన స్లాట్",

                        [

                            "09:00 AM - 11:00 AM",

                            "11:00 AM - 01:00 PM",

                            "02:00 PM - 04:00 PM",

                            "04:00 PM - 06:00 PM"

                        ]

                    )

                    submitted = st.form_submit_button(

                        "🎟️ Generate Digital Token →"

                    )


                    if submitted:

                        clean_phone = sanitize_mobile(
                            farmer_phone
                        )


                        if (

                            not farmer_name.strip()

                            or len(aadhaar.strip()) != 12

                            or not aadhaar.isdigit()

                            or len(clean_phone) != 10

                        ):

                            st.warning(
                                "Please fill all details correctly."
                            )

                        else:

                            new_token_num = str(
                                random.randint(14, 99)
                            )


                            selected_date_str = (
                                booking_date.strftime("%Y-%m-%d")
                            )


                            expected_amount = (
                                float(quantity)
                                * MSP_RATES.get(
                                    crop_type,
                                    2275.0
                                )
                            )


                            st.session_state.queue_data.append(

                                {

                                    "token": new_token_num,

                                    "farmer": farmer_name,

                                    "mobile": clean_phone,

                                    "aadhaar": aadhaar,

                                    "crop": crop_type,

                                    "mandi": selected_mandi,

                                    "quintals": quantity,

                                    "rate":
                                        MSP_RATES.get(
                                            crop_type,
                                            2275.0
                                        ),

                                    "amount":
                                        expected_amount,

                                    "quality": "Pending",

                                    "est_payment_date":
                                        "To be determined",

                                    "date":
                                        selected_date_str,

                                    "slot": time_slot,

                                    "status": "Waiting",

                                    "payment_status":
                                        "Pending Validation"

                                }

                            )


                            sms_msg = (

                                f"Token #{new_token_num} confirmed "
                                f"for {selected_mandi}. "
                                f"Note: Center status is "
                                f"[{st.session_state.center_bottlenecks.get(selected_mandi, 'Normal')}]."

                            )


                            dispatch_simulated_sms(

                                clean_phone,

                                sms_msg

                            )


                            st.success(

                                f"📱SMS delivered to +91 "
                                f"{clean_phone}: "
                                f"Token #{new_token_num} issued."

                            )


                            st.rerun()


        # ========================================================
        # RIGHT SIDE
        # ========================================================

        with col_queue:

            # ====================================================
            # 🟦 LIVE QUEUE
            # ====================================================

            with st.container(
                border=True,
                key="live_queue_card"
            ):

                st.markdown(

                    "<h3 style='color: #234F70;'>📡 Live Queue Status</h3>",

                    unsafe_allow_html=True

                )

                st.write(
                    "Current activity at the procurement network."
                )

                active_queue = [

                    q

                    for q in st.session_state.queue_data

                    if q["status"]

                    in [

                        "Waiting",

                        "Processing"

                    ]

                ]

                queue_count = len(active_queue)


                # --------------------------------------------------------------
                # QUEUE METRICS (Dynamic Calculation Logic)
                # --------------------------------------------------------------

                queue_metric_col1, queue_metric_col2 = st.columns(2)

                with queue_metric_col1:

                    st.metric(
                        "👨‍🌾 Farmers Ahead / Active",
                        queue_count
                    )

                with queue_metric_col2:

                    calculated_wait = max(5, int(queue_count * 2.4))

                    st.metric(
                        "⏱️ Estimated Average Wait",
                        f"{calculated_wait} mins"
                    )


                if active_queue:

                    df_queue = pd.DataFrame(
                        active_queue
                    )

                    queue_columns = [

                        "token",

                        "farmer",

                        "crop",

                        "mandi",

                        "status"

                    ]


                    styler_q = (

                        df_queue[

                            queue_columns

                        ].style

                    )


                    styled_queue = apply_styler_map(

                        styler_q,

                        color_status,

                        subset=["status"]

                    )


                    st.dataframe(

                        styled_queue,

                        use_container_width=True,

                        hide_index=True

                    )

                else:

                    st.info(
                        "No active tokens in queue."
                    )


            # ====================================================
            # 🟨 SMS LOG
            # ====================================================

            with st.container(
                border=True,
                key="sms_log_card"
            ):

                st.markdown(

                    "<h3 style='color: #5A4A22;'>✉️ Outgoing SMS Gateway Log</h3>",

                    unsafe_allow_html=True

                )

                st.write(
                    "Latest simulated farmer notifications."
                )


                if st.session_state.sms_gateway_log:

                    df_sms = pd.DataFrame(

                        st.session_state.sms_gateway_log

                    )


                    st.dataframe(

                        df_sms,

                        use_container_width=True,

                        hide_index=True

                    )

                else:

                    st.info(
                        "No SMS dispatched yet."
                    )


            # ====================================================
            # 🟩 SYSTEM INFORMATION
            # ====================================================

            with st.container(
                border=True,
                key="system_information_card"
            ):

                st.markdown(

                    "<h3 style='color: #193A59;'>📊 System Information</h3>",

                    unsafe_allow_html=True

                )

                st.write(
                    "Network-wide procurement snapshot."
                )

                system_col1, system_col2, system_col3 = st.columns(3)

                with system_col1:

                    st.metric(
                        "👨‍🌾 Total Farmers",
                        "1,248"
                    )

                with system_col2:

                    st.metric(
                        "🏛️ Total Mandis",
                        "3"
                    )

                with system_col3:

                    st.metric(
                        "◷ Avg. Processing",
                        "2.4 mins"
                    )


    # ============================================================
    # TRACK PAYMENT
    # ============================================================

    with tab2:

        with st.container(border=True):

            st.subheader(
                "Track Your Procurement & Payment Status"
            )

            search_token = st.text_input(

                "Enter Token Number (e.g., 13)"

            )


            if st.button(
                "Check Status"
            ):

                found = next(

                    (

                        item

                        for item in st.session_state.queue_data

                        if item["token"] == search_token

                    ),

                    None

                )


                if found:

                    st.success(

                        f"Record for **{found['farmer']}** "
                        f"(Token #{found['token']})"

                    )

                    center_issue = (

                        st.session_state.center_bottlenecks.get(

                            found["mandi"],

                            "Normal Operations"

                        )

                    )


                    if center_issue != "Normal Operations":

                        st.warning(
                            f"⚠️ Center Advisory ({found['mandi']}): {center_issue}. Expect adjusted queue movement."
                        )

                    c1, c2, c3, c4 = st.columns(4)

                    c1.metric(
                        "Weighment Status",
                        found["status"]
                    )

                    c2.metric(
                        "Quality Level",
                        found.get("quality", "N/A")
                    )

                    c3.metric(
                        "Final Amount",
                        f"₹{found['amount']:,.2f}"
                    )

                    c4.metric(

                        "Bank Credit Date",

                        found.get(
                            "est_payment_date",
                            "Pending"
                        )

                    )


                    if found["payment_status"] == "Sent to Bank":

                        st.info(

                            f"Crop procured. File sent to bank. "
                            f"Expected credit: "
                            f"**{found['est_payment_date']}**."

                        )

                        st.progress(85)


                    elif found["status"] == "Rejected":

                        st.error(

                            "Crop rejected at weighing bridge. "
                            "Procurement cancelled."

                        )

                        st.progress(100)


                    else:

                        st.warning(

                            "Awaiting final weighment "
                            "and quality inspection."

                        )

                        st.progress(33)


                else:

                    st.error(

                        "Token not found. "
                        "Please check your token number."

                    )


    # ============================================================
    # AI AGRI ADVISOR
    # ============================================================

    with tab3:

        with st.container(border=True):

            st.subheader(
                "Multilingual AI Agri-Advisor"
            )

            ai_tab1, ai_tab2 = st.tabs(

                [

                    "Voice Input",

                    "Text Input"

                ]

            )


            # ====================================================
            # VOICE
            # ====================================================

            with ai_tab1:

                spoken_lang = st.selectbox(

                    "Select Spoken Language",

                    [

                        "Telugu (తెలుగు)",

                        "Hindi (हिंदी)",

                        "English"

                    ],

                    key="voice_lang"

                )

                lang_code = (

                    "te"

                    if "Telugu" in spoken_lang

                    else (

                        "hi"

                        if "Hindi" in spoken_lang

                        else "en"

                    )

                )

                st.write(
                    "Click to record your question:"
                )

                audio_bytes = audio_recorder(

                    text="Click to record voice",

                    recording_color="#E05252",

                    neutral_color="#258667",

                    icon_size="2x",

                    key="voice_widget"

                )

                voice_query = ""


                if audio_bytes:

                    if len(audio_bytes) < 1000:

                        st.warning(

                            "Recorded audio is too short. "
                            "Please speak clearly."

                        )

                    else:

                        st.audio(
                            audio_bytes,
                            format="audio/wav"
                        )

                        with st.spinner(

                            "Translating and processing speech..."

                        ):

                            temp_audio_path = "temp_audio.wav"

                            with open(
                                temp_audio_path,
                                "wb"
                            ) as f:

                                f.write(audio_bytes)

                            try:

                                with open(
                                    temp_audio_path,
                                    "rb"
                                ) as audio_file:

                                    transcript = (

                                        rag.client.audio.transcriptions.create(

                                            model="whisper-large-v3",

                                            file=audio_file,

                                            language=lang_code,

                                            response_format="verbose_json",

                                            prompt=(
                                                "మండి, ధాన్యం, MSP, FCI, "
                                                "రైతు, గోధుమలు, కనీస మద్దతు ధర, ఎంత"
                                            )

                                        )

                                    )

                                    raw_text = (

                                        transcript.text

                                        if hasattr(
                                            transcript,
                                            "text"
                                        )

                                        else transcript["text"]

                                    )

                                    voice_query = (
                                        raw_text.replace("మరికి", "వరికి")
                                                .replace("మండి కేవేందే", "మండి వద్ద")
                                                .strip()
                                    )

                            except Exception as e:

                                st.error(

                                    f"Speech transcription error: {e}"

                                )


                if voice_query:

                    st.success(f"Recognized Speech: {voice_query}")
                    st.write("---")

                    with st.container(border=True):
                        st.markdown("🧑‍🌾 **User Question:**")
                        st.write(voice_query)

                    with st.spinner(

                        "Analyzing government agricultural guidelines..."

                    ):

                        answer, citations = (
                            rag.answer_question(
                                voice_query
                            )
                        )

                    with st.container(border=True):
                        st.markdown("🤖 **Official Guidelines & Response:**")
                        st.write(answer)


            # ====================================================
            # TEXT
            # ====================================================

            with ai_tab2:

                text_lang = st.selectbox(

                    "Select Input Language",

                    [

                        "Telugu (తెలుగు)",

                        "Hindi (हिंदी)",

                        "English"

                    ],

                    key="text_lang"

                )

                text_query = st.text_input(

                    "Type your question here...",

                    key="text_box"

                )


                if text_query:

                    st.write("---")

                    with st.container(border=True):
                        st.markdown("🧑‍🌾 **User Question:**")
                        st.write(text_query)

                    with st.spinner(
                        "Analyzing guidelines..."
                    ):

                        answer, citations = (
                            rag.answer_question(
                                text_query
                            )
                        )

                    with st.container(border=True):
                        st.markdown("🤖 **Official Guidelines & Response:**")
                        st.write(answer)


# ==============================================================================
# 2. CENTER STAFF PORTAL
# ==============================================================================

elif role == "🏢Center Staff Portal":

    st.markdown(

        "<h1 style='color: #172B40;'>Center Staff: Weighing Bridge & Inspection</h1>",

        unsafe_allow_html=True

    )

    with st.container(border=True):

        st.markdown(

            "<h3 style='color: #173A4D;'>Assigned Center Operations</h3>",

            unsafe_allow_html=True

        )

        current_staff_center = st.selectbox(

            "Select Your Assigned Center:",

            st.session_state.mandi_centers

        )

        st.write("---")

        st.markdown(
            "#### 🚨 Report Center Operational Bottleneck / Issue"
        )

        current_issue = (
            st.session_state.center_bottlenecks.get(
                current_staff_center,
                "Normal Operations"
            )
        )

        issue_options = [

            "Normal Operations",

            "Transport Delay (Trucks pending arrival)",

            "Storage Congestion (>90% full, slow clearance)",

            "Weighing Scale Malfunctioning / Maintenance",

            "Weather Alert (Rain Risk / Cover Required)"

        ]

        selected_issue = st.selectbox(

            "Select Current Center Status",

            issue_options,

            index=(

                issue_options.index(current_issue)

                if current_issue in issue_options

                else 0

            )

        )

        if st.button(
            "Broadcast Bottleneck Alert to Farmers & Admin"
        ):

            st.session_state.center_bottlenecks[
                current_staff_center
            ] = selected_issue

            center_farmers = [

                q

                for q in st.session_state.queue_data

                if current_staff_center in q["mandi"]

                and q["status"] == "Waiting"

            ]

            for farmer in center_farmers:

                dispatch_simulated_sms(

                    farmer["mobile"],

                    f"URGENT Notice for {current_staff_center}: "
                    f"Status updated to [{selected_issue}]. "
                    f"Please check slot timings."

                )

            st.success(

                f"Successfully broadcasted alert "
                f"[{selected_issue}] for "
                f"{current_staff_center} to all waiting farmers!"

            )

            st.rerun()

        st.write("---")

        active_items = [

            q

            for q in st.session_state.queue_data

            if current_staff_center in q["mandi"]

            and q["status"]

            in [

                "Waiting",

                "Processing",

                "Completed"

            ]

        ]

        if active_items:

            token_options = {

                f"Token #{item['token']} - "
                f"{item['farmer']} "
                f"[Status: {item['status']}]":

                item

                for item in active_items

            }

            selected_label = st.selectbox(

                "Select Farmer at Weighing Bridge:",

                list(token_options.keys())

            )

            selected_item = token_options[
                selected_label
            ]

            st.write("---")

            col_status, col_details = st.columns(

                [1, 1.2],

                gap="large"

            )

            with col_status:

                st.write(
                    "**Update Inspection Status:**"
                )

                current_status_idx = (

                    [

                        "Processing",

                        "Completed",

                        "Rejected"

                    ].index(

                        selected_item["status"]

                    )

                    if selected_item["status"]

                    in [

                        "Processing",

                        "Completed",

                        "Rejected"

                    ]

                    else 0

                )

                status_choice = st.radio(

                    "Status",

                    [

                        "Processing",

                        "Completed",

                        "Rejected"

                    ],

                    index=current_status_idx

                )

            with col_details:

                with st.form(
                    "inspection_form",
                    border=False
                ):

                    st.write(
                        "**Procurement Details (Bank Submission):**"
                    )

                    q_options = [

                        "Fair Average Quality (FAQ)",

                        "Grade A",

                        "Grade B",

                        "Rejected (High Moisture)"

                    ]

                    q_idx = (

                        q_options.index(

                            selected_item.get(

                                "quality",

                                "Fair Average Quality (FAQ)"

                            )

                        )

                        if selected_item.get("quality")
                        in q_options

                        else 0

                    )

                    quality_level = st.selectbox(

                        "Quality Level",

                        q_options,

                        index=q_idx

                    )

                    rate_val = st.number_input(

                        "Per Quintal Amount (₹)",

                        value=float(

                            selected_item.get(

                                "rate",

                                MSP_RATES.get(

                                    selected_item["crop"],

                                    2300.0

                                )

                            )

                        )

                    )

                    actual_q = st.number_input(

                        "Actual Weighed Quantity (Quintals)",

                        value=float(
                            selected_item["quintals"]
                        )

                    )

                    total_amount = (
                        rate_val * actual_q
                    )

                    st.write(

                        f"**Calculated Total Amount:** "
                        f"₹{total_amount:,.2f}"

                    )

                    default_est = (

                        datetime.date.today()
                        + datetime.timedelta(days=2)

                    )

                    est_date = st.date_input(

                        "Estimated Payment Date",

                        value=default_est

                    )

                    submit_inspection = (

                        st.form_submit_button(

                            "Submit Inspection & Send to Bank"

                        )

                    )

            if submit_inspection:

                prev_status = selected_item["status"]

                selected_item["status"] = (
                    status_choice
                )

                selected_item["quality"] = (
                    quality_level
                )

                selected_item["rate"] = (
                    rate_val
                )

                selected_item["quintals"] = (
                    actual_q
                )

                selected_item["amount"] = (
                    total_amount
                )

                target_mobile = selected_item.get(

                    "mobile",

                    "8143719699"

                )

                if status_choice == "Completed":

                    selected_item[
                        "est_payment_date"
                    ] = est_date.strftime(
                        "%Y-%m-%d"
                    )

                    selected_item[
                        "payment_status"
                    ] = "Sent to Bank"

                    st.success(

                        f"Token #{selected_item['token']} "
                        f"finalized! Sent to banking portal."

                    )

                    msg = (

                        f"Token #{selected_item['token']} completed. "
                        f"Final Amount: ₹{total_amount:,.2f}. "
                        f"Transfer expected by "
                        f"{selected_item['est_payment_date']}."

                    )

                    dispatch_simulated_sms(

                        target_mobile,

                        msg

                    )

                elif status_choice == "Processing":

                    selected_item[
                        "payment_status"
                    ] = "Pending Validation"

                    if prev_status != "Processing":

                        msg = (

                            f"Token #{selected_item['token']} "
                            f"is now being processed at "
                            f"the weighment bridge."

                        )

                        dispatch_simulated_sms(

                            target_mobile,

                            msg

                        )

                else:

                    selected_item[
                        "payment_status"
                    ] = "Cancelled"

                    selected_item[
                        "est_payment_date"
                    ] = "N/A"

                    if prev_status != "Rejected":

                        msg = (

                            f"Token #{selected_item['token']} "
                            f"rejected due to quality standards."

                        )

                        dispatch_simulated_sms(

                            target_mobile,

                            msg

                        )

                st.rerun()

        else:

            st.info(

                f"No active tokens for "
                f"{current_staff_center}."

            )

    with st.container(border=True):

        st.markdown(

            "<h3 style='color: #193A59;'>Active Register View</h3>",

            unsafe_allow_html=True

        )

        if st.session_state.queue_data:

            df_staff_view = pd.DataFrame(

                st.session_state.queue_data

            )

            cols_staff = [

                "token",

                "farmer",

                "crop",

                "quintals",

                "amount",

                "status",

                "payment_status"

            ]

            styler_staff = (
                df_staff_view[cols_staff].style
            )

            styled_staff = apply_styler_map(

                styler_staff,

                color_status,

                subset=[

                    "status",

                    "payment_status"

                ]

            )

            st.dataframe(

                styled_staff,

                use_container_width=True,

                hide_index=True

            )


# ==============================================================================
# 3. GOVERNMENT ADMIN PORTAL
# ==============================================================================

elif role == "🏛️Government Admin Portal":

    st.markdown(

        "<h1 style='color: #172B40;'>Government Admin Oversight</h1>",

        unsafe_allow_html=True

    )

    admin_tab1, admin_tab2, admin_tab3, admin_tab4 = st.tabs(

        [

            "Manage Centers",

            "Staff",

            "Reports & Ledger",

            "SMS Logs"

        ]

    )


    # ==========================================================================
    # MANAGE CENTERS
    # ==========================================================================

    with admin_tab1:

        with st.container(border=True):

            st.markdown(

                "<h3 style='color: #173A4D;'>Add Procurement Center & Monitor Bottlenecks</h3>",

                unsafe_allow_html=True

            )

            st.write(
                "**Live Center Operational Status:**"
            )

            for c, status in (
                st.session_state.center_bottlenecks.items()
            ):

                if status == "Normal Operations":

                    st.success(
                        f"📍 **{c}**: {status}"
                    )

                else:

                    st.error(
                        f"🚨 **{c}**: {status}"
                    )

            st.write("---")

            with st.form(
                "add_center",
                border=False
            ):

                new_center = st.text_input(
                    "Center Name"
                )

                if st.form_submit_button(
                    "Add Center"
                ) and new_center:

                    if new_center not in st.session_state.mandi_centers:

                        st.session_state.mandi_centers.append(
                            new_center
                        )

                        st.session_state.center_bottlenecks[
                            new_center
                        ] = "Normal Operations"

                        st.success(
                            "Added successfully."
                        )

                        st.rerun()

                    else:

                        st.warning(
                            "Center name is empty "
                            "or already exists."
                        )

            st.write("---")

            st.markdown(
                "<h3>Active Centers</h3>",
                unsafe_allow_html=True
            )

            for idx, center in enumerate(

                st.session_state.mandi_centers,

                1

            ):

                st.write(
                    f"**{idx}.** {center}"
                )


    # ==========================================================================
    # STAFF
    # ==========================================================================

    with admin_tab2:

        with st.container(border=True):

            st.markdown(

                "<h3 style='color: #173A4D;'>Assign Staff</h3>",

                unsafe_allow_html=True

            )

            with st.form(
                "staff_form",
                border=False
            ):

                new_staff_name = st.text_input(
                    "Staff Name"
                )

                assigned_center = st.selectbox(

                    "Assign to Center",

                    st.session_state.mandi_centers

                )

                if st.form_submit_button(
                    "Create Account"
                ) and new_staff_name:

                    st.session_state.staff_accounts.append(

                        {

                            "username": new_staff_name,

                            "center": assigned_center

                        }

                    )

                    st.success(
                        "Staff assigned!"
                    )

                    st.rerun()

            st.write("---")

            st.markdown(
                "<h3>Staff List</h3>",
                unsafe_allow_html=True
            )

            if st.session_state.staff_accounts:

                st.dataframe(

                    pd.DataFrame(
                        st.session_state.staff_accounts
                    ),

                    use_container_width=True,

                    hide_index=True

                )


    # ==========================================================================
    # REPORTS & LEDGER
    # ==========================================================================

    with admin_tab3:

        with st.container(border=True):

            st.markdown(

                "<h3 style='color: #193A4C;'>System Monitoring</h3>",

                unsafe_allow_html=True

            )

            total_bookings = len(
                st.session_state.queue_data
            )

            completed_count = len(

                [

                    q

                    for q in st.session_state.queue_data

                    if q["status"] == "Completed"

                ]

            )

            total_liability = sum(

                q.get("amount", 0)

                for q in st.session_state.queue_data

                if q["status"] == "Completed"

            )

            c1, c2, c3 = st.columns(3)

            c1.metric(
                "Total Bookings",
                total_bookings
            )

            c2.metric(
                "Procurements Completed",
                completed_count
            )

            c3.metric(
                "Sent to Bank (₹)",
                f"₹{total_liability:,.2f}"
            )

        with st.container(border=True):

            st.markdown(

                "<h3 style='color: #193A59;'>Master Ledger</h3>",

                unsafe_allow_html=True

            )

            if st.session_state.queue_data:

                df_all = pd.DataFrame(

                    st.session_state.queue_data

                )

                cols_admin = [

                    "token",

                    "mandi",

                    "crop",

                    "amount",

                    "status",

                    "payment_status"

                ]

                styler_admin = (
                    df_all[cols_admin].style
                )

                styled_all = apply_styler_map(

                    styler_admin,

                    color_status,

                    subset=[

                        "status",

                        "payment_status"

                    ]

                )

                st.dataframe(

                    styled_all,

                    use_container_width=True,

                    hide_index=True

                )


    # ==========================================================================
    # SMS LOGS
    # ==========================================================================

    with admin_tab4:

        with st.container(border=True):

            st.markdown(

                "<h3 style='color: #243D55;'>Outgoing SMS Gateway Log</h3>",

                unsafe_allow_html=True

            )

            if st.session_state.sms_gateway_log:

                st.dataframe(

                    pd.DataFrame(
                        st.session_state.sms_gateway_log
                    ),

                    use_container_width=True,

                    hide_index=True

                )

                if st.button(
                    "Clear Logs"
                ):

                    st.session_state.sms_gateway_log = []

                    st.rerun()

            else:

                st.info(
                    "No logs available."
                )