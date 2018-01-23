/* global django */

const $ = require('jquery')
// const L = require('leaflet')
const FileSaver = require('file-saver')
const shp = require('shpjs')

function createMap (L, baseurl, attribution, e) {
  var basemap = baseurl + '{z}/{x}/{y}.png'
  var baselayer = L.tileLayer(basemap, { maxZoom: 18, attribution: attribution })
  var map = new L.Map(e, {scrollWheelZoom: false, zoomControl: true, minZoom: 2})
  baselayer.addTo(map)
  return map
}

function getBaseBounds (L, polygon, bbox) {
  if (polygon) {
    if (polygon.type === 'FeatureCollection' && polygon.features.length === 0) {
      return bbox
    }
    return L.geoJson(polygon).getBounds()
  } else {
    return bbox
  }
}

function loadShape (map, group, shape, msg, $input) {
  var isEmpty = group.getLayers().length === 0

  if (isEmpty || window.confirm(msg)) {
    group.clearLayers()
    shape.eachLayer(function (layer) {
      group.addLayer(layer)
    })
    map.fitBounds(group.getBounds())

    $input.val(JSON.stringify(group.toGeoJSON()))
    $input.trigger('change')
  }
}

(function (init) {
  $(init)
  $(document).on('a4.embed.ready', init)
})(function () {
  // Prevent from including leaflet in this bundle
  var L = window.L

  $('[data-map="choose_polygon"]').each(function (i, e) {
    var name = e.getAttribute('data-name')
    var polygon = JSON.parse(e.getAttribute('data-polygon'))
    var bbox = JSON.parse(e.getAttribute('data-bbox'))
    var baseurl = e.getAttribute('data-baseurl')
    var attribution = e.getAttribute('data-attribution')

    var map = createMap(L, baseurl, attribution, e)

    var polygonStyle = {
      'color': '#0076ae',
      'weight': 2,
      'opacity': 1,
      'fillOpacity': 0.2
    }

    var drawnItems
    if (polygon) {
      drawnItems = L.geoJson(polygon, {
        style: polygonStyle
      })
      if (drawnItems.getLayers().length > 0) {
        map.fitBounds(drawnItems.getBounds())
      } else {
        map.fitBounds(getBaseBounds(L, polygon, bbox))
      }
    } else {
      drawnItems = L.featureGroup()
      map.fitBounds(getBaseBounds(L, polygon, bbox))
    }
    drawnItems.addTo(map)

    map.addControl(new L.Control.Draw({
      edit: {
        featureGroup: drawnItems,
        edit: {
          selectedPathOptions: {
            maintainColor: true
          }
        }
      },
      draw: {
        polygon: {
          shapeOptions: polygonStyle
        },
        rectangle: {
          shapeOptions: polygonStyle
        },
        marker: false,
        circlemarker: false,
        polyline: false,
        circle: false
      }
    }))

    map.on(L.Draw.Event.CREATED, function (event) {
      var layer = event.layer
      drawnItems.addLayer(layer)
      var shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.EDITED, function (event) {
      var shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.DELETED, function (event) {
      var shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      map.invalidateSize().fitBounds(getBaseBounds(L, polygon, bbox))
    })

    $('#select_' + name).on('change', function (event) {
      var geoJson = event.target.value
      if (geoJson) {
        var shape = L.geoJson(JSON.parse(geoJson), {
          style: polygonStyle
        })

        var msg = django.gettext('Do you want to load this preset and delete all the existing polygons?')
        loadShape(map, drawnItems, shape, msg, $('#id_' + name))
      }
    })

    var ExportControl = L.Control.extend({
      options: {
        position: 'topright'
      },
      onAdd: function (map) {
        var container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom')
        var exportLink = L.DomUtil.create('a', '', container)
        var exportIcon = L.DomUtil.create('i', 'fa fa-download', exportLink)
        exportLink.setAttribute('title', django.gettext('Export as GeoJSON'))
        exportIcon.setAttribute('aria-label', django.gettext('Export as GeoJSON'))

        exportLink.onclick = function () {
          var shape = drawnItems.toGeoJSON()
          var blob = new window.Blob([JSON.stringify(shape)], {type: 'application/json'})
          FileSaver.saveAs(blob, 'export.geojson')
        }

        var importInput = L.DomUtil.create('input', 'sr-only', container)
        importInput.setAttribute('type', 'file')

        var importLink = L.DomUtil.create('a', '', container)
        var importIcon = L.DomUtil.create('i', 'fa fa-upload', importLink)
        importLink.setAttribute('title', django.gettext('Import shapefile or GeoJSON file'))
        importIcon.setAttribute('aria-label', django.gettext('Import shapefile or GeoJSON file'))

        importLink.onclick = function (e) {
          e.preventDefault()
          e.stopPropagation()
          importInput.click()
        }

        importInput.onchange = function (e) {
          e.preventDefault()
          e.stopPropagation()

          // FIXME: need to check if there is a file?
          var file = e.target.files[0]

          if (file.name.slice(-3) === 'zip') {
            let reader = new window.FileReader()
            reader.onload = function (e) {
              shp(e.target.result).then(function (geoJson) {
                try {
                  var shape = L.geoJson(geoJson, {
                    style: polygonStyle
                  })
                } catch (e) {
                  window.alert(django.gettext('The uploaded file is not a valid shapefile.'))
                  return
                }

                var msg = django.gettext('Do you want to import this file and delete all the existing polygons?')
                loadShape(map, drawnItems, shape, msg, $('#id_' + name))
              }, function (e) {
                window.alert(django.gettext('The uploaded file is not a valid shapefile.'))
              })
            }
            reader.readAsArrayBuffer(file)
          } else if (file.name.slice(-4) === 'json') {
            let reader = new window.FileReader()
            reader.onload = function (e) {
              // FIXME: what about errors?
              var buffer = e.target.result
              var decodedString = String.fromCharCode.apply(null, new Uint8Array(buffer))
              try {
                var geoJson = JSON.parse(decodedString)
                var shape = L.geoJson(geoJson, {
                  style: polygonStyle
                })
              } catch (e) {
                window.alert(django.gettext('The uploaded file is not a valid geojson file.'))
                return
              }

              var msg = django.gettext('Do you want to import this file and delete all the existing polygons?')
              loadShape(map, drawnItems, shape, msg, $('#id_' + name))
            }
            reader.readAsArrayBuffer(file)
          } else {
            window.alert(django.gettext('Invalid file format. Only shapefiles (.zip) and geojson (.geojson or .json) are supported.'))
          }
        }

        return container
      }
    })
    map.addControl(new ExportControl())
  })
})
