let maxLocalKey = 0

export const getNextLocalKey = () => 'local_' + (maxLocalKey++)

// Question images are posted as base64 inside the poll JSON payload. Keep the
// encoded image small enough that the request stays below reverse proxy body
// limits (the preview proxy currently allows about 128 KB), while never
// scaling below the backend's minimum resolution.
const QUESTION_IMAGE_MIN_WIDTH = 1500
const QUESTION_IMAGE_MIN_HEIGHT = 500
const QUESTION_IMAGE_MAX_SIDE = 1500
const QUESTION_IMAGE_MAX_DATA_URL_LENGTH = 100 * 1024
const QUESTION_IMAGE_DIRECT_READ_MAX_BYTES = 60 * 1024
const QUESTION_IMAGE_QUALITY_STEPS = [0.85, 0.75, 0.65, 0.55, 0.45, 0.35, 0.25]

export const getQuestionImageTargetSize = (width, height) => {
  if (!width || !height) {
    return { width, height }
  }

  const landscape = width >= height
  const longestSide = landscape ? width : height
  const maxSideScale = Math.min(1, QUESTION_IMAGE_MAX_SIDE / longestSide)
  const minWidthScale = width >= QUESTION_IMAGE_MIN_WIDTH
    ? QUESTION_IMAGE_MIN_WIDTH / width
    : 0
  const minHeightScale = height >= QUESTION_IMAGE_MIN_HEIGHT
    ? QUESTION_IMAGE_MIN_HEIGHT / height
    : 0
  const minScale = Math.max(minWidthScale, minHeightScale)
  const scale = Math.min(1, Math.max(maxSideScale, minScale))

  return {
    width: Math.max(1, Math.round(width * scale)),
    height: Math.max(1, Math.round(height * scale))
  }
}

const readFileAsDataUrl = (file) => new Promise((resolve, reject) => {
  const reader = new FileReader()
  reader.onloadend = () => resolve(reader.result)
  reader.onerror = () => reject(reader.error)
  reader.readAsDataURL(file)
})

const loadImage = (file) => new Promise((resolve, reject) => {
  const objectUrl = URL.createObjectURL(file)
  const image = new Image()

  image.onload = () => {
    URL.revokeObjectURL(objectUrl)
    resolve(image)
  }
  image.onerror = () => {
    URL.revokeObjectURL(objectUrl)
    reject(new Error('Could not load image'))
  }
  image.src = objectUrl
})

const drawImageDataUrl = (image, width, height, quality) => {
  const canvas = document.createElement('canvas')
  canvas.width = width
  canvas.height = height

  const context = canvas.getContext('2d')
  // JPEG has no alpha channel; fill with white so transparent PNGs do not
  // turn black when they are converted.
  context.fillStyle = '#fff'
  context.fillRect(0, 0, width, height)
  context.drawImage(image, 0, 0, width, height)

  return canvas.toDataURL('image/jpeg', quality)
}

/**
 * Convert a selected file to a base64 data URL that is safe to submit with the
 * poll update request. Small files are passed through untouched; larger ones
 * are scaled down and re-encoded as JPEG until the payload fits.
 */
export const fileToQuestionImageDataUrl = async (file) => {
  if (file.size <= QUESTION_IMAGE_DIRECT_READ_MAX_BYTES) {
    return readFileAsDataUrl(file)
  }

  const image = await loadImage(file)
  const targetSize = getQuestionImageTargetSize(
    image.naturalWidth || image.width,
    image.naturalHeight || image.height
  )

  let dataUrl = ''
  for (const quality of QUESTION_IMAGE_QUALITY_STEPS) {
    dataUrl = drawImageDataUrl(image, targetSize.width, targetSize.height, quality)
    if (dataUrl.length <= QUESTION_IMAGE_MAX_DATA_URL_LENGTH) {
      break
    }
  }

  return dataUrl
}

/** Only used in tests to make generated keys deterministic. */
export const resetLocalKeys = () => {
  maxLocalKey = 0
}

export const createEmptyChoice = (isOther = false) => ({
  key: getNextLocalKey(),
  label: isOther ? 'other' : '',
  is_other_choice: isOther
})

export const createEmptyQuestion = (isOpen, multipleChoice = false) => ({
  key: getNextLocalKey(),
  label: '',
  help_text: '',
  multiple_choice: multipleChoice,
  is_open: isOpen,
  is_confidential: false,
  choices: isOpen ? [] : [createEmptyChoice(), createEmptyChoice()],
  image_base64: null,
  image_url: null,
  image_alt_text: ''
})

/**
 * Questions returned by the poll API are enriched with read-only fields
 * (userChoices, vote counts, ...). Attach stable local keys so the
 * management UI can track items (also unsaved ones) without ids.
 */
export const normalizeQuestion = (question) => ({
  ...question,
  key: question.id != null ? 'q_' + question.id : getNextLocalKey(),
  choices: (question.choices || []).map((choice) => ({
    ...choice,
    key: choice.id != null ? 'c_' + choice.id : getNextLocalKey()
  }))
})

const READ_ONLY_QUESTION_FIELDS = [
  'key',
  'answers',
  'image_url',
  'image_help_text',
  'userChoices',
  'userAnswer',
  'other_choice_answers',
  'other_choice_user_answer',
  'totalVoteCount',
  'totalVoteCountMulti',
  'totalAnswerCount',
  'isReadOnly',
  'authenticated',
  'count'
]

const READ_ONLY_CHOICE_FIELDS = ['key', 'count']

const omit = (object, fields) =>
  Object.keys(object).reduce((result, field) => {
    if (!fields.includes(field)) {
      result[field] = object[field]
    }
    return result
  }, {})

/**
 * Build the questions payload for the poll update API.
 * Read-only fields coming from the API are stripped so the request body
 * only contains what the backend serializer/service understands.
 */
export const buildQuestionsPayload = (questions) =>
  questions.map((question) => {
    const payload = omit(question, READ_ONLY_QUESTION_FIELDS)

    payload.choices = (question.choices || []).map((choice) =>
      omit(choice, READ_ONLY_CHOICE_FIELDS)
    )

    if (question.image_base64 !== undefined) {
      payload.image_base64 = question.image_base64
    }
    payload.image_alt_text = question.image_alt_text || ''
    return payload
  })

export const moveItem = (items, from, to) => {
  if (from === to || from < 0 || to < 0 || from >= items.length || to >= items.length) {
    return items
  }
  const result = [...items]
  const [moved] = result.splice(from, 1)
  result.splice(to, 0, moved)
  return result
}
