const $ = require('jquery')
const a4api = require('adhocracy4').api

$(function () {
  $('[data-toggle="popover"]').popover()

  $('#idea--popover__btn').on('hide.bs.popover', function () {
    var oldVal = $('#idea--popover__input')[0]['oldVal']
    var newVal = $('#idea--popover__input').val()

    if (oldVal !== newVal) {
      a4api.moderatorremark.change(
        {remark: $('#idea--popover__input').val()},
        $('#idea--popover__btn').data('slug')
      )
    }
  })

  $('#idea--popover__btn').on('show.bs.popover', function () {
    a4api.moderatorremark.get($('#idea--popover__btn').data('slug'))
      .done((v) => {
        $('#idea--popover__input')[0]['oldVal'] = v.remark
        $('#idea--popover__input').val(v.remark)
      })
  })
})
