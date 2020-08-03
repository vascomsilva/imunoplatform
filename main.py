import streamlit as st
import base64
import numpy as np
import pandas as pd
import time

st.title('Perfil')

st.write("Dados do doente")

st.checkbox("Feminino")



# GENERATE CSV FILE
data = [(1, 2, 3)]
# When no file name is given, pandas returns the CSV as a string, nice.
df = pd.DataFrame(data, columns=["Col1", "Col2", "Col3"])
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
st.markdown(href, unsafe_allow_html=True)
>>>>>>> cf0fde6dd9d741d16c986e3f2cd792869205d958
