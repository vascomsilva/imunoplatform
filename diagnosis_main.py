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
from PIL import Image

from rinite_alergica import page as page_RA
from urticaria_cronica import page as page_UC
from alergia_alimentar import page as page_AA
from hipersens_farmacos import page as page_HF

from automatic_text import automatic_text
# Falta colocar aqui a página do automatic_text
#@st.cache(suppress_st_warning=True)

def page(main_list, name, count):
    ###############################################################################
    # Check if personal file already exists and Rerun Page

    if os.path.exists('./patients/'+name.replace(' ','')+'.csv'):
        pass
    else:
        with open('./patients/'+name.replace(' ','')+'.csv', 'w') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['Data', 'Antecedentes', 'Teste',
                                 'Valor', 'Eosinófilos', 'IgE Total',
                                 'sIgE', 'Outros', 'Via Administração', 'Extratos',
                                 'Laboratórios', 'Desde', 'Efeitos Adversos',
                                 'Obstrução', 'Espirros', 'Prurido', 'Rinorreia', 'Medicação',
                                 'Início_UC', 'Características_UC', 'Controlo_UC',
                                 'Antecedentes_AA', 'Alimentos_AA', 'Idade_AA',
                                 'Alim Tolerados_AA', 'Reacao_MG_AA', 'Testes_AA',
                                 'Farmac_HF', 'Início_HF', 'Dosag Contexto_HF', 'Duração Admn-Reac_HF',
                                 'APs e Med Conc_HF', 'Med Simil Tol_HF', 'Reacao_MG_HF', 'Testes_HF',
                                 'Diagn_Adicion', 'Obsv'])

    ###############################################################################

    pcsv = pd.read_csv('patients/'+name.replace(' ','')+'.csv', header = 0, index_col = False)
    # Columns
    #col_1, col_2 = st.beta_columns(2)
    #with col_1:
        #image_HPA = Image.open('logo-hpa1.png')
        #st.image(image_HPA, use_column_width = True)

    st.header(name+' - '+'HPA Saúde'+' - '+count)

    #st.markdown('---')

    #st.subheader('Resumo :open_file_folder:')

    #if pcsv.shape[0] < 1:
        #st.text('Sem Informação Anterior')
    #else:
        #for i in range(pcsv.shape[0],-1,-1):
            #list_header = list(pcsv.columns.values)
            #for j in list_header:
                #if pd.notnull(pcsv.iloc[i-1][j]):
                    #st.markdown(j+' - :white_check_mark:'+'\n')
                #else:
                    #st.markdown(j+' - :red_circle:'+'\n')

    st.markdown('---')

    st.subheader('Preenchimento :memo:')
    col_RA, col_UC = st.beta_columns(2)

    with col_RA:
        st.subheader('Doença Alérgica Respiratória')
        concat_df_RA = page_RA(main_list, name)

    with col_UC:
        st.subheader('Urticária Crónica')
        concat_df_UC = page_UC(main_list, name)

    st.markdown('---')

    col_AA, col_HF = st.beta_columns(2)

    with col_AA:
        st.subheader('Alergia Alimentar')
        concat_df_AA = page_AA(main_list, name)

    with col_HF:
        st.subheader('Hipersensibilidade a Fármacos')
        concat_df_HF = page_HF(main_list, name)

    st.markdown('---')

    diagn = ['Rinite Crónica Não-Alérgica', 'Conjuntivite Alérgica', 'Tosse Crónica/Persistente',
            'Hipertrofia adenoides + Patologia Tubária', 'Rinossinusite Crónica sem Polipose Nasal',
            'Rinossinusite Crónica com Polipose Nasal', 'Hiperreatividade brônquica', 'Asma Não-Alérgica',
            'Sibilância Recorrente (associada a infecções)', 'Sibilância Recorrente (múltiplas causas)',
            'DPOC / Síndrome de Sobreposição Asma-DPOC', 'Doença Respiratória Exacerbada por AINEs (DREA)',
            'Infecções Recorrentes', 'Dermatite Atópica', 'Dermatite de Contacto', 'Prurido sem Alterações Cutâneas',
            'Angioedema Hereditário', 'Angioedema Idiopático Recorrente', 'Erupção Cutânea devida a Fármacos',
            'Anafilaxia', 'Esogastroenteropatia Eosinofílica Eosinofílica', 'Intolerância Alimentar',
            'Síndrome de Intestino Irritável', 'Reações Cutâneas Exuberantes a Artrópodes', 'Alergia a Himenópteros']

    adt_diagn = st.multiselect('Diagnóstico Adicional', diagn)

    for i in range(pcsv.shape[0],-1,-1):
        if pcsv.shape[0] == 0:
            break
        elif pd.isnull(pcsv.iloc[i-1]['Efeitos Adversos']):
            continue
        else:
            last_date = pcsv.iloc[i-1]['Data']
            last_ad_diagn = pcsv.iloc[i-1]['Diagn_Adicion']
            st.text(last_date + ' - ' + str(last_ad_diagn[1:-1]))
            break

    df_adt_diagn = pd.DataFrame({'Diagn_Adicion': [adt_diagn]})

    observ = st.text_area('Observações ou Comentários Adicionais')

    df_obsv = pd.DataFrame({'Obsv' : [observ]})

    st.markdown('---')

    ############################################################################

    # Saving data into pcsv

    full_info_ss = SessionState.get(new_df = 0)
    full_info_ss.new_df = pd.read_csv('patients/'+name.replace(' ','')+'.csv', header = 0, index_col = False)

    dates_verif = [concat_df_RA.iloc[0]['Desde'], concat_df_UC.iloc[0]['Início_UC'],
                   concat_df_HF.iloc[0]['Início_HF']]

    if st.button('Finish'):
        for i in range(0,len(dates_verif)):
            if dates_verif[i] == datetime.date.today():
                dates_verif[i] = dates_verif[i].strftime('%Y-%m-%d')
                dates_verif[i] = ''

        concat_df_RA.at[0,'Desde'] = dates_verif[0]
        concat_df_UC.at[0,'Início_UC'] = dates_verif[1]
        concat_df_HF.at[0,'Início_HF'] = dates_verif[2]

        new_appoint = pd.concat([concat_df_RA,concat_df_UC,concat_df_AA, concat_df_HF, df_adt_diagn, df_obsv], axis = 1)
        #st.dataframe(new_appoint)
        full_info_ss.new_df = full_info_ss.new_df.append(new_appoint)

        full_info_ss.new_df.to_csv('patients/'+name.replace(' ','')+'.csv', index = False)

        automatic_text(new_appoint, name, main_list)

    ############################################################################
    # Graphs or Charts

    st.markdown('---')

    st.subheader('Gráficos :chart_with_upwards_trend:')

    df_testing = []
    df_names = ['Obstrução', 'Espirros', 'Prurido', 'Rinorreia', 'Medicação']

    for i in range(0,full_info_ss.new_df.shape[0]):
        for j in range(0,len(df_names)):
            df_new = {'Data': full_info_ss.new_df.iloc[i]['Data'],
                      'Valor': full_info_ss.new_df.iloc[i][df_names[j]],
                      'Nome': df_names[j]}
            if full_info_ss.new_df.iloc[i][df_names[j]] != 0:
                df_testing.append(df_new)

    df_new = pd.DataFrame(df_testing)

    #df_new = df_new.reset_index().melt('Data', var_name='Nome', value_name='Valor')

    highlight = alt.selection(type='single', on='mouseover',
                              fields=['Nome'], nearest=True)

    base = alt.Chart(df_new).encode(
                                    x = 'Data:T',
                                    y = 'Valor:Q',
                                    color = 'Nome:N'
                                    )

    points = base.mark_circle().encode(
                                        opacity=alt.value(0)
                              ).add_selection(
                                        highlight
                              ).properties(
                                        width=600
                              )

    lines = base.mark_line().encode(
                size = alt.condition(~highlight, alt.value(1), alt.value(3))
            )
    c = alt.layer(
        points, lines
    ).properties(
        width=700, height=300
    )

    st.altair_chart(c)
