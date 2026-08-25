import { createMap } from './a4maps_common'

const $: any = window.jQuery

function createMarker ($: any, L: any, newlatln: any, oldlatln: any, basePolygon: any, map: any, name: string) {
  const icon = L.icon({
    iconUrl: '/static/images/map_pin_default.svg',
    shadowUrl: '/static/images/map_shadow_01.svg',
    iconSize: [30, 36],
    iconAnchor: [15, 36],
    shadowSize: [40, 54],
    shadowAnchor: [20, 54],
    popupAnchor: [0, -45]
  })

  const marker = L.marker(newlatln, { draggable: true, icon }).addTo(map)
  marker.on('dragend', function () {
    let markerInsidePolygon = false
    basePolygon.getLayers().forEach(function (each: any) {
      if (isMarkerInsidePolygon(marker, each)) {
        markerInsidePolygon = true
        oldlatln = marker.getLatLng()
        const shape = marker.toGeoJSON()
        // shape properties contain old address, therefore we clear them below
        shape.properties = {
          strasse: '',
          haus: '',
          plz: '',
          ortsteil: ''
        }
        $('#id_' + name).val(JSON.stringify(shape))
        $('#id_' + name).trigger('change')
      }
    })
    if (!markerInsidePolygon) {
      marker.setLatLng(oldlatln)
    }
  })
  return marker
}

function getLines (array: any) {
  const output: any[] = []
  if (array.length) {
    if ('lat' in array[0]) {
      for (let i = 0, j = array.length - 1; i < array.length; j = i++) {
        output.push([array[i], array[j]])
      }
    } else {
      array.forEach(function (a: any) {
        getLines(a).forEach(function (line: any) {
          output.push(line)
        })
      })
    }
  }
  return output
}

function isMarkerInsidePolygon (marker: any, poly: any) {
  const x = marker.getLatLng().lat
  const y = marker.getLatLng().lng

  // Algorithm comes from:
  // https://github.com/substack/point-in-polygon/blob/master/index.js
  let inside = false

  // FIXME: getLatLngs does not return holes. Maybe use toGetJson instead?
  getLines(poly.getLatLngs()).forEach(function (line: any) {
    const xi = line[0].lat
    const yi = line[0].lng
    const xj = line[1].lat
    const yj = line[1].lng

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
  })
  return inside
}

function init () {
  const L: any = (window as any).L

  $('[data-map="choose_point"]').each(function (i: number, e: any) {
    const name = e.getAttribute('data-name')
    const polygon = JSON.parse(e.getAttribute('data-polygon'))
    const point = JSON.parse(e.getAttribute('data-point'))

    const map = createMap(L, e, {
      baseUrl: e.getAttribute('data-baseurl'),
      useVectorMap: e.getAttribute('data-usevectormap'),
      attribution: e.getAttribute('data-attribution'),
      mapboxToken: e.getAttribute('data-mapbox-token'),
      omtToken: e.getAttribute('data-omt-token'),
      dragging: true,
      scrollWheelZoom: false,
      zoomControl: false
    })

    const polygonStyle = {
      color: '#0076ae',
      weight: 2,
      opacity: 1,
      fillOpacity: 0.2
    }

    const basePolygon = L.geoJson(polygon, { style: polygonStyle }).addTo(map)
    map.fitBounds(basePolygon.getBounds())
    map.options.minZoom = map.getZoom()
    L.control.zoom({
      position: 'topleft'
    }).addTo(map)

    let marker: any

    if (point) {
      L.geoJson(point, {
        pointToLayer: function (feature: any, newlatlng: any) {
          const oldlatlng = newlatlng
          marker = createMarker($, L, newlatlng, oldlatlng, basePolygon, map, name)
          return marker
        }
      })
    }

    basePolygon.on('click', function (event: any) {
      if (typeof marker === 'undefined') {
        const oldlatlng = event.latlng
        marker = createMarker($, L, event.latlng, oldlatlng, basePolygon, map, name)
        const shape = marker.toGeoJSON()
        $('#id_' + name).val(JSON.stringify(shape))
        $('#id_' + name).trigger('change')
      }
    })

    $('#id_' + name).on('change', function (this: any, _event: any) {
      if (!this.value) return
      const shape = L.geoJSON(JSON.parse(this.value))
      const point = shape.getLayers()[0]
      const latlng = point.getLatLng()
      if (typeof marker === 'undefined') {
        marker = createMarker($, L, latlng, null, basePolygon, map, name)
      } else {
        marker.setLatLng(latlng)
      }

      // Clear input field
      // eslint-disable-next-line no-restricted-syntax
      const $addressGroup = $(`[data-map="address"][data-name="${name}"]`)
      if ($addressGroup.length === 0) return

      const $addressInput = $addressGroup.find('input')
      $addressInput.val('')
    })
  })
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
