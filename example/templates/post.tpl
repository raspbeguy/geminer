# {{ post.title }}

by {{ post.author.name }}, on {{ post.date.strftime('%d %B %Y') }}
{% set tags = [] %}{% for tag in post.tags %}{{ tags.append(tag.name) or "" }}{% endfor %}{{ tags|join(", ") }}

{{ post.content }}

=> / Back to home
=> /authors/{{ post.author.slug }}.gmi More posts by {{ post.author.name }}

Posts having those tags:
{% for tag in post.tags|sort(attribute="name") -%}
=> /tags/{{ tag.slug }}.gmi {{ tag.name }}
{% endfor %}
