import React from 'react'

export const cleanPercentage = (percentage) => {
  const pct = (percentage * 100).toFixed(0)
  const isNegativeOrNaN = !Number.isFinite(+pct) || pct < 0
  const isTooHigh = pct > 100
  return isNegativeOrNaN ? 0 : isTooHigh ? 100 : +pct
}

const Circle = ({ color, percentage, size }) => {
  const adjustedSize = size - 3
  const circ = 2 * Math.PI * adjustedSize
  const strokePct = ((100 - percentage) * circ) / 100
  return (
    <circle
      r={adjustedSize}
      cx={175}
      cy={25}
      fill="transparent"
      stroke={strokePct !== circ ? color : ''}
      strokeWidth=".25rem"
      strokeDasharray={circ}
      strokeDashoffset={percentage ? strokePct : 0}
    />
  )
}

const Text = ({ percentage }) => {
  return (
    <text
      x="50%"
      y="50%"
      dominantBaseline="central"
      textAnchor="middle"
      fontSize="0.875rem"
    >
      {percentage}%
    </text>
  )
}

const ConfidenceCircle = ({ confidence, color, size = 25, defaultColor = 'lightgrey' }) => {
  const pct = cleanPercentage(confidence)
  return (
    <svg width={50} height={50} className="a4-confidence-circle">
      <g transform="rotate(-90 100 100)">
        <Circle color={defaultColor} size={size} />
        <Circle color={color} percentage={pct} size={size} />
      </g>
      <Text percentage={pct} />
    </svg>
  )
}

export default ConfidenceCircle
