
import streamlit as st

from rag_pipeline import build_rag_pipeline

from storage.chat_store import (
    initialize_database,
    create_conversation,
    get_all_conversations,
    get_messages,
    get_recent_messages,
    save_message,
    update_conversation_title,
    delete_conversation,
)


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Nexa AI | Document Assistant",
    page_icon="✨",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =====================================================
# CUSTOM CSS - CHATGPT INSPIRED DARK THEME
# =====================================================

st.markdown(
    """
    <style>

    /* -----------------------------------------------
       GLOBAL APPLICATION
    ----------------------------------------------- */

    .stApp {
        background-color: #212121;
        color: #ECECEC;
        font-family: Arial, sans-serif;
    }

    [data-testid="stAppViewContainer"] {
        background-color: #212121;
    }

    [data-testid="stMain"] {
        background-color: #212121;
    }

    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* -----------------------------------------------
       GLOBAL TEXT
    ----------------------------------------------- */

    h1, h2, h3, h4, h5, h6 {
        color: #FFFFFF !important;
    }

    p, li, label {
        color: #ECECEC;
    }

    [data-testid="stMarkdownContainer"] {
        color: #ECECEC;
    }

    [data-testid="stMarkdownContainer"] p,
    [data-testid="stMarkdownContainer"] li {
        color: #ECECEC !important;
        line-height: 1.7;
    }

    /* -----------------------------------------------
       SIDEBAR
    ----------------------------------------------- */

    section[data-testid="stSidebar"] {
        background-color: #171717;
        border-right: 1px solid #303030;
    }

    section[data-testid="stSidebar"] * {
        color: #ECECEC;
    }

    section[data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
        color: #ECECEC !important;
    }

    .sidebar-logo {
        color: #FFFFFF;
        font-size: 25px;
        font-weight: 800;
        margin-top: 10px;
        margin-bottom: 5px;
    }

    .sidebar-subtitle {
        color: #A0A0A0;
        font-size: 13px;
        margin-bottom: 25px;
    }

    .section-label {
        color: #A0A0A0;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        text-transform: uppercase;
        margin-top: 22px;
        margin-bottom: 12px;
    }

    /* -----------------------------------------------
       SIDEBAR BUTTONS
    ----------------------------------------------- */

    section[data-testid="stSidebar"] .stButton > button {
        background-color: #303030;
        color: #FFFFFF !important;
        border: 1px solid #454545;
        border-radius: 10px;
        font-weight: 600;
        padding: 10px;
        transition: all 0.2s ease;
    }

    section[data-testid="stSidebar"] .stButton > button:hover {
        background-color: #404040;
        border-color: #10A37F;
    }

    /* -----------------------------------------------
       MAIN HEADER
    ----------------------------------------------- */

    .main-title {
        font-size: 30px;
        font-weight: 700;
        color: #FFFFFF;
        letter-spacing: -0.7px;
        margin-bottom: 5px;
    }

    .main-subtitle {
        color: #A0A0A0;
        font-size: 14px;
        line-height: 1.6;
        margin-bottom: 25px;
    }

    /* -----------------------------------------------
       STATUS CARD
    ----------------------------------------------- */

    .status-card {
        background-color: #2A2A2A;
        border: 1px solid #3A3A3A;
        border-radius: 12px;
        padding: 15px 18px;
        margin-bottom: 20px;
    }

    .status-value {
        color: #10A37F;
        font-weight: 700;
        font-size: 14px;
    }

    .status-label {
        color: #B0B0B0;
        font-size: 13px;
    }

    /* -----------------------------------------------
       CHAT MESSAGES
    ----------------------------------------------- */

    [data-testid="stChatMessage"] {
        background-color: #2A2A2A;
        border: 1px solid #383838;
        border-radius: 14px;
        padding: 16px;
        margin-bottom: 14px;
    }

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] span {
        color: #ECECEC !important;
        font-size: 15px;
        line-height: 1.7;
    }

    [data-testid="stChatMessage"] code {
        color: #E5E7EB !important;
        background-color: #171717 !important;
    }

    [data-testid="stChatMessage"] pre {
        background-color: #171717 !important;
        border: 1px solid #404040;
        border-radius: 10px;
    }

    /* -----------------------------------------------
       CHAT INPUT
    ----------------------------------------------- */

    [data-testid="stChatInputContainer"] {
        background-color: #212121 !important;
        border-top: none !important;
        padding-top: 12px;
    }

    [data-testid="stChatInput"] {
        background-color: #303030 !important;
        border: 1px solid #505050 !important;
        border-radius: 24px !important;
    }

    [data-testid="stChatInput"]:focus-within {
        border-color: #10A37F !important;
        box-shadow: 0 0 0 1px #10A37F !important;
    }

    [data-testid="stChatInput"] textarea {
        background-color: transparent !important;
        color: #FFFFFF !important;
        -webkit-text-fill-color: #FFFFFF !important;
        font-size: 15px !important;
    }

    [data-testid="stChatInput"] textarea::placeholder {
        color: #A0A0A0 !important;
        -webkit-text-fill-color: #A0A0A0 !important;
    }

    [data-testid="stChatInput"] button {
        color: #FFFFFF !important;
    }

    /* -----------------------------------------------
       SELECT BOX
    ----------------------------------------------- */

    [data-testid="stSelectbox"] label {
        color: #ECECEC !important;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] {
        background-color: #303030;
        border-color: #454545;
        color: #FFFFFF;
    }

    [data-testid="stSelectbox"] div[data-baseweb="select"] * {
        color: #FFFFFF !important;
    }

    /* -----------------------------------------------
       EXPANDERS
    ----------------------------------------------- */

    [data-testid="stExpander"] {
        background-color: #2A2A2A;
        border: 1px solid #404040;
        border-radius: 10px;
    }

    [data-testid="stExpander"] summary {
        color: #ECECEC !important;
    }

    /* -----------------------------------------------
       GENERAL BUTTONS
    ----------------------------------------------- */

    .stButton > button {
        background-color: #303030;
        color: #FFFFFF !important;
        border: 1px solid #454545;
        border-radius: 10px;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #404040;
        border-color: #10A37F;
        color: #FFFFFF !important;
    }

    /* -----------------------------------------------
       DIVIDERS
    ----------------------------------------------- */

    hr {
        border-color: #383838;
    }

    /* -----------------------------------------------
       FOOTER
    ----------------------------------------------- */

    .footer {
        color: #888888;
        text-align: center;
        font-size: 12px;
        padding: 15px 0;
    }

    /* -----------------------------------------------
       STREAMLIT HEADER
    ----------------------------------------------- */

    header[data-testid="stHeader"] {
        background-color: transparent;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# DATABASE INITIALIZATION
# =====================================================

initialize_database()


# =====================================================
# LOAD RAG PIPELINE
# =====================================================

@st.cache_resource
def load_rag_pipeline():
    return build_rag_pipeline()


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    # Logo
    st.markdown(
        """
        <div class="sidebar-logo">✨ Nexa AI</div>
        <div class="sidebar-subtitle">
            Intelligent Document Assistant
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.divider()

    # Workspace
    st.markdown(
        '<div class="section-label">Workspace</div>',
        unsafe_allow_html=True,
    )

    if st.button(
        "＋  New Conversation",
        use_container_width=True,
        key="new_conversation_button",
    ):

        new_id = create_conversation()

        st.session_state.current_conversation_id = new_id

        # Keep the selectbox synchronized
        st.session_state.conversation_selector = new_id

        st.rerun()

    # Recent conversations
    st.markdown(
        '<div class="section-label">Recent Conversations</div>',
        unsafe_allow_html=True,
    )

    conversations = get_all_conversations()

    # Create a conversation if none exists
    if not conversations:

        new_id = create_conversation()
        conversations = get_all_conversations()

        st.session_state.current_conversation_id = new_id

    title_map = {
        c["conversation_id"]: c["title"]
        for c in conversations
    }

    chat_ids = list(title_map.keys())

    # Validate selected conversation
    if (
        "current_conversation_id" not in st.session_state
        or st.session_state.current_conversation_id not in chat_ids
    ):
        st.session_state.current_conversation_id = chat_ids[0]

    # Synchronize selectbox state
    if (
        "conversation_selector" not in st.session_state
        or st.session_state.conversation_selector not in chat_ids
    ):
        st.session_state.conversation_selector = (
            st.session_state.current_conversation_id
        )

    selected_chat = st.selectbox(
        "Select conversation",
        options=chat_ids,
        format_func=lambda x: "💬  " + title_map[x],
        label_visibility="collapsed",
        key="conversation_selector",
    )

    st.session_state.current_conversation_id = selected_chat

    st.divider()

    # Delete conversation
    if st.button(
        "🗑️  Delete Conversation",
        use_container_width=True,
        key="delete_conversation_button",
    ):

        delete_conversation(selected_chat)

        remaining = get_all_conversations()

        if remaining:

            next_id = remaining[0]["conversation_id"]

        else:

            next_id = create_conversation()

        st.session_state.current_conversation_id = next_id

        # Remove old selectbox state before rerun
        st.session_state.pop("conversation_selector", None)

        st.rerun()

    st.divider()

    # System information
    st.markdown(
        '<div class="section-label">System Information</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="status-card">

            <div class="status-label">
                VECTOR DATABASE
            </div>

            <div class="status-value">
                ● ChromaDB
            </div>

            <br>

            <div class="status-label">
                EMBEDDING MODEL
            </div>

            <div class="status-value">
                ● HuggingFace
            </div>

            <br>

            <div class="status-label">
                LLM PROVIDER
            </div>

            <div class="status-value">
                ● Groq API
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    st.caption("Nexa AI • RAG Assistant")


# =====================================================
# MAIN HEADER
# =====================================================

st.markdown(
    '<div class="main-title">Your Intelligent AI Assistant</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
    <div class="main-subtitle">
        Ask questions, explore your documents, and get intelligent
        answers powered by Retrieval-Augmented Generation.
    </div>
    """,
    unsafe_allow_html=True,
)

# System status
st.markdown(
    """
    <div class="status-card">
        <span class="status-value">● System Ready</span>
        &nbsp;&nbsp;
        <span class="status-label">
            Your document knowledge base is ready for queries.
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# CURRENT CONVERSATION
# =====================================================

conversation_id = st.session_state.current_conversation_id

messages = get_messages(conversation_id)


# =====================================================
# DISPLAY CHAT HISTORY
# =====================================================

if not messages:

    st.markdown(
        """
        <div style="
            text-align: center;
            padding: 55px 20px;
            background-color: #2A2A2A;
            border: 1px solid #383838;
            border-radius: 16px;
            margin: 25px 0;
        ">

            <div style="font-size: 45px;">✨</div>

            <h3 style="color: #FFFFFF;">
                Welcome to Nexa AI
            </h3>

            <p style="color: #A0A0A0;">
                Ask anything about your uploaded documents.
                Your AI assistant is ready to help.
            </p>

        </div>
        """,
        unsafe_allow_html=True,
    )

else:

    for message in messages:

        with st.chat_message(message["role"]):

            st.markdown(message["content"])


# =====================================================
# USER QUERY
# =====================================================

question = st.chat_input(
    "Ask anything about your documents..."
)


if question:

    # Get previous conversation history BEFORE saving
    # the current question.
    history = get_recent_messages(
        conversation_id,
        limit=8,
    )

    # Save user message
    save_message(
        conversation_id,
        "user",
        question,
    )

    # Generate title for the first user message
    if not messages:

        title = question[:40]

        update_conversation_title(
            conversation_id,
            title,
        )

    # Display user message
    with st.chat_message("user"):

        st.markdown(question)

    # Generate assistant response
    with st.chat_message("assistant"):

        with st.spinner(
            "Searching documents and generating your answer..."
        ):

            try:

                rag = load_rag_pipeline()

                answer, docs = rag(
                    question,
                    chat_history=history,
                )

                st.markdown(answer)

                # Save assistant response
                save_message(
                    conversation_id,
                    "assistant",
                    answer,
                )

                # Display source documents
                if docs:

                    with st.expander(
                        f"📚 View Sources ({len(docs)} documents)"
                    ):

                        for i, doc in enumerate(docs, start=1):

                            source = doc.metadata.get(
                                "source",
                                "Unknown",
                            )

                            page = doc.metadata.get(
                                "page",
                                "N/A",
                            )

                            st.markdown(
                                f"**Source {i}:** {source}"
                            )

                            st.caption(
                                f"Page: {page}"
                            )

                            st.write(doc.page_content)

                            st.divider()

            except Exception as e:

                st.error(
                    f"Something went wrong: {str(e)}"
                )

    st.rerun()


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.markdown(
    """
    <div class="footer">

        Powered by LangChain · ChromaDB · HuggingFace · Groq

        <br><br>

        Nexa AI © 2026

    </div>
    """,
    unsafe_allow_html=True,
)
