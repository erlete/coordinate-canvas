# Welcome to the contribution guidelines

In this document you will find out about all rules and criteria for successful contributions to the repository. It is important to maintain some standards, specially regarding code style and documentation formatting. Read code style and documentation conventions carefully, since their violation will most probably lead to requests for you to fix your contributions.

## Code style and documentation

### Code

All Python code follows the [Style Guide for Python Code](https://peps.python.org/pep-0008/), which can be automatically enforced using linters such as [`autopep8`](https://pypi.org/project/autopep8/) or [`flake8`](https://flake8.pycqa.org/en/latest/). Furthermore, [`mypy`](https://mypy-lang.org/) is used to ensure static data type usage and type hinting notation.

### Documentation

All Python docstrings follow the [Google Docstring Format](https://sphinxcontrib-napoleon.readthedocs.io/en/latest/example_google.html) conventions. These docstrings can be further parsed by [Sphinx](https://www.sphinx-doc.org/en/master/) using the [`napoleon`](https://github.com/sphinx-contrib/napoleon) extension. This contributes to a more legible and easier to write code documentation.

## Got it. Where do I start?

### Do not reinvent the wheel

You should start by [taking a look at the active issue list](https://github.com/erlete/coordinate-canvas/issues) in order to collaborate efficiently. If the functionality/bug you intend to implement/solve is not listed there, you can always [create a new issue](https://github.com/erlete/coordinate-canvas/issues/new/choose) and explain your idea.

### Get a fresh copy for yourself

After that, go ahead and [fork the repository](https://github.com/erlete/coordinate-canvas/fork). This will enable you to create new branches and implement your changes.

### Request implementation

Once all changes have been committed and pushed, feel free to create a pull request (do not forget to link it to the issue you opened before!) and publish all modifications. Most probably, the PR will be blocked due to several reasons (apart from the standard Git conflict reasons):

| Block reason | Solution |
| :----------: | :------: |
| The PR is not reviewed | Await revision |
| There are unresolved conversations | Await resolution confirmation |
| The branch is not updated | Click the **Update branch** button or merge latest changes manually |
| Status checks are not passing | Take a look at workflow logs and solve compatibility issues |

## Thank you

Go ahead and have some fun adding your grain of sand to the project. **Thank you for the help!**
