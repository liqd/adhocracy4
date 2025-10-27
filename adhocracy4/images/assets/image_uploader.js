function init () {
  const clearInputs = document.querySelectorAll('input[data-upload-clear]')
  const previewImages = document.querySelectorAll('img[data-upload-preview]')

  previewImages.forEach(function (previewImage) {
    previewImage = document.getElementById(previewImage.id)
    const inputId = previewImage.dataset.uploadPreview
    const clearInput = Array.from(clearInputs).filter(function (el) {
      return el.matches('[data-upload-clear="' + inputId + '"]')
    })

    // Load saved image from localStorage on page load
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
            if (clearInput?.[0]) {
              clearInput[0].checked = false
            }
            // Save image to localStorage
          })
          reader.readAsDataURL(file)
        } else if (clearInput?.[0]) {
          clearInput[0].checked = false
        }

        // Add the file size to the URL (if required for backend processing)
        const currentUrl = new URL(window.location.href)
        currentUrl.searchParams.set('file_size', sizeInBytes) // Add file_size as a query parameter
        window.history.replaceState(null, '', currentUrl.toString())
      }
    })

    // Clear localStorage when image is removed
    if (clearInput[0]) {
      clearInput[0].addEventListener('change', function (e) {
        if (e.target.checked) {
          clearImageFromStorage(inputId)
        }
      })
    }
  })
}

// Save image data to localStorage
function saveImageToStorage (inputId, imageDataUrl, fileName, fileSize) {
  console.log('Saving image to localStorage3:', inputId, imageDataUrl, fileName, fileSize)
  try {
    const imageData = {
      dataUrl: imageDataUrl,
      fileName,
      fileSize,
      timestamp: Date.now()
    }
    console.log('Try Saving image to localStorage:', imageData)
    localStorage.setItem('image_upload_' + inputId, JSON.stringify(imageData))
  } catch (e) {
    console.warn('Could not save image to localStorage:', e)
  }
}

// Load image data from localStorage
function loadImageFromStorage (inputId, previewImage) {
  try {
    // Check if image already has a server URL - if so, clear localStorage but keep server image
    if (previewImage.src && !previewImage.src.startsWith('data:') && previewImage.src.length > 0) {
      console.log('Server image exists, clearing localStorage')
      localStorage.removeItem('image_upload_' + inputId)
      return
    }

    const savedData = localStorage.getItem('image_upload_' + inputId)
    console.log('Loading image from localStorage saved Data5:', savedData)
    if (savedData) {
      const imageData = JSON.parse(savedData)

      // Check if data is not too old (24 hours)
      const maxAge = 30 * 60 * 1000 // 30 min  in milliseconds
      if (Date.now() - imageData.timestamp < maxAge) {
        // Restore preview image
        previewImage.setAttribute('src', imageData.dataUrl)

        // Restore text input with file info
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

        // Restore file size data attribute
        previewImage.dataset.fileSize = imageData.fileSize

        // Restore file to input element so it can be uploaded
        restoreFileToInput(inputId, imageData)

        // Uncheck clear input if it exists
        const clearInput = document.querySelector('input[data-upload-clear="' + inputId + '"]')
        if (clearInput) {
          clearInput.checked = false
        }
      } else {
        // Remove expired data
        clearImageFromStorage(inputId)
      }
    }
  } catch (e) {
    console.warn('Could not load image from localStorage:', e)
    clearImageFromStorage(inputId)
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
    const byteCharacters = atob(imageData.dataUrl.split(',')[1])
    const byteNumbers = new Array(byteCharacters.length)
    for (let i = 0; i < byteCharacters.length; i++) {
      byteNumbers[i] = byteCharacters.charCodeAt(i)
    }
    const byteArray = new Uint8Array(byteNumbers)
    const blob = new Blob([byteArray], { type: 'image/png' })

    // Convert blob to File object
    const file = new File([blob], imageData.fileName, { type: 'image/png', lastModified: Date.now() })

    // Set file to input element using DataTransfer API
    const dataTransfer = new DataTransfer()
    dataTransfer.items.add(file)
    inputElement.files = dataTransfer.files

    console.log('File restored to input:', file.name, file.size)
  } catch (e) {
    console.warn('Could not restore file to input:', e)
  }
}

// Clear image data from localStorage and reset UI
function clearImageFromStorage (inputId) {
  try {
    // Remove from localStorage
    localStorage.removeItem('image_upload_' + inputId)

    // Clear the file input element
    const inputElement = document.querySelector('#' + inputId)
    if (inputElement) {
      inputElement.value = ''
    }

    // Clear the preview image
    const previewImage = document.querySelector('img[data-upload-preview="' + inputId + '"]')
    if (previewImage) {
      previewImage.setAttribute('src', '')
    }

    // Clear the text input
    const text = document.querySelector('#text-' + inputId)
    if (text) {
      text.value = ''
      text.style.color = ''
    }

    console.log('Image cleared from input:', inputId)
  } catch (e) {
    console.warn('Could not clear image from localStorage:', e)
  }
}

document.addEventListener('DOMContentLoaded', init, false)
document.addEventListener('a4.embed.ready', init, false)
