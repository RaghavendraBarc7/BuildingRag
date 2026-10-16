import streamlit as st

from HR_ASSISTANT.pipeline import ask, build_hr_assistant

SUGGESTED_QUESTIONS = [
    "How many paid leave days do I get?",
    "Can I work from home every day?",
    "What's the notice period during probation?",
    "How do I claim a reimbursement?",
]

AVATARS = {"user": ":material/person:", "assistant": ":material/support_agent:"}

st.set_page_config(page_title="HR Policy Assistant", page_icon=":material/menu_book:", layout="centered")

# Theme the browser's own text selection and cursor to match the accent in .streamlit/config.toml
st.html("""
<style>
  ::selection { background: rgb(47 107 87 / 0.18); }
  textarea, input { caret-color: #2F6B57; }
</style>
""")


@st.cache_resource(show_spinner="Loading the HR policy handbook…")
def get_agent():
    return build_hr_assistant()


def start_new_chat():
    st.session_state.messages = []


def ask_suggested_question():
    # A starter question was clicked: queue it as the next question, then clear the selection.
    st.session_state.pending_question = st.session_state.suggested_question
    st.session_state.suggested_question = None


if "messages" not in st.session_state:
    st.session_state.messages = []

header = st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center")
header.title("HR Policy Assistant", anchor=False)
st.caption("Ask me anything about the company HR policy. Every answer is looked up in the policy handbook.")

try:
    agent = get_agent()
except ValueError as error:  # check_api_keys() raises this when a key is missing from .env
    st.error(str(error), icon=":material/key_off:")
    st.stop()
except Exception as error:
    st.error("The assistant couldn't start. Check your internet connection and the API keys in .env, then reload the page.", icon=":material/error:")
    with st.expander("Error details"):
        st.exception(error)
    st.stop()

# Read the chat box first so we know whether a question is coming before drawing the welcome screen
typed_question = st.chat_input("Ask a question about HR policy")
question = typed_question or st.session_state.pop("pending_question", None)

for message in st.session_state.messages:
    with st.chat_message(message["role"], avatar=AVATARS[message["role"]]):
        st.markdown(message["content"])

if not st.session_state.messages and not question:
    st.markdown(
        "I can help with leave, working from home, probation, notice periods, "
        "reimbursements, the code of conduct, holidays and leaving the company."
    )
    st.pills("Try asking", SUGGESTED_QUESTIONS, key="suggested_question", on_change=ask_suggested_question)

if question:
    with st.chat_message("user", avatar=AVATARS["user"]):
        st.markdown(question)

    with st.chat_message("assistant", avatar=AVATARS["assistant"]):
        try:
            with st.spinner("Checking the HR policy…"):
                answer = ask(agent, question)
        except Exception as error:
            st.error("I couldn't get an answer just now. Check your internet connection and API keys, then ask again.", icon=":material/error:")
            with st.expander("Error details"):
                st.exception(error)
            st.stop()
        st.markdown(answer)

    st.session_state.messages.append({"role": "user", "content": question})
    st.session_state.messages.append({"role": "assistant", "content": answer})

# Filled in last so the button also appears right after the first answer
if st.session_state.messages:
    header.button("New chat", icon=":material/edit_square:", type="tertiary", on_click=start_new_chat)
