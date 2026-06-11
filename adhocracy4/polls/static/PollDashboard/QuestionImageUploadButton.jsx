/* eslint-disable no-restricted-syntax */
import React, { useRef } from 'react'
import django from 'django'

const QuestionImageUploadButton = ({ id, question, onImageChange, error }) => {
  const fileInputRef = useRef(null)

  const handleFileChange = (e) => {
    const file = e.target.files[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => onImageChange(reader.result)
      reader.readAsDataURL(file)
    }
  }

  const handleRemove = () => {
    onImageChange('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleUploadClick = () => {
    fileInputRef.current.click()
  }

  return (
    <div className="form-group">
      <label id={`image-upload-label-${id}`}>
        {django.gettext('Question image')}
      </label>

      <div className={`image-upload-container ${error ? 'is-invalid' : ''}`}>
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
            onClick={handleUploadClick}
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

      {error && (
        <div className="invalid-feedback" role="alert">
          {Array.isArray(error)
            ? error.map((err, i) => {
              // Handle ErrorDetail objects from Django
              const message = typeof err === 'object' && err.string ? err.string : err
              return <div key={i}>{message}</div>
            })
            : (typeof error === 'object' && error.string ? error.string : error)}
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        id={`id_questions-${id}-image`}
        accept="image/jpeg,image/png,image/webp"
        onChange={handleFileChange}
        className="image-upload-hidden-input"
        aria-invalid={!!error}
        aria-describedby={error ? `image-error-${id}` : undefined}
      />
    </div>
  )
}

export default QuestionImageUploadButton
