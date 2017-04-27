(function () {
  var $inputs = $('.datepicker')

  $inputs.each(function (i, e) {
    var initObject = {formElements: {}}
    initObject.formElements[e.id] = '%d.%m.%Y'
    datePickerController.createDatePicker(initObject)
  })
}())
