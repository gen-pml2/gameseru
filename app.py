from flask import Flask, render_template, request, jsonify, session
import subprocess
import select
import os
import pty

app = Flask(__name__)
app.secret_key = "cyberpunk_terminal_secret"

# Kamus global untuk menyimpan proses terminal aktif per user
prosses_aktif = {}

def konversi_ansi_ke_html(text):
    """Mengubah kode warna ANSI komputer menjadi format HTML agar bisa berwarna di browser"""
    replacements = {
        "\033[0m": "</span>",
        "\033[1m": "<span style='font-weight:bold;'>",
        "\033[91m": "<span style='color:#ff5555;'>",
        "\033[92m": "<span style='color:#50fa7b;'>",
        "\033[93m": "<span style='color:#f1fa8c;'>",
        "\033[95m": "<span style='color:#ff79c6;'>",
        "\033[96m": "<span style='color:#8be9fd;'>",
        "\033[2J\033[H": "", # mengabaikan clear screen ansi standar
        "\x1bc": "" 
    }
    for ansi, html in replacements.items():
        text = text.replace(ansi, html)
    return text

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream', methods=['GET', 'POST'])
def stream():
    # Membuat sub-proses terminal baru jika game baru dimulai
    if 'user_id' not in session:
        session['user_id'] = os.urandom(8).hex()
    
    uid = session['user_id']

    if uid not in prosses_aktif or prosses_aktif[uid]['process'].poll() is not None:
        master, slave = pty.openpty()
        p = subprocess.Popen(['python', 'game_asli.py'], stdin=slave, stdout=slave, stderr=slave, close_fds=True, text=True)
        os.close(slave)
        prosses_aktif[uid] = {'process': p, 'fd': master}

    fd = prosses_aktif[uid]['fd']

    # Jika ada input tebakan dari user di browser
    if request.method == 'POST':
        user_input = request.json.get('input', '') + '\n'
        os.write(fd, user_input.encode())

    # Membaca output teks dari program game_asli.py
    output = ""
    while True:
        r, _, _ = select.select([fd], [], [], 0.1)
        if r:
            data = os.read(fd, 1024).decode(errors='ignore')
            if not data:
                break
            output += data
        else:
            break

    # Deteksi jika layar dibersihkan oleh os.system('cls'/'clear')
    is_cleared = "clear" if "\x1bc" in output or "\033[2J" in output else "none"
    
    return jsonify({
        'output': konversi_ansi_ke_html(output),
        'cleared': is_cleared,
        'game_over': prosses_aktif[uid]['process'].poll() is not None
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)
