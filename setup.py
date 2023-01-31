from distutils.core import setup

packages=["everywhereml", "everywhereml.plot", "everywhereml.xgboost", "everywhereml.tests", "everywhereml.tests.xgboost", "everywhereml.tests.runtime", "everywhereml.tests.sklearn", "everywhereml.tests.sklearn.ensemble", "everywhereml.tests.templates", "everywhereml.tests.preprocessing", "everywhereml.tests.preprocessing.image", "everywhereml.tests.data", "everywhereml.arduino", "everywhereml.sklearn", "everywhereml.sklearn.tree", "everywhereml.sklearn.ensemble", "everywhereml.get_started", "everywhereml.code_generators", "everywhereml.code_generators.jinja", "everywhereml.code_generators.jinja.filters", "everywhereml.code_generators.prettifiers", "everywhereml.templates", "everywhereml.templates.py", "everywhereml.templates.js", "everywhereml.templates.xgboost", "everywhereml.templates.xgboost.js", "everywhereml.templates.xgboost.cpp", "everywhereml.templates.sklearn", "everywhereml.templates.sklearn.tree", "everywhereml.templates.sklearn.tree.cpp", "everywhereml.templates.sklearn.ensemble", "everywhereml.templates.sklearn.ensemble.py", "everywhereml.templates.sklearn.ensemble.py.micro", "everywhereml.templates.sklearn.ensemble.cpp", "everywhereml.templates.cpp", "everywhereml.templates.preprocessing", "everywhereml.templates.preprocessing.image", "everywhereml.templates.preprocessing.image.cpp", "everywhereml.templates.preprocessing.image.object_detection", "everywhereml.templates.preprocessing.image.object_detection.cpp", "everywhereml.templates.preprocessing.image.transform", "everywhereml.templates.preprocessing.image.transform.cpp", "everywhereml.templates.preprocessing.cpp", "everywhereml.preprocessing", "everywhereml.preprocessing.image", "everywhereml.preprocessing.image.object_detection", "everywhereml.preprocessing.image.transform", "everywhereml.data", "everywhereml.data.collect"]
data=["tests/templates/pipeline.cpp.jinja", "tests/templates/classifier.cpp.jinja", "templates/py/vote.py.jinja", "templates/py/latency.py.jinja", "templates/py/class_map.py.jinja", "templates/py/BaseClassifier.py.jinja", "templates/js/BaseClassifier.js.jinja", "templates/js/class_map.js.jinja", "templates/js/vote.js.jinja", "templates/xgboost/js/tree.jinja", "templates/xgboost/js/XGBClassifier.jinja", "templates/xgboost/cpp/tree.jinja", "templates/xgboost/cpp/XGBClassifier.jinja", "templates/sklearn/tree/cpp/tree.cpp.jinja", "templates/sklearn/tree/cpp/DecisionTreeClassifier.cpp.jinja", "templates/sklearn/ensemble/py/micro/RandomForestClassifier.py.micro.jinja", "templates/sklearn/ensemble/py/micro/tree.py.jinja", "templates/sklearn/ensemble/cpp/tree.cpp.jinja", "templates/sklearn/ensemble/cpp/RandomForestClassifier.cpp.jinja", "templates/cpp/latency.cpp.jinja", "templates/cpp/vote.cpp.jinja", "templates/cpp/TensorFlowPorter.cpp.jinja", "templates/cpp/class_map.cpp.jinja", "templates/cpp/BaseClassifier.cpp.jinja", "templates/preprocessing/image/cpp/BaseImageStep.cpp.jinja", "templates/preprocessing/image/cpp/HOG.cpp.jinja", "templates/preprocessing/image/cpp/LBP.cpp.jinja", "templates/preprocessing/image/object_detection/cpp/HogPipeline.cpp.jinja", "templates/preprocessing/image/object_detection/cpp/BaseObjectDetectionPipeline.cpp.jinja", "templates/preprocessing/image/transform/cpp/Resize.cpp.jinja", "templates/preprocessing/cpp/Step.cpp.jinja", "templates/preprocessing/cpp/Pipeline.cpp.jinja", "templates/preprocessing/cpp/SpectralFeatures.cpp.jinja", "templates/preprocessing/cpp/Window.cpp.jinja", "templates/preprocessing/cpp/MinMaxScaler.cpp.jinja"]

setup(
  name='everywhereml',
  packages=packages,
  version='0.2.16',
  license='MIT',
  description='Train ML in Python, run everywhere',
  author='Simone Salerno',
  author_email='support@eloquentarduino.com',
  url='https://github.com/eloquentarduino/everywhereml',
  download_url='https://github.com/eloquentarduino/everywhereml/blob/master/dist/everywhereml-0.2.16.tar.gz?raw=true',
  keywords=[
    'ML',
    'machine learning'
  ],
  install_requires=[
    'numpy',
    'pandas',
    'seaborn',
    'scikit-learn',
    'scikit-image',
    'Jinja2',
    'cached-property',
    'umap-learn',
    'python-slugify',
    'hexdump',
    'jinja2_workarounds',
    'requests',
    'pySerial'
  ],
  extras_require={
    'tf': ['tensorflow']
  },
  package_data={
    'everywhereml': data
  },
  classifiers=[
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Code Generators',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)