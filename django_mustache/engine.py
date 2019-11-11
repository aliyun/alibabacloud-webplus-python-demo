from django.template.backends.base import BaseEngine
try:
    from django.template.exceptions import TemplateDoesNotExist
except ImportError:
    from django.template.base import TemplateDoesNotExist
from django.template.context import _builtin_context_processors
from django.utils.module_loading import import_string
from django.utils.functional import cached_property

import pystache
from pystache.common import (
    TemplateNotFoundError as PystacheTemplateDoesNotExist
)

import os
from pystache import TemplateSpec


class Mustache(BaseEngine):
    """
    Mustache template backend for Django 1.8+
    """

    app_dirname = "mustache"

    def __init__(self, params):
        params = params.copy()
        self.options = params.pop('OPTIONS').copy()
        self.options.setdefault('partial_dir', 'partials')
        self.options.setdefault('file_extension', 'html')

        super(Mustache, self).__init__(params)

        dirs = self.template_dirs
        if self.options['partial_dir']:
            for path in self.template_dirs:
                dirs += (os.path.join(path, self.options['partial_dir']),)

        self.engine = Engine(
            search_dirs=dirs,
            file_extension=self.options['file_extension'],
        )

        self.engine.file_encoding = "utf-8"
        self.locale_map = self._load_locales()

    @cached_property
    def template_context_processors(self):
        paths = _builtin_context_processors + tuple(self.options.get(
            'context_processors', []
        ))
        processors = []
        for path in paths:
            processors.append(import_string(path))
        return processors

    def get_template(self, template_name):
        template_name = template_name.replace(
            '.' + self.engine.file_extension, ''
        )
        try:
            template = self.engine.load_template(template_name)
        except PystacheTemplateDoesNotExist as e:
            raise TemplateDoesNotExist(e)
        return Template(template, self)

    def _load_locales(self):
        m = dict()
        for f in os.listdir("locales"):
            if not f.endswith(".properties"):
                continue
            code = f.split(".")[0]
            m[code] = self._load_locale("locales/" + f)
        return m

    def _load_locale(self, file_name):
        m = dict()
        with open(file_name, "rb") as f:
            for l in f.readlines():
                sp = l.strip().decode("utf-8").split("=", 1)
                m[sp[0]] = sp[1]
        return m


class I18nTemplate(TemplateSpec):
    def __init__(self, locale_map):
        self.locale_map = locale_map
        self.lang = "en"

    def i18n(self, text=None):
        def translate(code):
            # print code
            sp = code.split()
            if len(sp) == 1:
                return self.locale_map[self.lang].get(sp[0], "default")
            return self.locale_map[self.lang].get(sp[0], "default").format(*[i.strip("[]") for i in sp[1:]])
        return translate


class Template(object):
    """
    Analogue to django.template.backends.django.Template, with a bit of
    django.template.context.RequestContext built in.
    """
    def __init__(self, template, backend):
        t = I18nTemplate(backend.locale_map)
        t.template = template
        t.template_encoding = "utf-8"
        self.template = t
        self.backend = backend

    def render(self, context=None, request=None):
        contexts = []

        if context and not request:
            request = context.get('request', None)

        if request:
            for fn in self.backend.template_context_processors:
                contexts.append(fn(request))

        if context:
            contexts.append(context)

        if "_lang" in context:
            self.template.lang = context["_lang"]

        return self.backend.engine.render(
            self.template,
            *contexts
        )


class Engine(pystache.Renderer):
    """
    Rough analogue to django.template.engine.Engine, but almost entirely
    handled by Pystache.
    """
    def str_coerce(self, val):
        if val is None:
            return ""
        return str(val)
