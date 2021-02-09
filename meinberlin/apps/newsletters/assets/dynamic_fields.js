/* this code is used in the newsletter form to display a project
   dropdown when the user selects that he/she wants to send the
   newsletter to all followers of a project */

const $ = require('jquery')
$(function () {
  const $idReceivers0 = $('#id_receivers_0')
  const $idReceivers1 = $('#id_receivers_1')
  const $idReceivers2 = $('#id_receivers_2')
  const $projectSelect = $('#selection-project')
  const $organisationSelect = $('#selection-organisation')

  showField()
  $('#receiver-selection').on('change', showField)

  function hideSelection () {
    $organisationSelect.hide()
    $projectSelect.hide()
  }

  function showField () {
    hideSelection()
    if ($idReceivers0.prop('checked')) {
      $projectSelect.show()
    } else if ($idReceivers1.prop('checked') || $idReceivers2.prop('checked')) {
      $organisationSelect.show()
    }
  }
})
