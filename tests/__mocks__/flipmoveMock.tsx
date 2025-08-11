import React from 'react'
import { vi } from 'vitest'

const FlipMove = ({ children }: { children: React.ReactNode }) => <>{children}</>

vi.mock('react-flip-move', () => ({
    __esModule: true,
  default: FlipMove
}))

export default FlipMove