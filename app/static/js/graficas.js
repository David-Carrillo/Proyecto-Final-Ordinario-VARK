/*
 * Gráficas con Chart.js. Responsable: Valeria
 * El dashboard pide los datos a la API REST: /api/v1/estadisticas
 */
const Graficas = (function () {
  const COLORES_VARK = ['#2f6db5', '#e0a100', '#3a9b57', '#a3120a', '#777777'];
  const ROJO = '#a3120a';
  const instancias = {};

  function crear(id, config) {
    const lienzo = document.getElementById(id);
    if (!lienzo) return;
    if (instancias[id]) instancias[id].destroy();
    instancias[id] = new Chart(lienzo, config);
  }

  function barras(id, titulo, etiquetas, valores, colores) {
    const lienzo = document.getElementById(id);
    if (!lienzo) return;
    etiquetas = etiquetas || JSON.parse(lienzo.dataset.etiquetas);
    valores = valores || JSON.parse(lienzo.dataset.valores);
    crear(id, {
      type: 'bar',
      data: { labels: etiquetas, datasets: [{ label: titulo, data: valores, backgroundColor: colores || COLORES_VARK }] },
      options: {
        responsive: true,
        plugins: { legend: { display: false } },
        scales: { y: { beginAtZero: true, ticks: { precision: 0 } } }
      }
    });
  }

  function dona(id, etiquetas, valores, colores) {
    crear(id, {
      type: 'doughnut',
      data: { labels: etiquetas, datasets: [{ data: valores, backgroundColor: colores }] },
      options: { responsive: true, plugins: { legend: { position: 'bottom' } } }
    });
  }

  function dashboard(selector) {
    const $contenedor = $(selector);
    $.getJSON($contenedor.data('api'))
      .done(function (respuesta) {
        const d = respuesta.datos;
        const nombres = { V: 'Visual', A: 'Auditivo', R: 'Lectura/Escritura', K: 'Kinestésico' };

        barras('g-vark-suma', 'Puntos',
          Object.keys(d.vark.suma).map(function (k) { return nombres[k]; }),
          Object.values(d.vark.suma));

        dona('g-vark-dominantes', Object.keys(d.vark.dominantes), Object.values(d.vark.dominantes), COLORES_VARK);

        barras('g-tipos', 'Alumnos', Object.keys(d.personalidad.tipos), Object.values(d.personalidad.tipos), ROJO);

        dona('g-temperamentos', Object.keys(d.personalidad.temperamentos),
          Object.values(d.personalidad.temperamentos), ['#2f6db5', '#a3120a', '#3a9b57', '#e0a100']);

        const l = d.personalidad.letras;
        crear('g-letras', {
          type: 'bar',
          data: {
            labels: ['E / I', 'S / N', 'T / F', 'J / P'],
            datasets: [
              { label: 'E, S, T, J', data: [l.E, l.S, l.T, l.J], backgroundColor: ROJO },
              { label: 'I, N, F, P', data: [l.I, l.N, l.F, l.P], backgroundColor: '#696969' }
            ]
          },
          options: { indexAxis: 'y', responsive: true, scales: { x: { stacked: true, ticks: { precision: 0 } }, y: { stacked: true } } }
        });
      })
      .fail(function () {
        $contenedor.prepend('<div class="col-12"><div class="alert alert-warning">No se pudieron cargar las gráficas.</div></div>');
      });
  }

  return { barras: barras, dashboard: dashboard };
})();
