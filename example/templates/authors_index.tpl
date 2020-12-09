# Authors list

{% for author, value in prop.items()|sort(attribute='1.name') -%}
=> /authors/{{ author }}.gmi {{ value.name }} ({{ value.posts | length }} articles)
{% endfor %}
