// Generate a unique storage key based on URL path and inputId
function getStorageKey (inputId) {
  const urlPath = window.location.pathname
  const storageKey = 'image_upload_' + urlPath + '_' + inputId
  return storageKey
}

// Check if referer is from the same page, clear images if not
function checkRefererAndClearIfNeeded () {
  try {
    const referer = document.referrer
    const currentOrigin = window.location.origin
    const currentPathname = window.location.pathname

    // If no referer, clear all images
    if (!referer) {
      clearAllImagesFromStorage()
      return
    }

    try {
      const refererUrl = new URL(referer)
      // Check if referer is from same origin AND same page
      if (refererUrl.origin !== currentOrigin || refererUrl.pathname !== currentPathname) {
        clearAllImagesFromStorage()
      }
    } catch (e) {
      // If referer URL is invalid, clear images for security
      clearAllImagesFromStorage()
    }
  } catch (e) {
    console.error('Error in checkRefererAndClearIfNeeded:', e)
    // On error, clear images for security
    clearAllImagesFromStorage()
  }
}

function init () {
  console.log('init image_uploader version 2.1.8')
  // Check referer before loading images
  checkRefererAndClearIfNeeded()
  // Check if form was saved before loading images
  checkIfFormWasSaved()

  const clearInputs = document.querySelectorAll('input[data-upload-clear]')
  const previewImages = document.querySelectorAll('img[data-upload-preview]')

  previewImages.forEach(function (previewImage) {
    previewImage = document.getElementById(previewImage.id)
    const inputId = previewImage.dataset.uploadPreview
    const clearInput = Array.from(clearInputs).filter(function (el) {
      return el.matches('[data-upload-clear="' + inputId + '"]')
    })

    // Load saved image from sessionStorage on page load
    loadImageFromStorage(inputId, previewImage)

    document.querySelector('#' + inputId).addEventListener('change', function (e) {
      const domInput = e.target
      if (domInput.files && domInput.files[0]) {
        const file = domInput.files[0]
        const name = file.name
        const sizeInBytes = file.size
        const sizeInMB = (sizeInBytes / (1024 * 1024)).toFixed(2) // Convert bytes to MB and round to 2 decimal places
        const text = document.querySelector('#text-' + inputId)

        // Update the file name and size in the associated text input
        if (text != null) {
          text.value = name + ' - ' + sizeInMB + ' MB of 5MB'

          // Highlight in red if the size exceeds 5MB
          if (sizeInMB > 5) {
            text.style.color = 'red'
          } else {
            text.style.color = '' // Reset to default color
          }
        }

        // Add the file size to a custom data attribute on the preview image
        previewImage.dataset.fileSize = sizeInBytes

        // If supported, read the file as a URL for preview purposes
        if (window.FileReader) {
          const reader = new window.FileReader()
          reader.addEventListener('load', function (e) {
            previewImage.setAttribute('src', e.target.result)
            saveImageToStorage(inputId, e.target.result, name, sizeInBytes)
            if (clearInput[0]) {
              clearInput[0].checked = false
            }
          })
          reader.readAsDataURL(file)
        } else if (clearInput[0]) {
          clearInput[0].checked = false
        }

        // Add the file size to the URL (if required for backend processing)
        const currentUrl = new URL(window.location.href)
        currentUrl.searchParams.set('file_size', sizeInBytes) // Add file_size as a query parameter
        window.history.replaceState(null, '', currentUrl.toString())
      }
    })

    // Clear sessionStorage when image is removed
    if (clearInput[0]) {
      clearInput[0].addEventListener('change', function (e) {
        if (e.target.checked) {
          clearImageFromStorage(inputId)
        }
      })
    }
  })

  // Listen for form submit to set saved flag
  setupFormSubmitListener()
}

// Check if form was saved on previous page load
function checkIfFormWasSaved () {
  console.log('Checking if form was saved')
  try {
    const savedFlagKey = 'flag_image_upload_form_saved_' + window.location.pathname
    const wasSaved = sessionStorage.getItem(savedFlagKey)

    if (wasSaved !== 'true') {
      console.log('Form was not saved, clearing all images')
      clearAllImagesFromStorage()
    } else {
      sessionStorage.removeItem(savedFlagKey)
      console.log('Form was saved, removing flag')
    }
  } catch (e) {
    console.error('Error in checkIfFormWasSaved:', e)
  }
}

// Mark form as saved
function markFormAsSaved () {
  try {
    sessionStorage.setItem('flag_image_upload_form_saved_' + window.location.pathname, 'true')
  } catch (e) {
    console.error('Error in markFormAsSaved:', e)
  }
}

