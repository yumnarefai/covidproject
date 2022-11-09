""" CSC110 Fall 2020 Project Final Submission
===============================

This Python module contains several functions to visualize the results
of our research questions. We intend to look at the visualisations
such as pie charts and bar plots to explore these questions.

Instructions as follows:
Import the following libraries and call each functions separately to
obtain the respective pie charts and bar plots.


Copyright and Usage Information
===============================
This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Ipek Akyol, Yumna Refai, Helia Sajjadian Moosavi .
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import python_ta
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split

import get_data

data = get_data.get_organized_data(get_data.with_openpyxl())


def draw_pie_chart_source() -> None:
    """ Draws a pie chart that compares the weighted decrease of emission for each source.
    """
    get_data.get_data_for_pie_chart_source(data).plot.pie(autopct='%1.0f%%', subplots=True)
    plt.title('Weighted Decrease in Pollutant Emissions by Each Source')
    plt.legend(title='Types of Sources', bbox_to_anchor=(0.9, 0.3), loc='best')


def draw_bar_plot_source() -> None:
    """ Draws a bar plot that shows the total of all the pollutant gases
    emitted by each source in 2019(before Covid) and in 2020 (during Covid).
    """
    get_data.get_data_for_bar_source(data).plot.bar()
    plt.xticks(fontsize=8, rotation=10)
    plt.xlabel('Type of Sources', fontsize=8)
    plt.ylabel('Total of All the Pollutant Gases Emitted (tons)', fontsize=8)
    plt.title('Total of all the pollutant gases emitted by each source before and during Covid',
              fontsize=8)
    plt.legend(title='Before Covid (2019) vs During Covid (2020)', bbox_to_anchor=(0.6, 0.6), loc='best',
               title_fontsize=8)


def draw_pie_chart_industry() -> None:
    """ Draws a pie chart that compares the weighted decrease of emission for each industry.
    """
    p = get_data.get_data_for_pie_chart_industry(data)
    industries_of_sources = list(p.index.values)
    p.plot.pie(subplots=True, labels=None)
    plt.legend(fontsize=5, bbox_to_anchor=(0.1, 0.6), loc='best', labels=industries_of_sources,
               title='Industries of Sources')
    plt.tight_layout()
    plt.title('Weighted decrease of emission for each industry')


def draw_bar_plot_industry() -> None:
    """ Draws a bar plot that shows the total of all the pollutant gases emitted by
    each source in 2019(before Covid) and in 2020 (during Covid)
    """
    get_data.get_data_for_bar_industry(data).plot.bar()
    plt.xticks(fontsize=6)
    plt.xlabel('Type of Industries', fontsize=8)
    plt.tight_layout()
    plt.ylabel('Total of All the Pollutant Gases Emitted (tons)', fontsize=6)
    plt.title('Total of all the pollutant gases emitted by each industry before and during Covid',
              fontsize=8)
    plt.legend(title='Before Covid (2019) vs During Covid (2020)', bbox_to_anchor=(0.5, 0.6),
               loc='best', title_fontsize=8)


def draw_pie_chart_mobile() -> None:
    """ Draws a pie chart that compares the weighted decrease of emission for each pollutant
    produced by mobile sources (which was found to be the most affected source during Covid19)
    """
    q = get_data.get_data_for_pie_chart_mobile(data)
    pollutants_gases = (list(q.index.values))
    q.plot.pie(autopct='%1.0f%%', subplots=True, labels=None)
    plt.legend(fontsize=5, bbox_to_anchor=(0.1, 0.6), loc='best', labels=pollutants_gases, title='Types of Pollutants')
    plt.title('The Weighted decrease of emission for each pollutant produced by Mobile Sources', fontsize=8)


def draw_linear_regression(pollutant: str) -> None:
    """ Draws a linear regression model for the given pollutant.
    (Disclaimer:- This has failed because the graph took a quadratic shape instead of linear).
    Please see our limitations for more information.

    Preconditions:
      - pollutant in {"CO","CO2","SO2","NOx","NMVOCs","PM2.5","BC","OC"}
    """

    df = get_data.get_data_for_linear_regression(data, pollutant)

    print(df)
    print(type(df))

    df.plot(x='day', y='total', style='o')
    np.polyfit(x=df["day"], y=df["total"], deg=1)
    plt.title('Predicting trends in emissions during Covid')
    plt.xlabel('Time (Days)')
    plt.ylabel('Total Pollutant Emissions (tons)')
    plt.show()

    x = df.iloc[:, :-1].values  # we use -1 as range since we want our attribute to contain all the columns
    # except the last one i.e. total - this means x = day [first column at index 0]
    y = df.iloc[:, 1].values  # we use 1 as it is the index at 1 which contains data on total so y = total

    # we use the training data to fit the model and then make predictions by feeding new data into the model
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=0)

    regressor = LinearRegression()
    regressor.fit(x_train, y_train)  # training the algorithm

    print(regressor.intercept_)  # getting the intercept

    print(regressor.coef_)  # getting the slope parameter

    y_pred = regressor.predict(x_test)

    df = pd.DataFrame({'Actual': y_test.flatten(), 'Predicted': y_pred.flatten()})
    print(df)


python_ta.check_all(config={
    'extra-imports': ["matplotlib.pyplot", "numpy", "sklearn.linear_model",
                      "sklearn.model_selection", "random", "pandas", "get_data"],
    'allowed-io': ["draw_linear_regression"],  # the names (strs) of functions that call print/open/input
    'max-line-length': 200,
})
