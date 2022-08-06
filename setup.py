from distutils.core import setup

packages=["everywhereml", "everywhereml.plot", "everywhereml.tests", "everywhereml.tests.runtime", "everywhereml.tests.sklearn", "everywhereml.tests.sklearn.ensemble", "everywhereml.tests.templates", "everywhereml.tests.preprocessing", "everywhereml.tests.preprocessing.image", "everywhereml.tests.data", "everywhereml.sklearn", "everywhereml.sklearn.tree", "everywhereml.sklearn.tree.templates", "everywhereml.sklearn.ensemble", "everywhereml.sklearn.ensemble.templates", "everywhereml.get_started", "everywhereml.code_generators", "everywhereml.code_generators.jinja", "everywhereml.code_generators.jinja.filters", "everywhereml.code_generators.templates", "everywhereml.templates", "everywhereml.templates.cpp", "everywhereml.preprocessing", "everywhereml.preprocessing.image", "everywhereml.preprocessing.image.object_detection", "everywhereml.preprocessing.image.object_detection.templates", "everywhereml.preprocessing.image.templates", "everywhereml.preprocessing.image.transform", "everywhereml.preprocessing.image.transform.templates", "everywhereml.preprocessing.templates", "everywhereml.data", "everywhereml.data.collect"]
data=["tests/templates/pipeline.cpp.jinja", "tests/templates/classifier.cpp.jinja", "sklearn/tree/templates/tree.cpp.jinja", "sklearn/tree/templates/DecisionTreeClassifier.cpp.jinja", "sklearn/ensemble/templates/tree.cpp.jinja", "sklearn/ensemble/templates/RandomForestClassifier.cpp.jinja", "code_generators/templates/TensorFlowPorter.cpp.jinja", "templates/latency.cpp.jinja", "templates/vote.cpp.jinja", "templates/class_map.cpp.jinja", "templates/BaseClassifier.cpp.jinja", "preprocessing/image/object_detection/templates/HogPipeline.cpp.jinja", "preprocessing/image/object_detection/templates/BaseObjectDetectionPipeline.cpp.jinja", "preprocessing/image/templates/BaseImageStep.cpp.jinja", "preprocessing/image/templates/HOG.cpp.jinja", "preprocessing/image/templates/LBP.cpp.jinja", "preprocessing/image/transform/templates/Resize.cpp.jinja", "preprocessing/templates/Step.cpp.jinja", "preprocessing/templates/Pipeline.cpp.jinja", "preprocessing/templates/SpectralFeatures.cpp.jinja", "preprocessing/templates/Window.cpp.jinja", "preprocessing/templates/MinMaxScaler.cpp.jinja"]

setup(
  name='everywhereml',
  packages=packages,
  version='0.0.7',
  license='MIT',
  description='Train ML in Python, run everywhere',
  author='Simone Salerno',
  author_email='support@eloquentarduino.com',
  url='https://github.com/eloquentarduino/everywhereml',
  download_url='https://github.com/eloquentarduino/everywhereml/blob/master/dist/everywhereml-0.0.7.tar.gz?raw=true',
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
    'hexdump'
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
