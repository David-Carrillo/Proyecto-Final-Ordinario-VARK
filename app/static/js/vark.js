/*
 * Validación del cuestionario VARK con jQuery. Responsable: Valeria
 * - Datos del alumno obligatorios.
 * - Se pueden marcar varias opciones por pregunta o dejarla en blanco,
 *   pero debe haber al menos una respuesta en todo el cuestionario.
 * - Si quedan preguntas en blanco se pide confirmación.
 */
$(function () {
  const $form = $('#form-vark');
  const $preguntas = $form.find('.pregunta');
  const total = $preguntas.length;

  function actualizarAvance() {
    const contestadas = $preguntas.filter(function () {
      return $(this).find('input:checked').length > 0;
    }).length;
    const porcentaje = Math.round((contestadas * 100) / total);
    $('#barra-avance').css('width', porcentaje + '%').text(contestadas + ' / ' + total);
    return contestadas;
  }

  $form.on('change', 'input[type=checkbox]', function () {
    $(this).closest('.pregunta').removeClass('sin-respuesta');
    actualizarAvance();
  });

  $form.on('submit', function (e) {
    const errores = validarDatosAlumno($form);
    const contestadas = actualizarAvance();

    if (contestadas === 0) {
      errores.push('Marca al menos una respuesta en el cuestionario.');
    }
    if (errores.length) {
      e.preventDefault();
      mostrarErrores($('#error-vark'), errores);
      return;
    }

    const $vacias = $preguntas.filter(function () {
      return $(this).find('input:checked').length === 0;
    });
    if ($vacias.length) {
      $vacias.addClass('sin-respuesta');
      const ok = confirm('Dejaste ' + $vacias.length + ' pregunta(s) en blanco. ¿Quieres enviar así?');
      if (!ok) {
        e.preventDefault();
        $('html, body').animate({ scrollTop: $vacias.first().offset().top - 80 }, 300);
      }
    }
  });

  actualizarAvance();
});
