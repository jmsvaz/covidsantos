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

csvfilename = os.path.join('..', 'data', 'data.csv')
graphpath = os.path.join('..', 'docs', 'img')
webfilename = os.path.join('..', 'docs', 'index.md')
lastupdatestring = 'Última atualização: '

# Read CSV file into DataFrame df
df = pd.read_csv(csvfilename, parse_dates=[0], dayfirst=True)

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

print('CovidSantos - Tracking COVID-19 cases in Santos, Brazil.')
print('First day: ' + firstday.strftime('%Y-%m-%d'))
print('Last day: ' + lastday.strftime('%Y-%m-%d'))

print('creating graphic: Cases')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['cases'], label = 'cases')
#plt.xlabel('Date') 
plt.title('Casos Confirmados')
plt.tick_params(axis = 'both', which = 'major')
fig.savefig(os.path.join(graphpath, 'cases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Cases')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newcases'], color='grey',label = 'Novos casos')
plt.plot(df['date'], df['mean7newcases'], label = 'Média semanal de novos casos')
plt.plot(df['date'], df['mean30newcases'], label = 'Média mensal de novos casos')
#plt.xlabel('Date') 
plt.title('Novos Casos Confirmados')
plt.tick_params(axis = 'both', which = 'major')
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
fig.savefig(os.path.join(graphpath, 'newcasescases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: Deaths')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['deaths'], label = 'deaths')
#plt.xlabel('Date') 
plt.title('Óbitos')
plt.tick_params(axis = 'both', which = 'major')
fig.savefig(os.path.join(graphpath, 'deaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Deaths')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newdeaths'], color='grey',label = 'Novos óbitos')
plt.plot(df['date'], df['mean7newdeaths'], label = 'Média semanal de novos óbitos')
plt.plot(df['date'], df['mean30newdeaths'], label = 'Média mensal de novos óbitos')
#plt.xlabel('Date') 
plt.title('Novos Óbitos Confirmados')
plt.tick_params(axis = 'both', which = 'major')
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
fig.savefig(os.path.join(graphpath, 'newdeathsdeaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: Hospitalization')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['hospitalizeds'], label = 'Internações')
plt.plot(df['date'], df['UTI'], label = 'UTI')
#plt.xlabel('Date') 
plt.title('Internações')
plt.legend()
plt.tick_params(axis = 'both', which = 'major')
fig.savefig(os.path.join(graphpath, 'hospitalization.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('updating website with csv update date')
with fileinput.FileInput(webfilename, inplace = True, backup ='.bak') as f:
    for line in f:
        if lastupdatestring in line:
            print(lastupdatestring + lastday.strftime('%Y-%m-%d'),end ='\n')
        else:
            print(line, end ='') 

print('done')