#!/usr/bin/env python
import json
from itertools import product

from mdutils.mdutils import MdUtils
import yaml


def parse_resume():
    with open('resume.yaml') as resume_file:
        return yaml.load(resume_file, Loader=yaml.FullLoader)


def create_md_file(resume):
    md_file = MdUtils(file_name='index.md', title=resume['about_me']['name'])

    md_file.new_header(level=1, title='About me')
    md_file.new_header(level=2, title='Description')
    for line in resume['about_me']['description'].splitlines(keepends=True):
        md_file.new_line(line)
    md_file.new_header(level=2, title='Contact')
    for media, url in resume['about_me']['contact'].items():
        md_file.new_line(f'[{media}]({url})')

    md_file.new_header(level=2, title='Studies')
    md_file.new_header(level=2, title='Career')
    md_file.new_header(level=2, title='Projects')

    md_file.create_md_file()


if __name__ == '__main__':
    resume = parse_resume()
    #print(json.dumps(resume, indent=2))
    create_md_file(resume)
