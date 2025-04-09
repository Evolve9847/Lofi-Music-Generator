from flask import Flask, render_template, request, url_for, send_file
from pydub import AudioSegment
import os
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['PROCESSED_FOLDER'] = 'static/processed'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['PROCESSED_FOLDER'], exist_ok=True)

@app.route('/', methods=['GET', 'POST'])
def index():
    context = {
        "preview_url": None,
        "lyrics_text": "",
        "lyrics_only": False,
        "download_file": None,
        "form_data": {
            "preset": "",
            "speed": "1.0",
            "pitch": "0",
            "reverb": "5",
            "fx": [],
            "rain": False,
            "rain_volume": "1.0",
            "karaoke": False,
            "volume": "1.0",
            "lyrics": "",
            "lyrics_only": False
        }
    }

    if request.method == 'POST':
        file = request.files['song']
        form = request.form
        context["lyrics_text"] = form.get("lyrics", "")
        context["lyrics_only"] = form.get("lyrics_only") == "on"

        context["form_data"] = {
            "preset": form.get("preset", ""),
            "speed": form.get("speed", "1.0"),
            "pitch": form.get("pitch", "0"),
            "reverb": form.get("reverb", "5"),
            "fx": form.getlist("fx"),
            "rain": form.get("rain") == "on",
            "rain_volume": form.get("rain_volume", "1.0"),
            "karaoke": form.get("karaoke") == "on",
            "volume": form.get("volume", "1.0"),
            "lyrics": form.get("lyrics", ""),
            "lyrics_only": form.get("lyrics_only") == "on"
        }

        if file:
            filename = f"{uuid.uuid4()}.mp3"
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)

            if context["lyrics_only"]:
                context["preview_url"] = url_for('static', filename=f'uploads/{filename}')
                return render_template('index.html', **context)

            song = AudioSegment.from_file(filepath)

            preset = context["form_data"]["preset"]
            speed = float(context["form_data"]["speed"])
            pitch = int(context["form_data"]["pitch"])
            reverb = int(context["form_data"]["reverb"])
            fx = context["form_data"]["fx"]
            rain = context["form_data"]["rain"]
            rain_volume = float(context["form_data"]["rain_volume"])
            volume = float(context["form_data"]["volume"])
            karaoke = context["form_data"]["karaoke"]

            if preset == "chill":
                speed = 0.9
                pitch = -2
                reverb = 6
                if "echo" not in fx:
                    fx.append("echo")
            elif preset == "vintage":
                pitch = -1
                reverb = 4
                # no auto-bass
            elif preset == "deepnight":
                speed = 0.8
                pitch = -3
                reverb = 7
                if "echo" not in fx:
                    fx.append("echo")
                # no auto-bass

            # Speed
            song = song._spawn(song.raw_data, overrides={
                "frame_rate": int(song.frame_rate * speed)
            }).set_frame_rate(song.frame_rate)

            # Pitch
            new_sample_rate = int(song.frame_rate * (2.0 ** (pitch / 12.0)))
            song = song._spawn(song.raw_data, overrides={
                "frame_rate": new_sample_rate
            }).set_frame_rate(song.frame_rate)

            # Reverb
            if reverb > 0:
                echo = song - (10 - reverb)
                delayed = AudioSegment.silent(duration=200) + echo
                song = song.overlay(delayed)

            # FX
            if "echo" in fx:
                echo = song - 6
                delayed = AudioSegment.silent(duration=300) + echo
                song = song.overlay(delayed)
            if "bass" in fx:
                song = song.low_pass_filter(100)
            if "distortion" in fx:
                song += 10

            # Rain
            if rain:
                rain_path = os.path.join("static", "rain.mp3")
                if os.path.exists(rain_path):
                    rain_sound = AudioSegment.from_file(rain_path)
                    adjusted_rain = rain_sound.apply_gain(-5 + (10 * (rain_volume - 1.0)))
                    looped_rain = adjusted_rain * (len(song) // len(adjusted_rain) + 1)
                    song = song.overlay(looped_rain)

            # Volume
            song += 10 * (volume - 1.0)

            # Karaoke
            if karaoke and song.channels == 2:
                left, right = song.split_to_mono()
                inverted_right = right.invert_phase()
                song = left.overlay(inverted_right)

            output_filename = f"processed_{filename}"
            output_path = os.path.join(app.config['PROCESSED_FOLDER'], output_filename)
            song.export(output_path, format="mp3")

            context["preview_url"] = url_for('static', filename=f'processed/{output_filename}')
            context["download_file"] = output_filename

    return render_template('index.html', **context)

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['PROCESSED_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
