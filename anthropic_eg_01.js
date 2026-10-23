require("dotenv").config();
const Anthropic = require("@anthropic-ai/sdk");

const baseURL = process.env.ANTHROPIC_BASE_URL;
const apiKey = process.env.ANTHROPIC_API_KEY;
const authToken = process.env.ANTHROPIC_AUTH_TOKEN;

const client = new Anthropic({
  baseURL,
  apiKey, // required but ignored
  authToken,
});

const model = "qwen2.5-coder:7b";

async function main() {
  const message = await client.messages.create({
    model,
    max_tokens: 1024,
    messages: [
      { role: "user", content: "Write a function to check if a number is prime" },
    ],
  });

  console.log(message.content[0].text);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
