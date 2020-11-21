const {handler} = require('../get_trending_watchables')

it ('should return 405 if the method is not GET', async () => {
    const response = await handler({httpMethod:'POST'})

    expect(response.statusCode).toBe(405)
})

it('should return 200 if everything is fine', async() => {
    const response = await handler({httpMethod:'GET', queryStringParameters: {}})

    expect(response.statusCode).toBe(200)

    const body = JSON.parse(response.body)

    expect(body.length).toBeGreaterThan(0)
} )

it('should filter by type', async() => {
    const response = await handler({httpMethod:'GET', queryStringParameters: {type:'MOVIE'}})

    expect(response.statusCode).toBe(200)

    const body = JSON.parse(response.body)

    expect(body.every(watchable => watchable.type == 'MOVIE')).toBe(true)
} )
