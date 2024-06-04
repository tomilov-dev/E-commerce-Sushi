const path = require('path');

module.exports = {
    entry: './backend/staticfiles/js/dependencies.js',
    output: {
      path: path.resolve(__dirname, 'backend/staticfiles/js'),
      filename: 'bundle.js',
    },
};