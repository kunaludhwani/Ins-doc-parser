# Sacha Advisor - Frontend

React + Vite frontend for the Sacha Advisor AI-powered insurance document explainer.

## Features

- 🎨 Red-themed animated UI with Framer Motion
- 📤 Drag-and-drop file upload
- ✨ Typing animation for AI explanations
- 📱 Responsive design with Tailwind CSS
- ⚡ Fast development with Vite

## Setup

### Prerequisites

- Node.js 16+ 
- npm or yarn

### Installation

```bash
cd frontend
npm install
```

### Development

```bash
npm run dev
```

The app will be available at `http://localhost:5173`

### Build

```bash
npm run build
```

## File Structure

```
src/
├── components/
│   ├── Header.jsx          # App header
│   ├── FileUpload.jsx      # Upload component with drag-drop
│   ├── LoadingSpinner.jsx  # Loading animation
│   ├── ResultDisplay.jsx   # Results display
│   └── ResultSection.jsx   # Reusable section component
├── App.jsx                 # Main app component
├── index.css              # Global styles with Tailwind
└── main.jsx               # React entry point
```

## API Integration

The frontend expects the backend to be running on `http://localhost:8000`

### Upload Endpoint

**POST** `/api/upload`

**Request:** multipart/form-data with `file` field

**Response:**
```json
{
  "status": "success",
  "is_insurance": true,
  "summary": "AI-generated explanation..."
}
```

or

```json
{
  "status": "error",
  "message": "Error message..."
}
```

## Styling

- **Primary Color:** `#E63946` (Red)
- **Accent:** White and Black
- Uses Tailwind CSS for utility-first styling
- Framer Motion for smooth animations

## Technologies

- React 18
- Vite
- Tailwind CSS
- Framer Motion
- Axios
