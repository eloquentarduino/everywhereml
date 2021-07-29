from sklearn.model_selection import KFold
from everywhereml.IsPortableMixin import IsPortableMixin
from everywhereml.classification.utils import to_Xy
from everywhereml.templates import Jinja
from everywhereml.data.plot import plot_confusion_matrix


class BaseClassifier(IsPortableMixin):
    """
    Base class for classifiers
    """
    @property
    def num_inputs(self):
        """
        Get number of inputs
        :return: int
        """
        assert hasattr(self, 'X_train'), 'Unfitted'

        return self.X_train.shape[1]

    @property
    def num_classes(self):
        """
        Get number of classes
        :return: int
        """
        assert hasattr(self, 'y_train'), 'Unfitted'

        return len(set(self.y_train))

    @property
    def package_name(self):
        """
        Get base package name
        :return:
        """
        package_name = self.__module__.__str__().replace('everywhereml.classification.', '').split('.')[0]

        return package_name[0].upper() + package_name[1:]

    @property
    def classname(self):
        """
        Get class name
        :return: str
        """
        classname = self.__module__.__str__().replace('everywhereml.classification.', '').split('.')[-1]

        return classname[0].upper() + classname[1:]

    @property
    def packages(self):
        """
        Get package names
        :return: list
        """
        packages = self.__module__.__str__().replace('everywhereml.classification.', '').split('.')[:-1]

        return [package[0].upper() + package[1:] for package in packages]

    def clone(self):
        """
        Clone classifier
        :return: BaseClassifier
        """
        raise NotImplemented('classifiers MUST implement clone()')

    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        return {}

    def set_Xy(self, X, y):
        """
        Save X and y arrays
        :param X: ndarray|Dataset
        :param y: ndarray
        :return: self
        """
        self.X_train, self.y_train = to_Xy(X, y)

        return self.X_train, self.y_train

    def plot_confusion_matrix(self, X_test, y_test, labels=None, **kwargs):
        """
        Plot confusion matrix of predictions
        :param X_test:
        :param y_test:
        :param labels:
        :param kwargs:
        :return:
        """
        return plot_confusion_matrix(y_test, self.predict(X_test), labels=labels, **kwargs)

    def cross_validate(self, X, y=None, cv=3, shuffle=True):
        """
        Select best classifier using cross validation
        :param X: ndarray|Dataset either a X array or a Dataset instance
        :param y: ndarray
        :param cv: int number of folds
        :param shuffle: bool wether to shuffle data before k fold split
        :return: tuple First value is the best classifier after cross validation, second element is its accuracy
        """
        assert cv > 1, 'cv MUST be greater than 1'

        X, y = self.set_Xy(X, y)
        kfold = KFold(n_splits=cv, shuffle=shuffle)
        best_score = 0
        best_clf = None

        for train_idx, test_idx in kfold.split(X, y):
            clf = self.clone()
            X_train = X[train_idx]
            y_train = y[train_idx]
            X_test = X[test_idx]
            y_test = y[test_idx]

            score = clf.fit(X_train, y_train).score(X_test, y_test)

            if score > best_score:
                best_clf = clf

        # fit classifier on whole data
        best_clf.fit(X, y)

        return best_clf, best_score

    def port(self, language, classname=None, classmap=None, data=None, **kwargs):
        """
        Port classifier to given language
        :param language: str language to port to
        :param classname: str|None name of exported class
        :param classmap: dict mapping from class indices to class labels
        :param data: dict additional data for template
        :param kwargs:
        :return: str generated code
        """
        if data is None:
            data = {}

        data.update(classname=classname or self.classname, classmap=classmap)

        return IsPortableMixin.port(self, language, data=data, **kwargs)

    def get_default_template_data(self):
        """
        Get default data for template
        :return: dict
        """
        return {
            'num_inputs': self.num_inputs,
            'num_classes': self.num_classes,
            'package_name': self.package_name
        }

    def get_default_template_data_php(self, **kwargs):
        """

        :param kwargs:
        :return:
        """
        return {
            'namespace': '\\'.join(self.packages)
        }