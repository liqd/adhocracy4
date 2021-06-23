import React, { useState, useEffect, useRef, useImperativeHandle, forwardRef } from 'react'
import { usePopper } from 'react-popper'

const PopperMenu = (props, ref) => {
  const { children: { popperButton, popperMenuItems, popperConfig } } = props
  const referenceRef = useRef(null)
  const popperRef = useRef(null)
  const [visible, setVisible] = useState(false)

  let config = {
    placement: 'bottom-start'
  }

  popperConfig &&
    (config = { ...config, ...popperConfig })

  const popper = usePopper(
    referenceRef.current,
    popperRef.current,
    {
      ...config
    }
  )

  const { styles, attributes } = popper
  const containerStyleClass = props.containerStyleClass
    ? `popper-content--container ${props.containerStyleClass}`
    : 'popper-content--container'

  useEffect(() => {
    // listen for clicks and close dropdown on body
    document.addEventListener('mousedown', handleDocumentClick)
    return () => {
      document.removeEventListener('mousedown', handleDocumentClick)
    }
  }, [])

  const handleDocumentClick = (event) => {
    (referenceRef.current.contains(event.target) ||
    popperRef.current.contains(event.target)) ||
    setVisible(false)
  }
  const handleDropdownClick = (event) => {
    setVisible(!visible)
  }

  const handleClickAction = (menuItem) => {
    setVisible(false)
    menuItem.handleClick()
    popper.update()
  }

  useImperativeHandle(ref, () => ({
    instance: popper
  }))

  return (
    <>
      <button
        className={popperButton.styleClass ? popperButton.styleClass : ''}
        ref={referenceRef} onClick={handleDropdownClick}
        type="button"
      >
        {popperButton.icon && <i className={popperButton.icon} />} {popperButton.buttonText}
      </button>
      <div ref={popperRef} style={styles.popper} {...attributes.popper}>
        <div
          style={styles.offset}
          className={containerStyleClass}
          data-visible={visible}
        >
          <ul className="popper-container">
            {popperMenuItems.map((menuItem, idx) => (
              <li key={idx}>
                <button
                  className={`${menuItem.styleClass ? menuItem.styleClass : ''} popper-menuitem__button`}
                  type="button"
                  onClick={() => handleClickAction(menuItem)}
                >
                  {menuItem.text}
                </button>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </>
  )
}

export default forwardRef(PopperMenu)
