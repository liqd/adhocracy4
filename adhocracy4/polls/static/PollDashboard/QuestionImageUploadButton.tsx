/* eslint-disable no-restricted-syntax */
import React, { useRef } from 'react'
import django from 'django'
import FormFieldError from '../../../static/FormFieldError'
import type { PollQuestionEdit } from '../../../static/api/types'

interface QuestionImageUploadButtonProps {
  id: number | string
  question: PollQuestionEdit
  onImageChange?: (imageBase64: string | null) => void
  errors?: Record<string, string[]>
  helpText?: string
  altText?: string
  onAltTextChange?: (text: string) => void
}

const QuestionImageUploadButton = ({ id, question, onImageChange, errors, helpText, altText, onAltTextChange }: QuestionImageUploadButtonProps) => {
  const fileInputRef = useRef<HTMLInputElement>(null)
  const imageError = errors?.image_base64 || errors?.image
  const altTextError = errors?.image_alt_text

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      const reader = new FileReader()
      reader.onloadend = () => onImageChange?.(reader.result as string)
      reader.readAsDataURL(file)
    }
  }

  const handleRemove = () => {
    onImageChange?.('')
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const handleUploadClick = () => {
    fileInputRef.current?.click()
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

      <FormFieldError id={`image-error-${id}`} error={errors} field="image_base64" />

      {(question.image_url || altTextError) && (
        <div className={`form-group ${altTextError ? 'has-error' : ''}`}>
          <label htmlFor={`id_questions-${id}-image_alt_text`}>
            {django.gettext('Alt text')}
          </label>
          <input
            type="text"
            id={`id_questions-${id}-image_alt_text`}
            className={`form-control ${altTextError ? 'is-invalid' : ''}`}
            value={altText || ''}
            onChange={(e) => onAltTextChange?.(e.target.value)}
            maxLength={80}
            aria-invalid={!!altTextError}
            aria-describedby={altTextError ? `alt-text-error-${id}` : undefined}
          />
          <FormFieldError id={`alt-text-error-${id}`} error={errors} field="image_alt_text" />
        </div>
      )}

      <input
        ref={fileInputRef}
        type="file"
        id={`id_questions-${id}-image`}
        accept="image/jpeg,image/png,image/webp"
        onChange={handleFileChange}
        className="image-upload-hidden-input"
        aria-invalid={!!imageError}
        aria-describedby={imageError ? `image-error-${id}` : undefined}
      />
    </div>
  )
}

export default QuestionImageUploadButton