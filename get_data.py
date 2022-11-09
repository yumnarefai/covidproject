"""CSC110 Fall 2020 Project Final Submission
===============================

This Python module contains three dataclass definitions and several functions to read
and organize the dataset, hence presenting the foundation of our computational model
that analyses the effects of COVID19 on emissions of pollutant gases by sources and
it's respective industries.

Instructions as follows:
Please read through this file carefully and call the functions with the necessary
data at hand.

Copyright and Usage Information
===============================

This file is provided solely for the personal and private use of students
taking CSC110 at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited.

This file is Copyright (c) 2020 Ipek Akyol, Yumna Refai, Helia Sajjadian Moosavi .
"""
from dataclasses import dataclass
from datetime import datetime

import openpyxl
import pandas as pd
import python_ta

file_path = r'data.xlsx'

main_sources = ["Power plants", "Heavy industry",
                "Light industry", "Mobile sources", "Other sources"]


@dataclass
class Source:
    """
    A source of emission.

    Instance Attributes:
        - name: the name of the source of emission
        - total: the total value of the concentrations of a specific pollutant gas emitted
        by each industry within it's respective source.
        - industries: all industries that are a subset of the source
        with their co-responding pollutant value


    Representation Invariants:
        - self.name in main_sources
        - self.total >= 0
        - all(value>=0 for value in self.industries.values())
        - all(name!="" for name in self.industries.keys())

    Sample Usage:
    >>> mobile_source = Source("Mobile sources",89.0,{"Marine":78.0,"Aviation aircraft":11.0})
    >>> mobile_source.name == "Mobile sources"
    True
    """

    name: str
    total: float
    industries: dict[str, float]


@dataclass
class Pollutant:
    """
    A pollutant gas.

    Instance Attributes:
        - name: the name of pollutant gas
        - total: the sum of the concentrations of the pollutant emitted by each main source
        - sources: all sources that emitted this pollutant


    Representation Invariants:
        - self.name != ""
        - self.total >= 0
        - all(name in main_sources for name in self.sources.values())

    Sample Usage:
    >>> mobile_source = Source("Mobile sources",89.0,{"Marine":78.0,"Aviation aircraft":11.0})
    >>> so2 = Pollutant("SO2",89.0,{"Mobile sources":mobile_source})
    >>> so2.name
    'SO2'
    """
    name: str
    total: float
    sources: dict[str, Source]


@dataclass
class Day:
    """
    A day.

    Instance Attributes:
        - date: the date of the day
        - total: the total concentration of pollutants for that day
        - pollutants: all pollutants emitted for that day


    Representation Invariants:
        - self.date >= datetime(2019,1,1)
        - self.total >= 0
        - all(name != "" for name in self.pollutants.values())

    Sample Usage:
    >>> mobile_source = Source("Mobile sources",89.0,{"Marine":78.0,"Aviation aircraft":11.0})
    >>> so2 = Pollutant("SO2",89.0,{"Mobile sources":mobile_source})
    >>> day1 = Day(datetime(2019,1,1),89.0,{"SO2":so2})
    >>> day1.total
    89.0
    """
    date: datetime
    total: float
    pollutants: [str, Pollutant]


def with_openpyxl(file_name: str = file_path) -> list:
    """Return a list of lists corresponding to the excel table in the file with the file_name.
    """
    wb = openpyxl.load_workbook(file_name, data_only=True)
    sheet = wb.active
    columns = sheet.columns
    data = []
    for column in columns:
        record = []
        for cell in column:
            record.append(cell.value)
        data.append(record)
    return data


def get_organized_data(data: list) -> list[Day]:
    """Return the list of the objects with the type Day which
    summarises the whole dataset in the data list.
    """
    source = Source("", 0.0, {})
    sources = {}
    pollutants = {}
    organized_data = []
    for info in data[5:]:
        for i in range(2, len(data[0])):
            if data[2][i] == "kton":
                scale = 1000
            else:
                scale = 1
            if data[0][i] in main_sources + ["Total"]:
                if source.name != "":
                    sources[source.name] = source
                source = Source(data[0][i], info[i] * scale, {})
                if data[0][i] == "Total":
                    pollutant = Pollutant(data[1][i], info[i] * scale, sources)
                    pollutants[pollutant.name] = pollutant
                    sources = {}
            else:
                source.industries[data[0][i]] = info[i] * scale
        t = sum([pollutants[pollutant].total for pollutant in pollutants])
        day = Day(info[1], t, pollutants)
        organized_data.append(day)
        pollutants = {}
    return organized_data


