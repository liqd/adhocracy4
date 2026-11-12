import React from 'react'

export const LoadingSpinner = () => (
  <div className="u-spinner__container">
    <i className="fa fa-spinner fa-pulse" aria-hidden="true" />
    <span className="visually-hidden">Loading...</span>
  </div>
)

export const LoadingOverlay = () => (
  <div className="poll-loading-overlay">
    <LoadingSpinner />
  </div>
)
