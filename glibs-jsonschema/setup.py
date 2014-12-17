import setuptools


setuptools.setup(
    name="glibs-jsonschema",
    version="1.0",
    url="http://www.geekie.com.br",
    maintainer="Geekie",
    maintainer_email="geekie@geekie.com.br",
    packages=["geekie"],
    namespace_packages=["geekie"],
    include_package_data=True,
    zip_safe=False,
    setup_requires=["setuptools_git==1.0b1"],
    install_requires=[
        "jsonschema>=2.4.0",
    ],
    extras_require={
        "testing": [
            "mock==1.0.1",
        ],
    }
)
