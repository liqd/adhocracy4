import {
  fileToQuestionImageDataUrl,
  getQuestionImageTargetSize
} from '../PollDashboard/utils'

describe('getQuestionImageTargetSize', () => {
  it('keeps images that are already small enough', () => {
    expect(getQuestionImageTargetSize(1500, 500)).toEqual({ width: 1500, height: 500 })
    expect(getQuestionImageTargetSize(1000, 800)).toEqual({ width: 1000, height: 800 })
  })

  it('scales large landscape images down to the maximum side', () => {
    expect(getQuestionImageTargetSize(4000, 3000)).toEqual({ width: 1500, height: 1125 })
    expect(getQuestionImageTargetSize(1500, 500)).toEqual({ width: 1500, height: 500 })
  })

  it('does not scale below the minimum resolution', () => {
    // Portrait: scaling to a 1600px longest side would be too narrow.
    expect(getQuestionImageTargetSize(2000, 4000)).toEqual({ width: 1500, height: 3000 })
    // Panorama: scaling to a 1600px longest side would be too flat.
    expect(getQuestionImageTargetSize(6000, 1000)).toEqual({ width: 3000, height: 500 })
  })

  it('handles missing dimensions', () => {
    expect(getQuestionImageTargetSize(0, 0)).toEqual({ width: 0, height: 0 })
  })
})

describe('fileToQuestionImageDataUrl', () => {
  it('reads small files without re-encoding them', async () => {
    const file = new File(['small image'], 'small.png', { type: 'image/png' })

    await expect(fileToQuestionImageDataUrl(file)).resolves.toMatch(
      /^data:image\/png;base64,/
    )
  })
})
