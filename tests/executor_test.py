from befunge.executor import Executor


def test_executor_init():
    try:
        excr = Executor()
    except Exception as e:
        raise e
    else:
        assert excr is not None
        assert excr.instructions is not None


def test_executor_div():
    pass
