import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
    plugins: [react()],
    build: {
        outDir: 'dist',
        assetsDir: 'assets',
        sourcemap: false, // Disable sourcemaps in production
        minify: 'terser', // Better minification
        terserOptions: {
            compress: {
                drop_console: true, // Remove console.logs in production
                drop_debugger: true
            }
        },
        rollupOptions: {
            input: {
                main: './index.html'
            },
            output: {
                manualChunks: {
                    'react-vendor': ['react', 'react-dom'],
                    'framer-motion': ['framer-motion'],
                    'pdf-vendor': ['jspdf', 'html2canvas'],
                    'share-vendor': ['react-share']
                }
            }
        },
        chunkSizeWarningLimit: 1000
    },
    publicDir: 'public',
    server: {
        port: 5173,
        proxy: {
            '/api': {
                target: 'http://localhost:8000',
                changeOrigin: true,
                rewrite: (path) => path
            }
        }
    },
    // Optimize dependencies
    optimizeDeps: {
        include: ['react', 'react-dom', 'framer-motion']
    }
})
