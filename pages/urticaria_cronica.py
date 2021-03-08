import streamlit as st
import SessionState
import base64
import json
import csv
import numpy as np
import pandas as pd
import altair as alt
from datetime import datetime, timedelta, date
import os.path

from rinite_alergica import writereadlists

def page(main_list, name):

    ###############################################################################

    full_info_ss = SessionState.get(new_df = 0)
    full_info_ss.new_df = pd.read_csv('patients/'+name.replace(' ','')+'.csv', header = 0, index_col = False)

    ###############################################################################

    # Início

    expander_inicio_UC = st.beta_expander('Início', expanded = False)

    with expander_inicio_UC:
        select_inicio = st.date_input('Qual foi a data em que começou a urticária?',
                                        date.today())
        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif pd.isnull(full_info_ss.new_df.iloc[i-1]['Início_UC']):
                continue
            else:
                current_time = full_info_ss.new_df.iloc[i-1]['Início_UC']
                current_time = str(current_time)
                #st.text(current_time)
                current_time = date(int(current_time[0:4]), int(current_time[6:7]), int(current_time[9:10]))
                today = date.today()
                monday1 = (today - timedelta(days=today.weekday()))
                monday2 = (current_time - timedelta(days=current_time.weekday()))
                weeks = (monday1 - monday2).days / 7
                st.text('Começou o tratamento há '+str(weeks)+' semanas.')
                break

    df_inicio_UC = pd.DataFrame({'Início_UC': [select_inicio]})

    ###############################################################################

    # Características e Fatores Prognósticos

    expander_caract = st.beta_expander('Características e Fatores Prognósticos', expanded = False)

    with expander_caract:

        caract = writereadlists('características_UC', 'read', '')

        select_caract = st.multiselect('Quais as características e fatores prognóstico mais relevantes?', caract)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Características_UC'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_caract = full_info_ss.new_df.iloc[i-1]['Características_UC']
                st.text(last_date + ' - ' + last_caract[1:-1])
                break

        text_caract = st.text_area('Outros')

    df_caract = pd.DataFrame({'Características_UC': [select_caract]})

    ###############################################################################

    # Controlo

    expander_contr_UC = st.beta_expander('Controlo', expanded = False)

    with expander_contr_UC:

        controlo = writereadlists('controlo_UC', 'read', '')

        select_contr = st.multiselect('Controlo', controlo)

        for i in range(full_info_ss.new_df.shape[0],-1,-1):
            if full_info_ss.new_df.shape[0] == 0:
                break
            elif full_info_ss.new_df.iloc[i-1]['Controlo_UC'] == '[]':
                continue
            else:
                last_date = full_info_ss.new_df.iloc[i-1]['Data']
                last_contr = full_info_ss.new_df.iloc[i-1]['Controlo_UC']
                st.text(last_date + ' - ' + last_contr[1:-1])
                break

    df_controlo = pd.DataFrame({'Controlo_UC': [select_contr]})


    ###############################################################################
    # Save new info into csv file

    # O IDEAL SERÁ UMA CONCAT FINAL NO DIAGNOSIS_MAIN PARA JUNTAR A DATA DA CONSULTA
    concat_df_UC = pd.concat([df_inicio_UC, df_caract, df_controlo],
                           ignore_index = False, axis = 1)

    return concat_df_UC
