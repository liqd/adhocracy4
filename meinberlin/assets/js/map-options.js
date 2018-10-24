var options = {

  background: {
    fill: true,
    weight: 1,
    fillColor: '#E8E5D8',
    color: '#E8E5D8',
    fillOpactiy: 1,
    opacity: 0
  },
  landuse: function (properties, zoom) {
    if (properties.class === 'residential') {
      return {
        fill: true,
        weight: 1,
        fillColor: '#E0DED7',
        color: '#E0DED7',
        fillOpactiy: 0.7,
        opacity: 0
      }
    } else if (properties.class === 'agriculture') {
      return {
        fill: true,
        weight: 1,
        fillColor: '#eae0d0',
        fillOpactiy: 1,
        opacity: 0
      }
    } else if (properties.class === 'national_park') {
      var opacity = 0.75
      if (zoom >= 9) {
        opacity = 0
      }
      return {
        fill: true,
        weight: 1,
        fillColor: '#E1EBB0',
        color: '#E1EBB0',
        fillOpacity: opacity,
        opacity: 0
      }
    } else {
      return {
        fill: false,
        weight: 0,
        opacity: 0,
        fillOpacity: 0
      }
    }
  },
  landcover: function (properties, zoom) {
    if (properties.class === 'grass') {
      return {
        fill: true,
        weight: 1,
        fillColor: '#C0D897',
        fillOpacity: 0.45,
        opacity: 0
      }
    } else if (properties.class === 'wood') {
      let opacity = 0.6
      if (zoom >= 22) {
        opacity = 1
      }
      return {
        fill: true,
        weight: 1,
        fillColor: '#C0D897',
        fillOpacity: opacity,
        opacity: 0
      }
    } else if (properties.class === 'sand') {
      return {
        fill: true,
        weight: 1,
        fillColor: '#E8D626',
        fillOpacity: 0.3,
        opacity: 0
      }
    } else {
      return {
        fill: false,
        weight: 0,
        fillOpacity: 0,
        opacity: 0
      }
    }
  },
  park: function (properties, zoom) {
    return {
      fill: true,
      dashArray: '0.5, 1',
      weight: 1,
      fillColor: '#c0d897',
      color: '#9fb776',
      fillOpacity: 1,
      opacity: 1
    }
  },
  building: function (properties, zoom) {
    let opacity = 0
    if (zoom >= 15) {
      opacity = 1
    }
    return {
      fill: true,
      weight: 1,
      fillColor: '#DED3BE',
      color: '#d4b192',
      fillOpacity: opacity,
      opacity: opacity
    }
  },
  water: {
    fill: true,
    weight: 1,
    fillColor: '#94C1E1',
    fillOpacity: 1,
    opacity: 0
  },
  waterway: {
    weight: 1,
    fillColor: '#94C1E1',
    color: '#94C1E1',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  boundary: {
    fillOpacity: 0,
    opacity: 0
  },
  aeroway: {
    weight: 1,
    fillColor: '#51aeb5',
    color: '#51aeb5',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  road: function (properties, zoom, dimension) {
    console.log(properties)
    console.log(zoom)
    console.log(dimension)
    return {
      weight: 1,
      fillColor: '#F7F7F7',
      color: '#F7F7F7',
      fillOpacity: 0.2,
      opacity: 0.4
    }
  },
  tunnel: {
    weight: 0.5,
    fillColor: '#F7F7F7',
    color: '#F7F7F7',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  bridge: {
    weight: 0.5,
    fillColor: '#F7F7F7',
    color: '#F7F7F7',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  transportation: {
    weight: 0.5,
    fillColor: '#F7F7F7',
    color: '#F7F7F7',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  transit: {
    weight: 0.5,
    fillColor: '#F7F7F7',
    color: '#F7F7F7',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  water_name: {
    weight: 0,
    fillOpacity: 0,
    opacity: 0
  },
  transportation_name: {
    weight: 1,
    fillColor: '#F7F7F7',
    color: '#F7F7F7',
    fillOpacity: 0.2,
    opacity: 0.4
  },
  place: {
    weight: 0,
    fillOpacity: 0,
    opacity: 0
  },
  housenumber: {
    weight: 0,
    fillOpacity: 0,
    opacity: 0
  },
  poi: {
    weight: 0,
    fillOpacity: 0,
    opacity: 0
  },
  poi_label: {

  },
  mountain_peak: {
    opacity: 0,
    fillOpacity: 0
  },
  aerodrome_label: {
    opacity: 0,
    fillOpacity: 0
  },
  earth: {
    fill: true,
    weight: 1,
    fillColor: '#E8E5D8',
    color: '#E8E5D8',
    fillOpactiy: 1,
    opacity: 0
  }

}

var init = function () {
  window.options = options
}

window.jQuery(init)
