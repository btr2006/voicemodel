from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import FileResponse
from TTS.api import TTS
import shutil

app = FastAPI()

tts = TTS(model_name="tts_models/multilingual/multi-dataset/xtts_v2")

@app.post("/generate")
async def generate_audio(
    text: str = Form(...),
    language: str = Form("en"),
    file: UploadFile = File(None)
):
    text = text.replace("’", "'").replace("…", "...").replace("—", "-")

    sample_path = None

    if file:
        sample_path = "sample.wav"
        with open(sample_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    output_path = "output.wav"

    tts.tts_to_file(
        text=text,
        speaker_wav=sample_path,
        language=language,
        file_path=output_path
    )

    return FileResponse(output_path, media_type="audio/wav", filename="output.wav")