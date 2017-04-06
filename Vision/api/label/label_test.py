import re

from label import main


def test_main(resource, capsys):
    in_file = resource('Fat-hen-2.jpg')

    main(in_file)

    stdout, _ = capsys.readouterr()
    assert re.match(r'Found label:.*Plant', stdout)
