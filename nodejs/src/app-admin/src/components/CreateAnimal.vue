<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import AnimalForm from './AnimalForm.vue'

const router = useRouter()

const saving = ref(false)
const error = ref(null)

async function createAnimal(animalData) {
  saving.value = true
  error.value = null

  try {
    const response = await fetch('/api/admin/animals', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(animalData),
    })

    if (!response.ok) {
      const result = await response.json()
      throw new Error(result.message || `HTTP error! status: ${response.status}`)
    }

    router.push('/data')
  } catch (err) {
    error.value = err.message
  } finally {
    saving.value = false
  }
}

function cancelCreate() {
  router.push('/data')
}
</script>

<template>
  <main class="create-animal-page">
    <header class="page-header">
      <h1>Create Animal</h1>
      <p>Add a new animal record to the AAC Rescue database.</p>
    </header>

    <p v-if="error" class="error-msg">
      {{ error }}
    </p>

    <p v-if="saving" class="saving-msg">
      Saving animal...
    </p>

    <AnimalForm
      submit-label="Create Animal"
      @submit="createAnimal"
      @cancel="cancelCreate"
    />
  </main>
</template>

<style scoped>
.create-animal-page {
  min-height: 100vh;
  padding: 24px;
  color: #243447;
}

.page-header {
  margin-bottom: 20px;
}

.page-header h1 {
  margin: 0 0 6px;
}

.page-header p {
  margin: 0;
  color: #52616f;
}

.error-msg {
  color: #b42318;
  font-weight: 700;
  margin-bottom: 16px;
}

.saving-msg {
  color: #52616f;
  margin-bottom: 16px;
}
</style>
