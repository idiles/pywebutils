# -*- coding: UTF-8 -*-
#
# Turbogears projects
# Copyright (c) 2007 IDILES SYSTEMS, UAB
#
# Widgets.

from turbogears import widgets


def form_patch():
    def enhanced_init(self, formid=None, *args, **kargs):
        if formid is not None:
            fields = kargs['fields']
            formid = widgets.HiddenField(name='formid', default=str(formid))
            fields.append(formid)
        self.__original_init(*args, **kargs)

    widgets.Form.__original_init = widgets.Form.__init__
    widgets.Form.__init__ = enhanced_init

class TableForm(widgets.TableForm):
    """Identical to the TG TableForm except for the requiredfield notation
    """

    template = """
    <form xmlns:py="http://purl.org/kid/ns#"
        name="${name}"
        action="${action}"
        method="${method}"
        class="tableform"
        py:attrs="form_attrs"
    >
        <div py:for="field in hidden_fields" 
            py:replace="field.display(value_for(field), **params_for(field))" 
        />
        <table border="0" cellspacing="0" cellpadding="2" py:attrs="table_attrs">
            <tr py:for="i, field in enumerate(fields)" 
                class="${i%2 and 'odd' or 'even'}"
            >
                <th>
                    <label class="fieldlabel ${'required' and field.is_required or ''}"
                        for="${field.field_id}" py:content="field.label" />
                </th>
                <td>
                    <span py:replace="field.display(value_for(field), **params_for(field))" />
                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />
                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />
                </td>
            </tr>
            <tr>
                <td>&#160;</td>
                <td py:content="submit.display(submit_text)" />
            </tr>
        </table>
    </form>
    """

class LineForm(widgets.Form):
    template = """
    <?python
        from turbogears.widgets.forms import Button
    ?>
    <form xmlns:py="http://purl.org/kid/ns#"
        name="${name}"
        action="${action}"
        method="${method}"
        class="lineform"
        py:attrs="form_attrs">
        <div>
            <span py:for="field in hidden_fields"
                py:replace="field.display(value_for(field), **params_for(field))"
            />
            <span py:for="i, field in enumerate(fields)"
                py:if="not isinstance(field, Button)"
                class="${i%2 and 'odd' or 'even'}">
                <span py:replace="field.display(value_for(field), **params_for(field))" />
                <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />
                <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />
            </span>
            <span py:for="button in fields"
                py:if="isinstance(button, Button)"
                py:content="button.display()">
            </span>
        </div>
    </form>
    """
    
class TableFormNoSubmit(widgets.TableForm):
    template = """
    <?python
        from turbogears.widgets.forms import Button
    ?>
    <form xmlns:py="http://purl.org/kid/ns#"
        name="${name}"
        action="${action}"
        method="${method}"
        class="tableformnosubmit"
        py:attrs="form_attrs">
        <div py:for="field in hidden_fields" 
            py:replace="field.display(value_for(field), **params_for(field))" 
        />
        <table border="0" cellspacing="0" cellpadding="2" py:attrs="table_attrs">
            <tr py:for="i, field in enumerate(fields)" 
                class="${i%2 and 'odd' or 'even'}">
                <th>
                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />
                </th>
                <td>
                    <span py:replace="field.display(value_for(field), **params_for(field))" />
                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />
                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />
                </td>
            </tr>
        </table>
    </form>
    """
    params = ["table_attrs"]
    params_doc = {'table_attrs' : 'Extra (X)HTML attributes for the Table tag'}
    table_attrs = {}


class TableFormSubmitAlignLeft(widgets.TableForm):
    template = """
    <form xmlns:py="http://purl.org/kid/ns#"
        name="${name}"
        action="${action}"
        method="${method}"
        class="tableform"
        py:attrs="form_attrs"
    >
        <div py:for="field in hidden_fields" 
            py:replace="field.display(value_for(field), **params_for(field))" 
        />
        <table border="0" cellspacing="0" cellpadding="2" py:attrs="table_attrs">
            <tr py:for="i, field in enumerate(fields)" 
                class="${i%2 and 'odd' or 'even'}"
            >
                <th>
                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />
                </th>
                <td>
                    <span py:replace="field.display(value_for(field), **params_for(field))" />
                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />
                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />
                </td>
            </tr>
            <tr>
                <td colspan="2" py:content="submit.display(submit_text)" />
            </tr>
        </table>
    </form>
    """


class SmallTableForm(widgets.TableForm):
    """Table form without autogenerated submit button. This form places
    Button objects at the bottom of itself.
    """
    template = """
    <?python
        from turbogears.widgets.forms import Button
    ?>
    <form xmlns:py="http://purl.org/kid/ns#"
        name="${name}"
        action="${action}"
        method="${method}"
        class="smalltableform"
        py:attrs="form_attrs">
        <div py:for="field in hidden_fields" 
            py:replace="field.display(value_for(field), **params_for(field))" 
        />
        <table border="0" cellspacing="0" cellpadding="2" py:attrs="table_attrs">
            <tr py:for="i, field in enumerate(fields)"
                py:if="not isinstance(field, Button)"
                class="${i%2 and 'odd' or 'even'}">
                <th>
                    <label class="fieldlabel" for="${field.field_id}" py:content="field.label" />
                </th>
                <td>
                    <span py:replace="field.display(value_for(field), **params_for(field))" />
                    <span py:if="error_for(field)" class="fielderror" py:content="error_for(field)" />
                    <span py:if="field.help_text" class="fieldhelp" py:content="field.help_text" />
                </td>
            </tr>
            <tr>
                <td py:if="buttons == 'right'">&nbsp;</td>
                <td py:attrs="dict(colspan=2) if buttons != 'right' else {}">
                    <span py:for="button in fields"
                        py:if="isinstance(button, Button)"
                        py:replace="button.display(**params_for(field))">
                        Button
                    </span>
                </td>
            </tr>
        </table>
    </form>
    """
    params = ["table_attrs", 'buttons']
    params_doc = {'table_attrs' : 'Extra (X)HTML attributes for the Table tag'}
    table_attrs = {}
    buttons = 'right'



class ButtonLine(widgets.CompoundFormField):
    template = """
    <span xmlns:py="http://purl.org/kid/ns#"
        class="${field_class}" id="${field_id}">
        <span py:for="field in fields">
            <label class="fieldlabel" for="${field.field_id}"
                py:if="field.label" py:content="field.label" />
            <span py:replace="field.display(value_for(field), **params_for(field))" />
            <span py:if="error_for(field)" class="fielderror"
                py:content="error_for(field)" />
            <span py:if="field.help_text" class="fieldhelp"
                py:content="field.help_text" />
        </span>
    </span>
    """
    label = ''


class SubmitButton(widgets.Button):
    template = """
    <input xmlns:py="http://purl.org/kid/ns#"
        type="submit"
        class="button ${field_class}"
        value="${value}"
        py:attrs="attrs"
    />
    """

class SimpleButton(widgets.Button):
    template = """
    <input xmlns:py="http://purl.org/kid/ns#"
        type="button"
        class="button ${field_class}"
        value="${value}"
        py:attrs="attrs"
    />
    """

