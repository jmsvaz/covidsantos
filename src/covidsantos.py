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
import pandas as pd
import matplotlib.pyplot as plt

csvfilename = os.path.join('..', 'data', 'data.csv')
graphpath = os.path.join('..', 'docs', 'img')

# Read CSV file into DataFrame df
df = pd.read_csv(csvfilename, parse_dates=[0], dayfirst=True)

# get the first day of the dataset a compute a new column with from the date minus the first date
firstday = df['date'].min()
lastday = df['date'].max()
df['days']=df['date'] - firstday

df['newcases'] = df['cases'] - df['cases'].shift(1, fill_value=0)
df['meannewcases'] = df['newcases'].rolling(7).mean()
df['weekcases'] = df['newcases'].rolling(7).sum()

df['newdeaths'] = df['deaths'] - df['deaths'].shift(1, fill_value=0)
df['meannewdeaths'] = df['newdeaths'].rolling(7).mean()
df['weekdeaths'] = df['newdeaths'].rolling(7).sum()

print('First day: ' + str(firstday))
print('First day: ' + str(lastday))

print('creating graphic: Cases')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['cases'], label = 'cases')
#plt.xlabel('Date') 
plt.title('Casos Confirmados')
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'cases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Cases')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newcases'], color='grey')
plt.plot(df['date'], df['meannewcases'], label = 'meannewcases')
#plt.xlabel('Date') 
plt.title('Novos Casos Confirmados')
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'newcases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Cases X Cases')
fig = plt.figure(figsize=(10,5))
plt.plot(df['cases'], df['weekcases'], label = 'newcases-cases')
plt.yscale('log')
plt.xscale('log')
#plt.xlabel('Date') 
plt.title('Novos Casos na semana X Casos Totais')
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'newcasescases.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: Deaths')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['deaths'], label = 'deaths')
#plt.xlabel('Date') 
plt.title('Óbitos')
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'deaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Deaths')
fig = plt.figure(figsize=(10,5))
plt.bar(x=df['date'], height=df['newdeaths'], color='grey')
plt.plot(df['date'], df['meannewdeaths'], label = 'meannewdeaths')
#plt.xlabel('Date') 
plt.title('Novos Óbitos Confirmados')
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'newdeaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: New Deaths X Deaths')
fig = plt.figure(figsize=(10,5))
plt.plot(df['deaths'], df['weekdeaths'], label = 'newdeaths-deaths')
plt.yscale('log')
plt.xscale('log')
#plt.xlabel('Date') 
plt.title('Novos Óbitos na semana X Óbitos Totais')
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'newdeathsdeaths.svg'), bbox_inches='tight', dpi=150)
#plt.show()

print('creating graphic: Hospitalization')
fig = plt.figure(figsize=(10,5))
plt.plot(df['date'], df['hospitalizeds'], label = 'Internações')
plt.plot(df['date'], df['UTI'], label = 'UTI')
#plt.xlabel('Date') 
plt.title('Internações')
plt.legend()
plt.tick_params(axis = 'both', which = 'major' , labelsize = 16)
fig.savefig(os.path.join(graphpath, 'hospitalization.svg'), bbox_inches='tight', dpi=150)
#plt.show()