def get_data_for_linear_regression(dataset: list[Day], pollutant: str) -> pd.DataFrame:
    """ Return a pandas Data Frame that contains the value of
    the given pollutants total emission in each day.
    """
    first_day = datetime(2019, 1, 1)
    data = {"day": [], "total": []}
    for day in dataset:
        data["day"].append((day.date - first_day).days)
        data["total"].append(day.pollutants[pollutant].total)
    return pd.DataFrame.from_dict(data)


def get_total_per_source(dataset: list[Day]) -> dict[str, tuple[float, float]]:
    """ Return a dictionary that maps each source of emission to the corresponding
    value of the total pollutants emission for that source in 2019 (before Covid)
    and 2020 (during Covid).
    """
    data = {}
    for source in main_sources:
        total_2019 = 0
        total_2020 = 0
        for day in dataset:
            if day.date.year == 2019:
                for p in day.pollutants.values():
                    total_2019 += p.sources[source].total
            else:
                for p in day.pollutants.values():
                    total_2020 += p.sources[source].total
        data[source] = (total_2019, total_2020)
    return data


def get_total_per_industry(dataset: list[Day]) -> dict[str, tuple[float, float]]:
    """ Return a dictionary that maps each industry to the corresponding
    value of total pollutants emission for that industry in 2019 (before Covid)
    and 2020 (during Covid).
        """
    data = {}
    all_industries = {}
    for source in main_sources:
        for ind in dataset[0].pollutants["SO2"].sources[source].industries.keys():
            all_industries[ind] = source
    for industry in all_industries:
        total_2019 = 0
        total_2020 = 0
        for day in dataset:
            if day.date.year == 2019:
                for p in day.pollutants.values():
                    total_2019 += p.sources[all_industries[industry]].industries[industry]
            else:
                for p in day.pollutants.values():
                    total_2020 += p.sources[all_industries[industry]].industries[industry]
        data[industry] = (total_2019, total_2020)
    return data


def get_data_for_pie_chart_source(dataset: list[Day]) -> pd.DataFrame:
    """Return a pandas Data Frame that contains the weighted decrease of total pollutant
    emission for each source.
    """
    data = {}
    filtered_data = get_total_per_source(dataset)
    for source in filtered_data:
        data[source] = abs((filtered_data[source][0] - filtered_data[source][1])
                           / filtered_data[source][1])
    return pd.DataFrame.from_dict(data, orient='index')


def get_data_for_pie_chart_industry(dataset: list[Day]) -> pd.DataFrame:
    """Return a pandas Data Frame that contains the weighted decrease of total pollutant
        emission for each industry.
    """
    data = {}
    filtered_data = get_total_per_industry(dataset)
    for industry in filtered_data:
        data[industry] = abs((filtered_data[industry][0] - filtered_data[industry][1])
                             / filtered_data[industry][1])
    return pd.DataFrame.from_dict(data, orient='index')


def get_data_for_pie_chart_mobile(dataset: list[Day]) -> pd.DataFrame:
    """Return a pandas Data Frame that contains the weighted decrease of each pollutant
    emission for the mobile source which was the most impacted source by covid-19.
    """
    data = {}
    for p in dataset[0].pollutants:
        total_2019 = 0
        total_2020 = 0
        for day in dataset:
            if day.date.year == 2019:
                total_2019 += day.pollutants[p].sources["Mobile sources"].total
            else:
                total_2020 += day.pollutants[p].sources["Mobile sources"].total
        data[p] = abs((total_2020 - total_2019)
                      / total_2019)
    return pd.DataFrame.from_dict(data, orient='index')


def get_data_for_bar_source(dataset: list[Day]) -> pd.DataFrame:
    """ Return a Pandas Data Frame that contains the value of total pollutants emission
    for each source in 2019 (before Covid) and 2020 (during Covid).
    """
    data = get_total_per_source(dataset)
    year_2019 = [data[source][0] for source in data]
    year_2020 = [data[source][1] for source in data]
    sources = data.keys()
    return pd.DataFrame({'2019': year_2019, '2020': year_2020}, index=sources)


def get_data_for_bar_industry(dataset: list[Day]) -> pd.DataFrame:
    """ Return a Pandas Data Frame that contains the value of total pollutants emission
    for each industry in 2019 (before Covid) and 2020 (during Covid)
    """
    data = get_total_per_industry(dataset)
    year_2019 = [data[ind][0] for ind in data]
    year_2020 = [data[ind][1] for ind in data]
    industries = data.keys()
    return pd.DataFrame({'2019': year_2019, '2020': year_2020}, index=industries)


python_ta.check_all(config={
    'extra-imports': ["pandas", "openpyxl", "datetime"],  # the names (strs) of imported modules
    'allowed-io': [],  # the names (strs) of functions that call print/open/input
    'max-line-length': 100,
    'disable': ['R1705', 'C0200']
})
