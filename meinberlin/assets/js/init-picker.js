const $ = require('jquery')
const datePickerController = require('datepicker')
const django = require('django')

$(function () {
  let $inputs = $('.datepicker')

  $inputs.each(function (i, e) {
    let initObject = { formElements: {} }
    initObject.formElements[e.id] = django.get_format('DATE_INPUT_FORMATS')[0]
    datePickerController.createDatePicker(initObject)
  })
})
