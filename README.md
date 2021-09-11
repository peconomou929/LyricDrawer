# LyricDrawer
A tool, to be used by musicians, for generating lyric sheets to be read by non-musicians.

## Installation 
Clone the repository and use pip to install the underlying graphics tool:

```bash
pip install graphics.py
```

## Usage

```python
import document
document.LyricDocument(r"path/to/file.txt").draw(lyric_size = 11, margin = 3)
```

This will render the specified Lyric Sheet. The document will appear in a window, and will close upon being clicked. Meanwhile, a postscript file will be saved at `path/to/file.eps`.

### Format of Lyric Sheet
The Lyric Sheet must have a very specific format. It is read line by line. Each
line is either
- an *empty* line, in which case it renders as a blank line in the document
- a *text* line, in which case it must begin with "Title", "Header", or "Normal", followed by a colon ":" and then white space and then any text which should be rendered
- or a *lyric* line, described below

Lyric lines are put together into lyric sections if they are not separated by any empty lines or text lines.

### Format of Lyric Lines
A lyric line must have a specific format. It is read token by token, where tokens are separated by white space. Each token is either
- a note token
- or a lyric token

A note token indicates the pitch at which the lyric tokens are to be sung. 

#### Format of Note Tokens

A note token begins optionally with any number of ">" OR any number of "<"
but not both. This indicate octave changes; more on that below. The note token is then followed by a valid note name (like "A", "C#", or "Eb") and finally a colon ":". For example, 

```python
valid_note_tokens = ["Ab:", "<A#:", ">>Cb:"]
invalid_note_tokens = ["Ab", "<AA:", "<>Cb:"]
```

The note token indicates the note at which all subsequent lyric tokens are to be sung, until a note change occurs, indicated by new note token. 

There might be ambiguity regarding pitch. For example, "A" can be sung at different octaves. By default, the very first pitch in a line is chosen arbitrarily, and after that each pitch is chosen to be as close as possible (in half steps) to the previous pitch chosen. For example, when moving from "A" to "C", the pitch chosen for "C" is 3 half steps above the previous, rather than 9 half steps below. To indicate that you mean the "C" below, you would instead write "<C:". If you want the "C" an octave further down than this, you would use "<<C:". The other character ">" similarly indicates a motion upward.

#### Format of Lyric Tokens
Anything that cannot be interpreted as a note token will be interpreted as a lyric token.
A lyric token can be either
- a tone token
- a hold token
- a rest token
- a word token

Each token renders in some way on the screen at a height according to the current note being sung. By default there is a line joining each token to the next, unless it is what we call "disconnected," indicated by the character ";" at the end.

#### Tone Token
A tone token consists of a single asterisk "\*", optionally followed by a semicolon ";". This is a note that should be sung without any words.

#### Hold Token
A hold token consists of any number of hyphens "-" (ASCII 0x2D) and optionally a single ";" at the end. Each "-" indicates a single beat for which you want to hold (without any words) the note previously sung. 

You can always use "-" in place of "\*", but "\*" will render more nicely if you are changing pitches while singing without words.

#### Rest Token
A rest token consists of any number of ".", each indicating a single beat for which no sound is made. A rest is always disconnected, and so is the token immediately before the rest.

#### Word Token
Anything that cannot be interpreted as the above tokens will be interpreted as a word token. The main part of the word token is the token itself, or, if the last character is ";", then everything but the last character. The main part of the word token will render in its entirety on a screen, indicating the word to be sung.