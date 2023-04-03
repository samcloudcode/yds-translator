import streamlit as st
import pandas as pd


def initialise_states():

    df = pd.read_excel('presets.xlsx', engine='openpyxl', index_col=0)
    df.fillna('', inplace=True)
    ss['presets'] = df

    if 'current_preset' not in ss:
        ss['current_preset'] = 'New…'


def save_preset():
    new_values = {'from_language': from_language,
                  'to_language': to_language,
                  'context': context,
                  'expert_persona': expert_persona,
                  'tone': tone,
                  'brand_voice': brand_voice,
                  'audience': audience,
                  'style': style,
                  'audience_region': audience_region,
                  'translation_guide': translation_guide,
                  'prompt': prompt}

    ss.presets.loc[preset_name] = pd.Series(new_values)
    ss.presets.to_excel('presets.xlsx', engine='openpyxl')

    df = pd.read_excel('presets.xlsx', engine='openpyxl', index_col=0)
    ss['presets'] = df
    ss.current_preset = preset_name


def delete_preset(preset_name):
    ss.presets.drop(preset_name, inplace=True)
    ss.presets.to_excel('presets.xlsx', engine='openpyxl')

    df = pd.read_excel('presets.xlsx', engine='openpyxl', index_col=0)
    ss['presets'] = df


st.set_page_config(page_title="Presets | Yellow Door Studio", page_icon="yellow_door_favicon.png", layout="centered",
                   initial_sidebar_state="expanded")

st.image('Yellow Door Studio.webp', width=250)
st.header('Manage Presets')

ss = st.session_state
initialise_states()

options = ss.presets.index.tolist()
index = options.index(ss.current_preset)

ss.current_preset = st.selectbox('Select preset to edit or add new:', options=options, index=index)

with st.form("preset_form"):
    st.markdown('#### Preset settings')
    preset_name = st.text_input('Preset name:', ss.current_preset)
    from_language = st.text_input('Language to translate from:', placeholder='e.g. English', value=ss.presets.loc[ss.current_preset, 'from_language'])
    to_language = st.text_input('Language to translate to:', placeholder='e.g. Traditional Chinese', value=ss.presets.loc[ss.current_preset, 'to_language'])
    context = st.text_input('Context:', placeholder='e.g. The text is being translated for a company report', value=ss.presets.loc[ss.current_preset, 'context'])
    expert_persona = st.text_input('Persona of writer:', placeholder='e.g. expert presentation copywriter', value=ss.presets.loc[ss.current_preset, 'expert_persona'])
    tone = st.text_input('Tone:', placeholder='e.g. positive and friendly', value=ss.presets.loc[ss.current_preset, 'tone'])
    brand_voice = st.text_input('Brand voice:', placeholder='e.g. positive, friendly, inspiring and motivating', value=ss.presets.loc[ss.current_preset, 'brand_voice'])
    style = st.text_input('Style:', placeholder='e.g. Informal, chatty', value=ss.presets.loc[ss.current_preset, 'style'])
    audience = st.text_input('Audience:', placeholder='Company employees', value=ss.presets.loc[ss.current_preset, 'audience'])
    audience_region = st.text_input('Audience region:', placeholder='e.g. Hong Kong', value=ss.presets.loc[ss.current_preset, 'audience_region'])

    translation_guide = st.text_area('Translation guide:',
                                     placeholder='Enter any specific phrases or terms you want to '
                                     'use in this type of translation',
                                     value=ss.presets.loc[ss.current_preset, 'translation_guide'])

    prompt = f"""
    Act as a translator from {from_language} to {to_language}.

    When providing the translation, take on the persona of {expert_persona}.
    {context}. The writing style is {style}, targeted towards {audience} in {audience_region}.
    The tone should be {tone}, taking into consideration the brand voice: {brand_voice}.

    Adapt the sentence structure and order of text to read naturally in {to_language}. 

    ---

    Use the following translations for similar words or phrases:

    {translation_guide}

    ---

    When I provide you with {from_language} text, reply with the translation.
    """

    with st.expander('Translation prompt', expanded=False):
        st.markdown(prompt)

    col1, col2 = st.columns(2)

    with col1:
        if st.form_submit_button("Save preset", type='primary'):
            if preset_name != "New…":
                save_preset()
                st.write("Preset saved")
                ss.current_preset = preset_name
                st.experimental_rerun()
            else:
                st.warning('Please update the preset name')

    with col2:
        if st.form_submit_button("Delete preset"):
            print(ss.current_preset)
            if ss.current_preset != "New…":
                delete_preset(ss.current_preset)
                st.write("Preset removed")
                initialise_states()
                ss.current_preset = ss.presets.index[0] if not ss.presets.empty else ""
                st.experimental_rerun()




