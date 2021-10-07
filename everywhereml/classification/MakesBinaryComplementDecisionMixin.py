from everywhereml.classification.MakesBinaryDecisionMixin import MakesBinaryDecisionMixin


class MakesBinaryComplementDecisionMixin(MakesBinaryDecisionMixin):
    """
    Mixin to mark classes that, for binary classification, produces a label
    based on `decision > threshold ? 0 : 1`
    """
    pass
