# Posts list

{% for post in posts|sort(attribute="date",reverse=True) -%}
=> /{{ post.path }} [{{ post.date.strftime('%d/%m/%Y') }}] {{ post.title }}
{% endfor %}
