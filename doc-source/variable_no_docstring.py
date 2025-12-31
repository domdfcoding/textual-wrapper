# 3rd party
import sphinx.ext.autodoc
from sphinx.application import Sphinx
from sphinx_toolbox.more_autodoc.variables import VariableDocumenter
from sphinx_toolbox.utils import flag


def autovariable_add_nodocstring(app: Sphinx) -> None:
	"""
	Add the ``:no-docstring:`` option to autovariable directives.

	The option is used to exclude the docstring from the output

	:param app: The Sphinx application.
	"""

	VariableDocumenter.option_spec["no-docstring"] = flag

	app.setup_extension("sphinx.ext.autodoc")
	app.connect("autodoc-process-docstring", no_docstring_process_docstring, priority=1000)


def no_docstring_process_docstring(app: Sphinx, what, name: str, obj, options, lines: list[str]) -> None:
	if options.get("no-docstring", False):
		lines.clear()


def setup(app):
	autovariable_add_nodocstring(app)
