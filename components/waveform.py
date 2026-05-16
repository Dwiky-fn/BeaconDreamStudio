import base64

def waveform_editor(audio_bytes, audio_fmt, duration_sec):

    audio_b64 = base64.b64encode(
        audio_bytes
    ).decode()

    html = f"""
    <!DOCTYPE html>
    <html>
    <body>

    <h3>Waveform Editor</h3>

    <audio controls>
        <source
            src="data:audio/{audio_fmt};base64,{audio_b64}">
    </audio>

    </body>
    </html>
    """

    return html