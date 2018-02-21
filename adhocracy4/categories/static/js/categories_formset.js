/* global $ */
(function (init) {
  $(init)
  $(document).on('a4.embed.ready', init)
})(function () {
  // Dynamically add or remove subforms to a formset.

  var $formsets = $('.js-formset')
  var PLACEHOLDER = /__prefix__/g
  var dynamicFormSets = []

  var DynamicFormSet = function ($formset) {
    this.$formset = $formset
    this.$formTemplate = this.$formset.find('.js-form-template')
    this.prefix = this.$formset.data('prefix')
    this.$totalInput = this.$formset.find('#id_' + this.prefix + '-TOTAL_FORMS')
    this.total = parseInt(this.$totalInput.val())
    this.maxNum = parseInt(this.$formset.find('#id_' + this.prefix + '-MAX_NUM_FORMS').val())

    this.$formset.on('click', '.js-add-form', this.addForm.bind(this))
    this.$formset.on('click', '.js-remove-form', this.removeForm.bind(this))
  }

  DynamicFormSet.prototype.addForm = function () {
    if (this.total < this.maxNum) {
      this.total += 1
      this.$totalInput.val(this.total)
      var newForm = getNewForm(this.$formTemplate, this.total - 1)
      this.$formTemplate.before(newForm)
    }
  }

  DynamicFormSet.prototype.removeForm = function (event) {
    var _this = this

    this.total -= 1
    this.$totalInput.val(this.total)

    var $form = $(event.currentTarget).closest('.js-form')
    var id = this.$formset.find('.js-form').index($form)

    var updateAttr = function ($el, key, i) {
      if ($el.attr(key)) {
        var _old = _this.prefix + '-' + (id + i + 1)
        var _new = _this.prefix + '-' + (id + i)
        $el.attr(key, $el.attr(key).replace(_old, _new))
      }
    }

    $form.nextUntil(this.$formTemplate).each(function (i, sibling) {
      $(sibling).find('*').each(function (j, el) {
        var $el = $(el)
        // FIXME: only a limited number of attributes is supported
        updateAttr($el, 'name', i)
        updateAttr($el, 'for', i)
        updateAttr($el, 'id', i)
      })
    })

    $form.remove()
  }

  function getNewForm ($formTemplate, id) {
    return $formTemplate.html().replace(PLACEHOLDER, id)
  }

  $formsets.each(function (i) {
    dynamicFormSets.push(
      new DynamicFormSet($formsets.eq(i))
    )
  })

  // Note: the template used for dynamically adding formsets is also captured by this
  $('.select-icon').each(function () {
    var $container = $(this)
    var $select = $container.find('select')
    var $buttonLabel = $container.find('.select-icon__btn__label')
    var $menu = $container.find('.select-icon__menu')

    $select.find('option').each(function (i, option) {
      var $option = $(option)
      var label = $option.text()
      var value = $option.attr('value')
      var iconSrc = $option.data('icon-src')

      var iconLabel = $('<span><img src="' + iconSrc + '" class="select-icon__img">' + label + '</span>').html()
      var $item = $('<a class="dropdown-item select-icon__item" href="#">')
      $item.html(iconLabel)

      if ($option.is(':selected')) {
        $buttonLabel.html(iconLabel)
      }

      // data attributes set with jQuery won't be duplicated with the DOM node. Thus we have to use the native dataset
      $item[0].dataset['value'] = value

      $menu.append($item)
    })
  })

  $(document).on('click', '.select-icon__item', function (e) {
    e.preventDefault()

    var $container = $(e.target).closest('.select-icon')
    var $item = $(e.target).closest('.select-icon__item')

    var $select = $container.find('select')

    $container.find('.select-icon__item.selected').removeClass('selected')
    $item.addClass('selected')

    $select.val($item[0].dataset['value'])
    $container.find('.select-icon__btn__label').html($item.html())
  })
})
