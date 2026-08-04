const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const router = express.Router();

router.use(
  '/',
  createProxyMiddleware({
    target: 'http://dash:8050',
    changeOrigin: true,
    pathRewrite: {
      '^/dashboard': '',
    },
  })  
);

module.exports = router;
