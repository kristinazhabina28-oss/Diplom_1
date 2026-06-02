import runpy


class TestPraktikum:
    def test_script_prints_expected_demo_order(self, capsys):
        runpy.run_path('praktikum.py', run_name='__main__')

        output_lines = tuple(capsys.readouterr().out.splitlines())

        assert output_lines == (
            '(==== black bun ====)',
            '= sauce sour cream =',
            '= filling cutlet =',
            '= filling dinosaur =',
            '(==== black bun ====)',
            '',
            'Price: 700',
        )
