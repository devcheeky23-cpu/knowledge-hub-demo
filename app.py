import streamlit as st

st.set_page_config(
    page_title="Project Knowledge Hub",
    page_icon="📚",
    layout="wide",
)

# ---------------------------------------------------------------------------
# Mock data
# ---------------------------------------------------------------------------

MOCK_DOCUMENTS = [
    {"name": "product-requirements.md", "size": "18 KB", "chunks": 12},
    {"name": "api-spec.md", "size": "34 KB", "chunks": 27},
    {"name": "erd-description.md", "size": "9 KB", "chunks": 6},
    {"name": "system-architecture.md", "size": "22 KB", "chunks": 15},
]

MOCK_QA = {
    "order api": {
        "mode": "found",
        "answer": "The Order API exposes a `POST /api/orders` endpoint. It accepts a JSON body with `customer_id`, `items` (array of `{product_id, quantity}`), and `shipping_address`. On success it returns `201 Created` with the new order object including `order_id`, `status: \"pending\"`, and `estimated_delivery`.",
        "citations": [
            {"file": "api-spec.md", "section": "Order Endpoints", "preview": "POST /api/orders\nBody: { customer_id, items: [{product_id, quantity}], shipping_address }\nResponse 201: { order_id, status, estimated_delivery }"},
        ],
    },
    "payment": {
        "mode": "conflict",
        "answer": "Two documents describe the payment timeout differently.",
        "sides": [
            {
                "claim": "Payment requests time out after **30 seconds**. If no response is received the order is set to `payment_failed`.",
                "citation": {"file": "api-spec.md", "section": "Payment Endpoints"},
            },
            {
                "claim": "Payment gateway calls have a **60-second** timeout with one automatic retry before the order is marked as failed.",
                "citation": {"file": "system-architecture.md", "section": "Payment Processing"},
            },
        ],
    },
    "gdpr": {
        "mode": "abstain",
    },
}

def classify_query(text: str) -> str:
    t = text.lower()
    if any(k in t for k in ["order", "api", "endpoint", "field", "request", "response"]):
        return "order api"
    if any(k in t for k in ["payment", "timeout", "gateway"]):
        return "payment"
    return "gdpr"


# ---------------------------------------------------------------------------
# Session state
# ---------------------------------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []
if "documents" not in st.session_state:
    st.session_state.documents = MOCK_DOCUMENTS.copy()
if "page" not in st.session_state:
    st.session_state.page = "Chat"


# ---------------------------------------------------------------------------
# Sidebar
# ---------------------------------------------------------------------------

with st.sidebar:
    st.title("📚 Knowledge Hub")
    st.session_state.page = st.radio("", ["Chat", "Documents"], label_visibility="collapsed")
    st.divider()
    st.caption(f"**{len(st.session_state.documents)}** documents indexed")
    total_chunks = sum(d["chunks"] for d in st.session_state.documents)
    st.caption(f"**{total_chunks}** chunks in vector store")


# ---------------------------------------------------------------------------
# Documents page
# ---------------------------------------------------------------------------

if st.session_state.page == "Documents":
    st.header("Documents")

    uploaded = st.file_uploader(
        "Upload a document (Markdown, TXT, PDF)",
        type=["md", "txt", "pdf"],
        label_visibility="collapsed",
    )
    if uploaded:
        existing = [d["name"] for d in st.session_state.documents]
        if uploaded.name not in existing:
            st.session_state.documents.append({
                "name": uploaded.name,
                "size": f"{len(uploaded.getvalue()) // 1024 or 1} KB",
                "chunks": max(1, len(uploaded.getvalue()) // 800),
            })
            st.success(f"✓ **{uploaded.name}** ingested successfully")
        else:
            st.info(f"**{uploaded.name}** is already in the index")

    st.divider()

    if not st.session_state.documents:
        st.info("No documents indexed yet. Upload a file above.")
    else:
        for doc in list(st.session_state.documents):
            col1, col2, col3, col4 = st.columns([4, 1, 1, 1])
            col1.markdown(f"📄 **{doc['name']}**")
            col2.caption(doc["size"])
            col3.caption(f"{doc['chunks']} chunks")
            if col4.button("Delete", key=f"del_{doc['name']}"):
                st.session_state.documents = [
                    d for d in st.session_state.documents if d["name"] != doc["name"]
                ]
                st.rerun()


# ---------------------------------------------------------------------------
# Chat page
# ---------------------------------------------------------------------------

else:
    st.header("Ask anything about your project")

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg.get("citations"):
                for c in msg["citations"]:
                    with st.expander(f"📎 {c['file']} › {c['section']}"):
                        st.code(c["preview"], language="")
            if msg.get("sides"):
                for i, side in enumerate(msg["sides"], 1):
                    with st.expander(f"Source {i}: {side['citation']['file']} › {side['citation']['section']}"):
                        st.markdown(side["claim"])

    if prompt := st.chat_input("Ask a question about your project…"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.chat_message("user"):
            st.markdown(prompt)

        key = classify_query(prompt)
        result = MOCK_QA[key]

        with st.chat_message("assistant"):
            if result["mode"] == "found":
                st.markdown(result["answer"])
                for c in result["citations"]:
                    with st.expander(f"📎 {c['file']} › {c['section']}"):
                        st.code(c["preview"], language="")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": result["answer"],
                    "citations": result["citations"],
                })

            elif result["mode"] == "abstain":
                msg = "⚠️ ไม่พบข้อมูลเรื่องนี้ในเอกสารที่ upload ไว้ กรุณาตรวจสอบว่าเอกสารที่เกี่ยวข้องได้ถูก upload แล้ว"
                st.markdown(msg)
                st.session_state.messages.append({"role": "assistant", "content": msg})

            elif result["mode"] == "conflict":
                st.warning("⚡ พบข้อมูลขัดแย้งกันในเอกสาร — แสดงทั้งสองแหล่ง")
                for i, side in enumerate(result["sides"], 1):
                    with st.expander(f"Source {i}: {side['citation']['file']} › {side['citation']['section']}"):
                        st.markdown(side["claim"])
                st.caption("กรุณาตรวจสอบและอัปเดตเอกสารให้ตรงกัน")
                st.session_state.messages.append({
                    "role": "assistant",
                    "content": "⚡ พบข้อมูลขัดแย้งกันในเอกสาร",
                    "sides": result["sides"],
                })

    if not st.session_state.messages:
        st.divider()
        st.markdown("**ลองถามเช่น:**")
        col1, col2, col3 = st.columns(3)
        col1.info("Order API รับ field อะไรบ้าง?")
        col2.warning("payment timeout คือกี่วินาที?")
        col3.error("ระบบรองรับ GDPR มั้ย?")
