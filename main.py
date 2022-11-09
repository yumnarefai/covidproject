"""CSC110 Fall 2020 Project Final Submission
===============================

Main module: This module consists of a main block of the code necessary to
run our entire program from start to finish.

Instructions:
Uncomment the following code one by one.
For the first chunk of code, we intend to fit a linear regression model using a scatter plot
for the different pollutant gases.

For the next chunk of code, we look at the pie chart and bar chart of sources which presents which source
was affected the most/least during Covid19. Look at the source with the greatest/least
percentage decrease using the pie chart and see the bar plots to see the change in the total pollutant gas
emissions between 2019 (before Covid) and 2020 (during Covid).

We look at the pie chart and bar chart of industries within these sources to find out which industry
was affected the most/least during Covid19. Look at the bar plot and see which has the largest/smallest
wedge and compare your intuitive analysis to the data about the change in total pollutant gas emissions
 from each industry in the bar plot between 2019 (before Covid) and 2020 (during Covid).

From our sources bar plot and pie chart, it is clear that mobile sources was most impacted by Covid 19 so
we made another pie chart to address our final question from our introduction to see how and which
pollutant gases decreased most significantly due to Covid19.

The last chunk of code highlights how the data is used to derive the total emissions of all the pollutant
gases per source and the total emissions of all the pollutant gases per industry within each source.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult our Course Syllabus.

This file is Copyright (c) 2020 Ipek Akyol, Yumna Refai, Helia Sajjadian Moosavi .
"""
import get_data
import visualisation_functions

data = get_data.get_organized_data(get_data.with_openpyxl())

#visualisation_functions.draw_linear_regression("CO")
#visualisation_functions.draw_linear_regression("CO2")
#visualisation_functions.draw_linear_regression("NOx")
#visualisation_functions.draw_linear_regression("SO2")
#visualisation_functions.draw_linear_regression("NMVOCs")
#visualisation_functions.draw_linear_regression("PM2.5")
#visualisation_functions.draw_linear_regression("BC")
#visualisation_functions.draw_linear_regression("OC")

# visualisation_functions.draw_pie_chart_source()
# visualisation_functions.draw_bar_plot_source()
# visualisation_functions.draw_pie_chart_industry()
#visualisation_functions.draw_bar_plot_industry()
#visualisation_functions.draw_pie_chart_mobile()

#get_data.get_total_per_source(data)
get_data.get_total_per_industry(data)
