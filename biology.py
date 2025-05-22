from flask import Flask, render_template_string, request, jsonify
import math

app = Flask(__name__)

# Template HTML dengan CSS
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>BiologyHub - Portal Biologi Indonesia</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #e8f5e8 0%, #f0f8ff 100%);
        }

        header {
            background: linear-gradient(135deg, #2c5530 0%, #4a7c59 100%);
            color: white;
            text-align: center;
            padding: 2rem 0;
            box-shadow: 0 2px 5px rgba(0,0,0,0.1);
        }

        header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
        }

        nav {
            background: #1e3a20;
            padding: 1rem 0;
            position: sticky;
            top: 0;
            z-index: 100;
        }

        nav ul {
            list-style: none;
            display: flex;
            justify-content: center;
            flex-wrap: wrap;
        }

        nav li {
            margin: 0 1rem;
        }

        nav a {
            color: white;
            text-decoration: none;
            padding: 0.5rem 1rem;
            border-radius: 5px;
            transition: background 0.3s;
        }

        nav a:hover {
            background: #4a7c59;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 2rem;
        }

        .section {
            background: white;
            margin: 2rem 0;
            padding: 2rem;
            border-radius: 10px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }

        .section h2 {
            color: #2c5530;
            margin-bottom: 1rem;
            border-bottom: 2px solid #4a7c59;
            padding-bottom: 0.5rem;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }

        .card {
            background: #f8f9fa;
            padding: 1.5rem;
            border-radius: 8px;
            border-left: 4px solid #4a7c59;
        }

        .card h3 {
            color: #2c5530;
            margin-bottom: 0.5rem;
        }

        .calculator {
            background: #fff;
            padding: 1.5rem;
            border-radius: 8px;
            margin: 1rem 0;
            border: 1px solid #ddd;
        }

        .form-group {
            margin: 1rem 0;
        }

        label {
            display: block;
            margin-bottom: 0.5rem;
            font-weight: bold;
            color: #2c5530;
        }

        input, select {
            width: 100%;
            padding: 0.75rem;
            border: 1px solid #ddd;
            border-radius: 5px;
            font-size: 1rem;
        }

        button {
            background: #4a7c59;
            color: white;
            padding: 0.75rem 1.5rem;
            border: none;
            border-radius: 5px;
            cursor: pointer;
            font-size: 1rem;
            transition: background 0.3s;
        }

        button:hover {
            background: #2c5530;
        }

        .result {
            background: #e8f5e8;
            padding: 1rem;
            border-radius: 5px;
            margin-top: 1rem;
            border-left: 4px solid #4a7c59;
        }

        .hidden {
            display: none;
        }

        footer {
            background: #2c5530;
            color: white;
            text-align: center;
            padding: 2rem 0;
            margin-top: 3rem;
        }

        @media (max-width: 768px) {
            .container {
                padding: 1rem;
            }
            
            header h1 {
                font-size: 2rem;
            }
            
            nav ul {
                flex-direction: column;
                align-items: center;
            }
            
            nav li {
                margin: 0.25rem 0;
            }
        }
    </style>
