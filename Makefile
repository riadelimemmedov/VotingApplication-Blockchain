run_test:
	pytest -s .
run_test_coverage:
	coverage run -m pytest
generate_text_coverage:
	coverage report
generate_html_coverage:
	coverage html
generate_xml_coverage:
	coverage xml

open_doc:
	mkdocs serve --open

.PHONY: run_test,run_test_coverage,generate_text_coverage,generate_html_coverage,generate_xml_coverage
.PHONY: open_doc
