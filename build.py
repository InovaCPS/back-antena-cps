from pybuilder.core import use_plugin, init, task, Author

use_plugin("python.core")
# the python unittest plugin allows running python's standard library unittests
use_plugin("python.unittest")
# this plugin allows installing project dependencies with pip
use_plugin("python.install_dependencies")
# a linter plugin that runs flake8 (pyflakes + pep8) on our project sources
use_plugin("python.flake8")
# a plugin that measures unit test statement coverage
use_plugin("python.coverage")
# for packaging purposes since we'll build a tarball
use_plugin("python.distutils")
# PyCharm generate project files
use_plugin('python.pycharm')
# Tool used to run static analysis on the SonarQube Tool
use_plugin('python.sonarqube')
# Used do integrate the Sphinx generate documentation
use_plugin('python.sphinx')

default_task = ["install_dependencies", "clean", "analyze", "publish"]

name = "inova-central-de-parceiros"
version = "0.0.1"
summary = "Centro Paula Souza - Inova - Central de parceiros"
description = ""
authors = [Author("Eduardo Simão", "edu-simao@outlook.com"),
           Author("Italo Carvalho", "italo@fatecpg.com.br")]
license = "GNU General Public License v3.0"
url = "https://github.com/cpsinova/inova-log"


@init
def initialize(project):  # initialize dependencies, project version, properties, licence, etc.
    project.set_property('unittest_module_glob','*_test')
    project.set_property('coverage_break_build', False)
    project.set_property("coverage_threshold_warn", 80)
    project.set_property("coverage_branch_threshold_warn", 80)
    project.set_property("coverage_branch_partial_threshold_warn", 50)

    project.set_property('distutils_use_setuptools',True)
    project.set_property('distutils_setup_keywords', ['central', 'parceiros', 'inova'])

    project.set_property('flake8_exclude_patterns', '.git,__pycache__,docs,old,build,dist,unittest,venv')
    project.set_property('flake8_verbose_output', True)

    project.depends_on_requirements("requirements.txt")
    project.build_depends_on('mockito')


@task("say_hello", description='funny init task')
def say_hello(logger, project):  # dependency injection for "logger" and "project"
    print("Hello, PyBuilder of INOVA projects!")
    logger.info("I am building {0} in version {1}!".format(project.name, project.version))
    pass
