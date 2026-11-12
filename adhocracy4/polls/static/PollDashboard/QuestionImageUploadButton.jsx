/* eslint-disable no-restricted-syntax */
import React, { useEffect, useRef, useState } from 'react'
import django from 'django'
import '@uppy/core/css/style.min.css'
import '@uppy/dashboard/css/style.min.css'
import '@uppy/image-editor/css/style.min.css'
import Uppy from '@uppy/core'
import Dashboard from '@uppy/dashboard'
import ImageEditor from '@uppy/image-editor'
import deDE from '@uppy/locales/lib/de_DE.js'
import enUS from '@uppy/locales/lib/en_US.js'

import FormFieldError from '../../../static/FormFieldError'

const UPPY_LOCALES = {
  de: deDE,
  en: enUS
}

function getUppyLocale () {
  const pageLanguage = (document.documentElement.lang || 'en').toLowerCase()
  if (UPPY_LOCALES[pageLanguage]) {
    return UPPY_LOCALES[pageLanguage]
  }

  const languageCode = pageLanguage.split('-')[0]
  return UPPY_LOCALES[languageCode] || enUS
}

const OUTPUT_WIDTH = 2100
const OUTPUT_HEIGHT = 700
const MIN_OUTPUT_WIDTH = 300
const MAX_DATA_URL_LENGTH = 800 * 1024
const JPEG_QUALITY_STEPS = [0.85, 0.75, 0.65, 0.55, 0.45, 0.35]

const TRANSLATED = {
  imageTooLarge: django.gettext('The image could not be compressed enough. Please choose a smaller image.')
}

const readBlobAsDataUrl = (blob) => new Promise((resolve, reject) => {
  const reader = new FileReader()
  reader.onloadend = () => resolve(reader.result)
  reader.onerror = () => reject(reader.error)
  reader.readAsDataURL(blob)
})

const encodeCanvas = (canvas, hasTransparency) => {
  if (hasTransparency) {
    const png = canvas.toDataURL('image/png')
    if (png.length <= MAX_DATA_URL_LENGTH) {
      return png
    }
    // JPEG has no alpha channel. Put a white background behind the image
    // before falling back to a compressed JPEG.
    const context = canvas.getContext('2d')
    if (context) {
      context.globalCompositeOperation = 'destination-over'
      context.fillStyle = '#fff'
      context.fillRect(0, 0, canvas.width, canvas.height)
      context.globalCompositeOperation = 'source-over'
    }
  }

  let compressed = ''
  for (const quality of JPEG_QUALITY_STEPS) {
    compressed = canvas.toDataURL('image/jpeg', quality)
    if (compressed.length <= MAX_DATA_URL_LENGTH) {
      break
    }
  }
  return compressed
}

/**
 * The editor crops to 3:1 and 2100x700. Re-encode the result so the base64
 * payload stays below reverse proxy body limits. Opaque images become JPEG,
 * images with transparency stay PNG as long as the result fits. If even the
 * lowest quality is too large, the output dimensions are reduced step by step.
 * Rejects when no encoding fits so the caller can show an actionable error.
 */
const compressImageDataUrl = (dataUrl) => new Promise((resolve, reject) => {
  const image = new Image()
  image.onload = () => {
    let width = OUTPUT_WIDTH
    let height = OUTPUT_HEIGHT
    let hasTransparency = false
    let transparencyChecked = false
    let compressed = ''

    while (true) {
      const canvas = document.createElement('canvas')
      canvas.width = width
      canvas.height = height
      const context = canvas.getContext('2d')
      if (!context) {
        resolve(dataUrl)
        return
      }
      context.drawImage(image, 0, 0, width, height)

      if (!transparencyChecked) {
        try {
          const pixels = context.getImageData(0, 0, width, height).data
          for (let i = 3; i < pixels.length; i += 4) {
            if (pixels[i] < 255) {
              hasTransparency = true
              break
            }
          }
        } catch {
          hasTransparency = true
        }
        transparencyChecked = true
      }

      compressed = encodeCanvas(canvas, hasTransparency)
      if (compressed.length <= MAX_DATA_URL_LENGTH) {
        break
      }
      if (width <= MIN_OUTPUT_WIDTH) {
        reject(new Error('Image data URL exceeds the size limit.'))
        return
      }
      width = Math.max(MIN_OUTPUT_WIDTH, Math.round(width * 0.75))
      height = Math.max(1, Math.round(width * OUTPUT_HEIGHT / OUTPUT_WIDTH))
    }

    resolve(compressed)
  }
  image.onerror = () => resolve(dataUrl)
  image.src = dataUrl
})

