# This is the configuration file for geminer.
# It is not intended to be executed.

# locale (for templates, for example dates rendering)
locale = "en_US.utf8"

# path to directory containing markdonw files to convert
md_path = "/srv/gemini/example/md"

# path to gemini blog root directory
gmi_path = "/srv/gemini/example/gmi"

# directory within gmi_path which will contains converted posts
posts_dir = "posts"

# path to directory containing templates
tpl_path = "/srv/gemini/example/templates"

# list of markdown files extensions
# Any file with a different extension will be ignored.
md_extensions = [
        ".markdown",
        ".mdown",
        ".mkdn",
        ".md",
        ".mkd",
        ".mdwn",
        ".mdtxt",
        ".mdtext",
        ".text",
        ".Rmd"
        ]

# Specify gemini files extension. Set to empty string to disable extension.
# Warning: disabling could have unwanted side effects.
# Check out README for more informations.
gmi_extension = ".gmi"

# replacement map
# Some CMS make you use some placeholders (for instance for assets URL).
# You have to inform geminer of them here.
replace = [
        ("%assets_url%", "https://example.com/assets")
]

# md2gemini settings
# Check the documentation at https://pypi.org/project/md2gemini/l
code_tag=""
img_tag="[IMG]"
indent=" "
ascii_table=False
links="copy"
plain=True
strip_html=False
base_url=""
table_tag="table"

# default template for posts that don't specify one
default_post_template = "post"

# per-post properties to fetch in frontmatter
post_props = [
    "date",
    "title"
    ]

# indexable properties to fetch in frontmatter
# A lot of CMS will manage properties like tags ans authors, which are written
# in the frontmatter, and are used to make subgroups of posts.
# This setting enables to do the same for any frontmatter property you wish.
#
# Each indexable property generate two views:
#   * per-value post index:  This is a list of links to posts that have a given
#                            value of the property. There are as many per-value
#                            indexes as properties values.
#   * property values index: This is a list of links to per-value indexes.
#                            There is only one page of this kind, and it can be
#                            disabled.
#
# Exemple: if the property is tags, then it will generate a tag index tags.gmi,
# which will link to some subindexes like tags/computer (assuming computer is
# an existing tag).
#
# Specify here a list of dictionnary, each one with the following keys:
#   * property (mandatory):     name of the property present in the frontmatter
#   * list (facultative):       set to True if the property is a list of values
#   * item_dir (facultative):   directory containing per-value posts indexes
#   * item_tpl (facultative):   template of the per-value posts indexes
#   * index_name (facultative): filename of the property values index
#   * index_tpl (facultative):  template of the property values index
#
# Filenames are relative to meta_dir and extensions are automatically added.
# If filename contains an extension, it will override gmi_extension value.
# When a string value is facultative, it defaults to property name, except for
# index_name, which disables property values global index if not specified.
index_props = [
    {
        "property": "tags",
        "list": True,
        "item_dir": "tags",
        "item_tpl": "tag",
        "index_name": "tags",
        "index_tpl": "tags_index"
    },
    {
        "property": "author",
        "list": False,
        "item_dir": "authors",
        "item_tpl": "author",
        "index_name": "authors",
        "index_tpl": "authors_index"
    }
]


# custom extra pages to generate
# Each entry will generate a single page.
# This is the place to define homepage and feed page for instance.
# Templates will have to handle the full unsorted list of posts.
# "name" key is mandatory. It is the filename of the page.
# If filename contains an extension, it will override gmi_extension value.
# "tpl" key is facultative, defaults to name (without extension if any)
custom_pages = [
    {
        "name": "index",
        "tpl": "index"
    },
    {
        "name": "atom.xml",
        "tpl": "atom"
    }
]
