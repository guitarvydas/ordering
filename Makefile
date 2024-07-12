#	'ensure that formatted text option in draw.io is disabled everywhere'

all:
	./0D/das2json/das2json order.drawio
	python3 main.py . 0D/python "ignore this arg" main order.drawio.json

#########

# to install required libs, do this once
install-js-requires:
	npm install ohm-js yargs prompt-sync
