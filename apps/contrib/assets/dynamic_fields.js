
var $ = require('jquery')

$(function () {
  hide2()
  $('#receiver-selection').on('change', function () {
    hide2()
    if (document.getElementById('id_receivers_0').checked) {
      $('#selection-project').show()
    } else if (document.getElementById('id_receivers_1').checked) {
      $('#selection-organisation').show()
    }
  })
})

function hide2 () {
  $('#selection-organisation').hide()
  $('#selection-project').hide()
}
