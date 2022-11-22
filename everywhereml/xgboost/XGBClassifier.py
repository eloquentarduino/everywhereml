import json
import numpy as np
from tempfile import NamedTemporaryFile
from xgboost import XGBClassifier as Impl
from everywhereml.sklearn.SklearnBaseClassifier import SklearnBaseClassifier


class XGBClassifier(SklearnBaseClassifier, Impl):
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
            **kwargs)

    @property
    def sklearn(self):
        """
        Get sklearn native class
        :return: type
        """
        return [base for base in self.__class__.__bases__ if base.__module__.startswith('xgboost.')][0]

    def get_template_data(self):
        """
        Get additional data for template
        :return: dict
        """
        with NamedTemporaryFile('w+', suffix='.json', encoding='utf-8') as tmp:
            self.save_model(tmp.name)
            tmp.seek(0)
            decoded = json.load(tmp)
            trees = decoded['learner']['gradient_booster']['model']['trees']

            return {
                'n_classes': int(decoded['learner']['learner_model_param']['num_class']) or 2,
                'trees': [{
                    'left': tree['left_children'],
                    'right': tree['right_children'],
                    'features': tree['split_indices'],
                    'thresholds': tree['split_conditions'],
                } for tree in trees]
            }
