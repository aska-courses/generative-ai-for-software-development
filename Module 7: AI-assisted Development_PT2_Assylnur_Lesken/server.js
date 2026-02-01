/**
 * Data Validation API Server
 * Express server for validation endpoints
 */

const express = require('express');
const validationRouter = require('./src/api');

const app = express();
const PORT = process.env.PORT || 3000;

// Middleware
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// CORS for development (configure for production)
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*');
  res.header('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept');
  next();
});

// API Routes
app.use('/api/v1', validationRouter);

// Root endpoint
app.get('/', (req, res) => {
  res.json({
    name: 'Data Validation API',
    version: '1.0.0',
    status: 'running',
    endpoints: {
      validate: 'POST /api/v1/validate',
      rules: 'GET /api/v1/validation-rules',
      health: 'GET /api/v1/health'
    },
    documentation: '/docs/API_SPECIFICATION.md'
  });
});

// Error handling middleware
app.use((err, req, res, next) => {
  console.error('Server error:', err);
  res.status(500).json({
    error: 'Internal server error',
    message: process.env.NODE_ENV === 'development' ? err.message : 'An error occurred'
  });
});

// 404 handler
app.use((req, res) => {
  res.status(404).json({
    error: 'Not found',
    message: `Route ${req.method} ${req.url} not found`
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════════╗
║   Data Validation API Server                 ║
╚═══════════════════════════════════════════════╝

✓ Server running on http://localhost:${PORT}
✓ Environment: ${process.env.NODE_ENV || 'development'}
✓ API Version: 1.0.0

Available endpoints:
  POST   /api/v1/validate
  GET    /api/v1/validation-rules
  GET    /api/v1/health

Documentation: /docs/API_SPECIFICATION.md
  `);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received. Shutting down gracefully...');
  server.close(() => {
    console.log('Server closed');
    process.exit(0);
  });
});

module.exports = app;
