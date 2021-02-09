/* global django */

const apiUrl = 'https://bplan-prod.liqd.net/api/addresses/'

function pointInPolygon (point, polygon) {
  const x = point[0]
  const y = point[1]

  // Algorithm comes from:
  // https://github.com/substack/point-in-polygon/blob/master/index.js
  let inside = false

  for (let p = 0; p < polygon.length; p++) {
    const ring = polygon[p]

    for (let i = 0; i < ring.length - 1; i++) {
      const xi = ring[i][0]
      const yi = ring[i][1]
      const xj = ring[i + 1][0]
      const yj = ring[i + 1][1]

      //      *
      //     /
      // *--/----------->>
      //   *
      // Check that
      //
      // 1.  yi and yj are on opposite sites of a ray to the right
      // 2.  the intersection of the ray and the segment is right of x
      const intersect = ((yi > y) !== (yj > y)) &&
          (x < (xj - xi) * (y - yi) / (yj - yi) + xi)
      if (intersect) inside = !inside
    }
  }
  return inside
}

const pointInObject = function (point, geojson, failByDefault) {
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

const setBusy = function ($group, busy) {
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

const getPoints = function (address, cb) {
  $.ajax(apiUrl, {
    data: { address: address },
    success: function (geojson) {
      cb(geojson.features)
    },
    error: function () {
      const points = []
      cb(points)
    }
  })
}

const renderPoints = function (points) {
  if (points.length === 0) {
    return $('<span class="complete__warning">')
      .text(django.gettext('No matches found within the project area'))
  } else {
    const $list = $('<ul class="complete__list">')
      .text(django.gettext('Did you mean:'))
    points.forEach(function (point) {
      const text = point.properties.strname + ' ' +
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

function init () {
  $('[data-map="address"]').each(function (i, e) {
    const $group = $(e)
    const name = $group.data('name')
    const $input = $('#id_' + name)
    const $map = $('[data-map="choose_point"][data-name="' + name + '"]')
    const polygon = $map.data('polygon')

    const onSubmit = function (event) {
      event.preventDefault()
      setBusy($group, true)
      const address = $group.find('input').val()
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
      const data = $(event.target).attr('data-map-point')
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

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
