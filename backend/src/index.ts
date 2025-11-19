import { readFile } from 'node:fs/promises';
import { join } from 'node:path';
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';
import { ReposDataSchema } from './schema.js';

const app = new Hono();

app.use('*', cors());
app.use('*', logger());

app.get('/api/repos', async (c) => {
  try {
    const reposPath = join(process.cwd(), 'repos.json');
    const fileContent = await readFile(reposPath, 'utf-8');
    const data = JSON.parse(fileContent);

    const validatedData = ReposDataSchema.parse(data);

    return c.json(validatedData);
  } catch (error) {
    if (error instanceof Error) {
      if ('code' in error && error.code === 'ENOENT') {
        return c.json(
          {
            error: 'File Not Found',
            message: 'repos.json file not found. Please run the CLI tool to generate it.',
          },
          404,
        );
      }

      if (error.name === 'ZodError') {
        return c.json(
          {
            error: 'Invalid Data',
            message: 'repos.json contains invalid data',
            details: error.message,
          },
          400,
        );
      }

      return c.json(
        {
          error: 'Internal Server Error',
          message: error.message,
        },
        500,
      );
    }

    return c.json(
      {
        error: 'Internal Server Error',
        message: 'An unexpected error occurred',
      },
      500,
    );
  }
});

app.get('/', (c) => {
  return c.json({
    name: 'GitHub Star Manager API',
    version: '1.0.0',
    endpoints: {
      repos: '/api/repos',
    },
  });
});

app.onError((err, c) => {
  console.error('Unhandled error:', err);
  return c.json(
    {
      error: 'Internal Server Error',
      message: err.message,
    },
    500,
  );
});

const port = process.env.PORT ? Number.parseInt(process.env.PORT, 10) : 3000;

console.log(`Server starting on http://localhost:${port}`);

export default {
  port,
  fetch: app.fetch,
};