const QuestionImageUploadButton = ({ id, question, onImageChange, errors, helpText, altText, onAltTextChange }) => {
  const uppyRef = useRef(null)
  const onImageChangeRef = useRef(onImageChange)
  const [processingError, setProcessingError] = useState('')

  onImageChangeRef.current = onImageChange

  const imageError = errors?.image_base64 || errors?.image
  const altTextError = errors?.image_alt_text

  useEffect(() => {
    let uppy
    let active = true

    try {
      uppy = new Uppy({
        autoProceed: false,
        locale: getUppyLocale(),
        restrictions: {
          maxNumberOfFiles: 1,
          allowedFileTypes: ['image/jpeg', 'image/png', 'image/webp']
        }
      })

      uppy.use(Dashboard, {
        target: document.body,
        inline: false,
        hideUploadButton: true,
        proudlyDisplayPoweredByUppy: false,
        autoOpen: 'imageEditor',
        note: django.gettext('Images are resized and compressed automatically before you save the form.')
      })

      uppy.use(ImageEditor, {
        quality: 0.8,
        actions: {
          revert: true,
          rotate: true,
          zoomIn: true,
          zoomOut: true,
          flip: false,
          granularRotate: false,
          cropSquare: false,
          cropWidescreen: false,
          cropWidescreenVertical: false
        },
        cropperOptions: {
          viewMode: 1,
          autoCropArea: 1,
          aspectRatio: OUTPUT_WIDTH / OUTPUT_HEIGHT,
          initialAspectRatio: OUTPUT_WIDTH / OUTPUT_HEIGHT,
          croppedCanvasOptions: {
            width: OUTPUT_WIDTH,
            height: OUTPUT_HEIGHT,
            imageSmoothingQuality: 'high'
          }
        }
      })

      uppy.on('file-added', (file) => {
        uppy.getPlugin('ImageEditor')?.stop()
        uppy.getFiles().forEach((existingFile) => {
          if (existingFile.id !== file.id) {
            uppy.removeFile(existingFile.id)
          }
        })
      })

      uppy.on('file-editor:cancel', () => {
        uppy.getPlugin('ImageEditor')?.stop()
      })

      uppy.on('file-editor:complete', () => {
        uppy.upload().catch(() => {})
      })

      uppy.on('complete', (result) => {
        const file = result.successful[0] || uppy.getFiles()[0]
        if (file) {
          readBlobAsDataUrl(file.data)
            .then(compressImageDataUrl)
            .then((compressed) => {
              // The editor may have been switched to another question or
              // unmounted while the image was processed.
              if (!active) return
              setProcessingError('')
              onImageChangeRef.current(compressed)
            })
            .catch(() => {
              if (active) setProcessingError(TRANSLATED.imageTooLarge)
            })
        }
        uppy.getPlugin('Dashboard')?.closeModal()

        uppy.getFiles().forEach((uppyFile) => {
          uppy.removeFile(uppyFile.id)
        })
      })

      uppyRef.current = uppy
    } catch (error) {
      console.error('QuestionImageUploadButton: Uppy init failed', error)
    }

    return () => {
      active = false
      if (uppy) {
        uppy.destroy()
      }
      uppyRef.current = null
    }
  }, [])

  const handleOpenModal = () => {
    const uppy = uppyRef.current
    if (!uppy) return
    setProcessingError('')
    // Uppy's maxNumberOfFiles restriction rejects a second file before
    // file-added fires, so clear the previously queued file before replacing
    // it with a new one.
    uppy.getFiles().forEach((file) => uppy.removeFile(file.id))
    uppy.getPlugin('Dashboard')?.openModal()
  }

  const handleRemove = () => {
    onImageChange('')
  }

  return (
    <div className="question-image-upload form-group">
      <label id={`image-upload-label-${id}`}>
        {django.gettext('Question image')}
      </label>

      {helpText && <div className="form-hint">{helpText}</div>}

      <div className={`image-upload-container ${imageError ? 'is-invalid' : ''}`}>
        <span className="image-upload-text">
          {question.image_url
            ? django.gettext('Image uploaded')
            : django.gettext('No image uploaded')}
        </span>

        <div className="image-upload-actions">
          {question.image_url && (
            <img
              id={`image-preview-${id}`}
              src={question.image_url}
              alt={django.gettext('Preview')}
              className="image-upload-preview"
            />
          )}

          <button
            type="button"
            className="image-upload-upload-btn"
            onClick={handleOpenModal}
            aria-label={django.gettext('Upload image')}
            title={django.gettext('Upload image')}
          >
            <i className="fa fa-cloud-upload" aria-hidden="true" />
          </button>

          {question.image_url && (
            <button
              type="button"
              className="image-upload-remove-btn"
              onClick={handleRemove}
              aria-label={django.gettext('Remove image')}
              title={django.gettext('Remove image')}
            >
              <i className="fa fa-times" aria-hidden="true" />
            </button>
          )}
        </div>
      </div>

      {processingError && (
        <div className="form-hint" role="alert">{processingError}</div>
      )}

      <FormFieldError id={`image-error-${id}`} error={errors} field="image_base64" />

      {(question.image_url || altTextError) && (
        <div className={`form-group ${altTextError ? 'has-error' : ''}`}>
          <label htmlFor={`id_questions-${id}-image_alt_text`}>
            {django.gettext('Alt text')}
            <span
              role="presentation"
              title={django.gettext('This field is required')}
            >
              *
            </span>
          </label>
          <input
            type="text"
            id={`id_questions-${id}-image_alt_text`}
            className={`form-control ${altTextError ? 'is-invalid' : ''}`}
            value={altText || ''}
            onChange={(e) => onAltTextChange(e.target.value)}
            maxLength={80}
            required
            aria-invalid={!!altTextError}
            aria-describedby={altTextError ? `alt-text-error-${id}` : undefined}
          />
          <FormFieldError id={`alt-text-error-${id}`} error={errors} field="image_alt_text" />
        </div>
      )}
    </div>
  )
}

export default QuestionImageUploadButton
