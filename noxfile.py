import nox

nox.options.sessions = ["lint", "test"]


@nox.session
def lint(session):
    session.install("pre-commit")
    session.run("pre-commit", "run", "-a")


@nox.session(python=["2.7", "3.8", "3.9", "3.10"])
def test(session):
    session.install("pytest", "pytest-cov")
    session.install("-e", ".")
    if session.posargs:
        session.run("pytest", *session.posargs)
    else:
        session.run(
            "pytest",
            "--cov=glibs.jsonschema",
            "--cov-report=",
            env={"COVERAGE_FILE": f".coverage.{session.name}"},
        )
        session.notify("coverage")


@nox.session
def coverage(session):
    session.install("coverage")
    session.run("coverage", "combine")
    session.run("coverage", "report", "--fail-under=100", "--show-missing")
    session.run("coverage", "erase")
