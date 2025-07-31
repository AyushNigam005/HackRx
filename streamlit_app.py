import streamlit as st
import requests
import os

# ---------- 🎯 Page Config ----------
st.set_page_config(page_title="Insurance Q&A - HackRx", page_icon="📄")

# ---------- 🎯 Header ----------
st.title("🛡️ Insurance Policy Q&A Assistant")
st.markdown("**Ask questions about your uploaded policy PDFs. Get clause-based answers — fast.**")
st.markdown("---")

# ---------- 📄 Upload Section ----------
st.subheader("📤 Upload Policy PDF")
pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

# Show uploaded file name
if pdf_file:
    st.success(f"✅ Uploaded: `{pdf_file.name}`")

# ---------- ❓ Questions Section ----------
st.subheader("❓ Enter Your Questions")
questions_input = st.text_area(
    "Write one question per line (e.g. Is maternity covered?)",
    placeholder="e.g.\nIs maternity covered?\nWhat is the waiting period?\nDoes it cover knee surgery?",
    height=150
)

# ---------- 🚀 Button ----------
if st.button("Get Answers 🚀"):
    if not pdf_file or not questions_input.strip():
        st.warning("⚠️ Please upload a PDF and enter at least one question.")
    else:
        with st.spinner("🧠 Thinking... Getting answers from the policy..."):
            # Save uploaded PDF
            save_path = os.path.join(".", pdf_file.name)
            with open(save_path, "wb") as f:
                f.write(pdf_file.getbuffer())

            # Prepare API payload
            questions = [q.strip() for q in questions_input.strip().split("\n") if q.strip()]
            payload = {
                "documents": [pdf_file.name],
                "questions": questions
            }

            try:
                res = requests.post("https://huggingface.co/spaces/Ayush018/hackrx-ayush-backend", json=payload)
                if res.status_code == 200:
                    results = res.json()["answers"]
                    st.success("✅ Answers retrieved!")

                    # ---------- 📋 Display Answers ----------
                    for item in results:
                        st.markdown("### 📄 " + item["document"])
                        st.markdown(f"**❓ Question:** {item['question']}")
                        if item['answer'].startswith("❌"):
                            st.error(f"🟥 {item['answer']}")
                        else:
                            st.info(f"🧠 {item['answer']}")
                        st.markdown("---")

                else:
                    st.error(f"❌ Backend error: {res.status_code}")
            except Exception as e:
                st.error(f"❌ Failed to contact FastAPI backend: `{e}`")


