/* global django */

const $ = require('jquery')
// const L = require('leaflet')
const FileSaver = require('file-saver')
const shp = require('shpjs')

function createMap (L, baseurl, attribution, e) {
  const basemap = baseurl + '{z}/{x}/{y}.png'
  const baselayer = L.tileLayer(basemap, { maxZoom: 18, attribution: attribution })
  const map = new L.Map(e, {scrollWheelZoom: false, zoomControl: true, minZoom: 2})
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

function loadShape (map, group, shape, $input, msg) {
  const isEmpty = group.getLayers().length === 0

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
  const L = window.L

  const ExportControl = L.Control.extend({
    // Options
    options: {
      position: 'topright',
      onImportFileChange: null,
      onExportLinkClick: null
    },

    onAdd: function () {
      const container = L.DomUtil.create('div', 'leaflet-bar leaflet-control leaflet-control-custom')

      const exportLink = L.DomUtil.create('a', '', container)
      const exportIcon = L.DomUtil.create('i', 'fa fa-download', exportLink)
      exportLink.setAttribute('title', django.gettext('Export as GeoJSON'))
      exportIcon.setAttribute('aria-label', django.gettext('Export as GeoJSON'))

      if (this.options.onExportLinkClick) {
        exportLink.onclick = this.options.onExportLinkClick
      }

      // FIXME: is this accessible doe we need a label or something?
      const importInput = L.DomUtil.create('input', 'sr-only', container)
      importInput.setAttribute('type', 'file')

      const importLink = L.DomUtil.create('a', '', container)
      const importIcon = L.DomUtil.create('i', 'fa fa-upload', importLink)
      importLink.setAttribute('title', django.gettext('Import shapefile or GeoJSON file'))
      importIcon.setAttribute('aria-label', django.gettext('Import shapefile or GeoJSON file'))

      importLink.onclick = function (e) {
        // FIXME: is preventing the default event required?
        e.preventDefault()
        e.stopPropagation()
        importInput.click()
      }

      if (this.options.onImportFileChange) {
        importInput.onchange = this.options.onImportFileChange
      }

      return container
    }
  })

  $('[data-map="choose_polygon"]').each(function (i, e) {
    const name = e.getAttribute('data-name')
    const polygon = JSON.parse(e.getAttribute('data-polygon'))
    const bbox = JSON.parse(e.getAttribute('data-bbox'))
    const baseurl = e.getAttribute('data-baseurl')
    const attribution = e.getAttribute('data-attribution')

    const map = createMap(L, baseurl, attribution, e)

    const polygonStyle = {
      'color': '#0076ae',
      'weight': 2,
      'opacity': 1,
      'fillOpacity': 0.2
    }

    let drawnItems
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
      const layer = event.layer
      drawnItems.addLayer(layer)
      const shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.EDITED, function (event) {
      const shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.DELETED, function (event) {
      const shape = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(shape))
      $('#id_' + name).trigger('change')
    })

    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
      map.invalidateSize().fitBounds(getBaseBounds(L, polygon, bbox))
    })

    $('#select_' + name).on('change', function (event) {
      const geoJson = event.target.value
      if (geoJson) {
        const shape = L.geoJson(JSON.parse(geoJson), {
          style: polygonStyle
        })

        loadShape(map, drawnItems, shape, $('#id_' + name),
          django.gettext('Do you want to load this preset and delete all the existing polygons?'))
      }
    })

    map.addControl(new ExportControl({
      onExportLinkClick: function (e) {
        const shape = drawnItems.toGeoJSON()
        const blob = new window.Blob([JSON.stringify(shape)], {type: 'application/json'})
        FileSaver.saveAs(blob, 'export.geojson')
      },

      onImportFileChange: function (e) {
        e.preventDefault()
        e.stopPropagation()

        if (e.target.files.length < 1) {
          return
        }
        const file = e.target.files[0]

        if (file.name.slice(-3) === 'zip') {
          const reader = new window.FileReader()
          reader.onload = function (e) {
            const buffer = e.target.result
            shp(buffer).then(function (geoJson) {
              let shape
              try {
                shape = L.geoJson(geoJson, {
                  style: polygonStyle
                })
              } catch (e) {
                window.alert(django.gettext('The uploaded file is not a valid shapefile.'))
                return
              }
              loadShape(map, drawnItems, shape, $('#id_' + name),
                django.gettext('Do you want to import this file and delete all the existing polygons?'))
            }, function (e) {
              window.alert(django.gettext('The uploaded file is not a valid shapefile.'))
            })
          }
          reader.readAsArrayBuffer(file)
        } else if (file.name.slice(-4) === 'json') {
          let reader = new window.FileReader()
          reader.onload = function (e) {
            const buffer = e.target.result
            const decodedString = String.fromCharCode.apply(null, new Uint8Array(buffer))

            let shape
            try {
              const geoJson = JSON.parse(decodedString)
              shape = L.geoJson(geoJson, {
                style: polygonStyle
              })
            } catch (e) {
              window.alert(django.gettext('The uploaded file is not a valid geojson file.'))
              return
            }
            loadShape(map, drawnItems, shape, $('#id_' + name),
              django.gettext('Do you want to import this file and delete all the existing polygons?'))
          }
          reader.readAsArrayBuffer(file)
        } else {
          window.alert(django.gettext('Invalid file format. Only shapefiles (.zip) and geojson (.geojson or .json) are supported.'))
        }
      }
    }))
  })
})
