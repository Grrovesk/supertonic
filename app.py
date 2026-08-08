import os
import gradio as gr
from supertonic import TTS

print("Loading Supertonic 3...")
tts = TTS(auto_download=True)
print("Supertonic 3 loaded.")

VOICES = ["M1", "M2", "M3", "M4", "M5", "F1", "F2", "F3", "F4", "F5"]

LANGUAGES = {
    "English": "en",
    "Korean": "ko",
    "Japanese": "ja",
    "Arabic": "ar",
    "Bulgarian": "bg",
    "Czech": "cs",
    "Danish": "da",
    "German": "de",
    "Greek": "el",
    "Spanish": "es",
    "Estonian": "et",
    "Finnish": "fi",
    "French": "fr",
    "Hindi": "hi",
    "Croatian": "hr",
    "Hungarian": "hu",
    "Indonesian": "id",
    "Italian": "it",
    "Lithuanian": "lt",
    "Latvian": "lv",
    "Dutch": "nl",
    "Polish": "pl",
    "Portuguese": "pt",
    "Romanian": "ro",
    "Russian": "ru",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Swedish": "sv",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Vietnamese": "vi",
    "Auto / Unknown": "na",
}


def generate_speech(text, voice, language_name, steps, speed):
    if not text or not text.strip():
        raise gr.Error("Please enter some text.")

    language_code = LANGUAGES[language_name]

    print("Generating speech...")
    print("Voice:", voice)
    print("Language:", language_name, "->", language_code)
    print("Steps:", steps)
    print("Speed:", speed)

    try:
        style = tts.get_voice_style(voice_name=voice)

        wav, duration = tts.synthesize(
            text=text,
            voice_style=style,
            total_steps=int(steps),
            speed=float(speed),
            lang=language_code,
        )

        output_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "outputs",
        )
        os.makedirs(output_dir, exist_ok=True)

        output_file = os.path.join(
            output_dir,
            "supertonic_output.wav",
        )

        tts.save_audio(wav, output_file)

        print("Saved:", output_file)

        try:
            print(f"Duration: {float(duration[0]):.2f} seconds")
        except Exception:
            pass

        return output_file

    except Exception as e:
        print("ERROR:", repr(e))
        raise gr.Error(str(e))


with gr.Blocks(title="Supertonic 3 TTS") as demo:
    gr.Markdown(
        """
# Supertonic 3 TTS

Local multilingual text-to-speech powered by **Supertonic 3**.

**31 languages • 10 voices • Local only**
"""
    )

    with gr.Row():
        with gr.Column(scale=2):
            text = gr.Textbox(
                label="Text",
                lines=10,
                placeholder="Enter the text you want to convert to speech...",
                value=(
                    "This morning, I took a walk in the park, "
                    "and the sound of the birds and the breeze was so pleasant."
                ),
            )

            with gr.Row():
                voice = gr.Dropdown(
                    choices=VOICES,
                    value="M1",
                    label="Voice",
                )

                language = gr.Dropdown(
                    choices=list(LANGUAGES.keys()),
                    value="English",
                    label="Language",
                )

            with gr.Row():
                steps = gr.Slider(
                    minimum=5,
                    maximum=12,
                    value=8,
                    step=1,
                    label="Quality / Steps",
                )

                speed = gr.Slider(
                    minimum=0.7,
                    maximum=2.0,
                    value=1.05,
                    step=0.05,
                    label="Speech Speed",
                )

            generate = gr.Button(
                "Generate Speech",
                variant="primary",
            )

        with gr.Column(scale=1):
            audio = gr.Audio(
                label="Generated Audio",
                type="filepath",
            )

            gr.Markdown(
                """
### Output

The generated WAV file is saved to:

`outputs/supertonic_output.wav`

**No public Gradio sharing is enabled.**
"""
            )

    generate.click(
        fn=generate_speech,
        inputs=[text, voice, language, steps, speed],
        outputs=audio,
    )


if __name__ == "__main__":
    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        share=False,
        inbrowser=True,
    )
