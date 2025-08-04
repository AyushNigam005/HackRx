import streamlit as st
import requests
import os
import json
import time

# ---------- 🎯 Page Config ----------
st.set_page_config(page_title="Insurance Q&A - HackRx", page_icon="📄")

# ---------- 🎯 Header ----------
st.title("🛡️ Insurance Policy Q&A Assistant")
st.markdown("**Ask questions about your uploaded policy PDFs. Get clause-based answers — fast.**")
st.markdown("---")

# ---------- 📄 Upload Section ----------
st.subheader("📤 Upload Policy PDF")
pdf_file = st.file_uploader("Choose a PDF file", type=["pdf"])

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
            try:
                # Save uploaded file to local
                save_path = os.path.join(".", pdf_file.name)
                with open(save_path, "wb") as f:
                    f.write(pdf_file.getbuffer())

                # Prepare questions JSON
                questions = [q.strip() for q in questions_input.strip().split("\n") if q.strip()]
                questions_json = json.dumps(questions)

                # Prepare files and data
                with open(save_path, "rb") as pdf_bytes:
                    files = {
                        "pdf": (pdf_file.name, pdf_bytes, "application/pdf")
                    }
                    data = {
                        "questions": questions_json
                    }

                    # ✅ Backend URL
                    # ✅ Backend URL
                    backend_url = "https://ayush018-hackrx-fastapi.hf.space/run"


                    # 🔄 Optional: Ping retry loop
                    for _ in range(10):
                        try:
                            ping = requests.get("https://ayush018-hackrx-fastapi.hf.space/")
                            if ping.status_code == 200:
                                break
                        except:
                            pass
                        time.sleep(1)

                    # 🔗 POST request to backend
                    res = requests.post(backend_url, files=files, data=data)

                # ✅ Display results
                if res.status_code == 200:
                    json_data = res.json()
                    results = json_data.get("full_answers", [])
                    st.success("✅ Answers retrieved!")

                    for item in results:
                        st.markdown("### 📄 " + item.get("document", "Document"))
                        st.markdown(f"**❓ Question:** {item.get('question', '')}")

                        answer = item.get("answer", {})
                        if isinstance(answer, dict):
                            if answer.get("decision", "").startswith("❌"):
                                st.error(f"🟥 {answer.get('justification', 'No explanation.')}")
                            else:
                                st.success(f"✅ Decision: {answer.get('decision')}")
                                st.markdown(f"💰 **Amount**: {answer.get('amount')}")
                                st.markdown(f"📌 **Justification**: {answer.get('justification')}")
                        else:
                            st.warning(f"⚠️ Unexpected format:\n{answer}")
                        st.markdown("---")
                else:
                    st.error(f"❌ Backend error: {res.status_code}")
                    try:
                        st.json(res.json())
                    except:
                        st.write(res.text)

            except Exception as e:
                st.error(f"❌ Failed to contact backend: `{e}`")
