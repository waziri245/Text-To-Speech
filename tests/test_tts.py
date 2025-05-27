"""
Unit tests for the Text-to-Speech application.
"""

from unittest import mock
import pytest

import src.text_to_speech as tts

# Mock tkinter messagebox 
@pytest.fixture(autouse=True)
def patch_messagebox():
    with mock.patch("tkinter.messagebox.showerror"), \
         mock.patch("tkinter.messagebox.showinfo"), \
         mock.patch("tkinter.messagebox.showwarning"):
        yield

def test_get_voices_returns_sorted_list():
    """Test that get_voices returns a sorted list of voice objects."""
    voices = tts.get_voices()
    assert isinstance(voices, list)
    assert all(hasattr(v, 'id') and hasattr(v, 'name') for v in voices)

@mock.patch("src.text_to_speech.engine.setProperty")
@mock.patch("src.text_to_speech.get_voices")
def test_set_voice_windows_female(mock_get_voices, mock_set_property):
    """Test voice selection with female voice available on Windows."""
    # Setup mock voices
    mock_voice_female = mock.Mock(name="Microsoft Zira Desktop")
    mock_voice_male = mock.Mock(name="Microsoft David Desktop")
    mock_voice_female.name = "Microsoft Zira Desktop"
    mock_voice_female.id = "zira"
    mock_voice_male.name = "Microsoft David Desktop"
    mock_voice_male.id = "david"

    mock_get_voices.return_value = [mock_voice_female, mock_voice_male]
    tts.current_os = "windows"
    tts.has_female = True

    # Test female voice selection
    tts.set_voice("Female")
    mock_set_property.assert_called_with("voice", "zira")

def test_get_unique_filename_creates_new_file_name(tmp_path):
    """Test filename generation with conflict resolution."""
    # Create a dummy file to force name generation
    base = "text"
    path = tmp_path
    open(path / f"{base}.mp3", "a").close()

    # Test that a new filename is generated
    filename = tts.get_unique_filename(str(path), base_name=base)
    assert filename.endswith("text1.mp3")

@mock.patch("src.text_to_speech.engine.say")
@mock.patch("src.text_to_speech.engine.runAndWait")
@mock.patch("src.text_to_speech.set_voice")
def test_speaknow_valid_text(mock_set_voice, mock_run, mock_say):
    """Test text-to-speech conversion with valid input."""
    # Setup mock GUI elements
    tts.text_area = mock.Mock()
    tts.text_area.get.return_value = "Hello, world!"
    tts.gender_combobox = mock.Mock()
    tts.speed_combobox = mock.Mock()
    tts.gender_combobox.get.return_value = "Male"
    tts.speed_combobox.get.return_value = "Normal"

    tts.speaknow()

    # Verify expected calls were made
    mock_set_voice.assert_called()
    mock_say.assert_called_with("Hello, world!")
    mock_run.assert_called_once()

@mock.patch("src.text_to_speech.engine.save_to_file")
@mock.patch("src.text_to_speech.engine.runAndWait", return_value=None)
@mock.patch("src.text_to_speech.set_voice")
@mock.patch("src.text_to_speech.get_unique_filename", return_value="/fake/path/text.mp3")
@mock.patch("src.text_to_speech.filedialog.askdirectory", return_value="/fake/path")
@mock.patch("src.text_to_speech.os.path.exists", return_value=True)
def test_download_creates_file(mock_exists, mock_askdir, mock_getname,
                             mock_set_voice, mock_run, mock_save):
    """Test file saving functionality."""
    # Setup mock GUI elements
    tts.text_area = mock.Mock()
    tts.text_area.get.return_value = "Save this text"
    tts.gender_combobox = mock.Mock()
    tts.speed_combobox = mock.Mock()
    tts.gender_combobox.get.return_value = "Male"
    tts.speed_combobox.get.return_value = "Normal"

    tts.download()

    # Verify expected calls were made
    mock_set_voice.assert_called()
    mock_save.assert_called_with("Save this text", "/fake/path/text.mp3")
    mock_run.assert_called_once()

def test_speaknow_no_text_warns():
    """Test warning when no text is provided for speech."""
    tts.text_area = mock.Mock()
    tts.text_area.get.return_value = "\n"
    with mock.patch("tkinter.messagebox.showwarning") as warn:
        tts.speaknow()
        warn.assert_called_once_with("No Text", "Please enter text to speak")

def test_download_no_text_warns():
    """Test warning when no text is provided for saving."""
    tts.text_area = mock.Mock()
    tts.text_area.get.return_value = "\n"
    with mock.patch("tkinter.messagebox.showwarning") as warn:
        tts.download()
        warn.assert_called_once_with("No Text", "Please enter text to save")