import streamlit as st
import streamlit.components.v1 as components

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="Asisten Cerdas Super Pro v17", page_icon="🎙️", layout="wide")

# --- 2. MASTER KODE (SEMUA FITUR DALAM SATU WADAH) ---
master_kode = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <style>
        :root { --teal: #14b8a6; --orange: #f59e0b; --purple: #8b5cf6; --dark: #0f172a; --blue: #2563eb; --red: #ef4444; }
        body { font-family: 'Inter', sans-serif; margin: 0; background: #f1f5f9; color: #1e293b; }
        .navbar { background: var(--dark); padding: 1rem; display: flex; justify-content: space-around; position: sticky; top: 0; z-index: 100; }
        .nav-btn { padding: 10px 20px; border-radius: 10px; border: none; color: white; cursor: pointer; font-weight: bold; font-size: 0.8rem; transition: 0.2s; }
        .nav-btn:hover { opacity: 0.8; transform: translateY(-2px); }
        .container { max-width: 850px; margin: 20px auto; padding: 20px; }
        .card { background: white; border-radius: 20px; padding: 25px; box-shadow: 0 10px 15px rgba(0,0,0,0.1); margin-bottom: 20px; }
        textarea { width: 100%; min-height: 180px; padding: 15px; border: 2px solid #e2e8f0; border-radius: 12px; margin-top: 10px; box-sizing: border-box; font-family: inherit; font-size: 14px; }
        .action-btn { width: 100%; padding: 12px; margin-top: 10px; border-radius: 10px; border: none; color: white; font-weight: bold; cursor: pointer; transition: 0.3s; font-size: 0.9rem; }
        .action-btn:active { transform: scale(0.98); }
        .hidden { display: none; }
        .control-row { display: flex; gap: 10px; margin: 15px 0; align-items: center; background: #f8fafc; padding: 15px; border-radius: 12px; border: 1px solid #e2e8f0; flex-wrap: wrap; }
        .ctrl-item { flex: 1; min-width: 120px; }
        .btn-group-tts { display: grid; grid-template-columns: repeat(auto-fit, minmax(100px, 1fr)); gap: 10px; }
        .ai-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-bottom: 10px; }
        .download-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; margin-top: 10px; }
        hr { border: 0; border-top: 1px dashed #cbd5e1; margin: 20px 0; }
    </style>
</head>
<body>
    <div class="navbar">
        <button class="nav-btn" style="background:var(--teal)" onclick="buka('stt')">STT</button>
        <button class="nav-btn" style="background:var(--orange)" onclick="buka('tts')">TTS</button>
        <button class="nav-btn" style="background:var(--purple)" onclick="buka('ai')">AI</button>
        <button class="nav-btn" style="background:#10b981" onclick="buka('save')">SIMPAN</button>
    </div>

    <div class="container">
        <div id="stt" class="card">
            <h2>🎙️ Rekam & Media</h2>
            <input type="text" id="yt" placeholder="Tempel Link YouTube..." style="width:100%; padding:12px; border-radius:10px; border:1px solid #ccc; margin-bottom:5px;">
            <button class="action-btn" style="background:var(--red)" onclick="mainYT()">📺 MUAT YOUTUBE</button>
            <div id="player" style="margin-top:10px;"></div>
            <button class="action-btn" style="background:var(--teal)" onclick="mulaiSTT()">🎙️ MULAI REKAM SUARA</button>
            <textarea id="outSTT" placeholder="Hasil suara atau transkripsi media akan muncul di sini..."></textarea>
        </div>

        <div id="tts" class="card hidden">
            <h2>🔊 Kontrol Narasi</h2>
            <div class="control-row">
                <div class="ctrl-item" style="flex: 2;">
                    <label style="font-size:11px;">Pilih Suara</label>
                    <select id="suara" style="width:100%; padding:8px; border-radius:8px;"></select>
                </div>
                <div class="ctrl-item">
                    <label style="font-size:11px;">Pitch</label>
                    <input type="range" id="pitch" min="0.5" max="2" step="0.1" value="1" style="width:100%;">
                </div>
                <div class="ctrl-item">
                    <label style="font-size:11px;">Gaya</label>
                    <select id="speed" style="width:100%; padding:8px; border-radius:8px;">
                        <option value="1">Normal</option>
                        <option value="0.8">Santai</option>
                        <option value="1.3">Cepat</option>
                    </select>
                </div>
            </div>
            <textarea id="inTTS" placeholder="Ketik materi yang ingin dinarasikan..."></textarea>
            <div class="btn-group-tts">
                <button class="action-btn" style="background:var(--orange)" onclick="putar()">▶️ PUTAR</button>
                <button class="action-btn" style="background:#64748b" onclick="jeda()">⏸ JEDA</button>
                <button class="action-btn" style="background:#0ea5e9" onclick="lanjut()">⏯ LANJUT</button>
                <button class="action-btn" style="background:var(--red)" onclick="stop()">⏹ STOP</button>
            </div>
        </div>

        <div id="ai" class="card hidden">
            <h2>🤖 Cerdas AI</h2>
            <div class="ai-grid">
                <button class="action-btn" style="background:var(--purple)" onclick="ringkas()">📝 RINGKAS OTOMATIS</button>
                <button class="action-btn" style="background:var(--blue)" onclick="buatMindMap()">🌿 BUAT MIND MAP</button>
            </div>
            <textarea id="outAI" placeholder="Hasil olahan AI akan muncul di sini..."></textarea>
        </div>

        <div id="save" class="card hidden">
            <h2>💾 Pusat Unduhan</h2>
            <textarea id="final" readonly></textarea>
            <button class="action-btn" style="background:#6366f1" onclick="update()">🔄 REFRESH DATA</button>
            <div class="download-grid">
                <button class="action-btn" style="background:#10b981" onclick="unduh('txt')">📄 SIMPAN TXT</button>
                <button class="action-btn" style="background:var(--blue)" onclick="unduh('doc')">📘 SIMPAN WORD</button>
            </div>
            <hr>
            <button class="action-btn" style="background:var(--orange); padding:18px;" onclick="unduhAudioReal()">
                <i class="fas fa-file-audio"></i> UNDUH HASIL AUDIO (MP3)
            </button>
        </div>
    </div>

    <script>
        let synth = window.speechSynthesis;
        function buka(id){ document.querySelectorAll('.card').forEach(c=>c.classList.add('hidden')); document.getElementById(id).classList.remove('hidden'); if(id==='save') update(); }
        
        function mainYT(){ 
            const val = document.getElementById('yt').value;
            const id = val.includes('v=') ? val.split('v=')[1].split('&')[0] : val.split('/').pop();
            document.getElementById('player').innerHTML = `<iframe width="100%" height="250" src="https://www.youtube.com/embed/${id}" frameborder="0" allowfullscreen></iframe>`;
        }

        function mulaiSTT(){
            const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
            const rec = new SR(); rec.lang = 'id-ID'; rec.continuous = true;
            rec.onresult = (e) => { 
                let t = ""; for(let i=0; i<e.results.length; i++) t += e.results[i][0].transcript; 
                document.getElementById('outSTT').value = t; 
            };
            rec.start();
        }

        function putar(){ 
            synth.cancel(); 
            const t = document.getElementById('inTTS').value || document.getElementById('outSTT').value;
            const u = new SpeechSynthesisUtterance(t); 
            u.voice = synth.getVoices()[document.getElementById('suara').value]; 
            u.pitch = document.getElementById('pitch').value; 
            u.rate = document.getElementById('speed').value; 
            u.lang = 'id-ID'; synth.speak(u); 
        }
        function jeda(){ synth.pause(); }
        function lanjut(){ synth.resume(); }
        function stop(){ synth.cancel(); }

        function ringkas(){
            const t = document.getElementById('outSTT').value || document.getElementById('inTTS').value;
            document.getElementById('outAI').value = "📝 RINGKASAN MATERI:\\n" + t.substring(0, 500) + "...";
        }

        function buatMindMap(){
            const t = document.getElementById('outSTT').value || document.getElementById('inTTS').value;
            const keywords = t.split(' ').slice(0, 5);
            document.getElementById('outAI').value = "🌿 MIND MAP MATERI:\\n└── " + keywords.join("\\n└── ");
        }

        async function unduhAudioReal() {
            const t = document.getElementById('inTTS').value || document.getElementById('outSTT').value;
            const url = `https://translate.google.com/translate_tts?ie=UTF-8&q=${encodeURIComponent(t.substring(0,250))}&tl=id&client=tw-ob`;
            window.open(url, '_blank');
        }

        function update(){ 
            const data = "LAPORAN LENGKAP\\n===============\\n\\n[MATERI]\\n" + document.getElementById('inTTS').value + "\\n\\n[STT]\\n" + document.getElementById('outSTT').value + "\\n\\n[AI]\\n" + document.getElementById('outAI').value;
            document.getElementById('final').value = data; 
        }

        function unduh(tipe){ 
            update(); 
            const b = new Blob([document.getElementById('final').value], {type:'text/plain'}); 
            const a = document.createElement("a"); a.href=URL.createObjectURL(b); a.download="Laporan."+tipe; a.click(); 
        }

        function loadV(){ const s = document.getElementById("suara"); s.innerHTML = ""; synth.getVoices().forEach((v,i) => { if(v.lang.includes("id")){ let o=document.createElement("option"); o.value=i; o.textContent=v.name; s.appendChild(o); }}); }
        window.speechSynthesis.onvoiceschanged = loadV; setTimeout(loadV, 1000);
    </script>
</body>
</html>
"""

# --- 3. EKSEKUSI ---
components.html(master_kode, height=1200, scrolling=True)

with st.sidebar:
    st.header("🎓 Final Covenant v17")
    st.success("APLIKASI AKTIF!")
