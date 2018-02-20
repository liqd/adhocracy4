var api = require('adhocracy4').api
const $ = require('jquery')

$(function () {
  $('[data-toggle="popover"]').popover()

  $('#idea--popover__btn').on('hide.bs.popover', function () {
    api.moderatorremark.change(
      {remark: $('#idea--popover__input').val()},
      $('#idea--popover__btn').data('slug')
    )
  })

  $('#idea--popover__btn').on('show.bs.popover', function () {
    api.moderatorremark.get($('#idea--popover__btn').data('slug'))
  })
})
