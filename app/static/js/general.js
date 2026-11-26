/*
 * Comportamiento general del sitio (jQuery). Responsable: Valeria
 */
$(function () {
  // Confirmación antes de eliminar (bajas)
  $(document).on('submit', 'form.confirmar', function (e) {
    if (!confirm($(this).data('mensaje') || '¿Seguro?')) {
      e.preventDefault();
    }
  });

  // Validación visual de Bootstrap para formularios simples
  $('form.formulario-validado').on('submit', function (e) {
    if (!this.checkValidity()) {
      e.preventDefault();
      e.stopPropagation();
    }
    $(this).addClass('was-validated');
  });

  // Carrera: si eligen "Otra" aparece el campo para escribirla
  $('#carrera').on('change', function () {
    const otra = $(this).val() === '__otra__';
    $('#campo-carrera-otra').toggleClass('d-none', !otra);
    if (otra) $('#carrera_otra').trigger('focus');
  });

  // El grupo siempre en mayúsculas
  $('#grupo').on('input', function () {
    this.value = this.value.toUpperCase();
  });
});

/** Revisa los datos del alumno. Regresa un arreglo de errores. */
function validarDatosAlumno($form) {
  const errores = [];
  const campos = { matricula: 'matrícula', nombre: 'nombre', carrera: 'carrera', semestre: 'semestre', grupo: 'grupo' };
  $.each(campos, function (campo, etiqueta) {
    const $c = $form.find('[name="' + campo + '"]');
    const vacio = $.trim($c.val()) === '';
    $c.toggleClass('is-invalid', vacio);
    if (vacio) errores.push('Falta tu ' + etiqueta + '.');
  });
  const $otra = $form.find('[name="carrera_otra"]');
  const faltaOtra = $form.find('[name="carrera"]').val() === '__otra__' && $.trim($otra.val()) === '';
  $otra.toggleClass('is-invalid', faltaOtra);
  if (faltaOtra) errores.push('Escribe el nombre de tu carrera.');
  return errores;
}

/** Muestra los errores en una alerta y sube a ella. */
function mostrarErrores($alerta, errores) {
  if (errores.length === 0) {
    $alerta.addClass('d-none').empty();
    return;
  }
  const $lista = $('<ul class="mb-0"></ul>');
  errores.forEach(function (e) { $lista.append($('<li></li>').text(e)); });
  $alerta.removeClass('d-none').empty().append($lista);
  $('html, body').animate({ scrollTop: $alerta.offset().top - 80 }, 300);
}
