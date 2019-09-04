from collections import defaultdict
from bs4 import BeautifulSoup, Tag
import pandas as pd
import requests
import re
import json
import datetime

BASE_URL = 'http://www.columbia.edu'

def subjUrl(letter):
    return BASE_URL + '/cu/bulletin/uwb/sel/subj-{}.html'.format(letter)

def getSubjects(letter):
    r = requests.get(subjUrl(letter))
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.table
    rows = table.find_all('tr')[3:-2]
    return rows

subjPattern = re.compile('subj\/(\w{4})')
def getSubjectFromPath(p):
    matches = subjPattern.findall(p)
    if len(matches) == 0:
        return None
    return matches[0]

def parseForSection(contents):
    components = contents[2].contents
    section = {
         'number': contents[0].a.string.replace('Section ', ''),
    }
    header = None
    for component in components:
        if header is not None:
            text = component.strip()
            try:
                text = int(text)
            except ValueError:
                pass # This is expected since not all values are integers (e.g. instructor names)
            section[header] = text
            header = None
        if isinstance(component, Tag) and component.name == 'b':
            header = component.string.replace(':', '').strip()
    return section

CODE_PATTERN = re.compile(r'[A-Z]{1,2}\d{4}')
def getCoursesFromPath(p):
    r = requests.get(BASE_URL + p)
    r.raise_for_status()
    soup = BeautifulSoup(r.text, 'lxml')
    subject = getSubjectFromPath(p)
    course = None
    courseNumber = None
    courses = []
    for tr in soup.table.find_all('tr')[2:-1]:
        if tr.td.get('colspan') is not None:
            course = tr.td.b.contents[-1]
            courseNumber = CODE_PATTERN.search(tr.td.b.contents[0])
            if courseNumber is not None:
                courseNumber = courseNumber.group()
            continue
        section = parseForSection(tr.contents)
        section['course'] = course
        section['courseNumber'] = courseNumber
        section['subject'] = subject
        courses.append(section)
    return courses

def now(hours=True):
    f_string = '%Y-%m-%d'
    if hours:
        f_string += 'T%H:%M:%S'
    return datetime.datetime.now().strftime(f_string)

def main(semester):
    paths = []
    for c in range(65, 91):
        rows = getSubjects(chr(c))
        for row in rows:
            anchors = row.findAll('a')
            for a in anchors:
                href = a['href']
                if 'subj/AU' in href: # auditing
                    break
                if '__' in href: # seemingly invalid subjects
                    continue
                if semester not in href:
                    continue
                paths.append(href)

    print(f'Following {len(paths)} paths...')

    courses = []
    for p in paths:
        courses += getCoursesFromPath(p)

    print(f'Scanned {len(courses)} courses.')

    with open(f'archive-{semester}/{now()}.json', 'w') as f:
        f.write(json.dumps(courses))

if __name__ == '__main__':
    main('Fall2019')
    # main('Spring2019')

