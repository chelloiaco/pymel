
class {{ classname }}({{ parents }}):
{% if attrs %}
  {% for attr in attrs %}
    {{ attr.name }} = {{ attr.value }}
  {% endfor %}
{% endif %}
{% if methods %}

  {% for method in methods %}
    {% if method.type == 'query' %}
    @_f.addMelDocs('{{ method.command }}', '{{ method.flag }}')
    def {{ method.name }}(self, **kwargs):
      {% if method.returnFunc %}
        return {{ method.returnFunc }}(_f.asQuery(self, cmds.{{ method.command }}, kwargs, '{{ method.flag }}'))
      {% else %}
        return _f.asQuery(self, cmds.{{ method.command }}, kwargs, '{{ method.flag }}')
      {% endif %}
    {% elif method.type == 'edit' %}
    @_f.addMelDocs('{{ method.command }}', '{{ method.flag }}')
    def {{ method.name }}(self, val=True, **kwargs):
        {% if callbackFlags %}
        _f.handleCallbacks(args, kwargs, {{ callbackFlags }})
        {% endif %}
        return _f.asEdit(self, cmds.{{ method.command }}, kwargs, '{{ method.flag }}', val)
    {% elif method.type == 'api' %}
    {% if method.classmethod %}
    @classmethod
    {% endif %}
    {% if method.deprecated %}
    @_f.deprecated
    {% endif %}
    def {{ method.name }}({{ method.signature }}):
    {% if method.argList %}
      {% if method.undoable %}
        do, final_do, outTypes = _f.processApiArgs([{{ method.inArgs }}], {{ method.argList }}, self.{{ method.getter }}, self.{{ method.name }}, {{ method.getterInArgs}})
      {% else %}
        do, final_do, outTypes = _f.getDoArgs([{{ method.inArgs }}], {{ method.argList }})
      {% endif %}
      {% if method.classmethod %}
        res = _api.{{ method.apiClass }}.{{ method.apiName }}(*final_do)
      {% elif method.proxy %}
        res = _f.getProxyResult(self, _api.{{ method.apiClass }}, '{{ method.apiName }}', final_do)
      {% else %}
        res = _api.{{ method.apiClass }}.{{ method.apiName }}(self, *final_do)
      {% endif %}
      {% if method.returnType %}
        res = _f.ApiArgUtil._castResult(self, res, '{{ method.returnType }}', {{ method.unitType }})
      {% endif %}
        return _f.processApiResult(res, {{ method.outArgs }}, outTypes, do)
    {% else %}
      {% if method.undoable %}
        undoEnabled = cmds.undoInfo(q=1, state=1) and _f.apiUndo.cb_enabled
        if undoEnabled:
            undo = _f.getUndoArgs([{{ method.inArgs }}], [], self.{{ method.getter }}, {{ method.getterInArgs }})
      {% endif %}
      {% if method.undoable %}
        if undoEnabled:
            apiUndo.append(_f.ApiUndoItem(self.{{ method.name }}, [], undo))
      {% endif %}
      {% if method.classmethod %}
        res = _api.{{ method.apiClass }}.{{ method.apiName }}()
      {% elif method.proxy %}
        res = _f.getProxyResult(self, _api.{{ method.apiClass }}, '{{ method.apiName }}')
      {% else %}
        res = _api.{{ method.apiClass }}.{{ method.apiName }}(self)
      {% endif %}
      {% if method.returnType %}
        return _f.ApiArgUtil._castResult(self, res, '{{ method.returnType }}', {{ method.unitType }})
      {% else %}
        return res
      {% endif %}
    {% endif %}
    {% endif %}

  {% endfor %}
{% else %}

{% endif %}