import { useState, forwardRef, useEffect, useCallback } from 'react'
import { createPortal } from 'react-dom'
import { createElementHook, createControlHook } from '@react-leaflet/core'
import { Control, DomUtil, DomEvent } from 'leaflet'

const ControlWrapper: any = Control.extend({
  options: {
    className: '',
    onOff: '',
    handleOff: () => undefined
  },

  onAdd () {
    const _controlDiv = DomUtil.create('div', this.options.className)
    DomEvent.disableClickPropagation(_controlDiv)
    DomEvent.disableScrollPropagation(_controlDiv)
    return _controlDiv
  },

  onRemove (map: any) {
    if (this.options.onOff) {
      map.off(this.options.onOff, this.options.handleOff, this)
    }

    return this
  }
})

const createControl = (props: any, context: any): any => {
  const instance = new ControlWrapper(props)
  return { instance, context: { ...context, overlayContainer: instance } }
}

const useControlElement = createElementHook(createControl)
const useControl = createControlHook(useControlElement as any)

const useForceUpdate = () => {
  const [_, setValue] = useState(0) // integer state
  return useCallback(() => setValue((value) => value + 1), []) // update the state to force render
}

const createLeafletControl = (useElement: any) => {
  const Component = (props: any, _ref: any) => {
    const forceUpdate = useForceUpdate()
    const { instance } = useElement(props).current

    useEffect(() => {
      // Origin: https://github.com/LiveBy/react-leaflet-control/blob/master/lib/control.jsx
      // This is needed because the control is only attached to the map in
      // MapControl's componentDidMount, so the container is not available
      // until this is called. We need to now force a render so that the
      // portal and children are actually rendered.
      forceUpdate()
    }, [forceUpdate])

    const contentNode = instance.getContainer()
    return contentNode ? createPortal(props.children, contentNode) : null
  }
  return forwardRef(Component)
}

export default createLeafletControl(useControl)
