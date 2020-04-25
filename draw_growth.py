from datetime import datetime

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

FIRST_DATE = datetime(2020, 1, 22)  # Don't modify this value
# url = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv'
url = 'time_series_covid19_confirmed_global.csv'

global_data = pd.read_csv(url, index_col=0)
global_data.head()

global_data_summed = global_data.groupby('Country/Region').sum()
df = global_data_summed.drop(['Lat', 'Long'],
                             axis=1).reset_index()  # Doesn't make sense to keep Lat/Long after dataframe has been summed

countries_to_plot = ['Sri Lanka', 'Australia']
# US Date format: 'MM/DD/YYYY'
start_date = '01/27/2020'
end_date = '{}20'.format(df.columns[-1])


def get_index_from_date(date_string):
    date_list = [int(x) for x in date_string.split('/')]
    date_object = datetime(date_list[-1], date_list[0], date_list[1])

    return (date_object - FIRST_DATE).days


dates = list(df)[1:]

start_index = get_index_from_date(start_date)
end_index = get_index_from_date(end_date)
x_values = dates[start_index:end_index + 1]

country_dict = {}
plt.figure(1)
for country in countries_to_plot:
    country_df = df[df['Country/Region'] == country]
    y_values = [int(country_df[col]) for col in x_values]
    country_dict[country] = y_values
    plt.plot(x_values, y_values, label=country)

plt.title('Confirmed Cases Over Time')
skip = max(len(x_values) // 5, 1)  # Helps ensure we don't add too many date tick marks
plt.xticks(x_values[::skip])
plt.xlabel("Date (MM/DD/YY)")
plt.ylabel("# of Confirmed Cases")
plt.legend()
plt.grid()
plt.savefig('covid_confirmed.png', dpi=400)
# plt.show()

plt.figure(2)
skip = max(len(x_values) // 12, 1)
colours = ['blue', 'orange']
fig, axes = plt.subplots(2, 1)
new_dates = []

for idx, country in enumerate(countries_to_plot):
    total_num_cases = country_dict.get(country)
    new_cases_in_ = []
    for i, total_cases in enumerate(total_num_cases):
        new_dates.append(x_values[i])
        if i < 7:
            new_cases_in_.append(total_cases)
        else:
            new_cases_in_.append(total_cases - total_num_cases[i - 7])
    axes[idx].plot(total_num_cases, new_cases_in_, label=country, c=colours[idx])
    axes[idx].set_title(country, fontsize=12)
    axes[idx].grid()

    ax2 = axes[idx].twiny()
    ax2.plot(total_num_cases[::skip], np.zeros_like(total_num_cases[::skip]), alpha=0)  # Create a dummy plot
    ax2.set_xticks(total_num_cases[::skip])
    ax2.set_xticklabels(x_values[::skip])
    ax2.xaxis.set_tick_params(rotation=45)
    ax2.xaxis.set_ticks_position('top')

for ax in axes.flat:
    ax.set(xlabel='Total confirmed cases', ylabel="New cases (past 7 days)")


plt.suptitle('Trajectory of COVID-19 confirmed cases', fontsize=12)

fig.tight_layout()
plt.subplots_adjust(top=0.75)
plt.savefig('covid_growth.png', dpi=400)
# plt.show()