// Setup form submit listener to mark form as saved
function setupFormSubmitListener () {
  try {
    const previewImages = document.querySelectorAll('img[data-upload-preview]')
    if (previewImages.length === 0) return

    const form = previewImages[0].closest('form')
    if (!form) return

    // Listen for submit button clicks
    const submitButtons = form.querySelectorAll('input[type="submit"], button[type="submit"], button:not([type])')
    submitButtons.forEach(function (button) {
      button.addEventListener('click', markFormAsSaved, { capture: true })
    })

    // Also listen for form submit as backup
    form.addEventListener('submit', markFormAsSaved, { capture: true })
  } catch (e) {
    console.error('Error in setupFormSubmitListener:', e)
  }
}

// Save image data to sessionStorage
function saveImageToStorage (inputId, imageDataUrl, fileName, fileSize) {
  try {
    const imageData = {
      dataUrl: imageDataUrl,
      fileName,
      fileSize,
      timestamp: Date.now(),
      pagePath: window.location.pathname
    }
    sessionStorage.setItem(getStorageKey(inputId), JSON.stringify(imageData))
  } catch (e) {
    console.warn('Could not save image to sessionStorage:', e)
  }
}

// Load image data from sessionStorage
function loadImageFromStorage (inputId, previewImage) {
  try {
    // Check if image already has a server URL - if so, clear sessionStorage but keep server image
    if (previewImage.src && !previewImage.src.startsWith('data:') && previewImage.src.length > 0) {
      sessionStorage.removeItem(getStorageKey(inputId))
      return
    }

    const savedData = sessionStorage.getItem(getStorageKey(inputId))
    if (!savedData) return

    const imageData = JSON.parse(savedData)

    // Check if image is from a different page
    if (imageData.pagePath && imageData.pagePath !== window.location.pathname) {
      clearImageFromStorage(inputId)
      return
    }

    const maxAge = 30 * 60 * 1000 // 30 min in milliseconds
    if (Date.now() - imageData.timestamp < maxAge) {
      previewImage.setAttribute('src', imageData.dataUrl)
      previewImage.dataset.fileSize = imageData.fileSize
      restorePreviewText(inputId, imageData)
      restoreFileToInput(inputId, imageData)
    } else {
      clearImageFromStorage(inputId)
    }
  } catch (e) {
    console.warn('Could not load image from SessionStorage:', e)
    clearImageFromStorage(inputId)
  }
}

function restorePreviewText (inputId, imageData) {
  const text = document.querySelector('#text-' + inputId)
  if (text && imageData.fileName) {
    const sizeInMB = (imageData.fileSize / (1024 * 1024)).toFixed(2)
    text.value = imageData.fileName + ' - ' + sizeInMB + ' MB of 5MB'

    // Highlight in red if the size exceeds 5MB
    if (sizeInMB > 5) {
      text.style.color = 'red'
    } else {
      text.style.color = ''
    }
  }
}

// Restore file object from base64 data to input element
function restoreFileToInput (inputId, imageData) {
  try {
    const inputElement = document.querySelector('#' + inputId)
    if (!inputElement) {
      console.warn('Input element not found:', inputId)
      return
    }

    // Convert base64 data URL to File object
    const mimeType = imageData.dataUrl.split(',')[0].split(':')[1].split(';')[0]
    const byteCharacters = atob(imageData.dataUrl.split(',')[1])
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: mimeType })
    const file = new File([blob], imageData.fileName, { type: mimeType, lastModified: Date.now() })

    // Set file to input element using DataTransfer API
    const dataTransfer = new DataTransfer()
    dataTransfer.items.add(file)
    inputElement.files = dataTransfer.files
  } catch (e) {
    console.warn('Could not restore file to input:', e)
  }
}

// Clear image data from sessionStorage and reset UI
function clearImageFromStorage (inputId) {
  try {
    sessionStorage.removeItem(getStorageKey(inputId))

    const inputElement = document.querySelector('#' + inputId)
    if (inputElement) {
      inputElement.value = ''
    }

    const previewImage = document.querySelector('img[data-upload-preview="' + inputId + '"]')
    console.log('previewImage', previewImage)
    console.log('previewImage.src', previewImage.src)
    if (previewImage) {
      // Only clear src if it's a data URL, not a server URL
      if (previewImage.src && previewImage.src.startsWith('data:')) {
        console.log('Clearing preview image data URL')
        previewImage.setAttribute('src', '')
      }
    }

    const text = document.querySelector('#text-' + inputId)
    if (text) {
      text.value = ''
      text.style.color = ''
    }
  } catch (e) {
    console.warn('Could not clear image from sessionStorage:', e)
  }
}

// Clear all image upload data from sessionStorage
function clearAllImagesFromStorage () {
  try {
    // Find all preview images and clear their storage and UI
    const previewImages = document.querySelectorAll('img[data-upload-preview]')
    previewImages.forEach(function (previewImage) {
      const inputId = previewImage.dataset.uploadPreview
      if (inputId) {
        clearImageFromStorage(inputId)
      }
    })
  } catch (e) {
    console.error('Error in clearAllImagesFromStorage:', e)
  }
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
