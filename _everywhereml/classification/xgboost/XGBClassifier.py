import json
import warnings
import numpy as np
from cached_property import cached_property
from tempfile import NamedTemporaryFile
from xgboost import XGBClassifier as OriginalImplementation
from everywhereml.classification.BaseClassifier import BaseClassifier
from everywhereml.classification.MakesBinaryDecisionMixin import MakesBinaryDecisionMixin


class XGBClassifier(MakesBinaryDecisionMixin, BaseClassifier, OriginalImplementation):
    """
    xgboost.XGBClassifier wrapper
    """
    def __init__(self,
                 max_depth=None,
                 learning_rate=None,
                 n_estimators=100,
                 objective=None,
                 gamma=None,
                 min_child_weight=None,
                 max_delta_step=None,
                 subsample=None,
                 colsample_bytree=None,
                 colsample_bylevel=None,
                 colsample_bynode=None,
                 reg_alpha=None,
                 reg_lambda=None,
                 scale_pos_weight=None,
                 base_score=None,
                 random_state=None,
                 missing=np.nan,
                 num_parallel_tree=None,
                 monotone_constraints=None,
                 interaction_constraints=None,
                 importance_type="gain",
                 gpu_id=None,
                 validate_parameters=None,
                 use_label_encoder=True,
                 **kwargs):
        """
        Patch constructor
        """
        super(XGBClassifier, self).__init__(
            max_depth=max_depth,
            learning_rate=learning_rate,
            n_estimators=n_estimators,
            objective=objective,
            gamma=gamma,
            min_child_weight=min_child_weight,
            max_delta_step=max_delta_step,
            subsample=subsample,
            colsample_bytree=colsample_bytree,
            colsample_bylevel=colsample_bylevel,
            colsample_bynode=colsample_bynode,
            reg_alpha=reg_alpha,
            reg_lambda=reg_lambda,
            scale_pos_weight=scale_pos_weight,
            base_score=base_score,
            random_state=random_state,
            missing=missing,
            num_parallel_tree=num_parallel_tree,
            monotone_constraints=monotone_constraints,
            interaction_constraints=interaction_constraints,
            importance_type=importance_type,
            gpu_id=gpu_id,
            validate_parameters=validate_parameters,
            use_label_encoder=use_label_encoder,
            **kwargs)

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

    @cached_property
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
        blacklist = ['X_train', 'y_train', 'classes_', 'n_classes_']

        return {k: v for k, v in self.__dict__.items() if k not in blacklist}

    def fit(self, X, y=None, *args, **kwargs):
        """
        Fit data
        :param X: ndarray|Dataset
        :param y: ndarray
        """
        self.set_Xy(X, y)

        with warnings.catch_warnings():
            warnings.filterwarnings("ignore")
            self.xgboost_base.set_params(self, num_class=len(set(self.y_train)))
            self.xgboost_base.fit(self, self.X_train, self.y_train, *args, **kwargs)

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

            # @todo optimize degenerate trees (single value)

            return {
                'n_classes': int(model['learner']['learner_model_param']['num_class']),
                'trees': [{
                    # same interface as DecisionTree
                    'left': tree['left_children'],
                    'right': tree['right_children'],
                    'features': tree['split_indices'],
                    'thresholds': tree['split_conditions'],
                } for tree in trees]
            }