</head>
<body>
    <header>
        <h1>🧬 Biology</h1>
        <p>Portal Lengkap Informasi dan Tools Biologi</p>
    </header>

    <nav>
        <ul>
            <li><a href="#beranda" onclick="showSection('beranda', event)">Beranda</a></li>
            <li><a href="#info-biologi" onclick="showSection('info-biologi', event)">Info Biologi</a></li>
            <li><a href="#kalkulator" onclick="showSection('kalkulator', event)">Kalkulator Bio</a></li>
            <li><a href="#ensiklopedia" onclick="showSection('ensiklopedia', event)">Ensiklopedia</a></li>
            <li><a href="#quiz" onclick="showSection('quiz', event)">Quiz</a></li>
        </ul>
    </nav>

    <div class="container">
        <!-- Beranda -->
        <div id="beranda" class="section">
            <h2>Selamat Datang di BiologyHub</h2>
            <p>Website ini menyediakan berbagai informasi dan tools untuk mempelajari biologi. Fitur yang tersedia:</p>
            <div class="cards">
                <div class="card" style="cursor:pointer" onclick="showSection('info-biologi', event)">
                    <h3>📚 Informasi Biologi</h3>
                    <p>Materi lengkap tentang sel, genetika, ekologi, dan cabang biologi lainnya</p>
                </div>
                <div class="card" style="cursor:pointer" onclick="showSection('kalkulator', event)">
                    <h3>🧮 Kalkulator Biologi</h3>
                    <p>Tools untuk menghitung BMI, frekuensi Hardy-Weinberg, dan konversi unit</p>
                </div>
                <div class="card" style="cursor:pointer" onclick="showSection('ensiklopedia', event)">
                    <h3>🔍 Ensiklopedia</h3>
                    <p>Database lengkap tentang organisme, struktur biologis, dan proses kehidupan</p>
                </div>
                <div class="card" style="cursor:pointer" onclick="showSection('quiz', event)">
                    <h3>🎯 Quiz Interaktif</h3>
                    <p>Uji pengetahuan biologi Anda dengan berbagai pertanyaan menarik</p>
                </div>
            </div>       
         </div>

        <!-- Info Biologi -->
        <div id="info-biologi" class="section hidden">
            <h2>Informasi Biologi</h2>
            <div class="cards">
                <div class="card">
                    <h3>🦠 Biologi Sel</h3>
                    <p><strong>Sel Prokariota:</strong> Tidak memiliki membran inti, materi genetik tersebar di sitoplasma. Contoh: bakteri, archaea.</p>
                    <p><strong>Sel Eukariota:</strong> Memiliki membran inti, organel terspesialisasi. Contoh: sel tumbuhan, hewan, fungi.</p>
                    <p><strong>Organel Penting:</strong> Nucleus (pusat kontrol), mitokondria (powerhouse), ribosom (sintesis protein), retikulum endoplasma (transportasi)</p>
                </div>
                
                <div class="card">
                    <h3>🧬 Genetika</h3>
                    <p><strong>DNA:</strong> Pembawa informasi genetik, struktur double helix, basa nitrogen A-T, G-C</p>
                    <p><strong>Hukum Mendel:</strong> Pemisahan (segregasi) dan pengelompokan bebas (independent assortment)</p>
                    <p><strong>Mutasi:</strong> Perubahan urutan DNA yang dapat bersifat menguntungkan, merugikan, atau netral</p>
                </div>

                <div class="card">
                    <h3>🌿 Fotosintesis</h3>
                    <p><strong>Reaksi Terang:</strong> Terjadi di tilakoid, menghasilkan ATP dan NADPH</p>
                    <p><strong>Siklus Calvin:</strong> Terjadi di stroma, fiksasi CO₂ menjadi glukosa</p>
                    <p><strong>Persamaan:</strong> 6CO₂ + 6H₂O + energi cahaya → C₆H₁₂O₆ + 6O₂</p>
                </div>

                <div class="card">
                    <h3>🌍 Ekologi</h3>
                    <p><strong>Ekosistem:</strong> Interaksi antara komponen biotik dan abiotik</p>
                    <p><strong>Rantai Makanan:</strong> Produsen → Konsumen I → Konsumen II → Dekomposer</p>
                    <p><strong>Siklus Biogeokimia:</strong> Siklus karbon, nitrogen, fosfor, dan air</p>
                </div>

                <div class="card">
                    <h3>🧪 Biokimia</h3>
                    <p><strong>Karbohidrat:</strong> Sumber energi utama (glukosa, sukrosa, pati)</p>
                    <p><strong>Protein:</strong> Enzim, hormon, antibodi (tersusun dari asam amino)</p>
                    <p><strong>Lipid:</strong> Membran sel, cadangan energi (lemak, fosfolipid)</p>
                    <p><strong>Asam Nukleat:</strong> DNA dan RNA (penyimpan dan pembawa informasi genetik)</p>
                </div>

                <div class="card">
                    <h3>🫀 Sistem Tubuh Manusia</h3>
                    <p><strong>Sistem Peredaran Darah:</strong> Jantung, pembuluh darah, darah</p>
                    <p><strong>Sistem Pernapasan:</strong> Paru-paru, trakea, bronkus, alveolus</p>
                    <p><strong>Sistem Pencernaan:</strong> Mulut, lambung, usus, hati, pankreas</p>
                    <p><strong>Sistem Saraf:</strong> Otak, sumsum tulang belakang, saraf tepi</p>
                </div>
            </div>
        </div>

        <!-- Kalkulator -->
        <div id="kalkulator" class="section hidden">
            <h2>Kalkulator Biologi</h2>
            
            <div class="calculator">
                <h3>📏 Kalkulator BMI (Body Mass Index)</h3>
                <div class="form-group">
                    <label for="weight">Berat Badan (kg):</label>
                    <input type="number" id="weight" step="0.1" placeholder="Masukkan berat badan">
                </div>
                <div class="form-group">
                    <label for="height">Tinggi Badan (cm):</label>
                    <input type="number" id="height" step="0.1" placeholder="Masukkan tinggi badan">
                </div>
                <button onclick="calculateBMI()">Hitung BMI</button>
                <div id="bmi-result" class="result hidden"></div>
            </div>

            <div class="calculator">
                <h3>🧬 Kalkulator Hardy-Weinberg</h3>
                <p>Menghitung frekuensi alel dalam populasi yang seimbang</p>
                <div class="form-group">
                    <label for="freq-p">Frekuensi Alel Dominan (p):</label>
                    <input type="number" id="freq-p" step="0.01" min="0" max="1" placeholder="0.0 - 1.0">
                </div>
                <button onclick="calculateHardyWeinberg()">Hitung Frekuensi Genotip</button>
                <div id="hw-result" class="result hidden"></div>
            </div>

            <div class="calculator">
                <h3>🔬 Konverter Unit Mikroskopis</h3>
                <div class="form-group">
                    <label for="micro-value">Nilai:</label>
                    <input type="number" id="micro-value" step="0.001" placeholder="Masukkan nilai">
                </div>
                <div class="form-group">
                    <label for="from-unit">Dari Unit:</label>
                    <select id="from-unit">
                        <option value="mm">Milimeter (mm)</option>
                        <option value="um">Mikrometer (μm)</option>
                        <option value="nm">Nanometer (nm)</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="to-unit">Ke Unit:</label>
                    <select id="to-unit">
                        <option value="mm">Milimeter (mm)</option>
                        <option value="um">Mikrometer (μm)</option>
                        <option value="nm">Nanometer (nm)</option>
                    </select>
                </div>
                <button onclick="convertUnits()">Konversi</button>
                <div id="convert-result" class="result hidden"></div>
            </div>
        </div>

        <!-- Ensiklopedia -->
        <div id="ensiklopedia" class="section hidden">
            <h2>Ensiklopedia Biologi</h2>
            <div class="cards">
                <div class="card">
                    <h3>🦋 Kingdom Animalia</h3>
                    <p><strong>Vertebrata:</strong> Mammalia, Aves, Reptilia, Amphibia, Pisces</p>
                    <p><strong>Invertebrata:</strong> Arthropoda, Mollusca, Cnidaria, Porifera</p>
                    <p><strong>Ciri:</strong> Heterotrof, bergerak aktif, reproduksi seksual</p>
                </div>

                <div class="card">
                    <h3>🌱 Kingdom Plantae</h3>
                    <p><strong>Gymnospermae:</strong> Tumbuhan berbiji terbuka (pinus, cemara)</p>
                    <p><strong>Angiospermae:</strong> Tumbuhan berbunga (dikotil, monokotil)</p>
                    <p><strong>Ciri:</strong> Autotrof, fotosintesis, dinding sel selulosa</p>
                </div>

                <div class="card">
                    <h3>🍄 Kingdom Fungi</h3>
                    <p><strong>Struktur:</strong> Hifa, miselium, spora</p>
                    <p><strong>Reproduksi:</strong> Aseksual (fragmentasi, budding) dan seksual</p>
                    <p><strong>Peran:</strong> Dekomposer, simbiosis (mikoriza), industri makanan</p>
                </div>

                <div class="card">
                    <h3>🦠 Kingdom Monera</h3>
                    <p><strong>Bakteri:</strong> Prokariota, dinding sel peptidoglikan</p>
                    <p><strong>Archaea:</strong> Prokariota, lingkungan ekstrem</p>
                    <p><strong>Bentuk:</strong> Kokus (bulat), basil (batang), spiral</p>
                </div>

                <div class="card">
                    <h3>🦠 Kingdom Protista</h3>
                    <p><strong>Protozoa:</strong> Amoeba, Paramaecium, Plasmodium</p>
                    <p><strong>Alga:</strong> Chlorophyta, Rhodophyta, Phaeophyta</p>
                    <p><strong>Ciri:</strong> Eukariota, sebagian besar uniseluler</p>
                </div>

                <div class="card">
                    <h3>🧬 Biomolekul Penting</h3>
                    <p><strong>ATP:</strong> Adenosin trifosfat, mata uang energi sel</p>
                    <p><strong>Hemoglobin:</strong> Protein pembawa oksigen dalam darah</p>
                    <p><strong>Klorofil:</strong> Pigmen hijau untuk fotosintesis</p>
                    <p><strong>Enzim:</strong> Katalis biologis (amilase, pepsin, tripsin)</p>
                </div>
            </div>
        </div>

        <!-- Quiz -->
        <div id="quiz" class="section hidden">
            <h2>Quiz Biologi</h2>
            <div class="calculator">
                <div id="quiz-container">
                    <div id="question-container">
                        <h3 id="question-text">Klik "Mulai Quiz" untuk memulai!</h3>
                        <div id="options-container"></div>
                    </div>
                    <button id="quiz-btn" onclick="startQuiz()">Mulai Quiz</button>
                    <div id="quiz-result" class="result hidden"></div>
                </div>
            </div>
        </div>
    </div>

    <footer>
        <p>&copy; 2024 BiologyHub - Portal Biologi Indonesia</p>
        <p>Dibuat dengan Python Flask, HTML, dan CSS</p>
    </footer>

    <script>
        // Navigation
    function showSection(sectionId, event) {
        if (event) event.preventDefault(); // Tambahkan ini
        const sections = document.querySelectorAll('.section');
        sections.forEach(section => section.classList.add('hidden'));
        document.getElementById(sectionId).classList.remove('hidden');
    }

        // BMI Calculator
        function calculateBMI() {
            const weight = parseFloat(document.getElementById('weight').value);
            const height = parseFloat(document.getElementById('height').value) / 100; // convert to meters
            
            if (!weight || !height) {
                alert('Mohon masukkan berat dan tinggi badan yang valid!');
                return;
            }
            
            const bmi = weight / (height * height);
            let category, advice;
            
            if (bmi < 18.5) {
                category = 'Kurus';
                advice = 'Konsultasikan dengan dokter untuk program penambahan berat badan yang sehat.';
            } else if (bmi < 25) {
                category = 'Normal';
                advice = 'Pertahankan pola hidup sehat dengan diet seimbang dan olahraga teratur.';
            } else if (bmi < 30) {
                category = 'Overweight';
                advice = 'Disarankan untuk mengurangi berat badan dengan diet dan olahraga.';
            } else {
                category = 'Obesitas';
                advice = 'Konsultasikan dengan dokter untuk program penurunan berat badan.';
            }
            
            const resultDiv = document.getElementById('bmi-result');
            resultDiv.innerHTML = `
                <h4>Hasil BMI:</h4>
                <p><strong>BMI: ${bmi.toFixed(1)}</strong></p>
                <p><strong>Kategori: ${category}</strong></p>
                <p>${advice}</p>
            `;
            resultDiv.classList.remove('hidden');
        }

        // Hardy-Weinberg Calculator
        function calculateHardyWeinberg() {
            const p = parseFloat(document.getElementById('freq-p').value);
            
            if (isNaN(p) || p < 0 || p > 1) {
                alert('Frekuensi alel harus antara 0 dan 1!');
                return;
            }
            
            const q = 1 - p;
            const pp = p * p; // homozigot dominan
            const pq = 2 * p * q; // heterozigot
            const qq = q * q; // homozigot resesif
            
            const resultDiv = document.getElementById('hw-result');
            resultDiv.innerHTML = `
                <h4>Hasil Hardy-Weinberg:</h4>
                <p><strong>Frekuensi alel dominan (p): ${p.toFixed(3)}</strong></p>
                <p><strong>Frekuensi alel resesif (q): ${q.toFixed(3)}</strong></p>
                <p><strong>Genotip AA (p²): ${pp.toFixed(3)} (${(pp*100).toFixed(1)}%)</strong></p>
                <p><strong>Genotip Aa (2pq): ${pq.toFixed(3)} (${(pq*100).toFixed(1)}%)</strong></p>
                <p><strong>Genotip aa (q²): ${qq.toFixed(3)} (${(qq*100).toFixed(1)}%)</strong></p>
            `;
            resultDiv.classList.remove('hidden');
        }

        // Unit Converter
        function convertUnits() {
            const value = parseFloat(document.getElementById('micro-value').value);
            const fromUnit = document.getElementById('from-unit').value;
            const toUnit = document.getElementById('to-unit').value;
            
            if (!value) {
                alert('Mohon masukkan nilai yang valid!');
                return;
            }
            
            // Convert to nanometers first (base unit)
            let valueInNm;
            switch(fromUnit) {
                case 'mm': valueInNm = value * 1000000; break;
                case 'um': valueInNm = value * 1000; break;
                case 'nm': valueInNm = value; break;
            }
            
            // Convert from nanometers to target unit
            let result;
            switch(toUnit) {
                case 'mm': result = valueInNm / 1000000; break;
                case 'um': result = valueInNm / 1000; break;
                case 'nm': result = valueInNm; break;
            }
            
            const resultDiv = document.getElementById('convert-result');
            resultDiv.innerHTML = `
                <h4>Hasil Konversi:</h4>
                <p><strong>${value} ${fromUnit} = ${result.toExponential(3)} ${toUnit}</strong></p>
            `;
            resultDiv.classList.remove('hidden');
        }

        // Quiz System
        const quizQuestions = [
            {
                question: "Apa fungsi utama mitokondria dalam sel?",
                options: ["Sintesis protein", "Produksi energi (ATP)", "Pencernaan intraseluler", "Penyimpanan DNA"],
                correct: 1
            },
            {
                question: "Proses fotosintesis menghasilkan?",
                options: ["CO₂ dan H₂O", "Glukosa dan O₂", "ATP dan NADH", "Protein dan lemak"],
                correct: 1
            },
            {
                question: "Kingdom manakah yang termasuk organisme prokariotik?",
                options: ["Plantae", "Animalia", "Monera", "Fungi"],
                correct: 2
            },
            {
                question: "Bagian DNA yang mengkode protein disebut?",
                options: ["Intron", "Ekson", "Promoter", "Terminator"],
                correct: 1
            },
            {
                question: "Organel mana yang bertanggung jawab untuk sintesis protein?",
                options: ["Nukleus", "Ribosom", "Lisosom", "Vakuola"],
                correct: 1
            }
        ];

        let currentQuestion = 0;
        let score = 0;
        let quizActive = false;

        function startQuiz() {
            currentQuestion = 0;
            score = 0;
            quizActive = true;
            document.getElementById('quiz-result').classList.add('hidden');
            document.getElementById('quiz-btn').textContent = 'Jawab';
            document.getElementById('quiz-btn').onclick = checkAnswer;
            showQuestion();
        }

        function showQuestion() {
            if (currentQuestion < quizQuestions.length) {
                const question = quizQuestions[currentQuestion];
                document.getElementById('question-text').textContent = `${currentQuestion + 1}. ${question.question}`;
                
                const optionsContainer = document.getElementById('options-container');
                optionsContainer.innerHTML = '';
                
                question.options.forEach((option, index) => {
                    const optionElement = document.createElement('div');
                    optionElement.innerHTML = `
                        <input type="radio" name="answer" value="${index}" id="option${index}">
                        <label for="option${index}" style="margin-left: 10px;">${option}</label>
                    `;
                    optionsContainer.appendChild(optionElement);
                });
            } else {
                endQuiz();
            }
        }

        function checkAnswer() {
            const selectedAnswer = document.querySelector('input[name="answer"]:checked');
            if (!selectedAnswer) {
                alert('Pilih jawaban terlebih dahulu!');
                return;
            }
            
            if (parseInt(selectedAnswer.value) === quizQuestions[currentQuestion].correct) {
                score++;
            }
            
            currentQuestion++;
            showQuestion();
        }

        function endQuiz() {
            const percentage = (score / quizQuestions.length) * 100;
            let grade;
            
            if (percentage >= 80) grade = 'Sangat Baik!';
            else if (percentage >= 60) grade = 'Baik';
            else if (percentage >= 40) grade = 'Cukup';
            else grade = 'Perlu Belajar Lagi';
            
            document.getElementById('question-text').textContent = 'Quiz Selesai!';
            document.getElementById('options-container').innerHTML = '';
            
            const resultDiv = document.getElementById('quiz-result');
            resultDiv.innerHTML = `
                <h4>Hasil Quiz:</h4>
                <p><strong>Skor: ${score}/${quizQuestions.length} (${percentage.toFixed(1)}%)</strong></p>
                <p><strong>Grade: ${grade}</strong></p>
            `;
            resultDiv.classList.remove('hidden');
            
            document.getElementById('quiz-btn').textContent = 'Mulai Lagi';
            document.getElementById('quiz-btn').onclick = startQuiz;
        }

        // Initialize page
        document.addEventListener('DOMContentLoaded', function() {
            showSection('beranda');
        });
    </script>
</body>
</html>
"""

@app.route('/')
def home():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/calculate-bmi', methods=['POST'])
def calculate_bmi_api():
    data = request.json
    weight = data.get('weight')
    height = data.get('height') / 100  # convert to meters
    
    if not weight or not height:
        return jsonify({'error': 'Invalid input'}), 400
    
    bmi = weight / (height * height)
    
    if bmi < 18.5:
        category = 'Kurus'
    elif bmi < 25:
        category = 'Normal'
    elif bmi < 30:
        category = 'Overweight'
    else:
        category = 'Obesitas'
    
    return jsonify({
        'bmi': round(bmi, 1),
        'category': category
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)