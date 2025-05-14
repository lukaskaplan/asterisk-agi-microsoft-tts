# asterisk-agi-microsoft-tts

[![Lint](https://github.com/lukaskaplan/asterisk-agi-microsoft-tts/actions/workflows/lint.yml/badge.svg)](https://github.com/lukaskaplan/asterisk-agi-microsoft-tts/actions/workflows/lint.yml)

Microsoft Text-to-Speech (TTS) AGI Script for Asterisk

This script converts text to speech using **Microsoft Azure TTS** and saves the output as a **WAV file (8kHz, mono PCM)**, making it ideal for use with **Asterisk AGI**.

## Features

- Uses **Microsoft Azure Text-to-Speech API**
- Generates **8kHz, 16-bit, mono PCM WAV** files for Asterisk
- Designed for **AGI integration** in Asterisk dialplans
- Supports **environment variable-based API key management**
- Fast and efficient execution

## Installation

### Prerequisites

- **Python 3** (tested with Python 3.7+)
- `requests` library
- A **Microsoft Azure Speech API Key** with access to the Text-to-Speech service

### Install dependencies

```sh
pip install -r requirements.txt
```

## Usage

### 1️⃣ Set up the API Key

You can configure the API key in two ways:

**Option 1: Use an environment variable (recommended)**

```sh
export MICROSOFT_TTS_API_KEY="your-microsoft-api-key"
```

**Option 2: Set it inside the script (not recommended for security reasons)** Edit the script and replace:

```python
DEFAULT_API_KEY = "your-microsoft-api-key"
```

### 2️⃣ Run the script manually

```sh
python microsoft_tts.py "Hello, this is a test" /path/to/output.wav
```

### 3️⃣ Use as an Asterisk AGI Script

#### Copy the script to Asterisk AGI directory:

```sh
cp microsoft_tts.py /var/lib/asterisk/agi-bin/microsoft_tts.py
chmod +x /var/lib/asterisk/agi-bin/microsoft_tts.py
```

#### Example Asterisk Dialplan (extensions.conf):

```asterisk
exten => 1234,1,Answer()
same  => n,AGI(microsoft_tts.py,"Hello, welcome to our system","/var/lib/asterisk/sounds/custom/greeting.wav")
same  => n,Playback(custom/greeting)
same  => n,Hangup()
```

### 4️⃣ Unset API Key (if needed)

#### Linux/macOS:

```sh
unset MICROSOFT_TTS_API_KEY
```

## License

This project is licensed under the **MIT License**.

## Repository

GitHub: [github.com/lukaskaplan/asterisk-agi-microsoft-tts](https://github.com/lukaskaplan/asterisk-agi-microsoft-tts)

## Author

- Lukáš Kaplan
- GitHub: [lukaskaplan](https://github.com/lukaskaplan)

