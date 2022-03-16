<template>
  <section class="q-mt-xl q-ml-md">
    <h2 class="text-h6">View Data for Other User</h2>
    <p class="text-caption">User's Email:</p>

    <q-input
      value="text"
      :model-value="modelValue"
      filled
      debounce="1000"
      @update:model-value="change"
    />
  </section>
</template>

<script setup lang="ts">
defineProps({
  modelValue: { type: String, default: '' },
});

const emit = defineEmits(['update:modelValue']);

const change = (value: unknown) => {
  emit('update:modelValue', value);
};
</script>
