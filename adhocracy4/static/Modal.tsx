import React, { useId, useEffect, useRef, useState } from 'react'
import { createPortal } from 'react-dom'
import django from 'django'

const translated = {
  close: django.gettext('Close'),
  cancel: django.gettext('Cancel')
}

interface ModalPartials {
  title?: string
  body?: React.ReactNode
  description?: string
  hideFooter?: boolean
  bodyClass?: string
}

interface ModalProps {
  partials: ModalPartials
  handleSubmit?: (e?: React.MouseEvent) => void
  action?: string
  keepOpenOnSubmit?: boolean
  toggle: React.ReactNode
  onOpen?: () => void
  onClose?: () => void
}

const Modal = ({
  partials,
  handleSubmit,
  action,
  keepOpenOnSubmit,
  toggle,
  onOpen,
  onClose
}: ModalProps) => {
  const dialogRef = useRef<HTMLDialogElement>(null)
  const toggleButtonRef = useRef<HTMLButtonElement | null>(null)
  const uniqueId = useId()
  const titleId = `modal-title-${uniqueId}`
  const descriptionId = partials.description ? `modal-desc-${uniqueId}` : undefined
  const [isOpen, setIsOpen] = useState(false)

  const handleClose = () => {
    dialogRef.current?.close()
  }

  // Focus trap and initial focus
  useEffect(() => {
    const dialog = dialogRef.current
    if (!dialog) return

    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        handleClose()
      }
      if (e.key === 'Tab') {
        const focusableElements = dialog.querySelectorAll<HTMLElement>(
          'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
        )
        const firstElement = focusableElements[0]
        const lastElement = focusableElements[focusableElements.length - 1]

        if (e.shiftKey && document.activeElement === firstElement) {
          e.preventDefault()
          lastElement.focus()
        } else if (!e.shiftKey && document.activeElement === lastElement) {
          e.preventDefault()
          firstElement.focus()
        }
      }
    }

    if (isOpen) {
      dialog.addEventListener('keydown', handleKeyDown)
      // Set initial focus to first focusable element
      const focusableElements = dialog.querySelectorAll<HTMLElement>(
        'button, [href], input, select, textarea, [tabindex]:not([tabindex="-1"])'
      )
      if (focusableElements.length > 0) {
        setTimeout(() => focusableElements[0].focus(), 100)
      }
    }

    return () => {
      dialog.removeEventListener('keydown', handleKeyDown)
    }
  }, [isOpen])

  const focusButton = (button: HTMLButtonElement | null | undefined) => {
    if (button?.isConnected) {
      button.focus()
    }
  }

  useEffect(() => {
    const handleDialogClose = () => {
      setIsOpen(false)
      if (toggleButtonRef.current) {
        focusButton(toggleButtonRef.current)
        toggleButtonRef.current = null
      }
      onClose?.()
    }

    const dialog = dialogRef.current
    if (dialog) {
      dialog.addEventListener('close', handleDialogClose)
      return () => {
        dialog.removeEventListener('close', handleDialogClose)
      }
    }
    return undefined
  }, [onClose])

  const findDropdownToggle = (modalButton: HTMLElement): HTMLButtonElement => {
    return modalButton.closest('.dropdown')?.querySelector<HTMLButtonElement>('.dropdown-toggle[data-bs-toggle="dropdown"]') || modalButton as HTMLButtonElement
  }

  const handleOpen = (e: React.MouseEvent<HTMLElement>) => {
    e.preventDefault()
    toggleButtonRef.current = findDropdownToggle(e.currentTarget)
    dialogRef.current?.showModal()
    setIsOpen(true)
    onOpen?.()
  }

  const onConfirm = (e: React.MouseEvent<HTMLElement>) => {
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
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={descriptionId}
    >
      <div className="a4-modal__content">
        <header className="a4-modal__header">
          {partials.title && (
            <h2 className="a4-modal__title" id={titleId}>
              {partials.title}
            </h2>
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
            <div className="a4-modal__description" id={descriptionId}>
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
        ref={toggleButtonRef}
        className="a4-modal__toggle btn-link link"
        onClick={handleOpen}
        aria-haspopup="dialog"
        aria-expanded={isOpen}
      >
        {toggle}
      </button>
      {createPortal(dialogModal, document.body)}
    </>
  )
}

export default Modal
