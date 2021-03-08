## TESTE SOBRE SESSION STATE E CACHING

import streamlit as st
import SessionState
import altair as alt
from vega_datasets import data

st.sidebar.title("Pages")
radio = st.sidebar.radio(label="", options=["Set A", "Set B", "Add them"])

session_state = SessionState.get(a=0, b=0)  # Pick some initial values.

if radio == "Set A":
    session_state.a = float(st.text_input(label="What is a?", value=session_state.a))
    st.write(f"You set a to {session_state.a}")
elif radio == "Set B":
    session_state.b = float(st.text_input(label="What is b?", value=session_state.b))
    st.write(f"You set b to {session_state.b}")
elif radio == "Add them":
    st.write(f"a={session_state.a} and b={session_state.b}")
    button = st.button("Add a and b")
    if button:
        st.write(f"a+b={session_state.a+session_state.b}")

source = data.stocks()

highlight = alt.selection(type='single', on='mouseover',
                          fields=['symbol'], nearest=True)

base = alt.Chart(source).encode(
    x='date:T',
    y='price:Q',
    color='symbol:N'
)

points = base.mark_circle().encode(
    opacity=alt.value(0)
).add_selection(
    highlight
).properties(
    width=600
)

lines = base.mark_line().encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(3))
)

st.altair_chart(points + lines)

st.write(source)
