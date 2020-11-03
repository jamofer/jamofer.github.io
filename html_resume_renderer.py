from datetime import datetime


def create_html_file(resume):
    html_file = HtmlFile(file_name='index.html', title=resume['about_me']['name'])

    html_file.add_element(f'<h1>{resume["about_me"]["name"]}</h1><h3>Software Developer</h3></br>')

    _about_me(html_file, resume)
    _career(html_file, resume)
    _studies(html_file, resume)
    _projects(html_file, resume)

    html_file.create_file()


def _about_me(html_file, resume):
    header = HeaderElement(
        resume['about_me']['photo_url'],
        resume['about_me']['from'],
        resume['about_me']['date_of_birth'],
        resume['about_me']['contact']
    )
    about = AboutMeElement('About me', resume['about_me']['description'])
    html_file.add_element(about, header)


def _studies(html_file, resume):
    timeline_studies = []
    for study in resume['studies']:
        timeline_studies.append(TimelineElement(
            title=study['title'] + '. ' + study['college'],
            start_date=study['start_date'],
            end_date=study['end_date'],
            text=_project(study['project']),
        ))
    html_file.add_element(TimelineElements('Studies', timeline_studies))


def _project(project):
    return f'Final degree project: <a href="{project["url"]}">{project["title"]}</a>.<br>{project["notes"]}'


def _career(html_file, resume):
    timeline_studies = []
    for career in resume['career']:
        timeline_studies.append(TimelineElement(
            title=f"{career['company']}. {career['position']}",
            start_date=career['start_date'],
            end_date=career['end_date'],
            text=career['description'],
            url=career['url'] or '#',
            keywords=career['keywords']
        ))
    html_file.add_element(TimelineElements('Career', timeline_studies))


def _projects(html_file, resume):
    timeline_studies = []
    for project in resume['projects']:
        timeline_studies.append(TimelineElement(
            title=project['title'],
            start_date=project['date'],
            text=project['description'],
            url=project['url'],
            keywords=project['keywords']
        ))
    html_file.add_element(TimelineElements('Projects', timeline_studies))


class HeaderElement(object):
    def __init__(self, photo, location, date_of_birth, contact):
        self.date_of_birth = date_of_birth
        self.location = location
        self.photo = photo
        self.contact = contact

    def __str__(self):
        linkedin = f'<i class="fa fa-linkedin contact"></i>{self.contact["linkedin"]["name"]}'
        github = f'<i class="fa fa-github contact"></i>{self.contact["github"]["name"]}'
        email = f'<i class="fa fa-envelope contact"></i>{self.contact["email"]["name"]}'
        phone = f'<i class="fa fa-phone contact"></i>{self.contact["phone"]["name"]}'

        location = f'<i class="fa fa-home contact"></i>{self.location}'
        birth = f'<i class="fa fa-birthday-cake contact"></i>{self.date_of_birth}'

        return (
            '<div class="left-bar">' +
            f'<img class="photo contact" src="{self.photo}"></img>' +
            f'<a class="contact" href="#" >{location}</a>' +
            f'<a class="contact" href="#" >{birth}</a>' +
            '<hr class="contact" />' +
            f'<a class="contact" href="{self.contact["phone"]["url"]}" >{phone}</a>' +
            f'<a class="contact" href="mailto:{self.contact["email"]["url"]}" >{email}</a>' +
            f'<a class="contact" href="{self.contact["linkedin"]["url"]}" >{linkedin}</a>' +
            f'<a class="contact" href="{self.contact["github"]["url"]}" >{github}</a>'
            '</div>'
        )


class AboutMeElement(object):
    def __init__(self, title, description):
        self.title = title
        self.description = description

    def __str__(self):
        lines = [f'<p>{line}</p>' for line in self.description.splitlines()]
        return f'<h2>{self.title}</h2>{"".join(lines)}'


class TimelineElements(object):
    def __init__(self, title, timelines):
        self.title = title
        self.timelines = timelines

    def __str__(self):
        timelines = [f'<li>\n{timeline}\n</li>' for timeline in self.timelines]
        return f'<h2>{self.title}</h2><ul class="timeline">{"".join(timelines)}</ul>'


class TimelineElement(object):
    def __init__(self, title, text, start_date, end_date='', url='#', keywords=None):
        self.url = url
        self.keywords = keywords
        self.title = title
        self.text = text
        self.start_date = start_date
        self.end_date = end_date

    @property
    def date(self):
        start_date = self.start_date
        if is_valid_date(self.start_date):
            start_date = datetime.strptime(self.start_date, "%m-%Y").strftime("%B, %Y")

        end_date = self.end_date
        if is_valid_date(self.end_date):
            end_date = datetime.strptime(self.end_date, "%m-%Y").strftime("%B, %Y")

        if end_date:
            return f'{end_date}</br>{start_date}'

        return start_date

    def __str__(self):
        badges = []
        if self.keywords:
            badges = [f'<span class="badge badge-secondary">{keyword}</span>' for keyword in self.keywords]
        return (
            f'<a target="_blank" href="{self.url}">{self.title}</a>'
            f'<a href="#" class="date">{self.date}</a>'
            f'<p>{self.text}'
            f'{" ".join(badges)}</p>'
        )


class HtmlFile(object):
    def __init__(self, file_name, title):
        self.file_name = file_name
        self.title = title
        self.elements = []

    @property
    def html(self):
        return HTML_ENCLOSURE.format(content=HEADER.format(title=self.title) + self.body)

    @property
    def body(self):
        return (
            '<body>\n<div class="container-md">\n' +
            '\n'.join(self.elements) +
            '</div>\n</body>'
        )

    def add_element(self, right_element='', left_element=''):
        self.elements.append(ELEMENT_ENCLOUSRE.format(right=right_element, left=left_element))

    def create_file(self):
        with open(self.file_name, 'w', encoding='UTF-8') as html_file:
            html_file.write(self.html)


def is_valid_date(date_string):
    try:
        datetime.strptime(date_string, "%m-%Y")
    except:
        return False

    return True


HEADER = '''<head>
  <meta charset="UTF-8">
  <title>{title}</title>
  <link href="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/css/bootstrap.min.css" rel="stylesheet" id="bootstrap-css">
  <link href="style.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">
  <script src="//cdnjs.cloudflare.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
  <script src="//maxcdn.bootstrapcdn.com/bootstrap/4.1.1/js/bootstrap.min.js"></script>
</head>
'''

HTML_ENCLOSURE = '''<!DOCTYPE html>
<html lang="en">
{content}
</html>
'''


ELEMENT_ENCLOUSRE = '''<div class="row">
<div class="col-sm-2">
{left}
</div>
<div class="col-sm-8">
{right}
</div>
</div>
'''
