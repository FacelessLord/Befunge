from befunge.utils import Stack


def test_stack_init():
    try:
        stk = Stack()
    except Exception as e:
        raise e
    else:
        assert stk is not None


def test_stack_push_pop():
    stk = Stack()
    stk.push(2)
    stk.push(3)
    assert stk.peek() == 3
    assert stk.pop() == 3
    assert stk.peek() == 2
    assert stk.pop() == 2


def test_stack_dup():
    stk = Stack()
    stk.push(2)
    stk.push(3)
    stk.dup()
    assert stk.peek() == 3
    assert stk.pop() == 3
    assert stk.peek() == 3
    assert stk.pop() == 3
    assert stk.peek() == 2
    assert stk.pop() == 2


def test_stack_swap():
    stk = Stack()
    stk.push(2)
    stk.push(3)
    stk.swap()
    assert stk.peek() == 2
    assert stk.pop() == 2
    assert stk.peek() == 3
    assert stk.pop() == 3


def test_stack_to_string():
    stk = Stack()
    assert str(stk) == "[ ]"
    stk.push(2)
    assert str(stk) == "[2]"
    stk.push(3)
    assert str(stk) == "[3, 2]"
