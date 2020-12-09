<?xml version="1.0" encoding="utf-8"?>
<feed xmlns="http://www.w3.org/2005/Atom">
  <title>My blog</title>
  <subtitle>Les gentils du net</subtitle>
  <link href="gemini://example.com/atom.xml" rel="self"/>
  <link href="gemini://example.com" rel="alternate"/>
  <updated>{{ now().strftime('%FT%TZ') }}</updated>
  <author>
    <name>raspbeguy</name>
  </author>
  <category term="tech" />
  <id>gemini://example.com</id>
{%- for post in posts|sort(attribute="date",reverse=True) %}
  <entry>
    <title>{{ post.title }}</title>
    <id>gemini://example.com/{{ post.path }}</id>
    <link href="gemini://example.com/{{ post.path }}" rel="alternate"/>
    <updated>{{ post.date.strftime('%FT%TZ') }}</updated>
    <published>{{ post.date.strftime('%FT%TZ') }}</published>
    <author>
      <name>{{ post.author.name }}</name>
    </author>
{%- for tag in post.tags %}
    <category term="{{ tag.name }}"/>
{%- endfor %}
  </entry>
{%- endfor %}
</feed>
