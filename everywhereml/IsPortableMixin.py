from everywhereml.templates import Jinja


class IsPortableMixin:
    """
    Mixin that defines a class a capable of porting itself to any supported language
    """
    def port(self, language, data=None, **kwargs):
        """
        Port to given language
        :param language: str
        :param data: dict
        :return: str ported code
        """
        template_name = '%s.jinja' % self.__module__.__str__().replace('everywhereml.', '').replace('.', '/')
        template_data = self.get_template_data(**kwargs)
        template_data.update(self.get_template_data_for_language(language))
        template_data.update(data or {})

        for k, v in self.get_default_template_data_for_language(language).items():
            template_data.setdefault(k, v)

        for k, v in self.get_default_template_data().items():
            template_data.setdefault(k, v)

        for k, v in kwargs.items():
            template_data.setdefault(k, v)

        # ALWAYS inject these values
        template_data['uuid'] = 'UUID%d' % id(self)

        ported = Jinja('', language=language, dialect=kwargs.get('dialect', None)).render(template_name, template_data)

        return ported
        # return self.postprocess_port(jinja('ml/data/preprocessing/pipeline/%s.jinja' % template_name, template_data))

    def get_template_data(self, **kwargs):
        """
        Get data for jinja template
        :return: dict
        """
        return {}

    def get_default_template_data(self):
        """
        Get default template data
        :return: dict
        """
        return {
            'namespace': ''
        }

    def get_template_data_cpp(self):
        """
        Get template data specific for C++
        :return: dict
        """
        return {}

    def get_template_data_js(self):
        """
        Get template data specific for Js
        :return: dict
        """
        return {}

    def get_template_data_php(self):
        """
        Get template data specific for PHP
        :return: dict
        """
        return {}

    def get_template_data_for_language(self, language):
        """
        Get template data specific for a given language
        :param language: str
        :return: dict
        """
        func = 'get_template_data_%s' % language

        if hasattr(self, func):
            return getattr(self, func)()

        return {}

    def get_default_template_data_for_language(self, language):
        """
        Get template data specific for a given language
        :param language: str
        :return: dict
        """
        func = 'get_default_template_data_%s' % language

        if hasattr(self, func):
            return getattr(self, func)()

        return {}