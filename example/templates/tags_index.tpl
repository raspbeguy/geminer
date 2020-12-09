# Tags list

{% for tag, value in prop.items()|sort(attribute='1.name') -%}
=> /tags/{{ tag }}.gmi {{ value.name }} ({{ value.posts | length }} articles)
{% endfor %}
