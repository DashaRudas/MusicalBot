import requests

from pychord import Chord, find_chords_from_notes

CHORD_URL = "https://www.scales-chords.com/api/scapi.1.3.php"

WELCOME_MESSAGE = "Бот поможет переделать гитарную партию для пианино 🎹 \n\nВведите /help для просмотра команд"

HELP_MESSAGE = "*Доступные команды*:\n \
	\t /start -  Начать работу\n \
	\t /help  -  Показать это сообщение\n \
	\t /chord  -  Анализ аккорда \n \
	\t /compose  -  Поиск аккорда из ваших нот\n\n"

CHORD_MESSAGE = "Введите аккорд для анализа в таком формате: \n \
*[<аккорд>]* (_например, [Am7]_)"

COMPOSE_MESSAGE = "Введите список нот в таком формате: \n \
*{<нота1> <нота2> ... <нотаN>}* (_например, {C E G}_):"


def get_chord_analysis_message(chord: Chord):
	text = "*Аккорд:* `{}`\n\n".format(chord.chord)
	text += "*Тоника:* `{}`\t\t\t".format(chord.root)
	text += "*Вид:* `{}`\t\t\t".format(chord.quality)
	text += "*Ноты:* `{}`\n".format(', '.join(chord.components()))

	return text


def get_compose_analysis_message(notes):
	chords = find_chords_from_notes(notes)
	
	if chords:
		text = "*Возможные аккорды:*\n"
		text += "`{}`".format(', '.join([c.chord for c in chords]))
	else:
		text = "*К сожалению, из этих нот невозможно составить аккорд*"
	return text


def get_chord_image_url(chord: Chord):
	url = requests.post(CHORD_URL, data={"chord": chord.chord, "instrument": "piano"}).text.split("src=")[1][1:-2]
	return url

