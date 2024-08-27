from flask import Flask, request, send_file, jsonify
from pytube import YouTube
import os
from dotenv import load_dotenv

# Charger les variables d'environnement depuis le fichier .env
load_dotenv()

app = Flask(__name__)

# Récupérer la clé API YouTube à partir des variables d'environnement
YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")

@app.route('/download_audio', methods=['GET'])
def download_audio():
    video_url = request.args.get('video_url')
    if not video_url:
        return jsonify({"error": "video_url parameter is required"}), 400
    
    try:
        yt = YouTube(video_url)
        audio_stream = yt.streams.filter(only_audio=True).first()
        
        # Téléchargement de l'audio
        output_path = './'
        file_name = 'audio.mp3'
        audio_stream.download(output_path=output_path, filename=file_name)
        
        # Retourner le fichier téléchargé
        return send_file(os.path.join(output_path, file_name), as_attachment=True)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
