import base64
from collections import Counter
import io
import itertools
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from django.shortcuts import render
import urllib
from sklearn import metrics
from datetime import datetime, date
from matplotlib.backends.backend_agg import FigureCanvasAgg
from django.http import HttpResponse
import plotly.express as px
from plotly.offline import plot

from . import funcs


#carregando dados
dados_usp = pd.read_csv('data/letras_usp_course_completion.csv', sep=',')
df_final = pd.read_csv('data/teste.csv', sep=',')


# def year_max_min():

#     min_year = pd.to_datetime(dados_usp['dtaing']).dt.year.min()
#     max_year = pd.to_datetime(dados_usp['dtaing']).dt.year.max()

#     return (min_year, max_year)



def num_alunos():
    #função que conta numero e alunos não unicos

    num = len(dados_usp['dtanas'])

    return num

def evasao():

    evadidos = dados_usp['evadido'].value_counts()['sim']

    return evadidos

def idade_media():
    return dados_usp['idade_no_ingresso'].mean()

def evasao_failure1ano_pie(i):
    fig = plt.figure(figsize=(9,5))
    dados_usp[dados_usp.failures_in_first_year == i+1]['evadido'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    plt.title(f'Taxa de alunos que evadem curso ao reprovarem = {i+1}')
   

    uri = funcs.gerar_imagem(fig)

    return uri

def evasao_failure1ano_pieteste(i):

    fig = px.pie(values=list(dados_usp[dados_usp.failures_in_first_year == i+1]['evadido'].value_counts()),
                 names=['sim', 'não'])

    fig.update_layout(legend=dict(y=0.5))

    fig.update_layout({'paper_bgcolor': 'rgba(0, 0, 0, 0)', 'plot_bgcolor': 'rgba(0, 0, 0, 0)', }, margin=dict(
            l=20, r=20, t=20, b=20), legend=dict(orientation="v", yanchor="bottom", y=1.02, xanchor="right", x=1))

    uri = plot(fig, output_type='div', config={
            'displaylogo': False,
            'modeBarButtonsToRemove': ['select', 'zoomIn', 'zoomOut', 'autoScale', 'resetScale', 'zoom', 'pan', 'toImage']})

    return uri


def evasao_failure1ano_bar():

    fig = plt.figure(figsize=(9,5))

    df_final = pd.DataFrame()
    for i in range(5):
        df = pd.DataFrame(dados_usp[dados_usp.failures_in_first_year == i+1]['evadido'].value_counts())
        df['pct'] = df['evadido'] / df['evadido'].sum()
        
        #df_final[f'{i+1}'] =
        df[df.index=='sim']['pct'].plot(kind='barh')
    #df_final.rename({'sim' : 'aluno que evadiram'}, inplace=True)
    
    fig = plt.figure(figsize=(9,5))
    #df_final.T.sort_index(ascending=False).plot(kind='barh')
    # for index, value in enumerate(df_final.T.sort_index(ascending=False)['aluno que evadiram']):
        # plt.text(value, index,
        #         str(f'{value:.2%}'))
        
    #df_final.plot()
    #dados_usp[dados_usp.failures_in_first_year == 1]['evadido'].value_counts().plot(kind='pie', autopct='%1.1f%%')
    # plt.title('Porcentagem de alunos que evadiram por reprovação no primeiro ano')

   

    uri = funcs.gerar_imagem(fig)



    return uri

def idade_histograma():

    fig = plt.figure(figsize=(9,5))   
    dados_usp['idade_no_ingresso'].hist(bins=30, grid=False)
    plt.title(f'Histograma idade dos alunos no ingresso')

    uri = funcs.gerar_imagem(fig)

    return uri

