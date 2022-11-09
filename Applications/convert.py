from dataclasses import dataclass
from datetime import datetime
import openpyxl
import pandas as pd

root = r'/Users/helia/Desktop/uoft/2020/csc110/project/data.xlsx'

main_sources = ["Power plants", "Heavy industry",
                "Light industry", "Mobile sources", "Other sources"]

@dataclass
class Source:
    """
    A source of emission

    Attributes:
      - name: the name of source of emission
      - total: the total value of the concentrations of pollutant emitted
      by each industry within the source for a specific pollutant

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
    A pollutant gas

    Attributes:
      - name: the name of pollutant
      - total: the sum of the concentrations of the pollutant emitted by each main source
      - sources: all sources that produced this pollutant


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
    A day

    Attributes:
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


def with_openpyxl(file_name: str = root) -> list:
    """Return list of list co-responding to the exel table in the file with the file_name.
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
    summerises the whole dataset in the data list.
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
    """
    Return a pandas Data Frame that contains the value of
    the given pollutants total emission in each day
    """
    first_day = datetime(2019, 1, 1)
    data = {"day": [], "total": []}
    for day in dataset:
        data["day"].append((day.date - first_day).days)
        data["total"].append(day.pollutants[pollutant].total)
    return pd.DataFrame.from_dict(data)


def get_total_per_source(dataset) -> dict[str, tuple[float, float]]:
    """ Return a dictionary that maps each source of emission to
    the co-responding value of total pollutants emission for that source in 2019 and 2020
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


def get_total_per_industry(dataset) -> dict[str, tuple[float, float]]:
    """ Return a dictionary that maps each industry to the co-responding
    value of total pollutants emission for that industry in 2019 and 2020
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


def get_data_for_pie_chart_source(dataset):
    """Return a pandas Data Frame that contains the weighted decrease of total pollutant
    emission for each source.
    """
    data = {}
    filtered_data = get_total_per_source(dataset)
    for source in filtered_data:
        data[source] = abs((filtered_data[source][0] - filtered_data[source][1])
                           / filtered_data[source][1])
    return pd.DataFrame.from_dict(data, orient='index')


def get_data_for_pie_chart_industry(dataset):
    """Return a pandas Data Frame that contains the weighted decrease of total pollutant
        emission for each industry.
        """
    data = {}
    filtered_data = get_total_per_industry(dataset)
    for industry in filtered_data:
        data[industry] = abs((filtered_data[industry][0] - filtered_data[industry][1])
                             / filtered_data[industry][1])
    return pd.DataFrame.from_dict(data, orient='index')

def get_data_for_pie_chart_mobile(dataset):
    """Return a pandas Data Frame that contains the weighted decrease each pollutant
    emission for the mobilty source which was the most impacted source by covid-19.
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


def get_data_for_bar_source(dataset):
    """
    Return a Pandas Data Frame that contains the value of total pollutants emission
    for each source in 2019(before covid) and 2020(after covid)
    """
    data = get_total_per_source(dataset)
    year_2019 = [data[source][0] for source in data]
    year_2020 = [data[source][1] for source in data]
    sources = [source for source in data]
    return pd.DataFrame({'2019': year_2019, '2020': year_2020}, index=sources)


def get_data_for_bar_industry(dataset):
    """
    Return a Pandas Data Frame that contains the value of total pollutants emission
    for each industry in 2019(before covid) and 2020(after covid)
    """
    data = get_total_per_industry(dataset)
    year_2019 = [data[ind][0] for ind in data]
    year_2020 = [data[ind][1] for ind in data]
    industries = [ind for ind in data]
    return pd.DataFrame({'2019': year_2019, '2020': year_2020}, index=industries)


x = get_organized_data(with_openpyxl())

# get_data_for_pie_chart_industry(x).plot.pie(subplots=True,legend = None)
# get_data_for_pie_chart_source(x).plot.pie(subplots=True,legend = None)
# get_data_for_pie_chart_mobile(x).plot.pie(subplots=True, legend = None)
# get_data_for_bar_industry(x).plot.bar()
# get_data_for_bar_source(x).plot.bar()
