{% if obj.display %}
   {% if is_own_page %}
{{ obj.id }}
{{ "=" * obj.id | length }}

   {% endif %}
.. py:function:: {% if is_own_page %}{{ obj.id }}{% else %}{{ obj.short_name }}{% endif %}({{ obj.args|replace_typehint }}){% if obj.return_annotation is not none %} -> {{ obj.return_annotation|replace_typehint }}{% endif %}
   {% for (args, return_annotation) in obj.overloads %}

                 {%+ if is_own_page %}{{ obj.id }}{% else %}{{ obj.short_name }}{% endif %}({{ args|replace_typehint }}){% if return_annotation is not none %} -> {{ return_annotation|replace_typehint }}{% endif %}
   {% endfor %}
   {% for property in obj.properties %}

   :{{ property }}:
   {% endfor %}

   {% if obj.docstring %}

   {{ obj.docstring|indent(3) }}
   {% endif %}
{% endif %}
