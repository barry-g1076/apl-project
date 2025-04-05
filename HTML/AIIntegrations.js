require('dotenv').config(); // Load .env

const { OpenAI } = require('openai');

const openai = new OpenAI({
    apiKey: process.env.OPENAI_API_KEY, 
});

async function runChat() {
    const chatCompletion = await openai.chat.completions.create({
        model: "gpt-3.5-turbo",
        messages: [
            { role: "system", content: "You are a helpful assistant." },
            { role: "user", content: "How do I use OpenAI in JavaScript?" },
        ],
    });

    console.log(chatCompletion.choices[0].message.content);
}

runChat();