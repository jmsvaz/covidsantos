#!/usr/bin/env python
#    CovidSantos - Tracking COVID-19 cases in Santos, Brazil.
#    Copyright (C) 2021 João Marcelo S. Vaz
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <https://www.gnu.org/licenses/>.
#
# ==============================================================================

import os
import fileinput
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import date2num
import matplotlib.ticker as mtick

csvfilename = os.path.join('.', 'data', 'data.csv')
graphpath = os.path.join('.', 'docs', 'img')
webfilename = os.path.join('.', 'docs', 'index.md')
siteURL = 'https://jmsvaz.github.io/covidsantos/'

SantosPopulation = 433656

# Read CSV file into DataFrame df
# date,cases,deaths,suspectedcases,hospitalized,UTI,totalUTIoccupation,publicUTIoccupation,privateUTIoccupation,vaccinedoses
df = pd.read_csv(csvfilename, parse_dates=['date'], dayfirst=True)

# get the first and last day of the dataset
firstday = df['date'].min()
lastday = df['date'].max()

df['days']=df['date'] - firstday

df['newcases'] = df['cases'] - df['cases'].shift(1, fill_value=0)
df['mean7newcases'] = df['newcases'].rolling(7).mean()
df['mean30newcases'] = df['newcases'].rolling(30).mean()
df['weekcases'] = df['newcases'].rolling(7).sum()

df['newdeaths'] = df['deaths'] - df['deaths'].shift(1, fill_value=0)
df['mean7newdeaths'] = df['newdeaths'].rolling(7).mean()
df['mean30newdeaths'] = df['newdeaths'].rolling(30).mean()
df['weekdeaths'] = df['newdeaths'].rolling(7).sum()

df['newvaccinedoses'] = df['vaccinedoses'] - df['vaccinedoses'].shift(1, fill_value=0)
df['mean7newvaccinedoses'] = df['newvaccinedoses'].rolling(7).mean()
df['mean30newvaccinedoses'] = df['newvaccinedoses'].rolling(30).mean()

df['firstdose'] = SantosPopulation*df['firstdosepercent']/100
df['seconddose'] =  df['vaccinedoses'] - df['firstdose']

print('CovidSantos - Tracking COVID-19 cases in Santos, Brazil.')
print('First day: ' + firstday.strftime('%Y-%m-%d'))
print('Last day: ' + lastday.strftime('%Y-%m-%d'))

sns.set_style("whitegrid")
w = 0.5

print('creating graphic: Cases')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['cases'], label = 'cases')
#plt.xlabel('Date') 
plt.title('Casos Confirmados')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'cases.svg'), bbox_inches='tight', dpi=150)
plt.show()

print('creating graphic: New Cases')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newcases'], width = 1, color='black',label = 'Novos casos')
plt.plot(df['date'], df['mean7newcases'], label = 'Média semanal de novos casos')
plt.plot(df['date'], df['mean30newcases'], label = 'Média mensal de novos casos')
plt.plot(df['date'], df['suspectedcases'], label = 'Casos suspeitos em investigação')
#plt.xlabel('Date') 
plt.title('Novos Casos Confirmados')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
plt.legend()
fig.savefig(os.path.join(graphpath, 'newcases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Cases X Cases')
fig = plt.figure(figsize=(10,5))
plt.plot(df['cases'], df['weekcases'], label = 'newcases-cases')
plt.yscale('log')
plt.xscale('log')
#plt.xlabel('Date') 
plt.title('Novos Casos na semana X Casos Totais')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'newcasescases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: Deaths')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['deaths'], label = 'deaths')
#plt.xlabel('Date') 
plt.title('Óbitos')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'deaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Deaths')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newdeaths'], width = 1, color='black',label = 'Novos óbitos')
plt.plot(df['date'], df['mean7newdeaths'], label = 'Média semanal de novos óbitos')
plt.plot(df['date'], df['mean30newdeaths'], label = 'Média mensal de novos óbitos')
#plt.xlabel('Date') 
plt.title('Novos Óbitos Confirmados')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
plt.legend()
fig.savefig(os.path.join(graphpath, 'newdeaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Deaths X Deaths')
fig = plt.figure(figsize=(10,5))
plt.plot(df['deaths'], df['weekdeaths'], label = 'newdeaths-deaths')
plt.yscale('log')
plt.xscale('log')
#plt.xlabel('Date') 
plt.title('Novos Óbitos na semana X Óbitos Totais')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'newdeathsdeaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: Hospitalization')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['hospitalized'], label = 'Internações')
plt.plot(df['date'], df['UTI'], label = 'UTI')
#plt.xlabel('Date') 
plt.title('Internações')
plt.legend()
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'hospitalization.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: ICU Occupation')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['totalUTIoccupation'], color='black', label = 'Ocupação total')
plt.bar(date2num(df['date']), df['publicUTIoccupation'], label = 'Ocupação da UTI pública', width=w)
plt.bar(date2num(df['date']) + w, df['privateUTIoccupation'], label = 'Ocupação da UTI privada', width=w)
#plt.xlabel('Date') 
plt.axhline(90,color='red')
plt.axhline(100,color='black')
plt.title('Ocupação da UTI')
plt.legend()
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'ICUOccupation.svg'), bbox_inches='tight', dpi=150)
#plt.show()

def percentage(x):
    return x / SantosPopulation

def absolute(x):
    return x * SantosPopulation

print('creating graphic: Vaccine doses')
fig = plt.figure(figsize=(10,5))
w = 0.3
plt.plot(df['date'], df['vaccinedoses'], label = 'Doses de vacinas aplicadas')
plt.bar(date2num(df['date']), df['firstdose'], label = '1ª dose (estimativa)', width=w)
plt.bar(date2num(df['date']) + w, df['seconddose'], label = '2ª dose (estimativa)', width=w)
plt.axhline(SantosPopulation,color='black')
sec_ax = plt.gca().secondary_yaxis('right', functions=(percentage, absolute))
sec_ax.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
#plt.xlabel('Date') 
plt.title('Doses de vacinas aplicadas')
plt.legend()
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
fig.savefig(os.path.join(graphpath, 'vaccinedoses.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Vaccine doses')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newvaccinedoses'], width = 1, color='gray', alpha=0.7 ,label = 'Doses diárias aplicadas')
plt.plot(df['date'], df['mean7newvaccinedoses'], label = 'Média semanal de doses aplicadas')
plt.plot(df['date'], df['mean30newvaccinedoses'], label = 'Média mensal de doses aplicadas')
#plt.xlabel('Date') 
plt.title('Doses de vacinas aplicadas')
plt.tick_params(axis = 'both', which = 'major')
plt.figtext(0.02, 0.02, 'Atualizado em {}'.format(lastday.strftime('%d/%m/%Y')),fontsize=8)
plt.figtext(0.98, 0.02, siteURL, horizontalalignment='right',fontsize=8)
plt.legend()
fig.savefig(os.path.join(graphpath, 'newvaccinedoses.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('done')