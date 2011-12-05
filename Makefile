test:
	nosetests --with-doctest --doctest-tests
	nosetests2.4 --with-doctest --doctest-tests

clean:
	for f in `find . -name '*.pyc'`; do rm $$f; done
	for f in `find . -name '*.pyo'`; do rm $$f; done
	for f in `find . -name '.svn'`; do rm -rf $$f; done
