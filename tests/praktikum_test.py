import runpy


class TestPraktikum:
    def test_main_prints_burger_receipt(self, capsys):
        runpy.run_path('praktikum.py', run_name='__main__')

        captured = capsys.readouterr()

        assert captured.out == (
            '(==== black bun ====)\n'
            '= sauce sour cream =\n'
            '= filling cutlet =\n'
            '= filling dinosaur =\n'
            '(==== black bun ====)\n\n'
            'Price: 700\n'
        )
