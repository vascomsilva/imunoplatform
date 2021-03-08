import streamlit as st
import SessionState
import base64
import json
import csv
import numpy as np
import pandas as pd
import altair as alt
import datetime
import os.path

def writereadlists(list, action, new_elem):

    open_list = open(os.path.dirname(__file__) + '/../lists/'+list+'.txt', 'r+')
    read_list = open_list.read()

    if action == 'read':

        list_final = read_list.split(',')
        open_list.close()

    elif action == 'write':

        if new_elem != '':

            list_final = open_list.write(',' + new_elem)
            open_list.close()

    return list_final

def page(main_list, name):

    ###############################################################################

    full_info_ss = SessionState.get(new_df = 0)
    full_info_ss.new_df = pd.read_csv('patients/'+name.replace(' ','')+'.csv', header = 0, index_col = False)

    ###############################################################################

    # Antecedentes

    expander_antc = st.beta_expander('Antecedentes', expanded = False)

    with expander_antc:

        ante_RA = writereadlists('antecedentes_DAR', 'read', '')

        select_ante_RA = st.multiselect('Quais os antecedentes relativos a esta patologia?',
                                        ante_RA)
        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Antecedentes'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Antecedentes']
                st.text(last_date + ' - ' + last_info[1:-1])
                break

    df_ante_RA = pd.DataFrame({'Antecedentes': [select_ante_RA]})

    ###############################################################################

    # Testes Cutâneos

    expander_testcut = st.beta_expander('Testes Cutâneos', expanded = False)

    with expander_testcut:

        test_cut = writereadlists('testes_cutâneos_DAR', 'read', '')

        test_cut_selected = st.multiselect('Quais os testes cutâneos que pretende fazer?', test_cut)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Teste'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Teste']
                last_value = full_info_ss.new_df.iloc[i-1]['Valor']
                st.text(last_date + ' - ' + last_info[1:-1] + ' ---> ' + last_value)
                break

        df_test_values = []

        for i in range(len(test_cut_selected)):
            df_test_value = st.slider(test_cut_selected[i], 0, 20, 0)
            if df_test_value > 3:
                df_test_values.append(df_test_value)

    df_test_names = pd.DataFrame({'Teste': [test_cut_selected]})

    df_test_values = pd.DataFrame({'Valor': [df_test_values]})

    ###############################################################################

    # Análises

    expander_anal = st.beta_expander('Análises', expanded = False)

    with expander_anal:
        analises = ['Eosinófilos', 'IgE Total (kU/L)', 'sIgE (kU/L)', 'Outras Relevantes']

        eosi = st.number_input(analises[0], min_value = int(500), max_value = int(7000), step = int(50))

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Eosinófilos'] == 500.0:
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_eosi = full_info_ss.new_df.iloc[i-1]['Eosinófilos']
                st.text(last_date + ' - ' + str(last_eosi))
                break

        IgEt = st.number_input(analises[1], min_value = int(), max_value = int(300), step = int(10))

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['IgE Total'] == 0.0:
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_IgE = full_info_ss.new_df.iloc[i-1]['IgE Total']
                st.text(last_date + ' - ' + str(last_IgE))
                break

        sIgE = st.text_input(analises[2])

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif pd.isnull(full_info_ss.new_df.iloc[i-1]['sIgE']):
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_sIgE = full_info_ss.new_df.iloc[i-1]['sIgE']
                st.text(last_date + ' - ' + str(last_sIgE))
                break

        outros = st.text_input(analises[3])

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif pd.isnull(full_info_ss.new_df.iloc[i-1]['Outros']):
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_Outros = full_info_ss.new_df.iloc[i-1]['Outros']
                st.text(last_date + ' - ' + str(last_Outros))
                break

    df_anal = pd.DataFrame({'Eosinófilos': [eosi],
                            'IgE Total': [IgEt],
                            'sIgE': [sIgE],
                            'Outros': [outros]})

    ###############################################################################

    # Imunoterapia

    expander_imun = st.beta_expander('Imunoterapia', expanded = False)

    with expander_imun:

        via_imunoter = st.selectbox('Qual a via administrada?', ('','Subcutânea', 'Sublingual'))

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif pd.isnull(full_info_ss.new_df.iloc[i-1]['Via Administração']):
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_via = full_info_ss.new_df.iloc[i-1]['Via Administração']
                st.text(last_date + ' - ' + str(last_via))
                break

        extr_names = writereadlists('extratos_DAR', 'read', '')

        extr_imunoter = st.multiselect('Quais os extratos utilizados?', extr_names)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Extratos'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_ext = full_info_ss.new_df.iloc[i-1]['Extratos']
                st.text(last_date + ' - ' + last_ext[1:-1])
                break

        labs_names = writereadlists('labs_DAR', 'read', '')

        lab_imunoter = st.multiselect('Quais os laboratórios?', labs_names)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Laboratórios'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_lab = full_info_ss.new_df.iloc[i-1]['Laboratórios']
                st.text(last_date + ' - ' + last_lab[1:-1])
                break

        date_imunoter = st.date_input('Desde quando?',datetime.date.today())

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif pd.isnull(full_info_ss.new_df.iloc[i-1]['Desde']):
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_desde = full_info_ss.new_df.iloc[i-1]['Desde']
                st.text(last_date + ' - ' + 'Desde ' + str(last_desde))
                break

        efeit_imunoter = st.text_area('Quais os efeitos adversos?')

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif pd.isnull(full_info_ss.new_df.iloc[i-1]['Efeitos Adversos']):
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_efadv = full_info_ss.new_df.iloc[i-1]['Efeitos Adversos']
                st.text(last_date + ' - ' + str(last_efadv))
                break

    df_imunoter = pd.DataFrame({'Via Administração': [via_imunoter],
                                'Extratos': [extr_imunoter],
                                'Laboratórios': [lab_imunoter],
                                'Desde': [date_imunoter],
                                'Efeitos Adversos': [efeit_imunoter]})

    ###############################################################################

    # Controlo

    expander_contr_RA = st.beta_expander('Controlo', expanded = False)

    with expander_contr_RA:
        obstr_control = st.slider('Nariz Entupido', 0, 3, 0)

        esp_control = st.slider('Espirros', 0, 3, 0)

        prur_control = st.slider('Comichão no Nariz', 0, 3, 0)

        rinor_control = st.slider('Corrimento/Pingo no Nariz', 0, 3, 0)

        med_control = st.slider('Aumentar utilização dos medicamentos', 0, 3, 0)

    df_control = pd.DataFrame({'Obstrução': [obstr_control],
                               'Espirros': [esp_control],
                               'Prurido': [prur_control],
                               'Rinorreia': [rinor_control],
                               'Medicação': [med_control]})


    ###############################################################################
    # Save new info into csv file

    concat_df_RA = pd.concat([pd.DataFrame({'Data': [datetime.date.today()]}),
                           df_ante_RA, df_test_names, df_test_values, df_anal,
                           df_imunoter, df_control],
                           ignore_index = False, axis = 1)

    return concat_df_RA
