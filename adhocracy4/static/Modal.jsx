import React, { useId, useEffect, useRef } from 'react'
import { createPortal } from 'react-dom'
import django from 'django'

const translated = {
  close: django.gettext('Close'),
  cancel: django.gettext('Cancel')
}

const Modal = ({
  partials,
  handleSubmit,
  action,
  keepOpenOnSubmit,
  toggle,
  onOpen,
  onClose
}) => {
  const dialogRef = useRef(null)
  const uniqueId = useId()

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (event.target === dialogRef.current) {
        handleClose()
      }
    }

    const dialog = dialogRef.current
    if (dialog) {
      dialog.addEventListener('click', handleClickOutside)
      return () => dialog.removeEventListener('click', handleClickOutside)
    }
  })

  const handleOpen = (e) => {
    e.preventDefault()
    dialogRef.current?.showModal()
    onOpen?.()
  }

  const handleClose = () => {
    dialogRef.current?.close()
    onClose?.()
  }

  const onConfirm = (e) => {
    handleSubmit?.(e)
    if (!keepOpenOnSubmit) {
      handleClose()
    }
  }

  const dialogModal = (
    <dialog
      ref={dialogRef}
      id={uniqueId}
      className="a4-modal"
    >
      <div className="a4-modal__content">
        <header className="a4-modal__header">
          {partials.title && (
            <h2 className="a4-modal__title">{partials.title}</h2>
          )}
          <button
            className="a4-modal__close"
            aria-label={translated.close}
            onClick={handleClose}
            type="button"
          >
            <i className="fa fa-times" aria-hidden="true" />
          </button>
        </header>
        <div className={'a4-modal__body ' + (partials.bodyClass || '')}>
          {partials.description && (
            <div className="a4-modal__description">
              {partials.description}
            </div>
          )}
          {partials.body}
        </div>
        {!partials.hideFooter && (
          <footer className="form-submit-flex-end">
            <button
              className="a4-modal__cancel link form-submit-flex-end__link"
              onClick={handleClose}
              type="button"
            >
              {translated.cancel}
            </button>
            <button
              className="a4-modal__submit button"
              onClick={onConfirm}
              type="button"
            >
              {action}
            </button>
          </footer>
        )}
      </div>
    </dialog>
  )

  return (
    <>
      <button
        className="a4-modal__toggle btn-link link"
        onClick={handleOpen}
      >
        {toggle}
      </button>
      {createPortal(dialogModal, document.body)}
    </>
  )
}

export default Modal
