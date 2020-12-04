#!/usr/bin/env python3

from md2gemini import md2gemini
import frontmatter
from slugify import slugify
from jinja2 import Template
import os
import locale
from datetime import datetime

import config

# locale (for templates, for example dates rendering)
locale.setlocale(locale.LC_ALL, config.locale)

md_path = os.path.expanduser(config.md_dir)
gmi_path = os.path.expanduser(config.gmi_dir)
tpl_path = os.path.expanduser(config.tpl_dir)
meta_path = os.path.expanduser(config.meta_dir)

# Initiate meta lists
posts = []
tags = {}
authors = {}

os.chdir(md_path)

def add_ext_gmi(link):
    # Custom function to apply to links
    if "://" not in link: # apply only on local links
        return link+".gmi"
    else:
        return link

# Walk through markdown directories
for dirname, subdirlist, mdlist in os.walk('.'):
    
    # Create same hierarchy in GMI directory
    gmi_subpath = os.path.abspath(gmi_path+"/"+dirname)
    os.makedirs(gmi_subpath, exist_ok=True)

    for mdfile in mdlist:
        basename, extension = os.path.splitext(mdfile)
        extension = extension[1:]

        post = {}

        gmifile = basename
        if config.gmi_extension:
            gmifile += ".gmi"

        # We need the relative path without the "./"
        simpledirname = dirname[2:]
        if simpledirname == "":
            post["path"] = gmifile
        else:
            post["path"] = simpledirname + "/" + gmifile       

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
        post["template"] = meta.get("template", None)
        post["author"] = meta.get("author", None)
        post["date"] = meta.get("date", None)
        post["title"] = meta.get("title", None)
        post["tags"] = meta.get("tags", None).split(',')
        # For now, tags list must be a comma-separated string
        # TODO: make possible to list tags as a YAML list

        # Replace stuff
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
                link_func=add_ext_gmi,
                table_tag=config.table_tag
                )

        # Read template file
        with open(tpl_path+"/"+post["template"]+".tpl", 'r') as tpl:
            template = Template(tpl.read())

        # Integrate the GMI content in the template
        gmitext = template.render(content=gmitext, meta = post)
        
        # Dirty fix a weird bug where some lines are CRLF-terminated
        gmitext = gmitext.replace('\r\n','\n')
        
        posts.append(post)
        for tag in post["tags"]:
            slugtag = slugify(tag)
            if slugtag in tags:
                tags[tag]["posts"].append(post)
            else:
                tags[tag] = {"name": tag, "posts": [post]}
        slugauthor = slugify(post["author"])
        if slugauthor in authors:
            authors[post["author"]]["posts"].append(post)
        else:
            authors[post["author"]] = {"name": post["author"], "posts": [post]}

        # Time to write the GMI file
        with open(gmi_subpath+"/"+gmifile, 'w') as gmi:
            gmi.write(gmitext)

posts.sort(key=lambda p: p["date"], reverse=True)

# Generate home page
with open(tpl_path+"/index.tpl", 'r') as tpl:
    template = Template(tpl.read())
text = template.render(posts=posts)
with open(meta_path+"/index.gmi", 'w') as gmi:
    gmi.write(text)

# Generate posts list page
with open(tpl_path+"/posts_list.tpl", 'r') as tpl:
    template = Template(tpl.read())
text = template.render(posts=posts)
with open(meta_path+"/posts.gmi", 'w') as gmi:
    gmi.write(text)

# Generate tags list page
with open(tpl_path+"/tags_list.tpl", 'r') as tpl:
    template = Template(tpl.read())
text = template.render(tags=tags)
with open(meta_path+"/tags.gmi", 'w') as gmi:
    gmi.write(text)
