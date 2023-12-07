import React from 'react'
import { Popup } from 'react-leaflet'

export const MapPopup = ({ feature, className, children, ...rest }) => {
  const _className = 'maps-popups ' + (className ?? '')
  return (
    <Popup {...rest} className={_className} closeButton={false}>
      <div
        style={{ backgroundImage: 'url(' + feature.properties.image + ')' }}
        className={'maps-popups-popup-image' + (feature.properties.image ? '' : ' maps-popups-popup-no-image')}
      />
      <div className="maps-popups-popup-text-content">
        {children}
      </div>
    </Popup>
  )
}
