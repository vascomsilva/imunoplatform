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

from rinite_alergica import writereadlists

def page(main_list, name):

    ###############################################################################

    full_info_ss = SessionState.get(new_df = 0)
    full_info_ss.new_df = pd.read_csv('patients/'+name.replace(' ','')+'.csv', header = 0, index_col = False)

    ###############################################################################

    # Seleção de Fármacos

    expander_farm = st.beta_expander('Selecionar Fármacos', expanded = False)

    with expander_farm:

        select_num_farm = st.number_input('Número de Fármacos a Adicionar',
                                            min_value = 0)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Farmac_HF'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Farmac_HF']
                st.text(last_date + ' - ' + str(last_info[1:-1]))
                break

        list_farm = []
        for i in range(select_num_farm):
            farm = st.text_input('Fármaco '+str(i+1))
            list_farm.append(farm)

    df_farm = pd.DataFrame({'Farmac_HF': [list_farm]})


    ###############################################################################

    # Data de Início

    expander_inicio_HF = st.beta_expander('Início', expanded = False)

    list_data_HF = []
    with expander_inicio_HF:

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Início_HF'] == '[]':
                continue
            else:
                current_date = full_info_ss.new_df.iloc[i-1]['Início_HF']
                st.text('A data de início foi em '+str(current_date))
                break

        st.text('Deverá aparecer aqui o número de semanas/meses?')

        if not list_farm:
            st.text('Ainda não foram inseridos novos Fármacos')
        else:
            for i in range(len(list_farm)):
                select_inicio_HF = st.date_input('Data de início'+' - '+list_farm[i],
                                                datetime.date.today(), key = i)
                list_data_HF.append(str(select_inicio_HF))


    df_inicio_HF = pd.DataFrame({'Início_HF': [list_data_HF]})

    ###############################################################################

    # Medicação: Dosagem e contexto; Duração..; APs e...; Medicação...;

    expander_med = st.beta_expander('Medicação', expanded = False)

    list_DS_HF = []
    list_DARA_HF = []
    list_APs_HF = []
    list_MED_HF = []
    with expander_med:

        if not list_farm:
            st.text('Ainda não foram inseridos novos Fármacos')

        if not list_farm:
            None
        else:
            for i in range(len(list_farm)):
                dos_contex = st.text_input('Dosagem e contexto'+' - '+list_farm[i], key = i)
                list_DS_HF.append(dos_contex)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Dosag Contexto_HF'] == '[]':
                continue
            else:
                last_date = last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Dosag Contexto_HF']
                st.text(last_date + ' - ' + last_info)
                break

        if not list_farm:
            None
        else:
            for i in range(len(list_farm)):
                dura_admn_reac = st.text_input('Duração entre administração e reação adversa'+' - '+list_farm[i], key = i)
                list_DARA_HF.append(dura_admn_reac)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Duração Admn-Reac_HF'] == '[]':
                continue
            else:
                last_date = last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Duração Admn-Reac_HF']
                st.text(last_date + ' - ' + last_info)
                break

        if not list_farm:
            None
        else:
            for i in range(len(list_farm)):
                aps_conco = st.text_input('APs e medicação concomitante'+' - '+list_farm[i], key = i)
                list_APs_HF.append(aps_conco)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['APs e Med Conc_HF'] == '[]':
                continue
            else:
                last_date = last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['APs e Med Conc_HF']
                st.text(last_date + ' - ' + last_info)
                break

        if not list_farm:
            None
        else:
            for i in range(len(list_farm)):
                med_sim = st.text_input('Medicação similar tolerada'+' - '+list_farm[i], key = i)
                list_MED_HF.append(med_sim)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Med Simil Tol_HF'] == '[]':
                continue
            else:
                last_date = last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Med Simil Tol_HF']
                st.text(last_date + ' - ' + last_info)
                break

    df_medi = pd.DataFrame({'Dosag Contexto_HF': [list_DS_HF],
                            'Duração Admn-Reac_HF': [list_DARA_HF],
                            'APs e Med Conc_HF': [list_APs_HF],
                            'Med Simil Tol_HF': [list_MED_HF]})


    ###############################################################################

    # Reação Mais Grave

    expander_reacMG_HF = st.beta_expander('Reação Mais Grave', expanded = False)

    list_RMG_HF = []
    with expander_reacMG_HF:

        RMG_HF = writereadlists('reaçãomaisgrave_HF', 'read', '')

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Reacao_MG_HF'] == '[]':
                continue
            else:
                last_date = last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Reacao_MG_HF']
                st.text(last_date + ' - ' + last_info[1:-1])
                break

        if not list_farm:
            st.text('Ainda não foram inseridos novos Fármacos')
        else:
            for i in range(len(list_farm)):
                select_reac_HF = st.multiselect('Reação mais grave - HF'+' - '+list_farm[i],
                                                RMG_HF, key = i)
                list_RMG_HF.append(select_reac_HF)

    df_reac = pd.DataFrame({'Reacao_MG_HF': [list_RMG_HF]})

    ###############################################################################

    # Testes Realizados

    expander_test_HF = st.beta_expander('Testes', expanded = False)

    list_testes_HF = []
    with expander_test_HF:

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Testes_HF'] == '[]':
                continue
            else:
                last_date = last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Testes_HF']
                st.text(last_date + ' - ' + last_info)
                break

        if not list_farm:
            st.text('Ainda não foram inseridos novos Fármacos')
        else:
            for i in range(len(list_farm)):
                testes_HF = st.text_input('Testes Realizados - HF'+' - '+list_farm[i], key = i)
                list_testes_HF.append(testes_HF)

    df_testes = pd.DataFrame({'Testes_HF': [list_testes_HF]})

    ###############################################################################
    # Save new info into csv file

    # O IDEAL SERÁ UMA CONCAT FINAL NO DIAGNOSIS_MAIN PARA JUNTAR A DATA DA CONSULTA
    concat_df_HF = pd.concat([df_farm, df_inicio_HF, df_medi, df_reac, df_testes],
                           ignore_index = False, axis = 1)

    return concat_df_HF
