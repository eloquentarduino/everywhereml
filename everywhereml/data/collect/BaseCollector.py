import sys


class BaseCollector:
    """
    Base class for data collectors
    """
    def ask_target_name(self):
        """
        Ask user for target name
        :return:
        """
        print('This is an interactive data capturing procedure.')
        print('Keep in mind that as soon as you will enter a class name, the capturing will start, so be ready!')

        while True:
            try:
                target_name = input('Which class are you going to capture? (leave empty to exit) ').strip()

                if len(target_name) == 0 and input('Are you sure you want to exit? (y|n) ').strip().lower() == 'y':
                    break

                if len(target_name) == 0:
                    continue

                yield target_name

            except Exception as ex:
                print(ex, file=sys.stderr)