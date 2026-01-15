from setuptools import setup, find_packages

setup(
    name="log_laplace",                  # the package name
    version="0.1.0",
    description="Centralized logging library for Laplace apps",
    author="Semion Tchetovsky",
    # author_email="youremail@example.com",
    packages=find_packages(),             # automatically find all packages in log_laplace/
    python_requires=">=3.10",
    install_requires=[
        # no external dependencies for now, logging is standard
        # you can add things like 'rich' or 'colorama' later if needed
    ],
    include_package_data=True,
)
