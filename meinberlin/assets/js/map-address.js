/* global $,django */

var apiUrl = 'https://bplan-stage.liqd.net/api/addresses/'

var setBusy = function ($group, busy) {
  $group.attr('aria-busy', busy)
  $group.find('input').attr('disabled', busy)
  $group.find('button').attr('disabled', busy)
  if (busy) {
    $group.find('.fa')
      .addClass('fa-spinner fa-pulse')
      .removeClass('fa-search')
  } else {
    $group.find('.fa')
      .addClass('fa-search')
      .removeClass('fa-spinner fa-pulse')
  }
}

var getPoints = function (address, cb) {
  var $ = window.jQuery

  $.ajax(apiUrl, {
    data: {address: address},
    success: function (geojson) {
      // TODO: filter by polygon
      cb(geojson.features)
    },
    error: function () {
      var points = []
      cb(points)
    }
  })
}

var renderPoints = function (points) {
  if (points.length === 0) {
    return $('<span class="complete__warning">')
      .text(django.gettext('No matches found'))
  } else {
    var $list = $('<ul class="complete__list">')
      .text(django.gettext('Did you mean:'))
    points.forEach(function (point) {
      var text = point.properties.strname + ' ' +
        point.properties.hsnr + ', ' +
        point.properties.plz + ' ' +
        point.properties.bezirk_name
      $list.append($('<li>')
        .append($('<button type="button" class="complete__item">')
          .text(text)
          .attr('data-map-point', JSON.stringify(point))
        )
      )
    })
    return $list
  }
}

var init = function () {
  var $ = window.jQuery

  $('[data-map="address"]').each(function (i, e) {
    var $group = $(e)
    var $input = $('#id_' + $group.data('name'))

    var onSubmit = function (event) {
      event.preventDefault()
      setBusy($group, true)
      var address = $group.find('input').val()
      getPoints(address, function (points) {
        setBusy($group, false)
        $group.find('.complete')
          .empty()
          .append(renderPoints(points))
      })
    }

    // simulate a nested form
    $group.find('button').click(onSubmit)
    $group.find('input').on('change', onSubmit)
    $group.find('input').on('keydown', function (event) {
      if (event.keyCode === 13) {
        onSubmit(event)
      }
    })

    $group.on('click', '[data-map-point]', function (event) {
      var data = $(event.target).attr('data-map-point')
      $input.val(data).change()
  })
}

window.jQuery(init)
window.jQuery(document).on('a4.embed.ready', init)
