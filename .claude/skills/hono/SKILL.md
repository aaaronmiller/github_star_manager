# Hono Framework Skill

## Overview
Best practices and patterns for building APIs with Hono framework.

## Core Patterns

### 1. Basic Hono App Structure
```typescript
import { Hono } from 'hono';
import { cors } from 'hono/cors';
import { logger } from 'hono/logger';

const app = new Hono();

// Middleware
app.use('*', cors());
app.use('*', logger());

// Routes
app.get('/api/resource', async (c) => {
  return c.json({ data: [] });
});

export default app;
```

### 2. Zod Validation Pattern
```typescript
import { z } from 'zod';
import { zValidator } from '@hono/zod-validator';

const schema = z.object({
  name: z.string().min(1),
  url: z.string().url(),
});

app.post('/api/resource', zValidator('json', schema), async (c) => {
  const data = c.req.valid('json');
  // data is fully typed
  return c.json({ success: true, data });
});
```

### 3. Error Handling
```typescript
app.onError((err, c) => {
  console.error(err);
  return c.json({
    error: 'Internal Server Error',
    message: err.message
  }, 500);
});

// Custom error responses
app.get('/api/resource/:id', async (c) => {
  const id = c.req.param('id');
  const resource = await findResource(id);

  if (!resource) {
    return c.json({ error: 'Resource not found' }, 404);
  }

  return c.json(resource);
});
```

### 4. Environment Variables (Cloudflare)
```typescript
type Bindings = {
  DATABASE: D1Database;
  BUCKET: R2Bucket;
  API_KEY: string;
};

const app = new Hono<{ Bindings: Bindings }>();

app.get('/api/data', async (c) => {
  const db = c.env.DATABASE;
  const results = await db.prepare('SELECT * FROM table').all();
  return c.json(results);
});
```

### 5. Grouping Routes
```typescript
const app = new Hono();
const api = new Hono();

api.get('/repos', getRepos);
api.post('/repos', createRepo);

app.route('/api', api);
```

## Best Practices
- Always validate input with Zod
- Use TypeScript for type safety
- Return appropriate HTTP status codes
- Handle errors gracefully
- Use middleware for cross-cutting concerns
- Keep routes thin, business logic separate
- Add CORS middleware for frontend access
