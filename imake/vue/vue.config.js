const { defineConfig } = require('@vue/cli-service')
const path = require('path')
module.exports = defineConfig({
    transpileDependencies: true,
    outputDir: '../static/dist',
    publicPath: '/dist/',
})
