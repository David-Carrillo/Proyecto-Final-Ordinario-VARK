/*
 * Muestra solo los campos del ámbito elegido (individual, grupal o total).
 * Responsable: Valeria
 */
$(function () {
  function actualizar() {
    const ambito = $('#ambito').val();
    $('.campo-individual').toggle(ambito === 'individual');
    $('.campo-grupal').toggle(ambito === 'grupal');
  }
  $('#ambito').on('change', actualizar);
  actualizar();
});
