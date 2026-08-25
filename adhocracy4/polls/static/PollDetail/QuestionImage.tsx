/* eslint-disable no-restricted-syntax */
import React, { useState } from 'react'

interface QuestionImageProps {
  imageUrl?: string | null
  alt?: string
}

const QuestionImage = ({ imageUrl, alt }: QuestionImageProps) => {
  const [isExpanded, setIsExpanded] = useState(false)

  const handleClick = () => {
    setIsExpanded(!isExpanded)
  }

  return (
    <div
      className={`poll__question-image ${isExpanded ? 'poll__question-image--expanded' : ''}`}
      onClick={handleClick}
      role="button"
      tabIndex={0}
      onKeyDown={(e) => {
        if (e.key === 'Enter' || e.key === ' ') {
          e.preventDefault()
          setIsExpanded(!isExpanded)
        }
      }}
      style={{ cursor: isExpanded ? 'zoom-out' : 'zoom-in' }}
    >
      <img
        src={imageUrl as string | undefined}
        alt={alt}
        className="poll__question-image-img"
      />
      {!isExpanded && (
        <div className="poll__question-image-zoom-indicator">
          <i className="fa fa-search-plus" aria-hidden="true" />
        </div>
      )}
    </div>
  )
}

export default QuestionImage