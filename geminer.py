#!/usr/bin/env python3

from md2gemini import md2gemini
import frontmatter
from jinja2 import Template
import os
import locale

import config

# locale (for templates, for example dates rendering)
locale.setlocale(locale.LC_ALL, config.locale)

md_path = os.path.expanduser(config.md_dir)
gmi_path = os.path.expanduser(config.gmi_dir)
tpl_path = os.path.expanduser(config.tpl_dir)

os.chdir(md_path)

def add_ext_gmi(link):
    # Custom function to apply to links
    if "://" not in link: # apply only on local links
        return link+".gmi"

# Walk through markdown directories
for dirname, subdirlist, mdlist in os.walk('.'):
    
    # Create same hierarchy in GMI directory
    gmi_subpath = os.path.abspath(gmi_path+"/"+dirname)
    os.makedirs(gmi_subpath, exist_ok=True)

    for mdfile in mdlist:
        basename, extension = os.path.splitext(mdfile)
        extension = extension[1:]
        
        # We want to ignore the file if this isn't a markdown file
        if extension not in config.md_extensions:
            print("Ignoring file {}: \"{}\" not in markdown extensions list".format(mdfile, extension))
            pass
        
        # Read the Markdown file
        with open(dirname+"/"+mdfile, 'r') as md:
            mdtext = md.read()
        
        # Parse the YAML header
        meta = frontmatter.parse(mdtext)[0]
        
        # Extract useful informations from the header
        template = meta.get("template", None)
        author = meta.get("author", None)
        date = meta.get("date", None)
        title = meta.get("title", None)
        tags = meta.get("tags", None)
        # For now, tags list must be a comma-separated string
        # TODO: make possible to list tags as a YAML list
        for item in config.replace:
            mdtext = mdtext.replace(item[0],item[1])

        # Convert the post into GMI
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
                rellink_func=add_ext_gmi,
                table_tag=config.table_tag
                )

        # Read template file
        with open(tpl_path+"/"+template+".tpl", 'r') as tpl:
            template = Template(tpl.read())
        
        # We need the relative path without the "./"
        simpledirname = dirname[2:]
        if simpledirname == "":
            path = basename
        else:
            path = simpledirname + "/" + basename
        
        # Integrate the GMI content in the template
        gmitext = template.render(
                content=gmitext,
                tags=tags,
                template=template,
                author=author,
                date=date,
                title=title,
                path=path
                )
        
        # Dirty fix a weird bug where some lines are CRLF-terminated
        gmitext = gmitext.replace('\r\n','\n')
        
        # Time to write the GMI file
        gmifile = basename
        if config.gmi_extension:
            gmifile += ".gmi"
        print(gmi_subpath+"/"+gmifile)
        with open(gmi_subpath+"/"+gmifile, 'w') as gmi:
            gmi.write(gmitext)
