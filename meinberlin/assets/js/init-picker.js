const $ = require('jquery')
const datePickerController = require('datepicker')
const django = require('django')

$(function () {
  const $inputs = $('.datepicker')

  $inputs.each(function (i, e) {
    const initObject = { formElements: {} }
    initObject.formElements[e.id] = django.get_format('DATE_INPUT_FORMATS')[0]
    datePickerController.createDatePicker(initObject)
  })
})
