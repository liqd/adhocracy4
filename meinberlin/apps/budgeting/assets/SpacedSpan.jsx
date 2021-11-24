import React from 'react'

export const SpacedSpan = ({ className, children }) => {
  return (
    <>
      <span> </span>
      <span className={className}>
        {children}
      </span>
    </>
  )
}
