#!/usr/bin/env python
import yaml

import html_resume_renderer
import markdown_resume_renderer


def parse_resume():
    with open('resume.yaml') as resume_file:
        return yaml.load(resume_file, Loader=yaml.FullLoader)


if __name__ == '__main__':
    resume = parse_resume()
    markdown_resume_renderer.create_md_file(resume)
    html_resume_renderer.create_html_file(resume)
