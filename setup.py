from setuptools import setup, find_packages

import typographie

CLASSIFIERS = [
    "Intended Audience :: Developers",
    "Natural Language :: English",
    "Operating System :: OS Independent",
    "Programming Language :: Python",
]

KEYWORDS = "django typogrify french français règles typographiques"


setup(
    name="django-typographie",
    version=typographie.__version__,
    description="""Apply french typografy rules""",
    author=typographie.__author__,
    url="https://github.com/briefmnews/django-typographie",
    packages=find_packages(),
    classifiers=CLASSIFIERS,
    keywords=KEYWORDS,
    zip_safe=True,
    python_requires=">=3.11",
    install_requires=["Django>=4.0"],
    include_package_data=True,
)
