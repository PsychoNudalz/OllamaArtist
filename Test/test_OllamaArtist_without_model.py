import pytest
import OllamaArtist


# def test_ping():
#     if(OllamaArtist.ping()):
#         assert True
#         return True
#     else:
#         print("Error connecting to Ollama server")
#         assert False
#         return False

def test_remove_quotes_at_end():
    test_string = "{\"test\"\"}"
    assert OllamaArtist.remove_quotes_at_end(test_string) == "{\"test\"}"


def test_remove_quotes_at_end_no_quotes():
    test_string = "{test2}"
    assert OllamaArtist.remove_quotes_at_end(test_string) == "{test2}"
#
# def test_request_chat_image_order():
#     if(not test_ping()):return False
#     order = OllamaArtist.request_chat_image_order()
#     assert order.Text != ""
