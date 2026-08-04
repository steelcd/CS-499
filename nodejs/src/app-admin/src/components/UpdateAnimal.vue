<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import AnimalForm from './AnimalForm.vue'

const router = useRouter()
const route = useRoute()

const animal = ref({})
const loading = ref(true)
const saving = ref(false)
const error = ref(null)

async function fetchAnimal() {
    loading.value = true
    error.value = null

    try {
        const animalId = route.params.animalId

        const response = await fetch(`/api/admin/animals/${animalId}`)

        if (!response.ok) {
            const result = await response.json()
            throw new Error(result.message || `HTTP error! status: ${response.status}`)
        }

        const result = await response.json()

        animal.value = result

    } catch (err) {
        error.value = err.message
    } finally {
        loading.value = false
    }
}

async function updateAnimal(animalData) {
  saving.value = true
  error.value = null

  try {
    const response = await fetch(`/api/admin/animals/${animalData.animal_id}`, {
      method: 'PUT',
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

onMounted(() => {
  fetchAnimal()
})

</script>

<template>
  <main class="update-animal-page">
    <header class="page-header">
      <h1>Update Animal</h1>
      <p>Update an animal record in the AAC Rescue database.</p>
    </header>

    <p v-if="loading">Loading animal...</p>

    <p v-if="error" class="error-msg">
      {{ error }}
    </p>

    <p v-if="saving" class="saving-msg">
      Saving animal...
    </p>

    <AnimalForm
        :initial-animal="animal"
        submit-label="Update Animal"
        @submit="updateAnimal"
        @cancel="cancelCreate"
    />
  </main>
</template>

<style scoped>
.update-animal-page {
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
