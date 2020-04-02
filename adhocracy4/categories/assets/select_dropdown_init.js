/* global $ */
(function (init) {
  document.addEventListener('DOMContentLoaded', init, false)
  document.addEventListener('a4.embed.ready', init, false)
})(function () {
  if ($.fn.selectdropdown) {
    $('.select-dropdown').selectdropdown()
  }
})
