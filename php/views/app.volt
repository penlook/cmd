{# app/views/posts/show.phtml #}
<!DOCTYPE html>
<html>
    <head>
        <title>{{ title }} - An example blog</title>
    </head>
    <body>
        {% if show_navigation %}
            <ul id="navigation">
            {% for item in menu %}
                <li><a href="{{ item.href }}">{{ item.caption }}</a></li>
            {% endfor %}
            </ul>
        {% endif %}

        <h1>{{ post.title }}</h1>

        <div class="content">
            {{ post.content }}
        </div>

    </body>
</html>