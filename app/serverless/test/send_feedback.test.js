const {handler} = require('../send_feedback')

it ('should return 405 if the method is not POST', async () => {
    const response = await handler({httpMethod:'GET'})

    expect(response.statusCode).toBe(405)
})

it ('should return 400 if the body is not present', async () => {
    const response = await handler({httpMethod:'POST', body:''})

    expect(response.statusCode).toBe(400)
})
it ('should return 400 if the feedback is offensive', async () => {
    const response = await handler({httpMethod:'POST', body:'{"feedback":"You are such a retard"}'})

    expect(response.statusCode).toBe(400)
})

