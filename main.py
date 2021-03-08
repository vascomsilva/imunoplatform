# Main Ones
from streamlit import caching
import streamlit as st
import numpy as np
import pandas as pd
import datetime
import SessionState
import csv

# Others
import base64
import json

# Modules of Possible Diagnosis
import os.path
import sys
sys.path.append('pages/')

from diagnosis_main import page as main_page
from rinite_alergica import writereadlists

##############################################################################
st.set_page_config(page_title = 'ImmunoPlatform', layout="wide")
# This can only be set once and it must be the first streamlit command of the app
###############################################################################
def introduction_page(action):

    if action == 'ON':
        st.header('**IMMUNOPLATFORM - v1.0.0**')
        st.markdown('''
                    Bem-vindo à ImmunoPlatform! \n
                    Esta plataforma permite auxiliar consultas na área de Imunoalergologia
                    fornecendo *widgets* interativos com o intuito de facilitar o preenchimento,
                    por parte do médico, das diferentes variáveis para quatro diagnósticos distintos: \n
                    - Doença Alérgica Respiratória \n
                    - Urticária Crónica \n
                    - Alergia Alimentar \n
                    - Hipersensibilidade a Fármacos \n
                    Esta plataforma permite organizar os dados recolhidos de cada paciente
                    ao longo de diversas consultas, estando essa organização perfeitamente automatizada.
                    De forma global, esta plataforma possui três ações distintas: \n
                    - **New Patient** - permite guardar no gcsv informação básica de um novo paciente
                    que ainda não conste na base de dados (**Nota**: a submissão apenas é feita corretamente
                    se todos os campos forem preenchidos); \n
                    - **New Appointment** - permite guardar no pcsv informação referente a uma consulta
                    específica de um paciente específico (**Nota**: esta ação permite também a visualização de
                    gráficos de controlo e a geração de um texto-resumo que reflete aquilo que foi
                    preenchido na presente consulta e que pode ser utilizado para o preenchimento do
                    registo clínico do paciente - necessário clicar no botão “Finish”); \n
                    - **Edit Lists** - permite adicionar novos elementos a uma lista específica;
                    ''')
        st.subheader('Outras Notas Importantes')
        st.markdown('''
                    - Todos os *widgets*, de forma global (sejam eles de texto, data, números ou seleção), podem
                    ser alterados, bastando para isso alterar o valor/elemento que foi selecionado previamente.
                    No entanto, é necessário ter em atenção que, aquando do clique do botão **Finish**, todos os
                    valores/elementos preenchidos até à altura serão aqueles que entrarão no pcsv do paciente em causa.
                    **Nota**: caso se dê qualquer tipo de engano desta espécie, basta modificar
                    aquilo que foi inserido de forma errada e voltar a submeter (**Finish**). Assim que a consulta
                    acabar, poderá ir diretamente ao pcsv do paciente e apagar a linha que foi submetida por engano
                    e guardar esse pcsv; \n
                    - Para todos os *text_inputs*, o texto introduzido apenas é submetido se for clicado
                    (ENTER ou similar) - sendo que esta indicação aparece no *widget* enquanto o utilizador está
                    a preenchê-lo; \n
                    - Caso exista algum tempo prolongado sem mexer na plataforma é normal que, na primeira resposta
                    ao rato, a plataforma demore uns segundos a responder. Nestes casos, bastará aguardar meia dúzia
                    de segundos para que retome o funcionamento normal.\n
                    ''')
    else:
        return

def list_patient(info, type_pat):

    main_list = pd.read_csv('patient_list.txt',
    header = 0,
    index_col = False)

    (main_list.applymap(type) == str).all(0)

    if type_pat == 'Edit Lists':
        list = st.sidebar.selectbox('Que lista pretende editar?', ['Select','antecedentes_DAR',
                                    'antecedentes_AA', 'características_UC',
                                    'controlo_UC', 'extratos_DAR', 'labs_DAR', 'reaçãomaisgrave_AA',
                                    'reaçãomaisgrave_HF', 'testes_cutâneos_DAR'])
        if list != 'Select':
            edit_list(list)

    elif type_pat == 'New Appointment':
        patient_now = st.sidebar.selectbox('Search by Name or File number',
        ['Select']+[main_list['Code'][i] + ' | ' + main_list['Name'][i] for i in range(main_list.shape[0])])
        count = patient_now[:5]
        row_now = main_list[main_list['Code'].str.match(count)]
        if st.sidebar.button('Limpar Página'):
            return main_list
        if patient_now != 'Select':
            new_patient_now = patient_now.replace(count, '')
            name_patient = new_patient_now.replace('|', '')
            main_page(main_list, name_patient, count)

    elif type_pat == 'New Patient':
        main_list.loc[len(main_list.index)] = info
        row_now = main_list.loc[len(main_list.index) - 1]
        if len(info) - info.count('') == 5:
            main_list.to_csv('patient_list.csv',
            header = ['Name','Birth','Contact','Gender','Code'],
            index = False,
            encoding = 'utf_8')

            np.savetxt(r'patient_list.txt',
            main_list.to_numpy(),
            '%-10s',
            delimiter = ',',
            header = 'Name,Birth,Contact,Gender,Code',
            comments = '')

    return main_list


def edit_list(list):

    col_A, col_B = st.beta_columns(2)

    with col_A:
        st.subheader('Atual Lista - '+list)

        content_list = writereadlists(list, 'read', '')

        st.dataframe(content_list)

    with col_B:
        st.subheader('Adicionar Elementos')

        st.markdown('''
        Aqui deve adicionar um novo elemento à lista que acabou de selecionar. Caso
        pretenda remover algum elemento na lista, deverá abrir a pasta *"lists"* e
        remover manualmente o elemento que não pretende ver mais inserido nas opções
        da lista em questão.
        ''')

        new_elem = st.text_input('Novo Elemento')

        if new_elem != '':
            list_final = writereadlists(list, 'write', new_elem)



def after_session(name, gender, diagnosis, code):
    st.sidebar.subheader('Choose the action:')
    type_pat = st.sidebar.selectbox('', ['Select', 'New Patient', 'New Appointment', 'Edit Lists'])
    info = ['','','','','']
    if type_pat == 'Select':
        introduction_page('ON')
    elif type_pat == 'Edit Lists':
        list_patient(info, type_pat)
    elif type_pat == 'New Appointment':
        list_patient(info, type_pat)
    elif type_pat == 'New Patient':
        name = st.sidebar.text_input('Name')
        birth = st.sidebar.date_input('Birth date', datetime.date.today())
        contact = st.sidebar.text_input('Contact')
        gender = st.sidebar.selectbox('Gender', ['Male', 'Female', 'Other'])
        code = st.sidebar.text_input('File Number')
        info = [name, birth, contact, gender, code]
        list_patient(info, type_pat)


# Initiating Session States for Logins and Headers
login_ss = SessionState.get(username = '', password = '')
headers_ss = SessionState.get(main_title = '', date = '')

# Sidebar with Login
st.sidebar.subheader('Login')
login_ss.username = st.sidebar.text_input('Username')
login_ss.password = st.sidebar.text_input('Password', type = 'password')

# Check Login
def check_login(username, password):
    return login_ss.username == 'pedromorais' and login_ss.password == '12345'

if check_login(login_ss.username, login_ss.password):
    after_session(None, None, None, None)
elif not login_ss.password == '12345' and len(login_ss.password) != 0:
    st.sidebar.subheader('incorrect password')
