import streamlit as st
import openai
from streamlit_when2meet import streamlit_when2meet
import datetime
import datetime
from streamlit_calendar import calendar


st.set_page_config(
        page_title='When2meet Safety lab',
        page_icon=':calendar:',
        layout="wide"
)
st.title("우리 :red[언제] 만날까? :calendar:")
st.caption("🚀 가능한 날짜를 sidebar에서 채워주세요")

today = datetime.datetime.now()
month_1 = datetime.date(today.year, today.month, 1)
dec_31 = datetime.date(today.year, 12, 31)

initial=[]
if "meeting" not in st.session_state:
    st.session_state.meeting = initial

st.subheader("Sign In")
col1, col2 = st.columns(2)
with col1:
        with st.form(key="form"):
                name = st.text_input(
                        label="Your Name",
                )
                date = st.date_input(
                        "Possible dates",
                        (month_1, datetime.date(today.year, today.month, today.day)),
                        month_1,
                        dec_31,
                        format="MM.DD.YYYY",
                        )
                time = streamlit_when2meet(disabled=False, initial_data=None)
                submit = st.form_submit_button(label="Submit")
                if submit:
                        if not name:
                                st.error("이름을 입력해 주세요")
                        elif len(date) == 0:
                                st.error("날짜를 적어도 하루 선택해 주세요.")
                        else:
                                st.success("회의 가능 날짜를 추가할 수 있습니다.")
                                st.session_state.meeting.append({
                                        "name": name,
                                        "date": date,
                                        "time": time
                                })
with col2:
        c=st.container(border=True)
        c.write("Names of participated people")
        c.code("태안")
        c.write("meeting date")
        c.write(date)
        c.date2 = streamlit_when2meet(disabled=False, initial_data=None)

#st.markdown(data)