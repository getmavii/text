import fastify from "fastify";
import axios from "axios";
import readabilitySAX from "readabilitySAX";

const app = fastify({ logger: true });

app.get("/", async (request, reply) => {
  const { url } = request.query;
  const startTime = new Date();

  if (!url) {
    return reply.send({
      error: "Missing url parameter",
    });
  }

  try {
    const response = await axios.get(url, {
      headers: {
        "User-Agent":
          "Mozilla/5.0 (compatible; MaviiBot/1.0; +https://mavii.com/bots)",
      },
      responseType: "stream",
    });

    const readability = new readabilitySAX.WritableStream(
      {
        pageURL: url,
        type: "text",
      },
      (article) => {
        // Ignore nextPage
        delete article.nextPage;
        reply.send({
          ...article,
          time: new Date() - startTime,
        });
      }
    );

    response.data.pipe(readability);
  } catch (error) {
    reply.send({
      error: error.message,
    });
  }

  return reply;
});

const start = async () => {
  try {
    await app.listen({ port: 4000, host: "::" });
  } catch (err) {
    app.log.error(err);
    process.exit(1);
  }
};

start();
