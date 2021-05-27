from everywhereml.data.preprocessing import MinMaxScaler


class MinMaxScalerTest:
    def get_instances(self, dataset):
        return [
            MinMaxScaler(num_features=-1),
            MinMaxScaler(num_features=dataset.num_columns),
        ]