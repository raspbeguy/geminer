# Geminer

## Introduction

Geminer is a tool that was originally designed to convert a PicoCMS blog into a static version for Gemini. In fact, it can act as a markdown-based static site generator.

## Features

* Markdown to Gemtext conversion
* Conversion of local links
* Give your own metadata list to gather
* Custom indexes
* Jinja2 templating

## Workflow

Geminer execution can be decomposed in two steps :

1. Parse blog posts markdown files and write gemtext translation.
2. Generate meta pages, i.e. home page and custom indexes.

During the first step, frontmatter metadata is collected from markdown posts while gemtext posts are generated. This means that while rendering the template, a post will only have access to informations about itself.

During the second step, all metadata has been gathered, which enables creation of various indexed, which requires of course access to all posts metadata.

## Configuration

Soon. For now you can read [the example config](config.py.example).

## Gemini capsules using Geminer

* gemini://hashtagueule.fr

## TODO

* add parameter to give a function to treat local links
* clean the code (lots of work)
* add feed generation
* change configuration format?
