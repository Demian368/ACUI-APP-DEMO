<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sistema Acuícola Pro - Cachama</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf-autotable/3.5.25/jspdf.plugin.autotable.min.js"></script>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        body { font-family: 'Inter', sans-serif; }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body class="bg-slate-50 text-slate-800 min-h-screen flex flex-col">

    <!-- Top Navigation -->
    <nav class="bg-slate-900 text-white px-6 py-4 flex items-center justify-between shadow-md">
        <div class="flex items-center space-x-3">
            <i class="fa-solid fa-fish-fins text-2xl text-cyan-400"></i>
            <span class="text-xl font-bold tracking-wide">AcuiTech <span class="text-xs bg-cyan-500 text-slate-900 px-2 py-0.5 rounded font-semibold">Cachama PRO</span></span>
        </div>
        <div class="flex items-center space-x-4">
            <span class="text-sm text-slate-400"><i class="fa-solid fa-location-dot mr-1 text-cyan-400"></i> Estanque Principal B3</span>
            <div class="w-8 h-8 rounded-full bg-cyan-700 flex items-center justify-center font-bold text-sm">AC</div>
        </div>
    </nav>

    <div class="flex flex-1 overflow-hidden">
        <!-- Sidebar -->
        <aside class="w-64 bg-white border-r border-slate-200 p-4 flex flex-col justify-between hidden md:flex">
            <div class="space-y-1">
                <button onclick="switchTab('dashboard')" class="tab-btn w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition active-tab bg-cyan-50 text-cyan-700">
                    <i class="fa-solid fa-chart-pie w-5"></i>
                    <span>Panel General</span>
                </button>
                <button onclick="switchTab('system-flow')" class="tab-btn w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition text-slate-600 hover:bg-slate-100">
                    <i class="fa-solid fa-diagram-project w-5"></i>
                    <span>Flujo del Sistema</span>
                </button>
                <button onclick="switchTab('feed-manager')" class="tab-btn w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition text-slate-600 hover:bg-slate-100">
                    <i class="fa-solid fa-bowl-food w-5"></i>
                    <span>Control de Alimentación</span>
                </button>
                <button onclick="switchTab('water-quality')" class="tab-btn w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition text-slate-600 hover:bg-slate-100">
                    <i class="fa-solid fa-droplet w-5"></i>
                    <span>Calidad del Agua</span>
                </button>
                <button onclick="switchTab('bitacora')" class="tab-btn w-full flex items-center space-x-3 px-4 py-3 rounded-lg text-sm font-medium transition text-slate-600 hover:bg-slate-100">
                    <i class="fa-solid fa-book w-5"></i>
                    <span>Bitácora y Reportes</span>
                </button>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-200">
                <div class="flex items-center justify-between mb-2">
                    <span class="text-xs font-bold text-slate-500 uppercase">Estado del Sistema</span>
                    <span class="flex h-2 w-2 relative">
                        <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                        <span class="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
                    </span>
                </div>
                <div class="text-xs text-slate-600 space-y-1">
                    <p><span class="font-semibold text-slate-800">Oxígeno:</span> 5.8 mg/L (Óptimo)</p>
                    <p><span class="font-semibold text-slate-800">Biomasa Est.</span> 1,420 kg</p>
                </div>
            </div>
        </aside>

        <!-- Main Content Area -->
        <main class="flex-1 overflow-y-auto p-6 bg-slate-100">

            <!-- TAB 1: DASHBOARD -->
            <div id="dashboard" class="tab-content active space-y-6">
                <!-- Top Stats -->
                <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Biomasa Actual</p>
                            <h3 class="text-2xl font-bold text-slate-800 mt-1">1,420 <span class="text-sm font-normal text-slate-500">kg</span></h3>
                        </div>
                        <div class="w-12 h-12 rounded-lg bg-cyan-100 text-cyan-600 flex items-center justify-center text-xl">
                            <i class="fa-solid fa-weight-scale"></i>
                        </div>
                    </div>
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Alimento Suministrado</p>
                            <h3 class="text-2xl font-bold text-slate-800 mt-1">45.5 <span class="text-sm font-normal text-slate-500">kg/día</span></h3>
                        </div>
                        <div class="w-12 h-12 rounded-lg bg-amber-100 text-amber-600 flex items-center justify-center text-xl">
                            <i class="fa-solid fa-sack-dollar"></i>
                        </div>
                    </div>
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Conversión Alim. (FCA)</p>
                            <h3 class="text-2xl font-bold text-emerald-600 mt-1">1.45</h3>
                        </div>
                        <div class="w-12 h-12 rounded-lg bg-emerald-100 text-emerald-600 flex items-center justify-center text-xl">
                            <i class="fa-solid fa-chart-line"></i>
                        </div>
                    </div>
                    <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm flex items-center justify-between">
                        <div>
                            <p class="text-sm font-medium text-slate-500">Temp. Promedio Agua</p>
                            <h3 class="text-2xl font-bold text-slate-800 mt-1">28.4 <span class="text-sm font-normal text-slate-500">°C</span></h3>
                        </div>
                        <div class="w-12 h-12 rounded-lg bg-rose-100 text-rose-600 flex items-center justify-center text-xl">
                            <i class="fa-solid fa-temperature-half"></i>
                        </div>
                    </div>
                </div>

                <!-- Charts Row -->
                <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <h4 class="font-bold text-slate-800 mb-4">Crecimiento de Biomasa vs. Alimento</h4>
                        <canvas id="biomasaChart" height="250"></canvas>
                    </div>
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                        <h4 class="font-bold text-slate-800 mb-4">Parámetros de Calidad del Agua</h4>
                        <canvas id="aguaChart" height="250"></canvas>
                    </div>
                </div>
            </div>

            <!-- TAB 2: SISTEMA ACUÍCOLA (FLUJO) -->
            <div id="system-flow" class="tab-content space-y-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h2 class="text-xl font-bold text-slate-800 mb-2">Arquitectura del Sistema Acuícola</h2>
                    <p class="text-sm text-slate-500 mb-6">Modelo conceptual para el cultivo y nutrición de Cachama (*Piaractus brachypomus*).</p>

                    <div class="grid grid-cols-1 md:grid-cols-3 gap-6">
                        <!-- Entradas -->
                        <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
                            <div class="flex items-center space-x-2 text-emerald-600 mb-3">
                                <i class="fa-solid fa-right-to-bracket font-bold"></i>
                                <h3 class="font-bold text-slate-800">Entradas del Sistema</h3>
                            </div>
                            <ul class="space-y-2 text-sm">
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-water text-cyan-500 mr-2"></i> Agua dulce (controlada)</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-fish text-amber-600 mr-2"></i> Alevinos de Cachama</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-cubes text-emerald-600 mr-2"></i> Alimento balanceado extruido</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-apple-whole text-red-500 mr-2"></i> Suplementos orgánicos / Frutas</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-bolt text-yellow-500 mr-2"></i> Energía y Mano de obra</li>
                            </ul>
                        </div>

                        <!-- Procesos -->
                        <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
                            <div class="flex items-center space-x-2 text-cyan-600 mb-3">
                                <i class="fa-solid fa-gears font-bold"></i>
                                <h3 class="font-bold text-slate-800">Procesos Clave</h3>
                            </div>
                            <ul class="space-y-2 text-sm">
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100"><span class="font-bold text-cyan-600 mr-1">1.</span> Preparación y encalado de estanques</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100"><span class="font-bold text-cyan-600 mr-1">2.</span> Siembra y aclimatación</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100"><span class="font-bold text-cyan-600 mr-1">3.</span> Cálculo de tasa de alimentación</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100"><span class="font-bold text-cyan-600 mr-1">4.</span> Suministro fraccionado de alimento</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100"><span class="font-bold text-cyan-600 mr-1">5.</span> Biometrías periódicas</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100"><span class="font-bold text-cyan-600 mr-1">6.</span> Monitoreo fisicoquímico</li>
                            </ul>
                        </div>

                        <!-- Salidas -->
                        <div class="bg-slate-50 p-4 rounded-lg border border-slate-200">
                            <div class="flex items-center space-x-2 text-indigo-600 mb-3">
                                <i class="fa-solid fa-right-from-bracket font-bold"></i>
                                <h3 class="font-bold text-slate-800">Salidas del Sistema</h3>
                            </div>
                            <ul class="space-y-2 text-sm">
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-fish text-indigo-600 mr-2"></i> Biomasa de Cachama comercial</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-file-invoice text-slate-600 mr-2"></i> Registros de Conversión (FCA)</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-chart-pie text-cyan-500 mr-2"></i> Historial de calidad de agua</li>
                                <li class="bg-white p-2 rounded shadow-sm border border-slate-100 flex items-center"><i class="fa-solid fa-biohazard text-amber-500 mr-2"></i> Efluentes y materia orgánica</li>
                            </ul>
                        </div>
                    </div>
                </div>
            </div>

            <!-- TAB 3: CONTROL DE ALIMENTACIÓN -->
            <div id="feed-manager" class="tab-content space-y-6">
                <div class="grid grid-cols-1 lg:grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm lg:col-span-1">
                        <h3 class="font-bold text-slate-800 mb-4">Calcular Ración Diaria</h3>
                        <form id="feedForm" class="space-y-4">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Biomasa Total Estimada (kg)</label>
                                <input type="number" id="biomassInput" value="1420" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm focus:ring-cyan-500 focus:border-cyan-500">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">% Proteína Requerida</label>
                                <select id="proteinSelect" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm focus:ring-cyan-500 focus:border-cyan-500">
                                    <option value="32">32% - Iniciación (Alevinos)</option>
                                    <option value="28" selected>28% - Levante (Juveniles)</option>
                                    <option value="24">24% - Engorde Final</option>
                                </select>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Tasa de Alimentación (% Biomasa)</label>
                                <input type="number" id="rateInput" step="0.1" value="3.2" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm focus:ring-cyan-500 focus:border-cyan-500">
                            </div>
                            <button type="button" onclick="calcularAlimento()" class="w-full bg-cyan-600 text-white py-2.5 rounded font-semibold text-sm hover:bg-cyan-700 transition">Calcular Ración</button>
                        </form>

                        <div class="mt-6 p-4 bg-slate-50 rounded-lg border border-slate-200">
                            <p class="text-xs text-slate-500 mb-1">Resultado del Cálculo:</p>
                            <h4 class="text-xl font-bold text-cyan-600"><span id="resultadoRacion">45.44</span> <span class="text-sm font-normal text-slate-600">kg de alimento/día</span></h4>
                            <p class="text-[11px] text-slate-500 mt-2">Dividir en 3 tomas diarias (Mañana, Mediodía, Tarde).</p>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm lg:col-span-2">
                        <h3 class="font-bold text-slate-800 mb-4">Registro Rápido de Suministro</h3>
                        <form id="registroAlimentoForm" onsubmit="registrarAlimento(event)" class="space-y-4">
                            <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
                                <div>
                                    <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Fecha</label>
                                    <input type="date" id="logDate" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Cantidad Suministrada (kg)</label>
                                    <input type="number" id="logQty" step="0.5" required class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                                </div>
                                <div>
                                    <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Tipo de Alimento</label>
                                    <select id="logType" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                                        <option value="Extruido Comercial">Extruido Comercial</option>
                                        <option value="Fruta Local">Fruta Local</option>
                                        <option value="Complemento Agrícola">Complemento Agrícola</option>
                                    </select>
                                </div>
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Observaciones</label>
                                <input type="text" id="logObs" placeholder="Ej. Consumo total en 15 minutos..." class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                            </div>
                            <button type="submit" class="bg-emerald-600 text-white px-6 py-2.5 rounded font-semibold text-sm hover:bg-emerald-700 transition"><i class="fa-solid fa-plus mr-2"></i>Registrar en Bitácora</button>
                        </form>
                    </div>
                </div>
            </div>

            <!-- TAB 4: CALIDAD DEL AGUA -->
            <div id="water-quality" class="tab-content space-y-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <h3 class="font-bold text-slate-800 mb-4">Registro de Parámetros Físico-Químicos</h3>
                    <form id="aguaForm" onsubmit="registrarAgua(event)" class="grid grid-cols-1 md:grid-cols-5 gap-4">
                        <div>
                            <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Fecha</label>
                            <input type="date" id="aguaDate" class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Oxígeno Disuelto (mg/L)</label>
                            <input type="number" step="0.1" id="aguaO2" required class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Temperatura (°C)</label>
                            <input type="number" step="0.1" id="aguaTemp" required class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">pH</label>
                            <input type="number" step="0.1" id="aguaPH" required class="w-full p-2.5 bg-slate-50 border border-slate-300 rounded text-sm">
                        </div>
                        <div class="flex items-end">
                            <button type="submit" class="w-full bg-cyan-600 text-white py-2.5 rounded font-semibold text-sm hover:bg-cyan-700 transition">Guardar Parámetros</button>
                        </div>
                    </form>
                </div>
            </div>

            <!-- TAB 5: BITÁCORA Y REPORTES -->
            <div id="bitacora" class="tab-content space-y-6">
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex items-center justify-between mb-4">
                        <div>
                            <h3 class="font-bold text-slate-800">Bitácora de Eventos y Controles</h3>
                            <p class="text-sm text-slate-500">Historial de alimentación y calidad del agua.</p>
                        </div>
                        <div class="flex space-x-2">
                            <button onclick="exportarCSV()" class="bg-slate-800 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-slate-900 transition flex items-center"><i class="fa-solid fa-file-csv mr-2"></i>Exportar CSV</button>
                            <button onclick="exportarPDF()" class="bg-rose-600 text-white px-4 py-2 rounded text-sm font-semibold hover:bg-rose-700 transition flex items-center"><i class="fa-solid fa-file-pdf mr-2"></i>Exportar PDF</button>
                            <button onclick="vaciarBitacora()" class="bg-red-100 text-red-600 px-4 py-2 rounded text-sm font-semibold hover:bg-red-200 transition flex items-center"><i class="fa-solid fa-trash mr-2"></i>Vaciar</button>
                        </div>
                    </div>

                    <div class="overflow-x-auto">
                        <table class="w-full text-left text-sm text-slate-600">
                            <thead class="bg-slate-50 text-slate-700 uppercase font-semibold text-xs border-b border-slate-200">
                                <tr>
                                    <th class="py-3 px-4">Fecha</th>
                                    <th class="py-3 px-4">Tipo</th>
                                    <th class="py-3 px-4">Detalles</th>
                                    <th class="py-3 px-4">Observaciones</th>
                                </tr>
                            </thead>
                            <tbody id="bitacoraBody" class="divide-y divide-slate-100">
                                <!-- Dinámico -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

        </main>
    </div>

    <script>
        // Datos iniciales simulados
        let bitacoraData = [
            { id: 1, fecha: new Date().toISOString().split('T')[0], tipo: 'Alimentación', detalles: '45.0 kg - Extruido Comercial', obs: 'Consumo normal matutino' },
            { id: 2, fecha: new Date().toISOString().split('T')[0], tipo: 'Calidad Agua', detalles: 'O2: 6.0 mg/L | Temp: 28°C | pH: 7.2', obs: 'Sin novedades' }
        ];

        // Inicialización de la página
        window.onload = function() {
            document.getElementById('logDate').value = new Date().toISOString().split('T')[0];
            document.getElementById('aguaDate').value = new Date().toISOString().split('T')[0];
            renderCharts();
            renderBitacora();
        };

        // Cambio de pestañas
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(tc => tc.classList.remove('active'));
            document.querySelectorAll('.tab-btn').forEach(tb => {
                tb.classList.remove('bg-cyan-50', 'text-cyan-700');
                tb.classList.add('text-slate-600');
            });
            document.getElementById(tabId).classList.add('active');
            event.currentTarget.classList.add('bg-cyan-50', 'text-cyan-700');
            event.currentTarget.classList.remove('text-slate-600');
        }

        // Cálculo de alimento
        function calcularAlimento() {
            const biomasa = parseFloat(document.getElementById('biomassInput').value);
            const tasa = parseFloat(document.getElementById('rateInput').value);
            const resultado = (biomasa * (tasa / 100)).toFixed(2);
            document.getElementById('resultadoRacion').innerText = resultado;
        }

        // Registrar Alimentación
        function registrarAlimento(e) {
            e.preventDefault();
            const fecha = document.getElementById('logDate').value;
            const qty = document.getElementById('logQty').value;
            const type = document.getElementById('logType').value;
            const obs = document.getElementById('logObs').value;

            bitacoraData.push({
                id: Date.now(),
                fecha: fecha,
                tipo: 'Alimentación',
                detalles: `${qty} kg - ${type}`,
                obs: obs
            });

            renderBitacora();
            document.getElementById('registroAlimentoForm').reset();
            document.getElementById('logDate').value = new Date().toISOString().split('T')[0];
            alert("Registro de alimentación guardado.");
        }

        // Registrar Agua
        function registrarAgua(e) {
            e.preventDefault();
            const fecha = document.getElementById('aguaDate').value;
            const o2 = document.getElementById('aguaO2').value;
            const temp = document.getElementById('aguaTemp').value;
            const ph = document.getElementById('aguaPH').value;

            bitacoraData.push({
                id: Date.now(),
                fecha: fecha,
                tipo: 'Calidad Agua',
                detalles: `O2: ${o2} mg/L | Temp: ${temp}°C | pH: ${ph}`,
                obs: 'Control rutinario'
            });

            renderBitacora();
            document.getElementById('aguaForm').reset();
            document.getElementById('aguaDate').value = new Date().toISOString().split('T')[0];
            alert("Parámetros de agua registrados.");
        }

        // Renderizar Bitácora
        function renderBitacora() {
            const tbody = document.getElementById('bitacoraBody');
            tbody.innerHTML = '';
            bitacoraData.forEach(item => {
                const badgeClass = item.tipo === 'Alimentación' ? 'bg-amber-100 text-amber-800' : 'bg-cyan-100 text-cyan-800';
                tbody.innerHTML += `
                    <tr>
                        <td class="py-3 px-4 font-medium">${item.fecha}</td>
                        <td class="py-3 px-4"><span class="px-2 py-1 rounded-full text-xs font-semibold ${badgeClass}">${item.tipo}</span></td>
                        <td class="py-3 px-4">${item.detalles}</td>
                        <td class="py-3 px-4 text-slate-500">${item.obs}</td>
                    </tr>
                `;
            });
        }

        // Vaciar Bitácora
        function vaciarBitacora() {
            if(confirm("¿Estás seguro de vaciar todo el historial?")) {
                bitacoraData = [];
                renderBitacora();
            }
        }

        // Exportar a CSV
        function exportarCSV() {
            let csvContent = "data:text/csv;charset=utf-8,Fecha,Tipo,Detalles,Observaciones\n";
            bitacoraData.forEach(e => {
                csvContent += `"${e.fecha}","${e.tipo}","${e.detalles}","${e.obs}"\n`;
            });
            const encodedUri = encodeURI(csvContent);
            const link = document.createElement("a");
            link.setAttribute("href", encodedUri);
            link.setAttribute("download", "bitacora_acuicola.csv");
            document.body.appendChild(link);
            link.click();
            document.body.removeChild(link);
        }

        // Exportar a PDF
        function exportarPDF() {
            const { jsPDF } = window.jspdf;
            const doc = new jsPDF();
            doc.text("Bitácora de Control Acuícola - Cachama", 14, 16);
            const headers = [["Fecha", "Tipo", "Detalles", "Observaciones"]];
            const data = bitacoraData.map(e => [e.fecha, e.tipo, e.detalles, e.obs]);
            doc.autoTable({ head: headers, body: data, startY: 22 });
            doc.save("bitacora_acuicola.pdf");
        }

        // Gráficos con Chart.js
        let chartBiomasa, chartAgua;
        function renderCharts() {
            const ctxBiomasa = document.getElementById('biomasaChart').getContext('2d');
            chartBiomasa = new Chart(ctxBiomasa, {
                type: 'line',
                data: {
                    labels: ['Sem 1', 'Sem 2', 'Sem 3', 'Sem 4', 'Sem 5', 'Sem 6'],
                    datasets: [{
                        label: 'Biomasa Estimada (kg)',
                        data: [200, 450, 750, 1000, 1250, 1420],
                        borderColor: '#0284c7',
                        tension: 0.1,
                        fill: true,
                        backgroundColor: 'rgba(2, 132, 199, 0.1)'
                    }, {
                        label: 'Alimento Diario (kg)',
                        data: [10, 20, 35, 45, 42, 45],
                        borderColor: '#f59e0b',
                        tension: 0.1
                    }]
                },
                options: { responsive: true, maintainAspectRatio: false }
            });

            const ctxAgua = document.getElementById('aguaChart').getContext('2d');
            chartAgua = new Chart(ctxAgua, {
                type: 'line',
                data: {
                    labels: ['Lun', 'Mar', 'Mié', 'Jue', 'Vie', 'Sáb', 'Dom'],
                    datasets: [{
                        label: 'Oxígeno Disuelto (mg/L)',
                        data: [6.2, 5.9, 6.0, 5.8, 6.1, 5.9, 5.8],
                        borderColor: '#10b981',
                        yAxisID: 'y'
                    }, {
                        label: 'Temperatura (°C)',
                        data: [27.5, 28.0, 28.2, 28.4, 27.9, 28.1, 28.4],
                        borderColor: '#ef4444',
                        yAxisID: 'y1'
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    scales: {
                        y: { type: 'linear', position: 'left', min: 0, max: 10 },
                        y1: { type: 'linear', position: 'right', min: 20, max: 35, grid: { drawOnChartArea: false } }
                    }
                }
            });
        }
    </script>
</body>
</html>