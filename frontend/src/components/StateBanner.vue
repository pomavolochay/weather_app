<template>
  <div class="banner" :class="variant" role="status">
    <slot />
  </div>
</template>

<script setup lang="ts">
const props = defineProps<{ variant?: 'info' | 'error' | 'success' }>()
const variant = computed(() => props.variant || 'info')
</script>

<style scoped>
.banner {
  width: 100%;
  border-radius: 16px;
  padding: 0.85rem 1.25rem;
  border: 1px solid rgba(148, 163, 184, 0.3);
  background: rgba(15, 23, 42, 0.5);
  color: #e2e8f0;
  font-weight: 500;
}

.banner.info {
  border-color: var(--accent);
}

.banner.error {
  border-color: var(--danger);
  color: var(--danger);
}

.banner.success {
  border-color: var(--success);
  color: var(--success);
}
</style>
