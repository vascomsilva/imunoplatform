import streamlit as st
import base64
import numpy as np
import pandas as pd
import time

st.title('Perfil')

#Dados do doente
st.write("Dados do doente")
st.checkbox("Feminino")


#Antecedentes Rinite Alérgica


#Testes cutâneos com slider, gravar no txt nome dos testes com valor>3, separados por ";"
st.write("Testes cutâneos")

dermaptero = st.slider('Dermatophagoides pteronyssinus', 0, 5, 0)
st.write('Teste de Dermatophagoides pteronyssinus:', dermaptero)

dermafarinae = st.slider('Dermatophagoides farinae', 0, 5, 0)
lepi = st.slider('Lepidoglyphus destructor', 0, 5, 0)
blomia = st.slider('Blomia tropicalis', 0, 5, 0)
alternaria = st.slider('Alternaria Alternata', 0, 5, 0)
blatella = st.slider('Blatella germanica', 0, 5, 0)
cao = st.slider('Cão', 0, 5, 0)
gato = st.slider('Gato', 0, 5, 0)
gramineas = st.slider('Gramíneas', 0, 5, 0)
olea = st.slider('Olea europea', 0, 5, 0)
quercus = st.slider('Quercus ilex', 0, 5, 0)
betula = st.slider('Betula verrucosa', 0, 5, 0)
platanus = st.slider('Platanus acerifola', 0, 5, 0)
artemisia = st.slider('Artemisia vulgaris', 0, 5, 0)
parietaria = st.slider('Parietaria judaica', 0, 5, 0)
salsola = st.slider('Salsola kali', 0, 5, 0)
plantago = st.slider('Plantago lanceolata', 0, 5, 0)


# When no file name is given, pandas returns the CSV as a string, nice.
df = pd.DataFrame({
    'Teste': ["Dermatophagoides pteronyssinus",
    "Dermatophagoides farinae", "Lepidoglyphus destructor", "Blomia tropicalis",
    "Alternaria Alternata", "Blatella germanica","Cao", "Gato", "Gramineas", "Olea europea", "Quercus ilex",
    "Betula verrucosa", "Platanus acerifola", "Artemisia vulgaris",
    "Lepidoglyphus destructor", "Salsola kali", "Plantago lanceolata"],

    'Valor': [dermaptero, dermafarinae, lepi, blomia, alternaria, blatella, cao, gato, gramineas, olea, quercus, betula, platanus, artemisia, parietaria, salsola, plantago]
})

csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
st.markdown(href, unsafe_allow_html=True)






# GENERATE CSV FILE
data = [(1, 2, 3)]
# When no file name is given, pandas returns the CSV as a string, nice.
df = pd.DataFrame(data, columns=["Col1", "Col2", "Col3"])
csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
st.markdown(href, unsafe_allow_html=True)
#>>>>>>> cf0fde6dd9d741d16c986e3f2cd792869205d958
