const watchables = require('./serialized_data.json')

exports.handler = async function(event, context) {
    let result = watchables;

    const {type, search} = event.queryStringParameters

    if (type == 'MOVIE' || type == 'SERIES')
        result = result.filter(watchable => watchable.type == type)

    if (search)
        result = result.filter(({title, synopsis}) => title.includes(search) || synopsis.includes(search))

    return {
        statusCode: 200,
        body: JSON.stringify(result)
    };
}