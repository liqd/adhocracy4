/* global $ */
(function () {
  var $formsets = $('.js-formset')
  var PLACEHOLDER = /__prefix__/g
  var dynamicFormSets = []

  var DynamicFormSet = function ($formset) {
    this.$formset = $formset
    this.$emptyForm = this.$formset.find('.js-empty-form')
    this.$formset.find('.js-add-form').on('click', this.addForm.bind(this))
    this.prefix = this.$formset.data('prefix')
    this.$totalInput = this.$formset.find('#id_' + this.prefix + '-TOTAL_FORMS')
    this.id = parseInt(this.$formset.data('initial-id'))
  }

  DynamicFormSet.prototype.addForm = function () {
    this.id += 1
    this.$totalInput.val(this.id + 1)
    var newForm = getNewForm(this.$emptyForm, this.id)
    this.$emptyForm.before(newForm)
  }

  function getNewForm ($emptyForm, id) {
    return $emptyForm.html().replace(PLACEHOLDER, id)
  }

  $formsets.each(function (i) {
    dynamicFormSets.push(
      new DynamicFormSet($formsets.eq(i))
    )
  })
}())
