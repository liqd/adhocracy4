const $ = require('jquery')
const datePickerController = require('datepicker')

$(function () {
  let $inputs = $('.datepicker')

  $inputs.each(function (i, e) {
    let initObject = {formElements: {}}
    initObject.formElements[e.id] = '%d.%m.%Y'
    datePickerController.createDatePicker(initObject)
  })
})
