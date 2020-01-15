/* global django */

var apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'

function pointInPolygon (point, polygon) {
  var x = point[0]
  var y = point[1]

  // Algorithm comes from:
  // https://github.com/substack/point-in-polygon/blob/master/index.js
  var inside = false

  for (var p = 0; p < polygon.length; p++) {
    var ring = polygon[p]

    for (var i = 0; i < ring.length - 1; i++) {
      var xi = ring[i][0]
      var yi = ring[i][1]
      var xj = ring[i + 1][0]
      var yj = ring[i + 1][1]

      //      *
      //     /
      // *--/----------->>
      //   *
      // Check that
      //
      // 1.  yi and yj are on opposite sites of a ray to the right
      // 2.  the intersection of the ray and the segment is right of x
      var intersect = ((yi > y) !== (yj > y)) &&
          (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
      if (intersect) inside = !inside
    }
  }
  return inside
}

var pointInObject = function (point, geojson, failByDefault) {
  if (geojson.type === 'MultiPolygon') {
    return geojson.coordinates.some(function (polygon) {
      return pointInPolygon(point, polygon)
    })
  } else if (geojson.type === 'Polygon') {
    return pointInPolygon(point, geojson.coordinates)
  } else if (geojson.type === 'Feature') {
    return pointInObject(point, geojson.geometry, failByDefault)
  } else if (geojson.type === 'FeatureCollection') {
    return geojson.features.some(function (feature) {
      return pointInObject(point, feature, true)
    })
  } else {
    return !failByDefault
  }
}

var setBusy = function ($group, busy) {
  $group.attr('aria-busy', busy)
  $group.find('input').attr('disabled', busy)
  $group.find('button').attr('disabled', busy)
  if (busy) {
    $group.find('.fa, .fas, .far')
      .addClass('fa-spinner fa-pulse')
      .removeClass('fa-search')
  } else {
    $group.find('.fa, .fas, .far')
      .addClass('fa-search')
      .removeClass('fa-spinner fa-pulse')
  }
}

var getPoints = function (address, cb) {
  var $ = window.jQuery

  $.ajax(apiUrl, {
    data: { address: address },
    success: function (geojson) {
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
      .text(django.gettext('No matches found within the project area'))
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
    var name = $group.data('name')
    var $input = $('#id_' + name)
    var $map = $('[data-map="choose_point"][data-name="' + name + '"]')
    var polygon = $map.data('polygon')

    var onSubmit = function (event) {
      event.preventDefault()
      setBusy($group, true)
      var address = $group.find('input').val()
      getPoints(address, function (points) {
        setBusy($group, false)
        $group.find('.complete')
          .empty()
          .append(renderPoints(points.filter(function (point) {
            return pointInObject(point.geometry.coordinates, polygon)
          })))
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
      $group.find('.complete').empty()
      // NOTE that the text may not be a valid search query
      $group.find('input').val($(event.target).text())
      $input.val(data).change()
    })

    $(document).on('focusout', function (event) {
      if (!$.contains($group.get(0), event.relatedTarget)) {
        $group.find('.complete').empty()
      }
    })
  })
}

window.jQuery(init)
window.jQuery(document).on('a4.embed.ready', init)
