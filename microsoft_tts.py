#!/usr/bin/env python3

"""
Microsoft Text-to-Speech (TTS) AGI Script for Asterisk.
Author: Lukas Kaplan
GitHub: https://github.com/lukaskaplan/asterisk-agi-microsoft-tts
License: MIT

This script converts text to speech using Microsoft Azure TTS and saves the output
as a WAV file (8kHz, mono PCM). It is optimized for use as an AGI script in Asterisk.

Usage (in Asterisk dialplan):
    same => n,AGI(microsoft_tts.py,"Text to synthesize","/path/to/output.wav")

Requirements:
    - requests (pip install requests)
    - Microsoft Azure Speech API key (set as MICROSOFT_TTS_API_KEY environment variable)
"""

import sys
import os
import requests

# Configuration
DEFAULT_API_KEY = None  # Replace with your API key if necessary, but using env var is recommended
API_KEY = os.getenv("MICROSOFT_TTS_API_KEY", DEFAULT_API_KEY)
TTS_URL = os.getenv(
    "MICROSOFT_TTS_API_URL",
    "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
)
VOICE_NAME = "cs-CZ-VlastaNeural"  # Change voice as needed
AUDIO_FORMAT = "riff-8khz-16bit-mono-pcm"  # Format suitable for Asterisk

def synthesize_speech(text: str, output_file: str):
    """
    Sends a request to Microsoft Azure TTS API to synthesize speech from text.

    :param text: The text to be converted to speech.
    :param output_file: Path to the output WAV file.
    :return: Exit code (0 = success, 1 = failure)
    """
    if not API_KEY:
        sys.exit(1)  # Exit silently in AGI (Asterisk will handle the error)

    # SSML request body for better speech synthesis control
    ssml_payload = f'''
    <speak xmlns="http://www.w3.org/2001/10/synthesis"
           xmlns:mstts="http://www.w3.org/2001/mstts"
           xmlns:emo="http://www.w3.org/2009/10/emotionml"
           version="1.0" xml:lang="cs-CZ">
        <voice name="{VOICE_NAME}">
            <prosody rate="15%" pitch="5%">{text}</prosody>
        </voice>
    </speak>'''

    headers = {
        "Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": AUDIO_FORMAT,
        "Ocp-Apim-Subscription-Key": API_KEY,
        "User-Agent": "TTSPYTHON",
    }

    try:
        response = requests.post(
            TTS_URL,
            headers=headers,
            data=ssml_payload.encode("utf-8"),
            timeout=5
        )
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            os.chmod(output_file, 0o777)
            sys.exit(0)  # Success
        else:
            sys.exit(1)  # API request failed
    except requests.exceptions.RequestException:
        sys.exit(1)  # Network error

def main():
    """Main function to process AGI input arguments."""
    if len(sys.argv) != 3:
        sys.exit(1)  # Incorrect usage

    text = sys.argv[1]
    output_file = sys.argv[2]

    synthesize_speech(text, output_file)

if __name__ == "__main__":
    main()
