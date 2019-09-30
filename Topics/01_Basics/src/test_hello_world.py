# File: test_hello_world.py
from hello_world import hello_world

def test_hello_world(capsys): 
    hello_world() 
    out, _ = capsys.readouterr()
    assert out == "Hello World!\n"
