import runner


def test_runner_load():
    try:
        runner.main("tests/fld_test_program.txt", False)
    except Exception as e:
        raise e
