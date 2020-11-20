const watchables = require('./serialized_data.json')

const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE'
};

exports.handler = async function(event, context) {

    let result = watchables;

    const {type, search, orderBy} = event.queryStringParameters

    if (type == 'MOVIE' || type == 'SERIES')
        result = result.filter(watchable => watchable.type == type)

    if (search)
        result = result.filter(({title, synopsis}) => title.includes(search) || synopsis.includes(search))

    if (orderBy){
        const [field, order] = orderBy.split(',')

        if (order == 'ASC')
            result.sort((a,b) => a[field] - b[field])
        else
            result.sort((a,b) => b[field] - a[field])

    }

    return {
        statusCode: 200,
        headers,
        body: JSON.stringify(result)
    };
}