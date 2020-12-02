#!/usr/bin/env python3

from md2gemini import md2gemini
import frontmatter
from jinja2 import Template
import os

import config

md_path = os.path.expanduser(config.md_dir)
gmi_path = os.path.expanduser(config.gmi_dir)
tpl_path = os.path.expanduser(config.tpl_dir)

os.chdir(md_path)

for dirname, subdirlist, mdlist in os.walk('.'):
    gmi_subpath = os.path.abspath(gmi_path+"/"+dirname)
    os.makedirs(gmi_subpath, exist_ok=True)
    for mdfile in mdlist:
        basename, extension = os.path.splitext(mdfile)
        extension = extension[1:]
        if extension not in config.md_extensions:
            print("Ignoring file {}: \"{}\" not in markdown extensions list".format(mdfile, extension))
            pass
        with open(dirname+"/"+mdfile, 'r') as md:
            mdtext = md.read()
        meta = frontmatter.parse(mdtext)[0]
        template = meta.get("template", None)
        author = meta.get("author", None)
        date = meta.get("date", None)
        title = meta.get("title", None)
        tags = meta.get("tags", None)
        for item in config.replace:
            mdtext = mdtext.replace(item[0],item[1])
        gmitext = md2gemini(mdtext,
                code_tag=config.code_tag,
                img_tag=config.img_tag,
                indent=config.indent,
                ascii_table=config.ascii_table,
                frontmatter=True,
                links=config.links,
                plain=config.plain,
                strip_html=config.strip_html,
                base_url=config.base_url,
                md_links=True,
                table_tag=config.table_tag
                )
        with open(tpl_path+"/"+template+".tpl", 'r') as tpl:
            template = Template(tpl.read())
        simpledirname = dirname[2:]
        if simpledirname == "":
            path = basename
        else:
            path = simpledirname + "/" + basename
        gmitext = template.render(
                content=gmitext,
                tags=tags,
                template=template,
                author=author,
                date=date,
                title=title,
                path=path
                )
        gmitext = gmitext.replace('\r\n','\n')
        gmifile = basename
        if config.gmi_extension:
            gmifile += ".gmi"
        print(gmi_subpath+"/"+gmifile)
        with open(gmi_subpath+"/"+gmifile, 'w') as gmi:
            gmi.write(gmitext)
