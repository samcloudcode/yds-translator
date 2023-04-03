import streamlit as st
import openai
import time
import pandas as pd
import pyperclip


def initiate_states():

    # Create default session states
    if 'messages' not in ss:
        ss['messages'] = []

    if 'state' not in ss:
        ss['state'] = "Intro"

    if 'model_reply' not in ss:
        ss['model_reply'] = ""

    if 'user_reply' not in ss:
        ss['user_reply'] = ""

    if 'current_topic' not in ss:
        ss['current_topic'] = {}

    if 'topics' not in ss:
        ss['topics'] = {}

    if 'counts' not in ss:
        ss['counts'] = 1

    if 'user_info' not in ss:
        ss['user_info'] = {}

    if 'load_questions' not in ss:
        ss['load_questions'] = False

    if 'text_to_translate' not in ss:
        ss['text_to_translate'] = ""

    df = pd.read_excel('presets.xlsx', engine='openpyxl', index_col=0)
    df.fillna('', inplace=True)
    if 'presets' not in ss:
        ss['presets'] = df

    if 'current_preset' not in ss:
        ss['current_preset'] = 'New...'


def translate():
    ss.model_reply = ""


def update_model_response():
    """Calls the OpenAI API and updates model_response_display"""
    openai.api_key = st.secrets['SECRET_KEY']

    qu_attempts = 1
    while qu_attempts <= 10:
        print(ss.messages)

        try:
            response = []
            for resp in openai.ChatCompletion.create(
                    model="gpt-4",
                    messages=ss.messages,
                    stream=True):
                if 'content' in resp['choices'][0]['delta']:
                    response.append(resp['choices'][0]['delta']['content'])
                    result = "".join(response).strip()
                    model_response_display.markdown(f'{result}')

            ss.model_reply = "".join(response).strip()
            qu_attempts = 11

        except:
            print(f"openai error, attempt {qu_attempts}")
            qu_attempts += 1
            time.sleep(2)

    st.experimental_rerun()


# Initiate states and variables
st.set_page_config(page_title="Translate | Yellow Door Studio", page_icon="yellow_door_favicon.png", layout="centered",
                   initial_sidebar_state="auto")

ss = st.session_state
initiate_states()

st.image('Yellow Door Studio.webp', width=250)
st.header('Brand Translator')
st.markdown('Select translation preset and enter text to be translated in the area below.')


options = ss.presets.index.tolist()
options.pop(0)

try:
    index = options.index(ss.current_preset)
except ValueError:
    index = 0

ss.current_preset = st.selectbox('Load preset:', options=options, index=index)


with st.expander('Translation prompt', expanded=False):
    st.markdown(ss.presets.loc[ss.current_preset, 'prompt'])

ss.text_to_translate = st.text_area("Enter text to translate:", value=ss.text_to_translate)

ss.messages = [
    {"role": "system", "content": ss.presets.loc[ss.current_preset, 'prompt']},
    {"role": "user", "content": ss.text_to_translate}
]

if ss.model_reply == "":
    model_response_display = st.empty()
    if ss.text_to_translate != "":
        update_model_response()
else:
    model_response_display = st.text_area('Translation:', value=ss.model_reply)


st.button('Translate', on_click=translate, type='primary')

if st.button('Clear'):
    ss.model_reply = ""
    ss.text_to_translate = ""
    st.experimental_rerun()

