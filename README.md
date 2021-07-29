# EverywhereML

A Python package to train Machine Learning models that run (almost) everywhere, including:

 [X] C++ / embedded systems
 [X] Javascript
 [X] PHP
 [] Go / TinyGo
 [] Micropython
 []  ... other languages
 
This means you can deploy your models to:

 - Edge devices
 - Web servers
 - Web browsers
 - ... other environments
 
 
## Components

The package implements most of the tools you need to develop a fully functional model, including:

 [X] Data loading and visualization
 [X] Preprocessing
    [X] Pipeline
    [X] BoxCox (power transform)
    [X] CrossDiff
    [X] MinMaxScaler
    [X] Normalizer
    [X] PolynomialFeatures
    [X] RateLimit
    [X] StandardScaler
    [X] YeoJohnson (power transform)
    [] Feature selection
        [X] RFE
        [X] SelectKBest
    [] Time series analysis
        [X] Diff
        [X] Fourier transform
        [X] Rolling window
        []  TSFRESH 
 [] Classification
    [X] RandomForest
    [X] LogisticRegression
    [X] GaussianNB
    []  BernoulliNB
    [X] SVM
    []  LinearSVM
    [X] DecisionTree
    [X] XGBoost
    []  Catboost
 []  Regression
    [] LinearRegression
    
    
Each of these components can be trained in Python and exported to any of the supported languages
with no (or as few as possible) external dependencies.
    