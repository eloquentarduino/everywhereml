from everywhereml.tests.runtime.BaseRuntime import BaseRuntime


class PHPRuntime(BaseRuntime):
    """
    PHP runtime
    """
    def get_cmd(self):
        return ['php', 'main.php']