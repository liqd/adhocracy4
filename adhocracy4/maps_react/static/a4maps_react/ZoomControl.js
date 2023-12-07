import { createControlComponent } from '@react-leaflet/core'
import L from 'leaflet'

// Create a Leaflet Control
const createLeafletElement = (props) => {
  const zoomControl = L.control.zoom(props)

  const updateDisabled = () => {
    const map = zoomControl._map
    if (!map) {
      return
    }

    const className = 'leaflet-disabled'
    const zoomInBtn = zoomControl._zoomInButton
    const zoomOutBtn = zoomControl._zoomOutButton

    // disable button when at min/max zoom
    if (map._zoom === map.getMinZoom()) {
      L.DomUtil.addClass(zoomOutBtn, className)
    } else {
      L.DomUtil.removeClass(zoomOutBtn, className)
    }

    if (map._zoom === map.getMaxZoom() || (map._zoomSnap && Math.abs(map.getZoom() - map.getMaxZoom()) < map._zoomSnap)) {
      L.DomUtil.addClass(zoomInBtn, className)
    } else {
      L.DomUtil.removeClass(zoomInBtn, className)
    }
  }

  zoomControl.onAdd = (map) => {
    const container = L.Control.Zoom.prototype.onAdd.call(zoomControl, map)
    map.on('zoom', updateDisabled)
    updateDisabled()
    return container
  }

  zoomControl.onRemove = (map) => {
    map.off('zoom', updateDisabled)
    L.Control.Zoom.prototype.onRemove.call(zoomControl, map)
  }

  return zoomControl
}

const ZoomControl = createControlComponent(createLeafletElement)
export default ZoomControl
