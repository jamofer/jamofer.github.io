from mdutils import MdUtils


def create_md_file(resume):
    md_file = MdUtils(file_name='index.md', title=resume['about_me']['name'])

    _about_me(md_file, resume)
    _studies(md_file, resume)
    _career(md_file, resume)
    _projects(md_file, resume)

    md_file.create_md_file()


def _projects(md_file, resume):
    md_file.new_header(level=1, title='Projects')
    for project in resume['projects']:
        md_file.new_line(project['title'])


def _career(md_file, resume):
    md_file.new_header(level=1, title='Career')
    for career in resume['career']:
        md_file.new_line(career['company'])


def _studies(md_file, resume):
    md_file.new_header(level=1, title='Education')
    for study in resume['education']:
        md_file.new_line(study['title'])


def _about_me(md_file, resume):
    md_file.new_header(level=1, title='About me')
    _description(md_file, resume)
    _contact(md_file, resume)


def _contact(md_file, resume):
    md_file.new_header(level=2, title='Contact')
    for media, url in resume['about_me']['contact'].items():
        md_file.new_line(f'[{media}]({url})')


def _description(md_file, resume):
    md_file.new_header(level=2, title='Description')
    md_file.write('<img style="float: left;" src="photo2.jpg">')
    for line in resume['about_me']['description'].splitlines(keepends=True):
        md_file.new_line(line)
