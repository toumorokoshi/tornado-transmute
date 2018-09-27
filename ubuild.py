import os
import subprocess


def main(build):
    tornado_version = os.environ.get("TORNADO_VERSION")
    if tornado_version:
        build.packages.install("tornado", version=tornado_version)

    build.packages.install(".", develop=True)


def test(build):
    main(build)
    build.packages.install("jedi")
    build.packages.install("sphinx")
    build.packages.install("pytest")
    build.packages.install("pytest-cov")
    pytest = os.path.join(build.root, "bin", "py.test")
    subprocess.call([
        pytest, "--cov", "tornado_transmute",
        "tornado_transmute/tests",
        "--cov-report", "term-missing"
    ])


def publish(build):
    """ publish the package itself """
    build.packages.install("wheel")
    build.packages.install("twine")
    build.executables.run([
        "python", "setup.py",
        "sdist", "bdist_wheel", "--universal", "--release"
    ])
    build.executables.run([
        "twine", "upload", "dist/*"
    ])
