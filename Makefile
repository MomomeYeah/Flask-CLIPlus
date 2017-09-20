.PHONY: clean install uninstall

clean:
	rm -rf cli_plus/*.pyc sample/*.pyc

install:
	./sample/install.sh

uninstall:
	./sample/uninstall.sh
