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

    # Antecedentes Pessoais

    expander_antc_AA = st.beta_expander('Antecedentes', expanded = False)

    with expander_antc_AA:

        ante_AA = writereadlists('antecedentes_AA', 'read', '')

        select_ante_AA = st.multiselect('Quais os antecedentes relativos a Alergia Alimentar?',
                                        ante_AA)
        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Antecedentes_AA'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Antecedentes_AA']
                st.text(last_date + ' - ' + str(last_info[1:-1]))
                break

    df_ante_AA = pd.DataFrame({'Antecedentes_AA': [select_ante_AA]})

    ###############################################################################

    # Seleção de Alimentos

    expander_alim = st.beta_expander('Selecionar Alimentos', expanded = False)

    with expander_alim:

        select_num_alim = st.number_input('Número de Alimentos a Adicionar',
                                            min_value = 0)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Alimentos_AA'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Alimentos_AA']
                st.text(last_date + ' - ' + str(last_info[1:-1]))
                break

        list_alim = []
        for i in range(select_num_alim):
            alim = st.text_input('Alimento '+str(i+1))
            list_alim.append(alim)

    df_alim = pd.DataFrame({'Alimentos_AA': [list_alim]})

    ###############################################################################

    # Idade de Início

    expander_inicio_AA = st.beta_expander('Idade', expanded = False)

    list_idades = []
    with expander_inicio_AA:

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Idade_AA'] == '[]':
                continue
            else:
                current_time = full_info_ss.new_df.iloc[i-1]['Idade_AA']
                st.text('A idade de início foi aos ' + str(current_time) + ' anos')
                break

        if not list_alim:
            st.text('Ainda não foram inseridos novos Alimentos')
        else:
            for i in range(len(list_alim)):
                select_inicio = st.text_input('Qual foi a idade de início?'+' - '+list_alim[i], key = i)
                list_idades.append(select_inicio)

    df_inicio_AA = pd.DataFrame({'Idade_AA': [list_idades]})

    ###############################################################################

    # Alimentos Tolerados

    expander_alim_tol = st.beta_expander('Alimentos Tolerados', expanded = False)

    list_tol = []
    with expander_alim_tol:

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Alim Tolerados_AA'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Alim Tolerados_AA']
                st.text(last_date + ' - ' + str(last_info[1:-1]))
                break

        if not list_alim:
            st.text('Ainda não foram inseridos novos Alimentos')
        else:
            for i in range(len(list_alim)):
                select_alim_tol = st.text_input('Alimentos Tolerados'+' - '+list_alim[i], key = i)
                list_tol.append(select_alim_tol)

    df_alim_tol = pd.DataFrame({'Alim Tolerados_AA': [list_tol]})

    ###############################################################################

    # Reação Mais Grave

    expander_reacMG_AA = st.beta_expander('Reação Mais Grave', expanded = False)

    list_RMG = []
    with expander_reacMG_AA:

        RMG_AA = writereadlists('reaçãomaisgrave_AA', 'read', '')

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Reacao_MG_AA'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Reacao_MG_AA']
                st.text(last_date + ' - ' + str(last_info[1:-1]))
                break

        if not list_alim:
            st.text('Ainda não foram inseridos novos Alimentos')
        else:
            for i in range(len(list_alim)):
                select_reac_AA = st.multiselect('Reação mais grave'+' - '+list_alim[i], RMG_AA, key = i)
                list_RMG.append(select_reac_AA)

    df_reac = pd.DataFrame({'Reacao_MG_AA': [list_RMG]})

    ###############################################################################

    # Testes Realizados

    expander_test_AA = st.beta_expander('Testes', expanded = False)

    list_testes = []
    with expander_test_AA:

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Testes_AA'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_info = full_info_ss.new_df.iloc[i-1]['Testes_AA']
                st.text(last_date + ' - ' + str(last_info[1:-1]))
                break

        if not list_alim:
            st.text('Ainda não foram inseridos novos Alimentos')
        else:
            for i in range(len(list_alim)):
                testes_AA = st.text_input('Testes Realizados'+' - '+list_alim[i], key = i)
                list_testes.append(testes_AA)

    df_testes = pd.DataFrame({'Testes_AA': [list_testes]})

    ###############################################################################
    # Save new info into csv file

    # O IDEAL SERÁ UMA CONCAT FINAL NO DIAGNOSIS_MAIN PARA JUNTAR A DATA DA CONSULTA
    concat_df_AA = pd.concat([df_ante_AA, df_alim, df_inicio_AA, df_alim_tol,
                            df_reac, df_testes], ignore_index = False, axis = 1)

    return concat_df_AA
