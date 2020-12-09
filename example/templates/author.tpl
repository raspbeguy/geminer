# Posts by {{ prop_item.name }}

{% for post in prop_item.posts|sort(attribute="date",reverse=True) -%}
=> /{{ post.path }} [{{ post.date.strftime('%d/%m/%Y') }}] {{ post.title }}
{% endfor %}
