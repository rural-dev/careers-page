from bs4 import BeautifulSoup


def cleanhtml(raw_html):
  cleantext = BeautifulSoup(raw_html, "lxml").text
  return cleantext


def clean(data):
    data_cleaned = cleanhtml(data)
    return data_cleaned

def cleannewline(data):
    data_cleaned = str(data).encode("utf-8").decode('utf-8', 'ignore')\
        .replace("\n", "")\
        .replace('\r', "")\
        .replace('\t', "")\
        .replace('&rsquo;', "’")\
        .replace('&nbsp;', " ")\
        .replace('&amp;', "&")\
        .strip()
    return data_cleaned