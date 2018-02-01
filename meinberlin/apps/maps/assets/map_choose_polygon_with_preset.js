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

(function (init) {
  $(init)
  $(document).on('a4.embed.ready', init)
})(function () {
  // Prevent from including leaflet in this bundle
  const L = window.L

  const ImportControl = L.Control.extend({
    // Options
    options: {
      position: 'topright',
      polygonStyle: {}
    },

    initialize: function (layer, options) {
      L.Util.setOptions(this, options)
      this._layer = layer
    },

    onAdd: function (map) {
      const container = this._createControls()
      document.body.appendChild(this._createModal())

      $(document).on('click', '#map-export-link', (e) => {
        e.preventDefault()
        this._export(map)
      })

      $(document).on('submit', '#map-import-form', (e) => {
        e.preventDefault()

        const fileInput = $('#map-import-file-input')[0]
        if (fileInput.files.length < 1) {
          return
        }
        const file = fileInput.files[0]

        this._removeUploadError()
        fileInput.value = ''

        this._import(map, file)
      })

      $('#map-import-modal').on('hidden.bs.modal', () => this._removeUploadError())
      return container
    },

    _createControls: function () {
      const exportLabel = django.gettext('Export shape as GeoJSON')
      const importLabel = django.gettext('Import shape from file')
      return $.parseHTML(
        '<div class="leaflet-bar leaflet-control leaflet-control-custom">' +
          '<a href="#" id="map-export-link" title="' + exportLabel + '"><i class="fa fa-download" aria-label="' + exportLabel + '"></i></a>' +
          '<a href="#map-import-modal" data-toggle="modal" data-target="#map-import-modal" title="' + importLabel + '"><i class="fa fa-upload" aria-label="' + importLabel + '"></i></a>' +
        '</div>'
      )[0]
    },

    _createModal: function () {
      const modalTitle = django.gettext('Import shape from file')
      return $.parseHTML(
        '<div class="modal" id="map-import-modal" tabindex="-1" role="dialog" aria-label="' + modalTitle + '" aria-hidden="true">' +
          '<div class="modal-dialog modal-lg" role="document">' +
            '<div class="modal-content">' +
              '<div class="modal-header">' +
                '<h2 class="modal-title u-first-heading">' + modalTitle + '</h2>' +
                '<button class="close" aria-label="' + django.gettext('Close') + '" data-dismiss="modal"><i class="fa fa-times"></i></button>' +
              '</div>' +
              '<div class="modal-body">' +
                '<form id="map-import-form" data-ignore-submit="true">' +
                  '<div class="form-group">' +
                    '<label for="map-import-file-input">' + django.gettext('Import shape via file upload') + '</label>' +
                    '<div class="form-hint">' +
                      django.gettext('Upload a shape from a GeoJSON (.geojson) or a zipped Shapefile (.zip).') + '<br>' +
                      django.gettext('Note that uploading Shapefiles is not supported with Internet Explorer 10') + '<br>' +
                      '<strong>' + django.gettext('Attention importing a file will delete all the existing shapes.') + '</strong>' +
                    '</div>' +
                    '<div class="widget widget--fileinput">' +
                      '<div class="input-group">' +
                        '<input type="file" class="input-group__input" id="map-import-file-input" required>' +
                        '<input type="submit" class="btn btn--primary input-group__after" value="' + django.gettext('Upload') + '">' +
                      '</div>' +
                    '</div>' +
                  '</div>' +
                '</form>' +
              '</div>' +
              '<div class="modal-footer">' +
                '<button class="btn btn--light" data-dismiss="modal">' + django.gettext('Cancel') + '</button>' +
              '</div>' +
            '</div>' +
          '</div>' +
        '</div>'
      )[0]
    },

    _removeUploadError: function () {
      $('#map-import-form .errorlist').remove()
    },

    _showUploadError: function (msg) {
      $('#map-import-form .form-group').append('<ul class="errorlist"><li>' + msg + '</li>')
    },

    _export: function (map) {
      const geoJson = this._layer.toGeoJSON()
      const blob = new window.Blob([JSON.stringify(geoJson)], {type: 'application/json'})
      FileSaver.saveAs(blob, 'export.geojson')
    },

    _import: function (map, file) {
      if (file.name.slice(-3) === 'zip') {
        const reader = new window.FileReader()
        reader.onload = (e) => {
          const buffer = e.target.result
          shp(buffer).then((geoJson) => {
            try {
              let shape = L.geoJson(geoJson, {
                style: this.options.polygonStyle
              })
              this._addToMap(map, shape)
            } catch (e) {
              this._showUploadError(django.gettext('The uploaded file is not a valid shapefile.'))
            }
          }, (e) => this._showUploadError(django.gettext('The uploaded file is not a valid shapefile.'))
          ).catch((e) => {
            this._showUploadError(django.gettext('The uploaded file could not be imported.'))
          })
        }
        reader.readAsArrayBuffer(file)
      } else if (file.name.slice(-4) === 'json') {
        let reader = new window.FileReader()
        reader.onload = (e) => {
          try {
            const geoJson = JSON.parse(e.target.result)
            let shape = L.geoJson(geoJson, {
              style: this.options.polygonStyle
            })
            this._addToMap(map, shape)
          } catch (e) {
            this._showUploadError(django.gettext('The uploaded file is not a valid geojson file.'))
          }
        }
        reader.readAsText(file, 'utf-8')
      } else {
        this._showUploadError(django.gettext('Invalid file format.'))
      }
    },

    _addToMap: function (map, shape) {
      $('#map-import-modal').modal('hide')

      this._layer.clearLayers()
      shape.eachLayer((layer) => {
        this._layer.addLayer(layer)
      })
      map.fitBounds(this._layer.getBounds())
      map.fire(L.Draw.Event.EDITED)
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

    map.addControl(new ImportControl(drawnItems,
      {
        polygonStyle: polygonStyle
      }
    ))

    map.on(L.Draw.Event.CREATED, function (event) {
      const layer = event.layer
      drawnItems.addLayer(layer)
      const geoJson = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(geoJson))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.EDITED, function (event) {
      const geoJson = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(geoJson))
      $('#id_' + name).trigger('change')
    })

    map.on(L.Draw.Event.DELETED, function (event) {
      const geoJson = drawnItems.toGeoJSON()
      $('#id_' + name).val(JSON.stringify(geoJson))
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

        const isEmpty = drawnItems.getLayers().length === 0
        const msg = django.gettext('Do you want to load this preset and delete all the existing polygons?')
        if (isEmpty || window.confirm(msg)) {
          drawnItems.clearLayers()
          shape.eachLayer(function (layer) {
            drawnItems.addLayer(layer)
          })
          map.fitBounds(drawnItems.getBounds())
          map.fire(L.Draw.Event.EDITED)
        }
      }
    })
  })
})
