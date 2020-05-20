/*
This adds a jQuery plugin called `selectdropdown` which transforms a html <select> into a bootstrap dropdown.
The idea is borrowed from https://github.com/silviomoreto/bootstrap-select which provides a lot more functionality
which is not needed by us yet. If we need even more fancy dropdowns the bootstrap-select package should be considered
again.

The `selectdropdown` constructor accepts the following options as a dict or data atttributes.

- style: additional class passed to the dropdown button
- styleDropdown: additional class passed to the dropdown container

The options on the select may set the following options via data attributes:
- content: The label of the menu items and the button (for the selected item) as html
- iconSrc: Optional image source to an icon shown left of the label

The following classes are available:
- select-dropdown [$styleDropdown]
  - select-dropdown__btn [$style]
    - select-dropdown__btn__label
      - select-dropdown__btn__label__icon
      - select-dropdown__btn__label__label
  - select-dropdown__menu
    - select-dropdown__item [.selected]
      - select-dropdown__item__icon
      - select-dropdown__item__label
 */

(function ($) {
  var SelectDropdown = function (element, settings) {
    this.$element = $(element)
    this.settings = settings

    this.createDropdown()

    this.$element.hide()
    this.$dropdown.insertAfter(this.$element)
  }

  SelectDropdown.prototype = {
    createDropdown: function () {
      var $dropdown = $('<div class="dropdown select-dropdown ' + this.settings.styleDropdown + '">')

      var btnClasses = 'btn select-dropdown__btn ' + this.settings.style
      var $button = $('<button class="' + btnClasses + '" type="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">').appendTo($dropdown)
      var $buttonLabel = $('<span class="select-dropdown__btn__label">').appendTo($button)
      $('<i class="fa fa-caret-down" aria-hidden="true"></i>').appendTo($button)

      var $menu = $('<div class="dropdown-menu select-dropdown__menu">').appendTo($dropdown)

      this.$dropdown = $dropdown
      this.$buttonLabel = $buttonLabel

      $.each(this.getSelectOptions(), function (i, option) {
        var $item = $('<a class="dropdown-item select-dropdown__item" href="#">')
        this.appendOptionLabel($item, option, 'select-dropdown__item')

        $item.appendTo($menu)
        $item.on('click', null, option, this.onSelect.bind(this))

        if (option.selected) {
          this.selectItem($item, option)
        }
      }.bind(this))
    },

    appendOptionLabel ($element, option, classNameBase) {
      classNameBase = classNameBase || 'select-dropdown__item'

      if (option.iconSrc) {
        $('<img alt="" src="' + option.iconSrc + '" class="' + classNameBase + '__icon">').appendTo($element)
      }
      $('<span class="' + classNameBase + '__label">').html(option.label).appendTo($element)
    },

    onSelect (event) {
      event.preventDefault()
      // event.stopPropagation()
      var $item = $(event.target)
      var option = event.data
      this.selectItem($item, option)
    },

    selectItem ($item, option) {
      this.$buttonLabel.empty()
      this.appendOptionLabel(this.$buttonLabel, option, 'select-dropdown__btn__label')

      this.$dropdown.find('.select-dropdown__item.selected').removeClass('selected')
      $item.addClass('selected')
      this.$element.val(option.value)
    },

    getSelectOptions: function () {
      return this.$element.find('option').map(function (i, option) {
        var $option = $(option)

        var data = $.extend({
          content: null,
          iconSrc: null
        }, $option.data())

        var value = $option.attr('value')
        var label = data.content || $option.text()

        data = $.extend(data, {
          value: value,
          label: label,
          selected: $option.is(':selected')
        })

        return data
      })
    }
  }

  $.fn.selectdropdown = function (settings) {
    // Establish our default settings
    settings = $.extend({
      style: '',
      styleDropdown: ''
    }, settings)

    return this.each(function () {
      var $this = $(this)
      if ($this.is('select')) {
        var selectdropdown = $this.data('selectdropdown')

        if (!selectdropdown) {
          $this.data('selectdropdown', (selectdropdown = new SelectDropdown(this, settings)))
        }
      }
    })
  }
}(window.jQuery))
