function init () {
  // This function populates blueprint modal with the list from the link
  $('#module-blueprint-btn').on('click', function (e) {
    e.preventDefault()
    $('#module-blueprint-list').modal('show').find('.modal-body').load($(this).attr('href'))
  })
}

document.addEventListener('DOMContentLoaded', init, false)
