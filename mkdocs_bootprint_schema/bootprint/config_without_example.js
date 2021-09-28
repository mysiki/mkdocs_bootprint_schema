var path = require('path')
module.exports = {
    handlebars: {
        templates: path.join(__dirname, './template'),
        partials: path.join(__dirname, './partials_without_example')
    }
}