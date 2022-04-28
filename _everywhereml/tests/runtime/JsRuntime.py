from everywhereml.tests.runtime.BaseRuntime import BaseRuntime


class JsRuntime(BaseRuntime):
    """
    Js runtime
    """
    def get_cmd(self):
        return ['node', 'main.js']