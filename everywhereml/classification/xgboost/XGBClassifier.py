import json
import warnings
from xgboost import XGBClassifier as OriginalImplementation
from everywhereml.classification.BaseClassifier import BaseClassifier
from tempfile import NamedTemporaryFile


class XGBClassifier(BaseClassifier, OriginalImplementation):
    """
    xgboost.XGBClassifier wrapper
    """

    def __init__(self, random_state=0, use_label_encoder=False, **kwargs):
        """
        Patch constructor
        :param random_state: int
        """
        super().__init__(random_state=random_state, use_label_encoder=use_label_encoder, **kwargs)

    def __call__(self, *args, **kwargs):
        """
        Proxy all calls to native classifier
        """
        return self.xboost_base(self, *args, **kwargs)

    def __getattr__(self, item):
        """
        Proxy all calls to native classifier
        """
        return getattr(self.xgboost_base, item)

    @property
    def xgboost_base(self):
        """
        Get xgboost native class
        :return: type
        """
        return [base for base in self.__class__.__bases__ if base.__module__.startswith('xgboost.')][0]

    def get_params(self, deep=True):
        """
        Monkey patch
        :param deep: bool
        :return: dict
        """
        return {}

    def fit(self, X, y=None, *args, **kwargs):
        """
        Fit data
        :param X: ndarray|Dataset
        :param y: ndarray
        """
        self.set_Xy(X, y)

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore')
            OriginalImplementation.fit(self, self.X_train, self.y_train, *args, **kwargs)

        return self

    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        # it's easier to work with the json dump of the XGBClassifier
        with NamedTemporaryFile('w+', suffix='.json', encoding='utf-8') as tmp:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                self.save_model(tmp.name)

            tmp.seek(0)
            model = json.load(tmp)
            trees = model['learner']['gradient_booster']['model']['trees']

            return {
                'n_classes': int(model['learner']['learner_model_param']['num_class']),
                'trees': [{
                    'left': tree['left_children'],
                    'right': tree['right_children'],
                    'features': tree['split_indices'],
                    'thresholds': tree['split_conditions']
                } for tree in trees]
            }
