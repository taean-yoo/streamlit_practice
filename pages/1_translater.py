import streamlit as st
import openai

#openai.api_key=st.secrets['OPENAI_API_KEY']
st.set_page_config(
    page_title='ChatBot Streamlit',
    page_icon='✍️'
)
st.title("✍️ AI_번역기")
st.subheader("AI를 이용하여 상황에 맞는 번역을 해보세요.")
st.caption("🚀 A Streamlit chatbot powered by OpenAI")

auto_complete = st.toggle(label="예시로 채우기")

with st.sidebar:
    openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
    process = st.button("Process")
    "[Get an OpenAI API key](https://platform.openai.com/account/api-keys)"
    "[View the source code](https://github.com/streamlit/llm-examples/blob/main/Chatbot.py)"
    "[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/streamlit/llm-examples?quickstart=1)"
    if process:
        openai.api_key = openai_api_key
def request_chat_completion(
    prompt,
    system_role="당신은 영어 번역 전문가 입니다.",
    model="gpt-4o",
    stream=False
):
    messages = [
        {"role": "system", "content": system_role},
        {"role": "user", "content": prompt}
    ]
    response = openai.ChatCompletion.create(
        model=model,
        messages=messages,
        stream=stream
    )
    return response

def print_streaming_response(response):
    message=""
    placeholder=st.empty()
    for chunk in response:
        delta = chunk.choices[0]["delta"]
        if "content" in delta:
            message += delta["content"]
            placeholder.markdown(message+" ")
        else:
            break
    placeholder.markdown(message)
    return message

example = {
    "type":"논문",
    "text":"인공지능(AI) 기술은 다양한 분야에서 혁신을 가져왔으며, 교육 분야도 예외가 아니다. AI는 학생 개개인의 학습 선호도와 특성에 맞춘 개인화된 학습 경험을 제공하고, 방대한 학습 자료의 관리와 접근성을 높일 수 있다(Zhai et al., 2021; Limna et al., 2022). 그러나 AI 기술의 확장과 활용에는 가능성과 함께 위험과 리스크도 따른다. Rapp et al. (2021)은 AI를 그 효과성, 유용성, 사람들의 만족도와 참여도만으로 평가하는 것은 충분하지 않다고 지적한다. 본 보고서 에서는 AI 기술의 주요 위험성과 우려되는 점에 초점을 맞춰 논의하고자 한다.",
    "keywords": ["논리적","간결하게"]
}
type_dict = {
    "에세이": "✍🏻",
    "논문": "🕊",
    "보고서": "☠👮🏻‍♀️",
    "메일": "🕵🏻",
}
prompt_template = """
나는 지구환경도시건설공학과를 전공하고 있는 한국인 대학생이야.
{type} 형식으로 글을 하나 영어로 작성하고 싶어.
대학생 수준에서 그렇게 어렵지 않으면서 논리인 글을 작성해줘.
반드시 {max_length} 글자 이내로 작성해줘.
키워드가 주어질 경우, 반드시 키워드의 스타일대로 작성해줘.
출력 형식은 코드나 다른 형태가 아닌 무조건 줄글로 작성해줘!
---
글 형식: {type}
번역하고자 하는 글: {text}
키워드: {keywords}
---
""".strip()

with st.form("form"):
    col1, col2= st.columns(2)
    with col1:
        types = st.multiselect(
            label="글 형식",
            options=list(type_dict.keys()),
            max_selections=1,
            default=example["type"] if auto_complete else []
        )
    with col2:
        max_length=st.number_input(
            label="최대 글자 수",
            min_value=50,
            max_value=1000,
            step=50,
            value=100
        )
    text = st.text_input(
        "번역하고자 하는 글",
        placeholder=example["text"],
        value=example["text"] if auto_complete else ""
    )
    st.text("원하는 스타일을 최대 2개까지 입력해주세요")
    col1, col2= st.columns(2)
    with col1:
        keyword_1=st.text_input(
            label="keyword_1",
            label_visibility="collapsed",
            placeholder="키워드 1",
            value=example["keywords"][0] if auto_complete else ""
        )
    with col2:
        keyword_2=st.text_input(
            label="keyword_2",
            label_visibility="collapsed",
            placeholder="키워드 2",
            value=example["keywords"][1] if auto_complete else ""
        )

    submit = st.form_submit_button("Submit")

if submit:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    if not type:
        st.error("글 형식을 지정해주세요")
    elif not text:
        st.error("50자 이상의 글을 작성해주세요")
    else:
        keywords=[keyword_1,keyword_2]
        keywords=[x for x in keywords if x]
        prompt=prompt_template.format(
            text=text,
            type=type,
            max_length=max_length,
            keywords=keywords
        )
        system_role = "당신은 영어 번역 전문가 입니다."
        with st.spinner("번역중 입니다."):
            response = request_chat_completion(
                prompt=prompt,
                system_role=system_role,
                stream=True
            )
        st.form(print_streaming_response(response))
