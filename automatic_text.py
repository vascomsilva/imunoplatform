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

from dateutil.relativedelta import relativedelta


def automatic_text(dataframe, name, main_list):

    (dataframe.applymap(type) == str).all(0) #Tentar converter tudo para string
    (main_list.applymap(type) == str).all(0)

    content_pcsv = dataframe.loc[len(dataframe.index) - 1] # Apanhar a última linha

    content_gcsv = main_list.loc[len(main_list.index) - 1] # Apanhar a última linha - MUDAR ESTE

    ###########################################################################

    # Age

    end_date = datetime.date.today()
    start_date = datetime.datetime.strptime(content_gcsv['Birth'], '%Y-%m-%d')
    age = relativedelta(end_date, start_date).years

    ###########################################################################

    # Gender

    if content_gcsv['Gender'] == 'Male':
        adM = 'O'
        adm = 'o'
    else:
        adM = 'A'
        adm = 'a'

    ###########################################################################

    world = {
            'Nome' : content_gcsv['Name'],
            'Idade' : str(age),
            'Artigo Def_M' : adM,
            'Artigo Def_m' : adm,
    }

    appoint = {
              'Antec_DAR' : content_pcsv['Antecedentes'],
              'Teste' : content_pcsv['Teste'],
              'Valor' : content_pcsv['Valor'],
              'Eosi' : content_pcsv['Eosinófilos'],
              'IgE_T' : content_pcsv['IgE Total'],
              'sIgE' : content_pcsv['sIgE'],
              'Outros_DAR' : content_pcsv['Outros'],
              'Via Admn' : content_pcsv['Via Administração'],
              'Extratos' : content_pcsv['Extratos'],
              'Labs' : content_pcsv['Laboratórios'],
              'Desde_RA' : content_pcsv['Desde'],
              'Efeitos Adv' : content_pcsv['Efeitos Adversos'],
              'Obstrução' : content_pcsv['Obstrução'],
              'Espirros' : content_pcsv['Espirros'],
              'Prurido' : content_pcsv['Prurido'],
              'Rinorreia' : content_pcsv['Rinorreia'],
              'Medicação' : content_pcsv['Medicação'],
              'Início_UC' : content_pcsv['Início_UC'],
              'Carac_UC' : content_pcsv['Características_UC'],
              'Cont_UC' : content_pcsv['Controlo_UC'],
              'Antec_AA' : content_pcsv['Antecedentes_AA'],
              'Alim_AA' : content_pcsv['Alimentos_AA'],
              'Idade_AA' : content_pcsv['Idade_AA'],
              'Alim Tol_AA' : content_pcsv['Alim Tolerados_AA'],
              'Reação MG_AA' : content_pcsv['Reacao_MG_AA'],
              'Testes_AA' : content_pcsv['Testes_AA'],
              'Farmac_HF' : content_pcsv['Farmac_HF'],
              'Início_HF' : content_pcsv['Início_HF'],
              'Dos HF' : content_pcsv['Dosag Contexto_HF'],
              'Dur HF' : content_pcsv['Duração Admn-Reac_HF'],
              'APs_HF' : content_pcsv['APs e Med Conc_HF'],
              'Med_HF' : content_pcsv['Med Simil Tol_HF'],
              'Reação MG_HF' : content_pcsv['Reacao_MG_HF'],
              'Testes_HF' : content_pcsv['Testes_HF'],
              'Diagn_Adicion' : content_pcsv['Diagn_Adicion'],
              'Obsv' : content_pcsv['Obsv']
    }

    ###########################################################################

    # Introdução

    introd = world['Nome']+', '+world['Idade']+' '+'anos.\n'

    ###########################################################################

    # Antecedentes_DAR

    if appoint['Antec_DAR']:
        antec_DAR = 'Antecedentes_DAR - '+str(appoint['Antec_DAR'])[1:-1]+'.\n'
    else:
        antec_DAR = ''

    ###########################################################################

    # Testes Cutâneos e Valores em RA

    if content_pcsv['Teste']:
        if len(appoint['Teste']) > 1:
            main_test = ''
            main_val_test = ''
            for i in range(len(appoint['Teste'])):
                if i == 0:
                    main_test = main_test+str(''.join(appoint['Teste'][i]))
                    main_val_test = main_val_test+str(appoint['Valor'][i])
                else:
                    main_test = main_test+', '+str(''.join(appoint['Teste'][i]))
                    main_val_test = main_val_test+', '+str(appoint['Valor'][i])

            testesRA = 'Testes_DAR - '+main_test+ \
                        '; Valores - '+main_val_test+' respetivamente.\n'
        else:
            testesRA = 'Teste_DAR - '+str(''.join(appoint['Teste']))+ \
                        '; Valor - '+str(''.join(str(e) for e in appoint['Valor']))+'.\n'

    else:
        testesRA = ''

    ###########################################################################

    # Análises

    final_anal_DAR = ''
    if appoint['Eosi'] != 500:
        eosi = 'Eosinófilos - '+str(appoint['Eosi'])+'; '
        final_anal_DAR = final_anal_DAR+eosi
    else:
        eosi = ''

    if appoint['IgE_T'] != 0:
        IgE_T = 'IgE Total - '+str(appoint['IgE_T'])+' kU/L; '
        final_anal_DAR = final_anal_DAR+IgE_T
    else:
        IgE_T = ''

    if appoint['sIgE']:
        sIgE = 'sIgE - '+str(appoint['sIgE'])+' kU/L; '
        final_anal_DAR = final_anal_DAR+sIgE
    else:
        sIgE = ''

    if appoint['Outros_DAR']:
        outro_DAR = 'Outras Análises - '+appoint['Outros_DAR']+';'
        final_anal_DAR = final_anal_DAR+outro_DAR
    else:
        outro_DAR = ''

    if final_anal_DAR != '':
        final_anal_DAR = final_anal_DAR+'\n'

    ###########################################################################

    # Imunoterapia

    if appoint['Via Admn']:
        if len(appoint['Extratos']) > 1:
            imuno_RA = 'Desde - '+str(appoint['Desde_RA'])+ \
                        '; Extratos - '+str(appoint['Extratos'])+'; Labs - '+ \
                        str(appoint['Labs'])+'.\n'
            if appoint['Efeitos Adv']:
                efadv_RA = 'Efeitos Advs - '+str(appoint['Efeitos Adv'])+ \
                            '.\n'
            else:
                efadv_RA = 'Sem efeitos adversos.\n'
        else:
            imuno_RA = 'Desde - '+str(appoint['Desde_RA'])+ \
                        '; Extrato - '+str(''.join(appoint['Extratos']))+'; Labs - '+ \
                        str(''.join(appoint['Labs']))+'.\n'
            if appoint['Efeitos Adv']:
                efadv_RA = 'Efeitos Advs - '+str(appoint['Efeitos Adv'])+ \
                            '.\n'
            else:
                efadv_RA = 'Sem efeitos adversos.\n'
    else:
        imuno_RA = ''
        efadv_RA = ''

    ###########################################################################

    # Controlo

    if appoint['Obstrução'] or appoint['Espirros'] or appoint['Prurido'] or appoint['Rinorreia']:

        controlo = ['Obstrução', 'Espirros', 'Prurido', 'Rinorreia', 'Medicação']

        valores = [appoint['Obstrução'], appoint['Espirros'], appoint['Prurido'],
                    appoint['Rinorreia'], appoint['Medicação']]

        main_contr = ''
        main_val = ''
        for i in range(0, len(controlo)):
            if valores[i]:
                if i == 0:
                    main_contr = main_contr+controlo[i]
                    main_val = main_val+str(valores[i])
                else:
                    main_contr = main_contr+', '+controlo[i]
                    main_val = main_val+', '+str(valores[i])
            else:
                continue

        contr_RA = 'Controlo_DAR - '+main_contr+'; Valores - '+ \
                    main_val+' respetivamente.\n'

    else:
        contr_RA = ''

    ###########################################################################

    # Urticária Crónica

    if appoint['Início_UC']:
        inicio_UC = 'Início_UC - '+str(appoint['Início_UC'])+'.\n'
    else:
        inicio_UC = ''

    if appoint['Carac_UC']:
        carac_UC = ''
        for i in range(0, len(appoint['Carac_UC'])):
            if i == 0:
                carac_UC = carac_UC+str(''.join(appoint['Carac_UC'][i]))
            else:
                carac_UC = carac_UC+', '+str(''.join(appoint['Carac_UC'][i]))

        fin_carac_UC = 'Caracts_UC - '+carac_UC+'.\n'
    else:
        fin_carac_UC = ''

    if appoint['Cont_UC']:
        contr_UC = ''
        for i in range(0, len(appoint['Cont_UC'])):
            if i == 0:
                contr_UC = contr_UC+str(''.join(appoint['Cont_UC'][i]))
            else:
                contr_UC = contr_UC+', '+str(''.join(appoint['Cont_UC'][i]))

        fin_contr_UC = 'Controlo_UC - '+contr_UC+'.\n'
    else:
        fin_contr_UC = ''

    ###########################################################################

    # Alergia Alimentar

    if appoint['Antec_AA']:
        antec_AA = 'Antecedentes_AA - '+str(appoint['Antec_AA'])[1:-1]+'\n'
    else:
        antec_AA = ''

    if appoint['Alim_AA']:
        if len(appoint['Alim_AA']) > 1:
            list_AA = []
            final_AA = ''
            for i in range(len(appoint['Alim_AA'])):
                list_AA.append('AA a '+appoint['Alim_AA'][i]+' : '+'Idade de início - '+ \
                                appoint['Idade_AA'][i]+'; Alim Tol - '+ \
                                str(appoint['Alim Tol_AA'][i])+'; Reação MG - '+ \
                                str(appoint['Reação MG_AA'][i])[1:-1]+'; Testes - '+ \
                                appoint['Testes_AA'][i])

                final_AA = final_AA+list_AA[i]+'\n'
        else:
            final_AA = 'AA a '+appoint['Alim_AA'][0]+' : '+'Idade de início - '+ \
                       appoint['Idade_AA'][0]+'; Alim Tol - '+ str(appoint['Alim Tol_AA'][0])+ \
                       '; Reação MG - '+str(appoint['Reação MG_AA'][0])[1:-1]+'; Testes - '+ \
                        appoint['Testes_AA'][0]+'\n'
    else:
        final_AA = ''

    ###########################################################################

    # Hipersensibilidade a Fármacos

    if appoint['Farmac_HF']:
        if len(appoint['Farmac_HF']) > 1:
            list_HF = []
            final_HF = ''
            for i in range(len(appoint['Farmac_HF'])):
                list_HF.append(appoint['Farmac_HF'][i]+' - '+'Início - '+ \
                                appoint['Início_HF'][i]+'; Dos & Contex - '+ \
                                appoint['Dos HF'][i]+'; Dur Admn-Reac - '+ \
                                appoint['Dur HF'][i]+'; APs & Med - '+ \
                                appoint['APs_HF'][i]+'; Reação MG - '+ \
                                str(appoint['Reação MG_HF'][i])[1:-1]+'; Testes - '+ \
                                appoint['Testes_HF'][i])

                final_HF = final_HF+list_HF[i]+'\n'
        else:
            final_HF = 'HF a '+appoint['Farmac_HF'][0]+' : '+'Início - '+ \
                        appoint['Início_HF'][0]+'; Dos & Contex - '+ \
                        appoint['Dos HF'][0]+'; Dur Admn-Reac - '+ \
                        appoint['Dur HF'][0]+'; APs & Med - '+ \
                        appoint['APs_HF'][0]+'; Reação MG - '+ \
                        str(appoint['Reação MG_HF'][0])[1:-1]+'; Testes - '+ \
                        appoint['Testes_HF'][0]+'\n'
    else:
        final_HF = ''

    ###########################################################################

    # Diagnósticos Adicionais

    if appoint['Diagn_Adicion']:
        diagn_ad = 'Diagn Adic - '+str(appoint['Diagn_Adicion'])[1:-1]+'\n'
    else:
        diagn_ad = ''

    if appoint['Obsv']:
        obsv_final = 'Observações Extra - '+appoint['Obsv']+'\n'
    else:
        obsv_final = ''

    ###########################################################################

    st.text(introd+antec_DAR+testesRA+final_anal_DAR+imuno_RA+efadv_RA+contr_RA+ \
            inicio_UC+fin_carac_UC+fin_contr_UC+antec_AA+final_AA+final_HF+diagn_ad+obsv_final)
