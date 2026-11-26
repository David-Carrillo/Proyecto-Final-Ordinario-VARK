/*
 * Validación del test de personalidad con jQuery. Responsable: Valeria
 * Reglas del PDF: en cada renglón se reparten 10 puntos entre las dos frases,
 * con números enteros de 0 a 10 y SIN usar el 5.
 * El alumno escribe los puntos de la izquierda y los de la derecha = 10 - izquierda.
 */
$(function () {
  const $form = $('#form-personalidad');

  function valorValido(texto) {
    if (!/^\d{1,2}$/.test(texto)) return false;
    const n = parseInt(texto, 10);
    return n >= 0 && n <= 10 && n !== 5;
  }

  function actualizarPar($fila) {
    const $a = $fila.find('.puntos-a');
    const $b = $fila.find('.puntos-b');
    const texto = $.trim($a.val());
    if (texto === '') {
      $b.val('');
      $a.removeClass('is-invalid');
      return;
    }
    const valido = valorValido(texto);
    $a.toggleClass('is-invalid', !valido);
    $b.val(valido ? 10 - parseInt(texto, 10) : '');
  }

  function actualizarTotales() {
    let tipo = '';
    $form.find('.dimension').each(function () {
      let totalA = 0, totalB = 0, completos = 0;
      const $filas = $(this).find('.par');
      $filas.each(function () {
        const a = $(this).find('.puntos-a').val();
        const b = $(this).find('.puntos-b').val();
        if (a !== '' && b !== '') {
          totalA += parseInt(a, 10);
          totalB += parseInt(b, 10);
          completos++;
        }
      });
      $(this).find('.total-a').text(totalA);
      $(this).find('.total-b').text(totalB);
      if (completos === $filas.length) {
        // En empate gana la segunda letra (I, N, F, P), igual que en el servidor
        tipo += totalA > totalB ? $(this).data('a') : $(this).data('b');
      } else {
        tipo += '?';
      }
    });
    $('#tipo-preliminar').text(tipo);
  }

  $form.on('input', '.puntos-a', function () {
    actualizarPar($(this).closest('.par'));
    actualizarTotales();
  });

  $form.on('submit', function (e) {
    const errores = validarDatosAlumno($form);
    let vacios = 0, invalidos = 0;
    $form.find('.par').each(function () {
      const texto = $.trim($(this).find('.puntos-a').val());
      if (texto === '') {
        vacios++;
        $(this).find('.puntos-a').addClass('is-invalid');
      } else if (!valorValido(texto)) {
        invalidos++;
      }
    });
    if (vacios) errores.push('Faltan ' + vacios + ' renglón(es) por contestar.');
    if (invalidos) errores.push(invalidos + ' renglón(es) tienen un valor no válido (de 0 a 10, sin usar el 5).');

    if (errores.length) {
      e.preventDefault();
      mostrarErrores($('#error-personalidad'), errores);
    }
  });

  // Al cargar (por ejemplo, después de un error del servidor) recalcular todo
  $form.find('.par').each(function () { actualizarPar($(this)); });
  actualizarTotales();
});
