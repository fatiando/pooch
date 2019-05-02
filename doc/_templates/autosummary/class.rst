{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}

.. raw:: html

     <div style='clear:both'></div>

{% for item in members %}
{% if item in ['__call__'] %}
.. automethod:: {{ objname }}.{{ item }}
{% endif %}
{% endfor %}

{% for item in methods %}
{% if item != '__init__' %}
.. automethod:: {{ objname }}.{{ item }}
{% endif %}
{% endfor %}

.. raw:: html

     <div style='clear:both'></div>
