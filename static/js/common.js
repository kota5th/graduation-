$(function () {
  $(".answer").on('click', function () {
    var target = $(this).data('target');
    $('#' + target).slideToggle();
  })
})