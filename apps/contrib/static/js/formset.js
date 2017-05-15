/* global $ */
(function (init) {
  $(init)
  $(document).on('a4.embed.ready', init)
})(function () {
  // Dynamically add more subforms to a formset.
  // Removing subforms is not (yet) supported)

  var $formsets = $('.js-formset')
  var PLACEHOLDER = /__prefix__/g
  var dynamicFormSets = []

  var DynamicFormSet = function ($formset) {
    this.$formset = $formset
    this.$formTemplate = this.$formset.find('.js-form-template')
    this.prefix = this.$formset.data('prefix')
    this.$totalInput = this.$formset.find('#id_' + this.prefix + '-TOTAL_FORMS')
    this.id = parseInt(this.$formset.data('initial-id'))
    this.maxNum = parseInt(this.$formset.find('#id_' + this.prefix + '-MAX_NUM_FORMS').val())

    this.$formset.find('.js-add-form').on('click', this.addForm.bind(this))
  }

  DynamicFormSet.prototype.addForm = function () {
    if (this.id + 1 < this.maxNum) {
      this.id += 1
      this.$totalInput.val(this.id + 1)
      var newForm = getNewForm(this.$formTemplate, this.id)
      this.$formTemplate.before(newForm)
    }
  }

  function getNewForm ($formTemplate, id) {
    return $formTemplate.html().replace(PLACEHOLDER, id)
  }

  $formsets.each(function (i) {
    dynamicFormSets.push(
      new DynamicFormSet($formsets.eq(i))
    )
  })
})
