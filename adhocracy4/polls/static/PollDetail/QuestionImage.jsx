/* eslint-disable no-restricted-syntax */
import React, { useState } from 'react'

const QuestionImage = ({ imageUrl, alt }) => {
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
    >
      <img
        src={imageUrl}
        alt={alt}
        className="poll__question-image-img"
      />
    </div>
  )
}

export default QuestionImage
