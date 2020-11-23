const https = require('https');
const badWords = require('./bad-words')

const CHANNEL_NAME = '@sugerenciasQueVemos'

const headers = {
    'Access-Control-Allow-Origin': '*',
    'Content-Type': 'application/json; charset=UTF-8',
    'Access-Control-Allow-Headers': 'Content-Type',
}

exports.handler = async function(event, context) {

    if (event.httpMethod == 'OPTIONS')
        return {
            statusCode: 200,
            headers
        }
    else if (event.httpMethod != 'POST')
        return {
            statusCode: 405
        }

    let feedback

    try {
        feedback = JSON.parse(event.body).feedback
    }
    catch{
        return {
            statusCode: 400,
            body: JSON.stringify({msg: 'Bad request, couldnt parse json body'}),
            headers
        }
    }

    if (isOffensive(feedback))
        return {
            statusCode:400,
            body: JSON.stringify({msg:'Offensive feedback is not useful'}),
            headers
        }

    try{
        await sendMsgToTelegram(feedback)
    }
    catch{
        return {
            statusCode: 500,
            body: JSON.stringify({msg: 'Could not reach telegram service'}),
            headers
        }
    }

    return {
        statusCode: 201,
        body: JSON.stringify({msg:'Feedback sent'}),
        headers
    }
}


function sendMsgToTelegram(msg){
    return new Promise((resolve, reject) => {
        https.get(`https://api.telegram.org/bot${process.env.TELEGRAM_BOT_KEY}/sendMessage?chat_id=${CHANNEL_NAME}&text=${msg}`, (res) => {
            if (res.statusCode !== 200)
                reject()
            else
                resolve()
        });
    })
}

function isOffensive(msg){
    const msgWords = msg.split(' ')

    return msgWords.some(word => badWords.includes(word))
}

