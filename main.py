import streamlit as st
import base64
import numpy as np
import pandas as pd
import datetime

st.title('Perfil')

#Dados do doente
st.write("Dados do doente")
#st.checkbox("Feminino")

# Verificar depois de que forma podemos manusear isto
d = st.date_input("Nova atualização",datetime.date(2020, 8, 25))

###############################################################################

# Antecedentes

st.subheader('Antecedentes')

ante_RA = ['Atopia mãe/pai/irmãos', 'Prematuridade', 'Eczema Atópico', 'Parto cesariana/distócico/eutócico',
            'Aleitamento materno exclusivo 4+ meses', 'Fumador/ ex-fumador', 'Exposição a fumo de tabaco pai/mãe/outros',
            'Exposição a tóxicos ambientais', 'Exposição respiratória profissional', 'Frequenta infantário',
            'Hipertrofia adenoides']

select_ante_RA = st.multiselect('Quais os antecedentes relativos a esta patologia?',
    ante_RA)

df_ante_RA = pd.DataFrame({'Antecedentes': select_ante_RA})

###############################################################################

# Testes Cutâneos - ESTÁ BOM

st.subheader('Testes cutâneos')

test_cut = ['Dermatophagoides pteronyssinus', 'Dermatophagoides farinae', 'Lepidoglyphus destructor', 'Blomia tropicalis',
            'Alternaria Alternata', 'Blatella germanica', 'Cão', 'Gato', 'Gramíneas', 'Olea europea', 'Quercus ilex',
            'Betula verrucosa', 'Platanus acerifola', 'Artemisia vulgaris', 'Parietaria judaica', 'Salsola kali', 'Plantago lanceolata']

test_cut_selected = st.multiselect('Quais os testes cutâneos que pretende fazer?', test_cut)

df_test_values = []

for i in range(len(test_cut_selected)):
    df_test_value = st.slider(test_cut_selected[i], 0, 5, 0)
    if df_test_value > 3:
        df_test_values.append(df_test_value)

df_test_names = pd.DataFrame({'Teste': [test_cut_selected]})

df_test_values = pd.DataFrame({'Valor': [df_test_values]})

###############################################################################

# Análises - DE QUE FORMA LIDAR MELHOR COM ISTO?

st.subheader('Análises')

analises = ['Eosinófilos', 'IgE total (kU/L)', 'sIgE', 'Outras relavantes']

eosi = st.number_input(analises[0], min_value = int(500), max_value = int(7000), step = int(50))
IgEt = st.number_input(analises[1], min_value = int(), max_value = int(300), value = int(), step = int(10))
sIgE = st.text_input(analises[2])
outros = st.text_input(analises[3])

df_anal_names = pd.DataFrame({'Análise': analises})
df_anal_values = pd.DataFrame({'Valores': [eosi, IgEt, sIgE, outros]})

###############################################################################

# Imunoterapia - FALTA MELHORAR AQUI MUITA COISA

st.subheader('Imunoterapia')

extr_names = ['D. pteronyssinus', 'D. farinae', 'L. destructor', 'B. tropicalis', 'alternata', 'Cão', 'Gato',
            'Gramíneas selvagens', 'Oliveira', 'vulgaris', 'P. judaica', 'S. kali']

labs_names = ['Diater', 'Roxall', 'Leti', 'Inmunotek', 'Stallergennes', 'Allergy Therapeutics', 'Hal Allergy', 'Lofarma']

via_imunoter = st.selectbox('Qual a via administrada?', ('Subcutânea', 'Sublingual'))

extr_imunoter = st.multiselect('Quais os extratos utilizados?', extr_names)

lab_imunoter = st.multiselect('Quais os laboratórios??', labs_names)

date_imunoter = st.date_input('Desde quando?',datetime.date(2020,8,25))

efeit_imunoter = st.text_area('Quais os efeitos adversos?')

###############################################################################

# Controlo - MELHORAR

st.subheader('Controlo')

obstr_control = st.slider('Nariz Entupido', 0, 3, 0)

esp_control = st.slider('Espirros', 0, 3, 0)

prur_control = st.slider('Comichão no Nariz', 0, 3, 0)

rinor_control = st.slider('Corrimento/Pingo no Nariz', 0, 3, 0)

med_control = st.slider('Aumentar utilização dos medicamentos', 0, 3, 0)

df_control_names = pd.DataFrame({'Controlo': ['Obstrução', 'Espirros', 'Prurido', 'Rinorreia', 'Medicação']})
df_control_values = pd.DataFrame({'Valores': [obstr_control, esp_control, prur_control, rinor_control, med_control]})

###############################################################################

# When no file name is given, pandas returns the CSV as a string, nice.
df = pd.concat([df_ante_RA, df_test_names, df_test_values, df_anal_names, df_anal_values,
                df_control_names, df_control_values], ignore_index = True, axis = 1)

csv = df.to_csv(index=False)
b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
href = f'<a href="data:file/csv;base64,{b64}">Tabela - Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
st.markdown(href, unsafe_allow_html=True)
