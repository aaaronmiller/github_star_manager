# Svelte 5 Skill

## Overview
Best practices and patterns for building UIs with Svelte 5 and the Runes API.

## Core Patterns

### 1. Component State with $state
```svelte
<script lang="ts">
  let count = $state(0);
  let user = $state({ name: 'Alice', age: 30 });

  function increment() {
    count++;
  }
</script>

<button onclick={increment}>
  Count: {count}
</button>
```

### 2. Derived State with $derived
```svelte
<script lang="ts">
  let count = $state(0);
  let doubled = $derived(count * 2);
  let isEven = $derived(count % 2 === 0);
</script>

<p>Count: {count}</p>
<p>Doubled: {doubled}</p>
<p>Is even: {isEven}</p>
```

### 3. Effects with $effect
```svelte
<script lang="ts">
  let count = $state(0);

  $effect(() => {
    console.log(`Count changed to: ${count}`);

    // Cleanup function
    return () => {
      console.log('Cleanup');
    };
  });
</script>
```

### 4. API Data Fetching
```svelte
<script lang="ts">
  interface Repo {
    name: string;
    url: string;
  }

  let repos = $state<Repo[]>([]);
  let loading = $state(true);
  let error = $state<string | null>(null);

  async function loadRepos() {
    try {
      loading = true;
      const response = await fetch('/api/repos');
      if (!response.ok) throw new Error('Failed to fetch');
      repos = await response.json();
    } catch (e) {
      error = e instanceof Error ? e.message : 'Unknown error';
    } finally {
      loading = false;
    }
  }

  $effect(() => {
    loadRepos();
  });
</script>

{#if loading}
  <p>Loading...</p>
{:else if error}
  <p class="text-red-500">{error}</p>
{:else}
  <ul>
    {#each repos as repo}
      <li>{repo.name}</li>
    {/each}
  </ul>
{/if}
```

### 5. Props with TypeScript
```svelte
<script lang="ts">
  interface Props {
    title: string;
    count?: number;
    onIncrement?: () => void;
  }

  let { title, count = 0, onIncrement }: Props = $props();
</script>

<h1>{title}</h1>
<p>Count: {count}</p>
{#if onIncrement}
  <button onclick={onIncrement}>Increment</button>
{/if}
```

### 6. Tailwind Styling
```svelte
<div class="container mx-auto px-4 py-8">
  <h1 class="text-3xl font-bold text-gray-900 mb-6">
    Dashboard
  </h1>

  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
    {#each items as item}
      <div class="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition">
        <h2 class="text-xl font-semibold mb-2">{item.title}</h2>
        <p class="text-gray-600">{item.description}</p>
      </div>
    {/each}
  </div>
</div>
```

### 7. Event Handling
```svelte
<script lang="ts">
  function handleClick(event: MouseEvent) {
    console.log('Clicked!', event);
  }

  function handleSubmit(event: SubmitEvent) {
    event.preventDefault();
    const formData = new FormData(event.target as HTMLFormElement);
    // Process form data
  }
</script>

<button onclick={handleClick}>Click me</button>

<form onsubmit={handleSubmit}>
  <input type="text" name="query" />
  <button type="submit">Search</button>
</form>
```

## Best Practices
- Use $state for reactive values
- Use $derived for computed values
- Use $effect for side effects
- Type your props interface
- Use Tailwind utility classes
- Keep components focused and small
- Handle loading and error states
- Use semantic HTML
- Add ARIA labels for accessibility
- Mobile-first responsive design
