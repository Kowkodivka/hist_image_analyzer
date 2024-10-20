import path from 'path'
import { fileURLToPath } from 'url'
import { dirname } from 'path'
import { BrowserWindow, app, shell } from 'electron'

let window: BrowserWindow

const __filename = fileURLToPath(import.meta.url)
const __dirname = dirname(__filename)

const appName = 'Hist Image Analyzer'
const urlPage = path.join(__dirname, 'public', 'index.html')
const urlPreload = path.join(__dirname, 'preload.js')

async function createWindow() {
  const options = {
    title: appName,
    width: 1080,
    height: 720,
    show: false,
    webPreferences: {
      nodeIntegration: false,
      contextIsolation: true,
      preload: urlPreload,
    },
  }

  window = new BrowserWindow(options)
  window.loadFile(urlPage)

  window.once('ready-to-show', () => {
    window.show()
  })

  window.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })
}

app.on('ready', async () => {
  await createWindow()

  app.on('activate', async () => {
    if (BrowserWindow.getAllWindows.length === 0) await createWindow()
  })
})

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})
