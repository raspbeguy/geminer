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

md_path = os.path.abspath(os.path.expanduser(config.md_path))
gmi_path = os.path.abspath(os.path.expanduser(config.gmi_path))
tpl_path = os.path.abspath(os.path.expanduser(config.tpl_path))

posts_path = os.path.abspath(gmi_path + "/" + config.posts_dir)

# Initiate meta lists
posts = [] # This is a flat, unsorted list of posts
posts_prop_index = {} # This is a dict containing posts sorted by properties

for prop_dict in config.index_props:
    posts_prop_index[prop_dict["property"]] = {}


def add_ext_gmi(link):
    # Custom function to apply to links
    if "://" not in link:  # apply only on local links
        return os.path.splitext(link)[0] + ".gmi"
    else:
        return link


# Walk through markdown directories
for dirname, subdirlist, mdlist in os.walk(md_path):

    # Create same hierarchy in GMI directory
    gmi_subpath = os.path.abspath(posts_path + "/" + os.path.relpath(dirname, md_path))
    os.makedirs(gmi_subpath, exist_ok=True)

    for mdfile in mdlist:
        basename, extension = os.path.splitext(mdfile)

        # We want to ignore the file if this isn't a markdown file
        if extension not in config.md_extensions:
            print(
                'Ignoring file {}: "{}" not in markdown extensions list'.format(
                    mdfile, extension
                )
            )
            pass

        post = {}

        gmifile = basename
        if config.gmi_extension:
            gmifile += ".gmi"

        post["path"] = os.path.relpath(dirname + "/" + gmifile, md_path)

        # Read the Markdown file
        with open(dirname + "/" + mdfile, "r") as md:
            mdtext = md.read()

        # Parse the YAML header
        meta = frontmatter.parse(mdtext)[0]

        # Extract template
        post["template"] = meta.get("template", config.default_post_template)

        # Extract post properties
        for prop in config.post_props:
            post[prop] = meta.get(prop, None)

        # Extract index properties
        for prop_dict in config.index_props:
            prop = prop_dict["property"]
            prop_raw = meta.get(prop, None)
            if prop_dict.get("list", False) and prop_raw:
                post[prop] = [
                    {"name": word, "slug": slugify(word)}
                    for word in prop_raw.split(",")
                ]
                for item in post[prop]:
                    slug = item["slug"]
                    if slug in posts_prop_index[prop]:
                        posts_prop_index[prop][slug]["posts"].append(post)
                    else:
                        posts_prop_index[prop][slug] = {
                            "name": item["name"],
                            "posts": [post],
                        }
            else:
                post[prop] = {"name": prop_raw, "slug": slugify(prop_raw)}
                slug = post[prop]["slug"]
                if slug in posts_prop_index[prop]:
                    posts_prop_index[prop][slug]["posts"].append(post)
                else:
                    posts_prop_index[prop][slug] = {
                        "name": post[prop]["name"],
                        "posts": [post],
                    }

        posts.append(post)

        # For now, list properties must be comma-separated strings.
        # TODO: make possible to list values as a YAML list

        # Replace stuff
        for item in config.replace:
            mdtext = mdtext.replace(item[0], item[1])

        # Convert the post into GMI
        gmitext = md2gemini(
            mdtext,
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
            table_tag=config.table_tag,
        )

        post["content"] = gmitext

        # Read template file
        with open(tpl_path + "/" + post["template"] + ".tpl", "r") as tpl:
            template = Template(tpl.read())

        # Integrate the GMI content in the template
        gmitext = template.render(post=post)

        # Dirty fix a weird bug where some lines are CRLF-terminated
        gmitext = gmitext.replace("\r\n", "\n")

        # Time to write the GMI file
        with open(gmi_subpath + "/" + gmifile, "w") as gmi:
            gmi.write(gmitext)

# Generate custom extra pages
for page_dict in config.custom_page:
    rel_path, filename = os.path.split(page_dict["name"])
    os.makedirs(rel_path, exist_ok=True)
    basename, extension = os.path.spolitext(page_dict["name"])
    if not extension:
        extention = gmi_extension
    filename = basename + extension
    with open(tpm_path + "/" + page_dict.get("tpl", basename) + ".tpl", "r") as tpl:
        template = Template(tpl.read())
    text = template.render(posts=posts)
    with open(gmi_path + rel_path + "/" + filename, "w") as gmi:
        gmi.write(text)

# Generate custom meta pages
for prop_dict in config.index_props:
    prop = prop_dict["property"]
    if "index_name" in prop_dict:
        with open(
            tpl_path + "/" + prop_dict.get("index_tpl", prop) + ".tpl", "r"
        ) as tpl:
            template = Template(tpl.read())
        text = template.render(prop=posts_prop_index[prop])
        with open(gmi_path + "/" + prop_dict["index_name"] + gmi_extension, "w") as gmi:
            gmi.write(text)
    os.makedirs(gmi_path + "/" + prop_dict.get("item_dir", prop), exist_ok=True)
    with open(tpl_path + "/" + prop_dict.get("item_tpl", prop) + ".tpl", "r") as tpl:
        template = Template(tpl.read())
    for item in posts_prop_index[prop]:
        text = template.render(prop_item=posts_prop_index[prop][item])
        with open(
            gmi_path + "/" + prop_dict.get("item_dir", prop) + "/" + item + gmi_extension, "w"
        ) as gmi:
            gmi.write(text)
