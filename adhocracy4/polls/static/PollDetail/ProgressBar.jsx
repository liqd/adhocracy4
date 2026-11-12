import React from 'react'

const ProgressBar = ({ current, total }) => {
  const percentage = total > 0 ? (current / total) * 100 : 0
  const rounded = Math.round(percentage)

  return (
    <div className="poll-progress">
      <div className="poll-progress__track">
        <div
          className="poll-progress__bar"
          role="progressbar"
          style={{ width: percentage + '%' }}
          aria-valuenow={rounded}
          aria-valuemin={0}
          aria-valuemax={100}
        />
      </div>
    </div>
  )
}

export default ProgressBar
