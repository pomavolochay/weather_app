<template>
  <form class="form" @submit.prevent="onSubmit">
    <div class="input-wrapper">
      <label class="sr-only" for="city-input">{{ t('formLabel') }}</label>
      <input
        id="city-input"
        v-model="draft"
        type="text"
        :placeholder="t('formPlaceholder')"
        autocomplete="off"
        required
      />
    </div>
    <button type="submit" :disabled="disabled">
      <span v-if="disabled">{{ t('formSubmitting') }}</span>
      <span v-else>{{ t('formSubmit') }}</span>
    </button>
  </form>
</template>

<script setup lang="ts">
const props = defineProps<{ disabled?: boolean; modelValue: string }>()
const emits = defineEmits<{ (e: 'update:modelValue', value: string): void; (e: 'submit'): void }>()
const draft = ref(props.modelValue)
const { t } = useWeatherI18n()

watch(
  () => props.modelValue,
  (value) => {
    draft.value = value
  }
)

watch(draft, (value) => {
  emits('update:modelValue', value)
})

const onSubmit = () => {
  if (!draft.value.trim()) return
  emits('submit')
}
</script>

<style scoped>
.form {
  display: flex;
  align-items: center;
  gap: 1rem;
  width: 100%;
}

.input-wrapper {
  flex: 1;
}

input {
  width: 100%;
  padding: 1rem 1.25rem;
  border-radius: 999px;
  border: 1px solid rgba(148, 163, 184, 0.4);
  background: rgba(15, 23, 42, 0.6);
  color: #fff;
  font-size: 1rem;
  outline: none;
  transition: border-color 0.2s ease;
}

input:focus {
  border-color: var(--accent);
}

button {
  padding: 0.9rem 1.5rem;
  border-radius: 999px;
  border: none;
  background: linear-gradient(135deg, var(--accent), var(--accent-strong));
  color: #020617;
  font-weight: 600;
  cursor: pointer;
  min-width: 160px;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  transition: opacity 0.2s ease;
}

button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.sr-only {
  position: absolute;
  width: 1px;
  height: 1px;
  padding: 0;
  margin: -1px;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  border: 0;
}

@media (max-width: 640px) {
  .form {
    flex-direction: column;
  }

  button {
    width: 100%;
  }
}
</style>
